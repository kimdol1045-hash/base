#!/usr/bin/env python3
"""Skill Version Management — 버전 관리, 아카이브, 히스토리, 버전 diff.

Usage:
    python scripts/version_skill.py --bump dev.backend.auth.jwt-auth
    python scripts/version_skill.py --history dev.backend.auth.jwt-auth
    python scripts/version_skill.py --diff dev.backend.auth.jwt-auth
    python scripts/version_skill.py --diff dev.backend.auth.jwt-auth --v1 1 --v2 2
    python scripts/version_skill.py --check-all
    python scripts/version_skill.py --add-version-all
"""

from __future__ import annotations

import argparse
import difflib
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
ARCHIVE_DIR = SKILLS_DIR / "_archive"


def _resolve_path(skill_id: str) -> Path | None:
    """skill_id → file path."""
    parts = skill_id.split(".")
    if len(parts) < 2:
        return None
    path = SKILLS_DIR / "/".join(parts[:-1]) / f"{parts[-1]}.yaml"
    return path if path.exists() else None


def bump_version(skill_id: str) -> None:
    """Bump skill version and archive old version."""
    path = _resolve_path(skill_id)
    if not path:
        print(f"ERROR: Skill not found: {skill_id}")
        sys.exit(1)

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    old_version = data.get("version", 1)
    new_version = old_version + 1

    # Archive current version
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_name = f"{skill_id}_v{old_version}.yaml"
    archive_path = ARCHIVE_DIR / archive_name
    shutil.copy2(path, archive_path)
    print(f"  Archived: {archive_name}")

    # Update version
    data["version"] = new_version
    data["version_date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    print(f"  Bumped: {skill_id} v{old_version} → v{new_version}")


def show_history(skill_id: str) -> None:
    """Show version history for a skill."""
    path = _resolve_path(skill_id)
    if not path:
        print(f"ERROR: Skill not found: {skill_id}")
        sys.exit(1)

    current = yaml.safe_load(path.read_text(encoding="utf-8"))
    print(f"\n{skill_id} — Version History")
    print(f"  Current: v{current.get('version', 1)} ({current.get('version_date', 'unknown')})")

    # Check archive
    if ARCHIVE_DIR.exists():
        archives = sorted(ARCHIVE_DIR.glob(f"{skill_id}_v*.yaml"))
        for ap in archives:
            ad = yaml.safe_load(ap.read_text(encoding="utf-8"))
            v = ad.get("version", "?")
            d = ad.get("version_date", "unknown")
            chars = len(ad.get("content", ""))
            print(f"  Archive: v{v} ({d}) — {chars} chars")
    else:
        print("  No archived versions")


def _load_version(skill_id: str, version: int | None) -> tuple[str, int]:
    """Load a specific version's YAML text. Returns (text, version_number).

    If version is None, loads the current (latest) version.
    """
    if version is None:
        path = _resolve_path(skill_id)
        if not path:
            print(f"ERROR: Skill not found: {skill_id}")
            sys.exit(1)
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return path.read_text(encoding="utf-8"), data.get("version", 1)

    # Look in archive first
    archive_path = ARCHIVE_DIR / f"{skill_id}_v{version}.yaml"
    if archive_path.exists():
        return archive_path.read_text(encoding="utf-8"), version

    # Maybe it's the current version
    path = _resolve_path(skill_id)
    if path:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if data.get("version", 1) == version:
            return path.read_text(encoding="utf-8"), version

    print(f"ERROR: Version {version} not found for {skill_id}")
    sys.exit(1)


def show_diff(skill_id: str, v1: int | None = None, v2: int | None = None) -> None:
    """Show diff between two versions of a skill.

    If v1/v2 not specified, diffs the latest archive against current.
    """
    path = _resolve_path(skill_id)
    if not path:
        print(f"ERROR: Skill not found: {skill_id}")
        sys.exit(1)

    if v1 is not None and v2 is not None:
        text_a, ver_a = _load_version(skill_id, v1)
        text_b, ver_b = _load_version(skill_id, v2)
    else:
        # Find latest archived version and diff against current
        if not ARCHIVE_DIR.exists():
            print(f"No archived versions for {skill_id}")
            return
        archives = sorted(ARCHIVE_DIR.glob(f"{skill_id}_v*.yaml"))
        if not archives:
            print(f"No archived versions for {skill_id}")
            return
        latest_archive = archives[-1]
        text_a = latest_archive.read_text(encoding="utf-8")
        ad = yaml.safe_load(text_a)
        ver_a = ad.get("version", "?")
        text_b = path.read_text(encoding="utf-8")
        bd = yaml.safe_load(text_b)
        ver_b = bd.get("version", "?")

    lines_a = text_a.splitlines(keepends=True)
    lines_b = text_b.splitlines(keepends=True)

    diff = difflib.unified_diff(
        lines_a,
        lines_b,
        fromfile=f"{skill_id} v{ver_a}",
        tofile=f"{skill_id} v{ver_b}",
        lineterm="",
    )
    diff_text = "".join(diff)
    if diff_text:
        print(f"\n{skill_id}: v{ver_a} → v{ver_b}")
        print(diff_text)
    else:
        print(f"\n{skill_id}: v{ver_a} and v{ver_b} are identical")


def check_all() -> None:
    """List skills without version field."""
    missing = []
    total = 0
    for path in sorted(SKILLS_DIR.rglob("*.yaml")):
        if "_archive" in str(path):
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if data and "id" in data:
                total += 1
                if "version" not in data:
                    missing.append(data["id"])
        except Exception:
            continue

    print(f"\nTotal skills: {total}")
    print(f"Missing version: {len(missing)}")
    if missing:
        for sid in missing[:20]:
            print(f"  - {sid}")
        if len(missing) > 20:
            print(f"  ... and {len(missing) - 20} more")


def add_version_all() -> None:
    """Add version: 1 to all skills that don't have it."""
    updated = 0
    for path in sorted(SKILLS_DIR.rglob("*.yaml")):
        if "_archive" in str(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
            data = yaml.safe_load(text)
            if data and "id" in data and "version" not in data:
                data["version"] = 1
                with open(path, "w", encoding="utf-8") as f:
                    yaml.dump(data, f, allow_unicode=True, default_flow_style=False)
                updated += 1
        except Exception:
            continue

    print(f"Added version: 1 to {updated} skills")


def main() -> None:
    parser = argparse.ArgumentParser(description="Skill Version Management")
    parser.add_argument("--bump", metavar="SKILL_ID", help="Bump version of a skill")
    parser.add_argument("--history", metavar="SKILL_ID", help="Show version history")
    parser.add_argument("--diff", metavar="SKILL_ID", help="Show diff between versions")
    parser.add_argument("--v1", type=int, default=None, help="First version for diff (default: latest archive)")
    parser.add_argument("--v2", type=int, default=None, help="Second version for diff (default: current)")
    parser.add_argument("--check-all", action="store_true", help="List skills without version field")
    parser.add_argument("--add-version-all", action="store_true", help="Add version: 1 to all skills")

    args = parser.parse_args()

    if args.bump:
        bump_version(args.bump)
    elif args.history:
        show_history(args.history)
    elif args.diff:
        show_diff(args.diff, args.v1, args.v2)
    elif args.check_all:
        check_all()
    elif args.add_version_all:
        add_version_all()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
