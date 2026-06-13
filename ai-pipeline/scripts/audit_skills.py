#!/usr/bin/env python3
"""Automated skill quality audit for the AI Pipeline.

Scans all YAML files in skills/ and checks for quality issues.
Usage: python scripts/audit_skills.py
"""

from __future__ import annotations

import ast
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

VALID_TYPES = {"role", "rule", "pattern", "stack", "verify"}
REQUIRED_FIELDS = {"id", "domain", "type", "content", "tags", "token_estimate"}
MIN_CONTENT_LENGTH = 50
TOKEN_ESTIMATE_TOLERANCE = 0.50  # 50%

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"
SELECTOR_PATH = ROOT / "packages" / "hook_engine" / "selector.py"


def _load_yaml_simple(path: Path) -> dict | None:
    """Minimal YAML loader that handles the skill YAML subset without PyYAML."""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None

    # Try PyYAML first
    try:
        import yaml  # noqa: F811

        return yaml.safe_load(text)
    except ImportError:
        pass

    # Fallback: manual parse for our simple YAML structure
    result: dict = {}
    lines = text.split("\n")
    current_key: str | None = None
    multiline_buf: list[str] = []
    in_multiline = False

    for line in lines:
        # Multiline block scalar continuation
        if in_multiline:
            if line and not line[0].isspace() and not line.startswith("#"):
                # End of multiline
                result[current_key] = "\n".join(multiline_buf)  # type: ignore[index]
                in_multiline = False
                # fall through to parse this line
            else:
                multiline_buf.append(line)
                continue

        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # Top-level key: value
        m = re.match(r'^(\w[\w_-]*)\s*:\s*(.*)', line)
        if not m:
            continue

        key = m.group(1)
        value = m.group(2).strip()

        if value == "|" or value == ">":
            # Block scalar
            current_key = key
            multiline_buf = []
            in_multiline = True
            continue

        # Inline list: [a, b, c]
        if value.startswith("["):
            try:
                result[key] = ast.literal_eval(value)
            except Exception:
                # Try to parse as string list
                inner = value.strip("[]")
                result[key] = [s.strip().strip('"').strip("'") for s in inner.split(",") if s.strip()]
            continue

        # Quoted string
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            result[key] = value[1:-1]
            continue

        # Number
        try:
            result[key] = int(value)
            continue
        except ValueError:
            pass
        try:
            result[key] = float(value)
            continue
        except ValueError:
            pass

        # Plain string
        result[key] = value

    # Flush remaining multiline
    if in_multiline and current_key:
        result[current_key] = "\n".join(multiline_buf)

    return result if result else None


def _path_to_expected_id(path: Path) -> str:
    """Convert file path to expected skill ID.

    skills/dev/backend/api/auth.yaml -> dev.backend.api.auth
    """
    rel = path.relative_to(SKILLS_DIR)
    parts = list(rel.parts)
    # Remove .yaml extension from last part
    parts[-1] = parts[-1].removesuffix(".yaml").removesuffix(".yml")
    return ".".join(parts)


def _estimate_tokens(content: str) -> int:
    """Estimate token count: len//2 for Korean, len//4 for English."""
    if not content:
        return 0
    korean_chars = sum(1 for c in content if "\uac00" <= c <= "\ud7a3")
    ratio = korean_chars / len(content) if content else 0
    if ratio > 0.1:
        return len(content) // 2
    return len(content) // 4


def _extract_selector_skill_ids() -> set[str]:
    """Parse selector.py and extract all skill IDs from BASE_SKILLS and KEYWORD_SKILLS.

    Only extracts IDs that appear inside list values (not dict keys).
    """
    if not SELECTOR_PATH.exists():
        return set()

    text = SELECTOR_PATH.read_text(encoding="utf-8")
    skill_ids: set[str] = set()

    # Match skill IDs inside list brackets within the two dicts.
    # We parse line-by-line, tracking whether we're inside a list value.
    in_skills_dict = False
    in_list = False
    brace_depth = 0

    for line in text.split("\n"):
        stripped = line.strip()

        # Detect start of BASE_SKILLS or KEYWORD_SKILLS dict
        if re.match(r'^(BASE_SKILLS|KEYWORD_SKILLS)\b', stripped):
            in_skills_dict = True
            brace_depth = 0

        if not in_skills_dict:
            continue

        # Track brace depth to know when the dict ends
        brace_depth += line.count("{") - line.count("}")
        if brace_depth <= 0 and in_skills_dict and "{" not in line and "}" in line:
            in_skills_dict = False
            in_list = False
            continue

        # Track list context: lines with [ start a list, ] ends it
        if "[" in line:
            in_list = True
        if in_list:
            # Extract all quoted dot-separated identifiers on this line
            for m in re.finditer(
                r'"((?:[a-z][a-z0-9]*(?:-[a-z0-9]+)*)(?:\.(?:[a-z][a-z0-9]*(?:-[a-z0-9]+)*))+)"',
                line,
            ):
                candidate = m.group(1)
                # Exclude dict keys: they appear as `"key": [` pattern.
                # A dict key would be the only quoted string before the colon.
                # Skill IDs inside lists are after [ or , so we check position.
                pos = m.start()
                prefix = line[:pos].rstrip()
                # If the char before the quote is a colon or colon+space, it's a dict key context.
                # But dict keys for KEYWORD_SKILLS are simple words, not dot-separated.
                # The dot-separated strings before ]: [ are domain dict keys in BASE_SKILLS.
                # We skip those by checking if this string is followed by "]: [" or ": ["
                after = line[m.end():].lstrip()
                if after.startswith(":") or after.startswith("]:"):
                    continue
                skill_ids.add(candidate)

        if "]" in line:
            in_list = False

    return skill_ids


# ---------------------------------------------------------------------------
# Issue tracking
# ---------------------------------------------------------------------------

class Issue:
    """Represents a single quality issue."""

    def __init__(self, level: str, category: str, skill_id: str, message: str) -> None:
        self.level = level  # "FAIL" or "WARN"
        self.category = category
        self.skill_id = skill_id
        self.message = message

    def __str__(self) -> str:
        return f"[{self.level}] {self.skill_id}: {self.message}"


# ---------------------------------------------------------------------------
# Main audit
# ---------------------------------------------------------------------------

def audit() -> None:
    """Run all quality checks and print report."""
    # Collect YAML files
    yaml_files: list[Path] = sorted(
        p for p in SKILLS_DIR.rglob("*") if p.suffix in (".yaml", ".yml")
    )

    if not yaml_files:
        print("No YAML files found in", SKILLS_DIR)
        sys.exit(1)

    issues: list[Issue] = []
    seen_ids: dict[str, Path] = {}
    yaml_skill_ids: set[str] = set()

    skills_data: list[tuple[Path, dict]] = []
    for path in yaml_files:
        data = _load_yaml_simple(path)
        if data is None:
            issues.append(Issue("FAIL", "parse", str(path.relative_to(ROOT)), "failed to parse YAML"))
            continue
        skills_data.append((path, data))

    # ── Check each skill ──
    for path, data in skills_data:
        rel_path = str(path.relative_to(ROOT))
        skill_id = data.get("id", rel_path)

        # 1. Required fields
        for field in REQUIRED_FIELDS:
            if field not in data:
                issues.append(Issue("WARN", "fields", skill_id, f"missing '{field}' field"))

        # Track ID
        if "id" in data:
            yaml_skill_ids.add(data["id"])

        # 2. ID consistency
        expected_id = _path_to_expected_id(path)
        actual_id = data.get("id", "")
        if actual_id and actual_id != expected_id:
            issues.append(Issue("FAIL", "id_consistency", rel_path, f"id '{actual_id}' does not match expected '{expected_id}'"))

        # 3. Content length
        content = data.get("content", "")
        if isinstance(content, str):
            content_len = len(content.strip())
            if content_len == 0:
                issues.append(Issue("FAIL", "fields", skill_id, "content is empty"))
            elif content_len < MIN_CONTENT_LENGTH:
                issues.append(Issue("WARN", "fields", skill_id, f"content too short ({content_len} chars)"))

        # 4. Token estimate accuracy
        if "token_estimate" in data and "content" in data:
            declared = data["token_estimate"]
            if isinstance(declared, (int, float)) and isinstance(data["content"], str):
                calculated = _estimate_tokens(data["content"].strip())
                if calculated > 0 and declared > 0:
                    off_pct = abs(declared - calculated) / calculated
                    if off_pct > TOKEN_ESTIMATE_TOLERANCE:
                        issues.append(Issue(
                            "WARN", "token_estimate", skill_id,
                            f"token_estimate={declared}, calculated={calculated} ({off_pct:.0%} off)",
                        ))

        # 5. Valid type
        skill_type = data.get("type", "")
        if skill_type and skill_type not in VALID_TYPES:
            issues.append(Issue("FAIL", "fields", skill_id, f"invalid type '{skill_type}' (expected: {', '.join(sorted(VALID_TYPES))})"))

        # 6. Tags non-empty
        tags = data.get("tags")
        if tags is not None:
            if not isinstance(tags, list) or len(tags) == 0:
                issues.append(Issue("WARN", "fields", skill_id, "tags is empty or not a list"))
        # (missing tags is caught by required fields check)

        # 7. Domain consistency
        domain = data.get("domain", "")
        if domain and actual_id:
            # Map domain to expected skill ID prefix(es)
            domain_prefix_map: dict[str, list[str]] = {
                "development.backend": ["dev.backend"],
                "development.frontend": ["dev.frontend"],
                "development.database": ["dev.backend.database"],
                "development.infra": ["dev.infra"],
                "development.security": ["dev.security"],
                "development.performance": ["dev.performance"],
                "development.ai": ["dev.ai"],
                "qa": ["qa.code-review", "qa.test-gen", "qa.ux-audit"],
                "qa.code-review": ["qa.code-review"],
                "qa.testing": ["qa.test-gen", "qa.code-review", "qa.ux-audit"],
                "qa.ux-audit": ["qa.ux-audit"],
            }
            prefixes = domain_prefix_map.get(domain, [domain])
            if not any(
                actual_id.startswith(p + ".") or actual_id == p for p in prefixes
            ):
                expected = " or ".join(f"'{p}.*'" for p in prefixes)
                issues.append(Issue("WARN", "domain", skill_id, f"domain '{domain}' does not match id prefix (expected {expected})"))

        # 8. Duplicate IDs
        if actual_id:
            if actual_id in seen_ids:
                issues.append(Issue("FAIL", "duplicate", skill_id, f"duplicate id (also in {seen_ids[actual_id].relative_to(ROOT)})"))
            else:
                seen_ids[actual_id] = path

    # ── Selector coverage ──
    selector_ids = _extract_selector_skill_ids()
    orphaned = yaml_skill_ids - selector_ids
    phantom = selector_ids - yaml_skill_ids
    registered_count = len(yaml_skill_ids & selector_ids)

    for sid in sorted(phantom):
        issues.append(Issue("WARN", "phantom", sid, "referenced in selector.py but no YAML file found"))

    # ── Report ──
    total = len(yaml_files)
    field_issues = [i for i in issues if i.category == "fields"]
    id_issues = [i for i in issues if i.category == "id_consistency"]
    token_issues = [i for i in issues if i.category == "token_estimate"]
    domain_issues = [i for i in issues if i.category == "domain"]
    dup_issues = [i for i in issues if i.category == "duplicate"]
    parse_issues = [i for i in issues if i.category == "parse"]
    phantom_issues = [i for i in issues if i.category == "phantom"]

    critical = sum(1 for i in issues if i.level == "FAIL")
    warnings = sum(1 for i in issues if i.level == "WARN")

    print("=== AI Pipeline Skill Quality Audit ===")
    print()
    print(f"Total skills scanned: {total}")

    # Field checks
    print()
    print("--- Field Checks ---")
    if field_issues:
        for i in field_issues:
            print(i)
    else:
        print("All field checks passed.")

    # Parse errors
    if parse_issues:
        print()
        print("--- Parse Errors ---")
        for i in parse_issues:
            print(i)

    # ID consistency
    print()
    print("--- ID Consistency ---")
    if id_issues:
        for i in id_issues:
            print(i)
    else:
        print("All IDs match file paths.")

    # Domain consistency
    print()
    print("--- Domain Consistency ---")
    if domain_issues:
        for i in domain_issues:
            print(i)
    else:
        print("All domains match ID prefixes.")

    # Duplicates
    if dup_issues:
        print()
        print("--- Duplicate IDs ---")
        for i in dup_issues:
            print(i)

    # Token estimate
    print()
    print("--- Token Estimate ---")
    if token_issues:
        for i in token_issues:
            print(i)
    else:
        print("All token estimates within tolerance.")

    # Selector coverage
    print()
    print("--- Selector Coverage ---")
    if yaml_skill_ids:
        pct = registered_count / len(yaml_skill_ids) * 100
        print(f"Registered in selector: {registered_count}/{len(yaml_skill_ids)} ({pct:.1f}%)")
    else:
        print("No skill IDs found.")
    print(f"Orphaned (YAML only): {len(orphaned)} skills")
    print(f"Phantom (selector only): {len(phantom)} skills")
    if phantom_issues:
        for i in phantom_issues:
            print(f"  {i}")

    # Summary
    print()
    print("--- Summary ---")
    print(f"Total issues: {len(issues)}")
    print(f"  Critical: {critical}")
    print(f"  Warnings: {warnings}")
    print()
    if len(issues) == 0:
        print("All checks passed! \u2713")
    else:
        print(f"{len(issues)} issues found")

    sys.exit(1 if critical > 0 else 0)


if __name__ == "__main__":
    audit()
