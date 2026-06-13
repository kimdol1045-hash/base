#!/usr/bin/env python3
"""외부 프로젝트에 AI Pipeline 연동 설정 생성.

사용법:
  # 글로벌 설정 (모든 프로젝트에 적용)
  python /path/to/ai-pipeline/scripts/init_project.py --global

  # 특정 프로젝트에만 설정 생성
  python /path/to/ai-pipeline/scripts/init_project.py --target /path/to/my-project

  # Hook 없이 MCP만 설정
  python /path/to/ai-pipeline/scripts/init_project.py --target /path/to/project --mcp-only

  # 글로벌 설정 제거
  python /path/to/ai-pipeline/scripts/init_project.py --global --remove

생성 파일:
  --global:
    ~/.claude.json          — MCP 서버 설정 (14 tools)
    ~/.claude/settings.json — Hook 설정 (자동 분류 + 스킬 주입)
  --target:
    <target>/.mcp.json               — MCP 서버 설정
    <target>/.claude/settings.json   — Hook 설정
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ai-pipeline 루트 경로 (이 스크립트 기준)
PIPELINE_ROOT = Path(__file__).resolve().parent.parent
VENV_PYTHON = PIPELINE_ROOT / ".venv" / "bin" / "python"
HOME = Path.home()


def _mcp_server_entry() -> dict:
    """MCP 서버 설정 항목 (절대 경로)."""
    return {
        "command": str(VENV_PYTHON),
        "args": ["-m", "packages.skill_store.server"],
        "cwd": str(PIPELINE_ROOT),
        "env": {
            "SKILL_DIR": str(PIPELINE_ROOT / "skills"),
            "PYTHONPATH": str(PIPELINE_ROOT),
        },
        "type": "stdio",
    }


def _mcp_config() -> dict:
    """프로젝트 레벨 .mcp.json 전체 구조."""
    return {"mcpServers": {"ai-pipeline": _mcp_server_entry()}}


def _hook_command(script_name: str) -> str:
    """절대 경로 Hook 커맨드 생성."""
    return f"{VENV_PYTHON} {PIPELINE_ROOT / 'hooks' / script_name}"


def _hooks_config() -> dict:
    """Claude Code Hook 설정 (절대 경로)."""
    return {
        "hooks": {
            "UserPromptSubmit": [
                {
                    "matcher": "",
                    "hooks": [
                        {
                            "type": "command",
                            "command": _hook_command("on_prompt.py"),
                            "timeout": 30,
                        }
                    ],
                }
            ],
            "Stop": [
                {
                    "matcher": "",
                    "hooks": [
                        {
                            "type": "command",
                            "command": _hook_command("on_stop.py"),
                            "timeout": 20,
                        }
                    ],
                }
            ],
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": _hook_command("pre_tool_bash.py"),
                            "timeout": 5,
                        }
                    ],
                },
                {
                    "matcher": "Write",
                    "hooks": [
                        {
                            "type": "command",
                            "command": _hook_command("pre_tool_write.py"),
                            "timeout": 5,
                        }
                    ],
                },
                {
                    "matcher": "Edit",
                    "hooks": [
                        {
                            "type": "command",
                            "command": _hook_command("pre_tool_write.py"),
                            "timeout": 5,
                        }
                    ],
                },
            ],
            "PostToolUse": [
                {
                    "matcher": "Write",
                    "hooks": [
                        {
                            "type": "command",
                            "command": _hook_command("post_tool_write.py"),
                            "timeout": 5,
                        }
                    ],
                },
                {
                    "matcher": "Edit",
                    "hooks": [
                        {
                            "type": "command",
                            "command": _hook_command("post_tool_write.py"),
                            "timeout": 5,
                        }
                    ],
                },
            ],
        }
    }


def _write_json(path: Path, data: dict, force: bool) -> bool:
    """JSON 파일 쓰기. 이미 있으면 머지."""
    if path.exists() and not force:
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            existing = {}

        # 딥 머지 (최상위 키 기준)
        for key, value in data.items():
            if key in existing and isinstance(existing[key], dict) and isinstance(value, dict):
                existing[key].update(value)
            else:
                existing[key] = value
        data = existing

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return True


def _install_global(force: bool) -> list[str]:
    """글로벌 설정에 ai-pipeline 등록."""
    created = []

    # 1. ~/.claude.json — MCP 서버 추가
    claude_json = HOME / ".claude.json"
    if claude_json.exists():
        data = json.loads(claude_json.read_text(encoding="utf-8"))
    else:
        data = {}

    if "mcpServers" not in data:
        data["mcpServers"] = {}
    data["mcpServers"]["ai-pipeline"] = _mcp_server_entry()

    claude_json.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    created.append(str(claude_json) + " (mcpServers.ai-pipeline)")

    # 2. ~/.claude/settings.json — Hook 추가
    settings_path = HOME / ".claude" / "settings.json"
    _write_json(settings_path, _hooks_config(), force)
    created.append(str(settings_path) + " (hooks)")

    return created


def _remove_global() -> list[str]:
    """글로벌 설정에서 ai-pipeline 제거."""
    removed = []

    # 1. ~/.claude.json — MCP 서버 제거
    claude_json = HOME / ".claude.json"
    if claude_json.exists():
        data = json.loads(claude_json.read_text(encoding="utf-8"))
        if "mcpServers" in data and "ai-pipeline" in data["mcpServers"]:
            del data["mcpServers"]["ai-pipeline"]
            claude_json.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            removed.append(str(claude_json) + " (mcpServers.ai-pipeline)")

    # 2. ~/.claude/settings.json — Hook 제거
    settings_path = HOME / ".claude" / "settings.json"
    if settings_path.exists():
        data = json.loads(settings_path.read_text(encoding="utf-8"))
        if "hooks" in data:
            del data["hooks"]
            settings_path.write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            removed.append(str(settings_path) + " (hooks)")

    return removed


def _install_project(target: Path, mcp_only: bool, hooks_only: bool, force: bool) -> list[str]:
    """프로젝트 레벨 설정 생성."""
    created = []

    if not hooks_only:
        mcp_path = target / ".mcp.json"
        _write_json(mcp_path, _mcp_config(), force)
        created.append(str(mcp_path))

    if not mcp_only:
        settings_path = target / ".claude" / "settings.json"
        _write_json(settings_path, _hooks_config(), force)
        created.append(str(settings_path))

    return created


def main() -> None:
    parser = argparse.ArgumentParser(
        description="AI Pipeline 연동 설정 생성",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""예시:
  # 글로벌 (모든 프로젝트)
  python scripts/init_project.py --global

  # 특정 프로젝트
  python scripts/init_project.py --target ~/my-project

  # 글로벌 제거
  python scripts/init_project.py --global --remove
""",
    )
    parser.add_argument(
        "--global",
        dest="is_global",
        action="store_true",
        help="글로벌 설정 (~/.claude.json + ~/.claude/settings.json)",
    )
    parser.add_argument(
        "--target",
        type=str,
        default="",
        help="프로젝트 경로 (기본: 현재 디렉토리)",
    )
    parser.add_argument("--mcp-only", action="store_true", help="MCP 설정만 생성")
    parser.add_argument("--hooks-only", action="store_true", help="Hook 설정만 생성")
    parser.add_argument("--force", action="store_true", help="기존 설정 덮어쓰기")
    parser.add_argument("--remove", action="store_true", help="설정 제거 (--global 전용)")
    args = parser.parse_args()

    # 사전 검증
    if not VENV_PYTHON.exists():
        print(f"Error: Python venv not found at {VENV_PYTHON}", file=sys.stderr)
        print(
            "  → ai-pipeline/.venv를 먼저 생성하세요: python -m venv .venv && pip install -e .",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.remove:
        if not args.is_global:
            print("Error: --remove는 --global과 함께 사용하세요.", file=sys.stderr)
            sys.exit(1)
        removed = _remove_global()
        if removed:
            print("\n🗑️  AI Pipeline 글로벌 설정 제거 완료\n")
            for f in removed:
                print(f"  {f}")
        else:
            print("제거할 설정이 없습니다.")
        print()
        return

    if args.is_global:
        created = _install_global(args.force)
        scope = "글로벌 (모든 프로젝트)"
    else:
        target = Path(args.target or ".").resolve()
        if not target.is_dir():
            print(f"Error: {target} is not a directory", file=sys.stderr)
            sys.exit(1)
        created = _install_project(target, args.mcp_only, args.hooks_only, args.force)
        scope = str(target)

    print(f"\n✅ AI Pipeline 연동 완료 — {scope}\n")
    print("생성/업데이트된 파일:")
    for f in created:
        print(f"  {f}")

    print(f"\n📍 AI Pipeline: {PIPELINE_ROOT}")
    print(f"📍 Skills: {PIPELINE_ROOT / 'skills'} ({_count_skills()}개)")
    print(f"📍 Python: {VENV_PYTHON}")

    print("\n🔧 MCP 도구 (14개):")
    print("  get_skill, get_skills_batch, search_skills, assemble_prompt,")
    print("  prepare_plan, validate, get_evolution_stats, run_decay,")
    print("  get_pipeline_status, get_domain_skills, get_usage_stats,")
    print("  get_cost_stats, get_recommendations, get_ab_tests")

    print("\n🪝 Hook 자동화:")
    print("  UserPromptSubmit → 요구사항 분류 + Atomic Skill 주입")
    print("  Stop → POST 검증 (코드 품질 체크)")
    print("  PreToolUse/PostToolUse → 코드 품질 가드")
    print()


def _count_skills() -> int:
    """스킬 수 카운트."""
    skills_dir = PIPELINE_ROOT / "skills"
    if not skills_dir.exists():
        return 0
    return sum(1 for _ in skills_dir.rglob("*.yaml") if "_archive" not in str(_))


if __name__ == "__main__":
    main()
