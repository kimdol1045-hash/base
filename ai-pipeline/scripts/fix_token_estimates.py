#!/usr/bin/env python3
"""Auto-fix token_estimate in all skill YAML files.

Scans skills/**/*.yaml, calculates the correct token estimate based on
content length and language, and updates files where the estimate is
off by more than 20%.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
TOLERANCE = 0.20  # 20%


def estimate_tokens(content: str) -> int:
    """Estimate token count: len//2 for Korean-heavy text, len//4 otherwise.

    Matches the logic in audit_skills.py _estimate_tokens().
    """
    if not content:
        return 0
    korean_chars = sum(1 for c in content if "\uac00" <= c <= "\ud7a3")
    ratio = korean_chars / len(content) if content else 0
    if ratio > 0.1:
        return len(content) // 2
    return len(content) // 4


def main() -> None:
    yaml_files = sorted(SKILLS_DIR.rglob("*.yaml"))

    total = 0
    updated = 0
    unchanged = 0
    added = 0
    errors = 0

    for path in yaml_files:
        total += 1
        try:
            text = path.read_text(encoding="utf-8")
            data = yaml.safe_load(text)
        except Exception as e:
            print(f"  ERROR: {path.relative_to(ROOT)}: {e}")
            errors += 1
            continue

        if not isinstance(data, dict):
            print(f"  ERROR: {path.relative_to(ROOT)}: not a dict")
            errors += 1
            continue

        content = data.get("content", "")
        if not isinstance(content, str) or not content.strip():
            unchanged += 1
            continue

        calculated = estimate_tokens(content.strip())
        if calculated == 0:
            unchanged += 1
            continue

        existing = data.get("token_estimate")
        needs_update = False

        if existing is None:
            needs_update = True
        elif isinstance(existing, (int, float)):
            if existing == 0 or abs(existing - calculated) / calculated > TOLERANCE:
                needs_update = True
        else:
            needs_update = True

        if not needs_update:
            unchanged += 1
            continue

        # Update the value
        data["token_estimate"] = calculated

        # Write back
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

        action = "added" if existing is None else "updated"
        if existing is None:
            added += 1
        else:
            updated += 1

        rel = path.relative_to(ROOT)
        print(f"  {action}: {rel} — {existing} -> {calculated}")

    print()
    print("=== Token Estimate Fix Summary ===")
    print(f"  Total scanned: {total}")
    print(f"  Updated:       {updated}")
    print(f"  Added:         {added}")
    print(f"  Unchanged:     {unchanged}")
    print(f"  Errors:        {errors}")


if __name__ == "__main__":
    main()
