#!/usr/bin/env python3
"""Auto-generate Atomic Skill YAML files.

Usage:
    python scripts/generate_skill.py --domain dev.backend --topic caching --type rule
    python scripts/generate_skill.py --domain dev.backend --topic caching --type rule --tags "cache,redis,performance"
    python scripts/generate_skill.py --batch skills_to_create.json
    python scripts/generate_skill.py --batch skills_to_create.json --force
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

VALID_TYPES = {"role", "rule", "pattern", "verify", "stack"}

# Domain prefix mapping (dot notation → directory path)
DOMAIN_PREFIX_MAP = {
    "dev": "dev",
    "development": "dev",
    "design": "design",
    "planning": "planning",
    "marketing": "marketing",
    "analytics": "analytics",
    "content": "content",
    "qa": "qa",
    "meta": "meta",
}

CONTENT_TEMPLATES = {
    "role": "당신은 {topic} 전문가입니다.\n\n## 역할\n- {topic} 관련 작업을 수행합니다\n- 베스트 프랙티스를 적용합니다\n- 코드 품질을 보장합니다",
    "rule": "# {topic} 규칙\n\n## 핵심 원칙\n- TODO: 핵심 원칙을 작성하세요\n\n## DO\n- TODO: 권장 사항을 작성하세요\n\n## DON'T\n- TODO: 금지 사항을 작성하세요",
    "pattern": "# {topic} 패턴\n\n## 패턴 설명\nTODO: 패턴의 목적과 적용 상황을 설명하세요\n\n## 구현 예시\n```\nTODO: 코드 예시를 작성하세요\n```\n\n## 주의사항\n- TODO: 주의사항을 작성하세요",
    "verify": "# {topic} 검증 체크리스트\n\n- [ ] TODO: 검증 항목 1\n- [ ] TODO: 검증 항목 2\n- [ ] TODO: 검증 항목 3",
    "stack": "# {topic} 기술 스택\n\n## 필수 기술\n- TODO: 기술 스택을 나열하세요\n\n## 권장 라이브러리\n- TODO: 권장 라이브러리를 나열하세요",
}


def _estimate_tokens(content: str) -> int:
    """Estimate token count."""
    korean_chars = sum(1 for c in content if "\uac00" <= c <= "\ud7a3")
    ratio = korean_chars / len(content) if content else 0
    if ratio > 0.1:
        return len(content) // 2
    return len(content) // 4


def _domain_to_path(domain: str) -> str:
    """Convert dot domain to directory path. e.g., dev.backend → dev/backend"""
    parts = domain.split(".")
    first = DOMAIN_PREFIX_MAP.get(parts[0], parts[0])
    return "/".join([first] + parts[1:])


def _build_skill_id(domain: str, topic: str) -> str:
    """Build full skill ID. e.g., dev.backend + caching → dev.backend.caching"""
    # Normalize domain prefix
    parts = domain.split(".")
    first = DOMAIN_PREFIX_MAP.get(parts[0], parts[0])
    normalized = ".".join([first] + parts[1:])
    return f"{normalized}.{topic}"


def _domain_to_yaml_domain(domain: str) -> str:
    """Convert shorthand domain to full YAML domain field.
    e.g., dev.backend → development.backend
    """
    REVERSE_MAP = {
        "dev": "development",
    }
    parts = domain.split(".")
    first = REVERSE_MAP.get(parts[0], parts[0])
    return ".".join([first] + parts[1:])


def generate_skill(
    domain: str,
    topic: str,
    skill_type: str = "rule",
    tags: list[str] | None = None,
    force: bool = False,
) -> Path | None:
    """Generate a single skill YAML file.

    Returns the path of the created file, or None if skipped.
    """
    if skill_type not in VALID_TYPES:
        print(f"  ERROR: Invalid type '{skill_type}'. Valid: {VALID_TYPES}")
        return None

    skill_id = _build_skill_id(domain, topic)
    dir_path = SKILLS_DIR / _domain_to_path(domain)
    file_path = dir_path / f"{topic}.yaml"

    if file_path.exists() and not force:
        try:
            rel = file_path.relative_to(ROOT)
        except ValueError:
            rel = file_path
        print(f"  SKIP: {rel} already exists (use --force to overwrite)")
        return None

    # Auto-generate tags if not provided
    if tags is None:
        tags = [topic.replace("-", " ").replace("_", " ")]
        # Add domain-related tags
        domain_parts = domain.split(".")
        if len(domain_parts) > 1:
            tags.append(domain_parts[-1])

    content = CONTENT_TEMPLATES.get(skill_type, CONTENT_TEMPLATES["rule"]).format(topic=topic)
    yaml_domain = _domain_to_yaml_domain(domain)

    skill_data = {
        "id": skill_id,
        "domain": yaml_domain,
        "type": skill_type,
        "theory": f"{topic} — TODO: 이론 설명 추가",
        "bloom_level": "APPLY",
        "tags": tags,
        "token_estimate": _estimate_tokens(content),
        "content": content,
    }

    # Validate required fields
    required = {"id", "domain", "type", "tags", "content", "token_estimate"}
    missing = required - set(skill_data.keys())
    if missing:
        print(f"  ERROR: Missing required fields: {missing}")
        return None

    dir_path.mkdir(parents=True, exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        yaml.dump(skill_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    try:
        rel = file_path.relative_to(ROOT)
    except ValueError:
        rel = file_path
    print(f"  CREATED: {rel} (id={skill_id}, type={skill_type})")
    return file_path


def batch_generate(batch_file: str, force: bool = False) -> None:
    """Generate multiple skills from a JSON batch file.

    Expected format:
    [
        {"domain": "dev.backend", "topic": "caching", "type": "rule", "tags": ["cache", "redis"]},
        {"domain": "dev.frontend", "topic": "ssr", "type": "pattern"}
    ]
    """
    path = Path(batch_file)
    if not path.exists():
        print(f"ERROR: Batch file not found: {batch_file}")
        sys.exit(1)

    with open(path, encoding="utf-8") as f:
        if path.suffix == ".csv":
            import csv
            reader = csv.DictReader(f)
            items = list(reader)
            for item in items:
                if "tags" in item and isinstance(item["tags"], str):
                    item["tags"] = [t.strip() for t in item["tags"].split(",")]
        else:
            items = json.load(f)

    created = 0
    skipped = 0
    errors = 0

    for item in items:
        domain = item.get("domain", "")
        topic = item.get("topic", "")
        skill_type = item.get("type", "rule")
        tags = item.get("tags")

        if not domain or not topic:
            print(f"  ERROR: Missing domain or topic: {item}")
            errors += 1
            continue

        result = generate_skill(domain, topic, skill_type, tags, force)
        if result:
            created += 1
        else:
            skipped += 1

    print()
    print("=== Batch Generation Summary ===")
    print(f"  Created: {created}")
    print(f"  Skipped: {skipped}")
    print(f"  Errors:  {errors}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Atomic Skill YAML files")
    parser.add_argument("--domain", help="Skill domain (e.g., dev.backend)")
    parser.add_argument("--topic", help="Skill topic (e.g., caching)")
    parser.add_argument("--type", default="rule", choices=sorted(VALID_TYPES), help="Skill type")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--batch", help="Path to JSON/CSV batch file")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")

    args = parser.parse_args()

    if args.batch:
        batch_generate(args.batch, args.force)
    elif args.domain and args.topic:
        tags = [t.strip() for t in args.tags.split(",")] if args.tags else None
        result = generate_skill(args.domain, args.topic, args.type, tags, args.force)
        if not result:
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
