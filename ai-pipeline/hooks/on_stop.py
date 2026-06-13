#!/usr/bin/env python3
"""Stop Hook — Claude Code 응답 완료 후 POST 검증 자동 실행.

Claude Code가 코드 생성을 마치면 자동 실행.
transcript에서 마지막 assistant 응답을 읽어 POST 체크리스트로 검증.
FAIL이면 exit 2 (Claude Code 계속 작업), PASS이면 exit 0 (정상 종료).
"""

from __future__ import annotations

import json
import logging
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# .env 로드
from hooks.common import load_env  # noqa: E402
load_env(PROJECT_ROOT)

# 로그는 파일로 (stderr 오염 방지)
_log_path = os.path.join(PROJECT_ROOT, ".claude", "hook_stop.log")
logging.basicConfig(
    filename=_log_path,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

# plan 상태 파일 경로
PLAN_STATE_DIR = os.path.join(PROJECT_ROOT, ".claude", "state")

# 무한 루프 방지: FAIL 재시도 최대 횟수
MAX_STOP_RETRIES = 3


def _read_last_assistant_output(transcript_path: str) -> str:
    """transcript JSONL에서 마지막 assistant 응답 텍스트 추출."""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""

    last_output = ""
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                # assistant 메시지에서 텍스트 추출
                if entry.get("role") == "assistant":
                    content = entry.get("content", "")
                    if isinstance(content, str):
                        last_output = content
                    elif isinstance(content, list):
                        texts = [
                            c.get("text", "") for c in content
                            if isinstance(c, dict) and c.get("type") == "text"
                        ]
                        if texts:
                            last_output = "\n".join(texts)
    except Exception as e:
        logger.error("Failed to read transcript: %s", e)

    return last_output


def _load_plan_state(session_id: str) -> dict | None:
    """저장된 plan 상태 로드."""
    path = os.path.join(PLAN_STATE_DIR, f"{session_id}.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def _save_plan_state(session_id: str, plan_state: dict) -> None:
    """plan 상태 저장 (retry_count 등 업데이트용)."""
    path = os.path.join(PLAN_STATE_DIR, f"{session_id}.json")
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(plan_state, f, ensure_ascii=False)
    except Exception as e:
        logger.error("Failed to save plan state: %s", e)


def main():
    try:
        raw = sys.stdin.read()
        input_data = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    transcript_path = input_data.get("transcript_path", "")
    session_id = input_data.get("session_id", "")

    # transcript에서 마지막 응답 추출
    output = _read_last_assistant_output(transcript_path)
    if not output or len(output) < 20:
        sys.exit(0)  # 응답이 없거나 너무 짧으면 스킵

    # 저장된 plan 상태 확인
    plan_state = _load_plan_state(session_id) if session_id else None
    if not plan_state:
        sys.exit(0)  # plan 없으면 일반 대화 — 검증 불필요

    post_checks = plan_state.get("post_checks", [])
    skip_validation = plan_state.get("skip_validation", False)

    if skip_validation or not post_checks:
        sys.exit(0)

    # 재시도 횟수 확인 — 무한 루프 방지
    retry_count = plan_state.get("_retry_count", 0)
    if retry_count >= MAX_STOP_RETRIES:
        logger.warning("Max retries (%d) reached, allowing stop", MAX_STOP_RETRIES)
        sys.exit(0)

    # POST 검증 실행
    import asyncio
    from packages.post_validator.validator import validate_output

    async def _validate():
        return await validate_output(output=output, post_checks=post_checks)

    try:
        result = asyncio.run(_validate())
    except Exception as e:
        logger.error("POST validation error: %s", e)
        sys.exit(0)  # 검증 실패 시 정상 종료 허용

    if result.status == "FAIL" and result.issues:
        # retry_count 증가 후 저장
        plan_state["_retry_count"] = retry_count + 1
        _save_plan_state(session_id, plan_state)

        # FAIL → Claude Code에게 계속 작업하라고 지시
        remaining = MAX_STOP_RETRIES - retry_count - 1
        fail_output = json.dumps({
            "decision": "block",
            "reason": (
                f"POST 검증 FAIL (재시도 {retry_count + 1}/{MAX_STOP_RETRIES}). "
                f"다음 항목을 수정하세요:\n{result.issues}"
            ),
        }, ensure_ascii=False)
        print(fail_output)
        logger.info("POST validation FAIL — blocking stop (retry %d/%d)",
                     retry_count + 1, MAX_STOP_RETRIES)
        sys.exit(2)  # exit 2 = block stop

    logger.info("POST validation %s", result.status)
    sys.exit(0)


if __name__ == "__main__":
    main()
