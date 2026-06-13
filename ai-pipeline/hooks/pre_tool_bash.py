#!/usr/bin/env python3
"""PreToolUse Hook (Bash) — 위험한 쉘 명령 차단.

Claude Code가 Bash 도구를 실행하기 직전에 호출.
위험 명령 패턴을 감지하면 차단(deny)하고, 안전하면 허용(approve).
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

# ─── 위험 명령 패턴 ───

DANGEROUS_PATTERNS: list[tuple[str, str]] = [
    # 파일 시스템 파괴
    (r"rm\s+(-[rfv]+\s+)*/((?!Users|home|tmp)\S+|$)", "루트 경로에서 rm 실행 금지"),
    (r"rm\s+-[rfv]*\s+\.\s*$", "현재 디렉토리 전체 삭제 금지"),
    (r"mkfs\.", "파일 시스템 포맷 금지"),
    (r"dd\s+.*of=/dev/", "디바이스 직접 쓰기 금지"),
    # Git 위험 명령
    (r"git\s+push\s+.*--force(?!-with-lease)", "git push --force 금지 (--force-with-lease 사용)"),
    (r"git\s+reset\s+--hard\s+origin/", "원격 기준 hard reset 금지"),
    (r"git\s+clean\s+-[fdxX]+", "git clean 위험 — 추적 안 되는 파일 삭제"),
    # 데이터베이스 파괴
    (r"DROP\s+(DATABASE|TABLE|SCHEMA)\s+", "DROP DATABASE/TABLE 금지"),
    (r"TRUNCATE\s+TABLE\s+", "TRUNCATE TABLE 금지"),
    (r"DELETE\s+FROM\s+\S+\s*;?\s*$", "WHERE 없는 DELETE 금지"),
    # 컨테이너/프로세스
    (r"docker\s+rm\s+-f\s+", "docker 강제 삭제 금지"),
    (r"docker\s+system\s+prune\s+-a", "docker 전체 정리 금지"),
    (r"kill\s+-9\s+1\b", "PID 1 kill 금지"),
    # 네트워크/보안
    (r"curl\s+.*\|\s*(bash|sh|zsh)", "curl | bash (원격 스크립트 직접 실행) 금지"),
    (r"wget\s+.*\|\s*(bash|sh|zsh)", "wget | bash 금지"),
    # 환경 변수 노출
    (r"echo\s+\$\{?(ANTHROPIC_API_KEY|API_KEY|SECRET|PASSWORD|TOKEN)", "비밀 환경변수 출력 금지"),
    (r"printenv\s+(ANTHROPIC_API_KEY|API_KEY|SECRET|PASSWORD|TOKEN)", "비밀 환경변수 출력 금지"),
]


def check_command(command: str) -> tuple[bool, str]:
    """명령어가 위험한지 검사.

    Returns:
        (is_dangerous, reason)
    """
    for pattern, reason in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return True, reason
    return False, ""


def main():
    try:
        raw = sys.stdin.read()
        input_data = json.loads(raw) if raw.strip() else {}
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

    tool_input = input_data.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command:
        sys.exit(0)

    is_dangerous, reason = check_command(command)

    if is_dangerous:
        logger.warning("BLOCKED: %s | reason: %s", command[:100], reason)
        output = json.dumps({
            "decision": "deny",
            "reason": f"위험 명령 차단: {reason}\n명령어: {command[:200]}",
        }, ensure_ascii=False)
        print(output)
        sys.exit(0)

    # 안전한 명령 — 기본 허용 (사용자 설정에 따라)
    sys.exit(0)


if __name__ == "__main__":
    main()
