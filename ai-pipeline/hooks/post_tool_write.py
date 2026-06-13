#!/usr/bin/env python3
"""PostToolUse Hook (Write/Edit) — 파일 작성 후 즉시 코드 품질 검사.

Claude Code가 Write/Edit 도구를 실행한 직후 호출.
TypeScript any 타입, console.log 잔여, 보안 이슈를 즉시 감지하여 피드백.
"""

from __future__ import annotations

import json
import logging
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_log_dir = os.path.join(PROJECT_ROOT, ".claude")
os.makedirs(_log_dir, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(_log_dir, "hook_post_tool.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

# ─── 파일 타입별 검사 규칙 ───

TS_CHECKS: list[tuple[str, str]] = [
    (r"\bany\b(?!\s*\()", "`any` 타입 사용 감지 — 구체적 타입으로 교체하세요"),
    (r"// @ts-ignore", "@ts-ignore 사용 감지 — 타입 에러를 수정하세요"),
    (r"// @ts-expect-error(?!\s+//)", "@ts-expect-error에 설명 주석이 없습니다"),
    (r"\bas\s+any\b", "`as any` 캐스팅 감지 — 타입 가드를 사용하세요"),
]

JS_TS_CHECKS: list[tuple[str, str]] = [
    (r"console\.(log|debug|info)\(", "console.log 잔여 감지 — 프로덕션 코드에서 제거하세요"),
    (r"(?<!\/\/\s*)TODO(?!\s*\()", "TODO 주석 감지 — 완료 후 제거하세요"),
    (r"alert\(", "alert() 사용 감지 — 적절한 UI 컴포넌트로 교체하세요"),
]

PYTHON_CHECKS: list[tuple[str, str]] = [
    (r"print\((?!.*#\s*noqa)", "print() 감지 — logger 사용을 권장합니다"),
    (r"import\s+pdb|pdb\.set_trace", "pdb 디버거 잔여 감지 — 제거하세요"),
    (r"# type:\s*ignore(?!\[)", "# type: ignore에 구체적 에러 코드가 없습니다"),
]

SECURITY_CHECKS: list[tuple[str, str]] = [
    (r"eval\(", "eval() 사용 감지 — 코드 인젝션 위험"),
    (r"innerHTML\s*=", "innerHTML 직접 할당 — XSS 위험, sanitize 필요"),
    (r"dangerouslySetInnerHTML", "dangerouslySetInnerHTML 사용 — XSS 위험, sanitize 확인"),
    (r"document\.write\(", "document.write() 사용 금지"),
    (r"exec\(", "exec() 사용 감지 — 코드 인젝션 위험"),
    (r"\.raw\(|\.unsafeRaw\(", "raw SQL 사용 감지 — 파라미터 바인딩 확인"),
]


def get_file_extension(file_path: str) -> str:
    """파일 확장자 반환."""
    _, ext = os.path.splitext(file_path)
    return ext.lower()


def check_content(file_path: str, content: str) -> list[str]:
    """파일 내용 검사. 경고 메시지 리스트 반환."""
    warnings: list[str] = []
    ext = get_file_extension(file_path)

    # 보안 검사 (모든 파일)
    for pattern, msg in SECURITY_CHECKS:
        if re.search(pattern, content):
            warnings.append(f"[보안] {msg}")

    # TypeScript 전용
    if ext in (".ts", ".tsx"):
        for pattern, msg in TS_CHECKS:
            if re.search(pattern, content):
                warnings.append(f"[TS] {msg}")

    # JavaScript/TypeScript 공통
    if ext in (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"):
        for pattern, msg in JS_TS_CHECKS:
            if re.search(pattern, content):
                warnings.append(f"[JS] {msg}")

    # Python
    if ext == ".py":
        for pattern, msg in PYTHON_CHECKS:
            if re.search(pattern, content):
                warnings.append(f"[PY] {msg}")

    return warnings


def main():
    try:
        raw = sys.stdin.read()
        input_data = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content", "") or tool_input.get("new_string", "")

    if not file_path or not content:
        sys.exit(0)

    warnings = check_content(file_path, content)

    if warnings:
        warning_text = "\n".join(f"  - {w}" for w in warnings[:5])  # 최대 5개
        logger.info("Warnings for %s: %d issues", file_path, len(warnings))
        output = json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": (
                    f"[코드 품질 경고] {os.path.basename(file_path)}:\n{warning_text}\n"
                    "위 항목을 확인하고 필요시 수정하세요."
                ),
            }
        }, ensure_ascii=False)
        print(output)

    sys.exit(0)


if __name__ == "__main__":
    main()
