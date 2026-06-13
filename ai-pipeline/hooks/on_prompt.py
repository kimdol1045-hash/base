#!/usr/bin/env python3
"""UserPromptSubmit Hook — 요구사항 분류 → 스킬 선택 → 시스템 프롬프트 주입.

Claude Code에서 사용자가 프롬프트를 제출하면 자동 실행.
Haiku 1회 호출로 분류 후, 매칭된 Atomic Skill을 조립하여
Claude Code 컨텍스트에 주입한다.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import sys

# ai-pipeline 루트를 path에 추가
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# .env에서 ANTHROPIC_API_KEY 로드
from hooks.common import load_env  # noqa: E402
load_env(PROJECT_ROOT)

# 로그는 파일로 (stderr 오염 방지, 하지만 진단은 유지)
_log_dir = os.path.join(PROJECT_ROOT, ".claude")
os.makedirs(_log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(_log_dir, "hook_prompt.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

# stderr를 파일로 리다이렉트 (Claude Code가 stderr도 읽으므로 콘솔 억제, 디버깅은 유지)
sys.stderr = open(os.path.join(_log_dir, "hook_prompt_stderr.log"), "a")

from apps.server.pipeline import prepare_plan  # noqa: E402

# Plan 상태 저장 디렉토리 (Stop 훅에서 읽음)
PLAN_STATE_DIR = os.path.join(PROJECT_ROOT, ".claude", "state")
os.makedirs(PLAN_STATE_DIR, exist_ok=True)

# 파이프라인 실패 시 주입할 최소한의 품질 가이드
FALLBACK_CONTEXT = """## AI Pipeline 지시사항 (fallback)
파이프라인 분류에 실패했지만, 아래 기본 품질 기준을 따라주세요.

### 기본 규칙
- TypeScript strict mode, any 타입 금지
- 모든 외부 입력은 검증 (Zod 등)
- 에러는 삼키지 않고 로깅 또는 재throw
- 하드코딩된 비밀값 금지
- 일관된 에러 응답 형식 사용"""


async def _prepare(prompt: str, session_id: str) -> dict | None:
    try:
        return await prepare_plan(user_input=prompt, session_id=session_id)
    except Exception as e:
        logger.error("prepare_plan error: %s", e)
        return None


def _save_plan_state(session_id: str, result: dict) -> None:
    """Stop 훅에서 사용할 plan 상태 저장."""
    try:
        state = {
            "post_checks": result.get("post_checks", []),
            "skip_validation": result.get("skip_validation", False),
            "plan": result.get("plan") or result.get("overall_plan"),
        }
        path = os.path.join(PLAN_STATE_DIR, f"{session_id}.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False)
    except Exception as e:
        logger.error("Failed to save plan state: %s", e)


def _format_single(result: dict) -> str:
    plan = result["plan"]
    checks = "\n".join(f"- [ ] {c}" for c in result.get("post_checks", []))
    skills = ", ".join(plan["skill_ids"][:10])
    if len(plan["skill_ids"]) > 10:
        skills += f" 외 {len(plan['skill_ids']) - 10}개"

    warnings = ""
    if result.get("warnings"):
        warnings = "\n### 경고\n" + "\n".join(f"- {w}" for w in result["warnings"])

    return f"""## AI Pipeline 지시사항
아래 System Prompt의 지시사항과 품질 기준을 반드시 따라 코드를 작성하세요.

### System Prompt
{result["system_prompt"]}

### 작성 후 자가 검증 (POST Check)
코드 작성이 끝나면 아래 항목을 하나씩 확인하고,
FAIL 항목이 있으면 코드를 수정하세요.
{checks}

### 메타데이터
- 복잡도: {plan["complexity"]}/10 | 블룸: {plan["bloom_level"]}
- 도메인: {", ".join(plan["domains"])}
- 로드된 스킬: {skills}{warnings}"""


def _format_split(result: dict) -> str:
    parts = []
    for i, p in enumerate(result["plans"], 1):
        checks = "\n".join(f"  - [ ] {c}" for c in p.get("post_checks", []))
        parts.append(f"""### Step {i}: {p["domain"]}
{p["system_prompt"]}

검증 항목:
{checks}""")

    warnings = "\n".join(f"- {w}" for w in result.get("warnings", []))
    return f"""## AI Pipeline 지시사항 (분할 실행 모드)
다중 도메인 요청입니다. 아래 순서대로 도메인별로 작업하세요.
각 단계의 System Prompt를 따르고, 완료 후 검증 항목을 확인하세요.

{chr(10).join(parts)}

### 경고
{warnings}"""


def main():
    try:
        raw = sys.stdin.read()
        input_data = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    prompt = input_data.get("prompt", "").strip()
    session_id = input_data.get("session_id", "default")

    # 너무 짧은 입력은 스킵 (인사, 단답 등)
    if not prompt or len(prompt) < 5:
        sys.exit(0)

    logger.info("Hook triggered: prompt=%s..., session=%s", prompt[:50], session_id)

    result = asyncio.run(_prepare(prompt, session_id))

    if not result:
        # 파이프라인 실패 시 fallback 품질 가이드 주입
        logger.warning("Pipeline failed, injecting fallback context")
        output = json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": FALLBACK_CONTEXT,
            }
        }, ensure_ascii=False)
        print(output)
        sys.exit(0)

    # Stop 훅을 위한 plan 상태 저장
    _save_plan_state(session_id, result)

    # 컨텍스트 포맷
    if result["mode"] == "single":
        context = _format_single(result)
    else:
        context = _format_split(result)

    logger.info("Plan ready: mode=%s, skills=%d",
                result["mode"],
                len(result.get("plan", {}).get("skill_ids", [])))

    output = json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": context,
        }
    }, ensure_ascii=False)

    print(output)
    sys.exit(0)


if __name__ == "__main__":
    main()
