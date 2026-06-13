#!/usr/bin/env python3
"""Skill Quality Evaluator — 휴리스틱 기반 스킬 품질 점수 매기기.

Usage:
    python scripts/evaluate_skills.py
    python scripts/evaluate_skills.py --min-score 5
    python scripts/evaluate_skills.py --type rule
    python scripts/evaluate_skills.py --domain development.backend
    python scripts/evaluate_skills.py --output report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = ROOT / "skills"

# Expected sections by type
EXPECTED_SECTIONS = {
    "role": ["역할", "작업", "범위", "품질", "기준", "핵심"],
    "rule": ["핵심 원칙", "DO", "DON'T", "원칙", "규칙"],
    "pattern": ["적용", "구현", "예시", "주의", "패턴"],
    "verify": ["확인", "검증", "체크", "필수", "권장"],
    "stack": ["기술", "라이브러리", "필수", "권장"],
}

# Minimum content length by type
MIN_CONTENT_LENGTH = {
    "role": 300,
    "rule": 400,
    "pattern": 400,
    "verify": 250,
    "stack": 200,
}


def score_completeness(content: str, skill_type: str) -> float:
    """Check if skill has expected sections for its type (0-10)."""
    expected = EXPECTED_SECTIONS.get(skill_type, EXPECTED_SECTIONS["rule"])
    found = 0
    for section in expected:
        if section.lower() in content.lower():
            found += 1
    if not expected:
        return 5.0
    return min(10.0, (found / len(expected)) * 10)


def score_specificity(content: str) -> float:
    """Check for concrete examples vs vague advice (0-10)."""
    score = 5.0  # baseline

    # Code blocks = +3
    code_blocks = content.count("```")
    if code_blocks >= 2:
        score += 3.0
    elif code_blocks >= 1:
        score += 1.5

    # Specific examples (함수명, 클래스명 패턴)
    camel_case = len(re.findall(r'[a-z][A-Z]', content))
    snake_case = len(re.findall(r'[a-z]_[a-z]', content))
    if camel_case + snake_case >= 3:
        score += 1.5

    # Numbers/metrics = specificity
    numbers = len(re.findall(r'\d+', content))
    if numbers >= 3:
        score += 1.0

    return min(10.0, score)


def score_actionability(content: str) -> float:
    """Check for clear DO/DON'T or implementation steps (0-10)."""
    score = 3.0

    # Bullet points
    bullets = content.count("- ") + content.count("* ")
    if bullets >= 10:
        score += 3.0
    elif bullets >= 5:
        score += 2.0
    elif bullets >= 3:
        score += 1.0

    # Checklist items
    checklists = content.count("- [ ]") + content.count("- [x]")
    if checklists >= 5:
        score += 2.0
    elif checklists >= 2:
        score += 1.0

    # Action verbs (Korean)
    action_words = ["사용", "적용", "구현", "설정", "확인", "검증", "작성", "설계", "분석"]
    action_count = sum(1 for w in action_words if w in content)
    if action_count >= 4:
        score += 2.0
    elif action_count >= 2:
        score += 1.0

    return min(10.0, score)


def score_consistency(content: str, skill_type: str) -> float:
    """Check formatting conventions (0-10)."""
    score = 5.0

    # Has section headers
    headers = len(re.findall(r'^#{1,3}\s', content, re.MULTILINE))
    if headers >= 3:
        score += 2.0
    elif headers >= 1:
        score += 1.0

    # Content length relative to type
    min_len = MIN_CONTENT_LENGTH.get(skill_type, 300)
    length = len(content)
    if length >= min_len * 2:
        score += 2.0
    elif length >= min_len:
        score += 1.0
    elif length < min_len * 0.5:
        score -= 2.0

    # No TODO markers
    if "TODO" in content or "placeholder" in content.lower():
        score -= 3.0

    return max(0.0, min(10.0, score))


def evaluate_skill(skill: dict) -> dict:
    """Evaluate a single skill and return score breakdown."""
    content = skill.get("content", "").strip()
    skill_type = skill.get("type", "rule")
    skill_id = skill.get("id", "unknown")

    if not content:
        return {
            "id": skill_id,
            "type": skill_type,
            "domain": skill.get("domain", ""),
            "total_score": 0.0,
            "completeness": 0.0,
            "specificity": 0.0,
            "actionability": 0.0,
            "consistency": 0.0,
            "content_length": 0,
            "issues": ["Empty content"],
        }

    completeness = score_completeness(content, skill_type)
    specificity = score_specificity(content)
    actionability = score_actionability(content)
    consistency = score_consistency(content, skill_type)

    total = (completeness + specificity + actionability + consistency) / 4

    issues = []
    if completeness < 4:
        issues.append("Missing expected sections")
    if specificity < 4:
        issues.append("Lacks concrete examples")
    if actionability < 4:
        issues.append("Not actionable enough")
    if consistency < 4:
        issues.append("Formatting issues")
    if len(content) < MIN_CONTENT_LENGTH.get(skill_type, 300):
        issues.append(f"Content too short ({len(content)} chars)")
    if "TODO" in content:
        issues.append("Contains TODO markers")

    return {
        "id": skill_id,
        "type": skill_type,
        "domain": skill.get("domain", ""),
        "total_score": round(total, 2),
        "completeness": round(completeness, 2),
        "specificity": round(specificity, 2),
        "actionability": round(actionability, 2),
        "consistency": round(consistency, 2),
        "content_length": len(content),
        "issues": issues,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Skill Quality Evaluator")
    parser.add_argument("--min-score", type=float, default=0, help="Show only skills below this score")
    parser.add_argument("--type", help="Filter by skill type")
    parser.add_argument("--domain", help="Filter by domain prefix")
    parser.add_argument("--output", help="Save report as JSON")
    parser.add_argument("--top-n", type=int, default=0, help="Show top N worst skills")

    args = parser.parse_args()

    results = []
    for path in sorted(SKILLS_DIR.rglob("*.yaml")):
        if "_archive" in str(path):
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not data or "id" not in data:
                continue
            if args.type and data.get("type") != args.type:
                continue
            if args.domain and not data.get("domain", "").startswith(args.domain):
                continue
            results.append(evaluate_skill(data))
        except Exception:
            continue

    # Sort by score ascending (worst first)
    results.sort(key=lambda x: x["total_score"])

    # Filter
    if args.min_score > 0:
        results = [r for r in results if r["total_score"] < args.min_score]
    if args.top_n > 0:
        results = results[:args.top_n]

    # Display
    print(f"\n{'='*70}")
    print(f"  Skill Quality Report — {len(results)} skills evaluated")
    print(f"{'='*70}\n")

    for r in results:
        issues_str = ", ".join(r["issues"]) if r["issues"] else "OK"
        print(f"  [{r['total_score']:5.1f}] {r['id']:<50} ({r['content_length']:4d} chars) {issues_str}")

    # Summary
    if results:
        avg_score = sum(r["total_score"] for r in results) / len(results)
        print(f"\n{'─'*70}")
        print(f"  평균 점수: {avg_score:.2f}/10")

        # Per-domain averages
        domain_scores = defaultdict(list)
        for r in results:
            domain_scores[r["domain"]].append(r["total_score"])
        print(f"\n  도메인별 평균:")
        for domain in sorted(domain_scores.keys()):
            scores = domain_scores[domain]
            avg = sum(scores) / len(scores)
            print(f"    {domain:<35} {avg:.2f} ({len(scores)}개)")

        # Per-type averages
        type_scores = defaultdict(list)
        for r in results:
            type_scores[r["type"]].append(r["total_score"])
        print(f"\n  타입별 평균:")
        for t in sorted(type_scores.keys()):
            scores = type_scores[t]
            avg = sum(scores) / len(scores)
            print(f"    {t:<15} {avg:.2f} ({len(scores)}개)")

    # Save JSON
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n  Report saved: {args.output}")


if __name__ == "__main__":
    main()
