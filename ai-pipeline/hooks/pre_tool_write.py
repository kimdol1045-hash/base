#!/usr/bin/env python3
"""PreToolUse Hook (Write/Edit) — 민감 파일 쓰기 및 비밀값 하드코딩 차단.

Claude Code가 Write 또는 Edit 도구를 실행하기 직전에 호출.
민감 파일 경로나 하드코딩된 비밀값 패턴을 감지하면 차단.
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
    filename=os.path.join(_log_dir, "hook_pre_tool.log"),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

# ─── 민감 파일 패턴 ───

SENSITIVE_FILE_PATTERNS: list[tuple[str, str]] = [
    (r"\.env($|\.local|\.production|\.staging)", ".env 파일 직접 수정 금지"),
    (r"\.(pem|key|cert|p12|pfx|jks)$", "인증서/키 파일 수정 금지"),
    (r"credentials\.json$", "credentials 파일 수정 금지"),
    (r"\.aws/credentials$", "AWS credentials 수정 금지"),
    (r"\.ssh/(id_rsa|id_ed25519|authorized_keys)", "SSH 키 수정 금지"),
    (r"secrets?\.(ya?ml|json|toml)$", "secrets 파일 수정 금지"),
    (r"\.git/", ".git 내부 직접 수정 금지"),
    (r"node_modules/", "node_modules 직접 수정 금지"),
]

# ─── 하드코딩 비밀값 패턴 ───

SECRET_PATTERNS: list[tuple[str, str]] = [
    # API 키 형태 (긴 영숫자 문자열이 할당문에 있을 때)
    (r"""(?:api[_-]?key|secret|token|password|passwd|credential)\s*[=:]\s*["'][A-Za-z0-9+/=_-]{20,}["']""",
     "하드코딩된 API 키/시크릿 감지"),
    # AWS 키
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID 하드코딩 감지"),
    # 일반적인 비밀번호 할당
    (r"""password\s*[=:]\s*["'][^"']{8,}["']""",
     "하드코딩된 비밀번호 감지 (환경변수 사용 권장)"),
    # Bearer 토큰
    (r"""["']Bearer\s+[A-Za-z0-9._-]{20,}["']""",
     "하드코딩된 Bearer 토큰 감지"),
    # Private Key 블록
    (r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----",
     "Private Key 하드코딩 감지"),
]


def check_file_path(file_path: str) -> tuple[bool, str]:
    """파일 경로가 민감한지 검사."""
    for pattern, reason in SENSITIVE_FILE_PATTERNS:
        if re.search(pattern, file_path, re.IGNORECASE):
            return True, reason
    return False, ""


def check_content(content: str) -> tuple[bool, str]:
    """콘텐츠에 하드코딩된 비밀값이 있는지 검사."""
    for pattern, reason in SECRET_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            return True, reason
    return False, ""


def main():
    try:
        raw = sys.stdin.read()
        input_data = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})

    # Write: file_path + content
    # Edit: file_path + old_string + new_string
    file_path = tool_input.get("file_path", "")
    content = tool_input.get("content", "") or tool_input.get("new_string", "")

    # 1. 파일 경로 검사
    if file_path:
        is_sensitive, reason = check_file_path(file_path)
        if is_sensitive:
            logger.warning("BLOCKED file: %s | reason: %s", file_path, reason)
            output = json.dumps({
                "decision": "deny",
                "reason": f"민감 파일 쓰기 차단: {reason}\n파일: {file_path}",
            }, ensure_ascii=False)
            print(output)
            sys.exit(0)

    # 2. 콘텐츠에서 비밀값 검사
    if content:
        has_secret, reason = check_content(content)
        if has_secret:
            logger.warning("BLOCKED secret in: %s | reason: %s", file_path, reason)
            output = json.dumps({
                "decision": "deny",
                "reason": (
                    f"비밀값 하드코딩 차단: {reason}\n"
                    f"파일: {file_path}\n"
                    "환경변수(process.env)나 시크릿 매니저를 사용하세요."
                ),
            }, ensure_ascii=False)
            print(output)
            sys.exit(0)

    # 안전 — 기본 허용
    sys.exit(0)


if __name__ == "__main__":
    main()
