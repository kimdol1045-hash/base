"""Skill Recommendation Engine — 사용 패턴 기반 스킬 추천.

Co-occurrence 분석과 도메인 친화도를 기반으로 스킬을 추천.
"""

from __future__ import annotations

import threading
from collections import Counter, defaultdict

# Co-occurrence matrix: tracks which skills are used together
_cooccurrence_lock = threading.Lock()
_cooccurrence: dict[str, Counter] = defaultdict(Counter)  # skill_id -> {co_skill_id: count}
_MIN_COOCCURRENCE = 2  # minimum co-occurrence count to recommend


def record_cooccurrence(skill_ids: list[str]) -> None:
    """Record co-occurrence for a set of skills used together."""
    with _cooccurrence_lock:
        for i, sid in enumerate(skill_ids):
            for j, other in enumerate(skill_ids):
                if i != j:
                    _cooccurrence[sid][other] += 1


def _domain_from_id(skill_id: str) -> str:
    """Extract domain from skill_id. e.g., dev.backend.auth.role → development.backend"""
    parts = skill_id.split(".")
    # Map short prefixes to full domain names
    domain_map = {
        "dev": "development",
        "qa": "qa",
        "design": "design",
        "marketing": "marketing",
        "analytics": "analytics",
        "content": "content",
        "meta": "meta",
        "planning": "planning",
    }
    if parts:
        first = domain_map.get(parts[0], parts[0])
        if len(parts) >= 3:
            return f"{first}.{parts[1]}"
        return first
    return ""


# Domain affinity: related domains get a boost
DOMAIN_AFFINITY = {
    "development.backend": ["development.database", "development.security", "qa.testing"],
    "development.frontend": ["design.design-system", "development.performance", "design.ux-psychology"],
    "development.database": ["development.backend", "analytics"],
    "development.security": ["development.backend", "qa.code-review"],
    "development.ai": ["meta", "development.backend"],
    "development.infra": ["development.backend", "qa.testing"],
    "design.ux-psychology": ["design.wireframe", "design.design-system"],
    "marketing.seo": ["content", "marketing.growth"],
    "marketing.growth": ["analytics", "marketing.persuasion"],
    "analytics": ["development.database", "marketing.growth"],
    "qa.testing": ["development.backend", "qa.code-review"],
}


def recommend_skills(
    current_skills: list[str],
    top_n: int = 5,
    exclude: list[str] | None = None,
) -> list[dict]:
    """Recommend skills based on co-occurrence and domain affinity.

    Args:
        current_skills: Currently selected skill IDs
        top_n: Number of recommendations to return
        exclude: Skill IDs to exclude from recommendations

    Returns:
        List of {skill_id, score, reason} dicts
    """
    exclude_set = set(exclude or []) | set(current_skills)
    candidates: dict[str, dict] = {}  # skill_id -> {score, reasons}

    # 1. Co-occurrence based recommendations
    with _cooccurrence_lock:
        for sid in current_skills:
            if sid in _cooccurrence:
                for co_skill, count in _cooccurrence[sid].most_common(20):
                    if co_skill in exclude_set:
                        continue
                    if count < _MIN_COOCCURRENCE:
                        continue
                    if co_skill not in candidates:
                        candidates[co_skill] = {"score": 0.0, "reasons": []}
                    candidates[co_skill]["score"] += count * 0.5
                    candidates[co_skill]["reasons"].append(f"co-occurs with {sid} ({count}x)")

    # 2. Domain affinity based recommendations
    current_domains = set()
    for sid in current_skills:
        current_domains.add(_domain_from_id(sid))

    # Get all skill IDs from YAML files (cached)
    _ensure_skill_index()

    for domain in current_domains:
        related_domains = DOMAIN_AFFINITY.get(domain, [])
        for related in related_domains:
            for candidate_id in _skill_index.get(related, []):
                if candidate_id in exclude_set:
                    continue
                if candidate_id not in candidates:
                    candidates[candidate_id] = {"score": 0.0, "reasons": []}
                candidates[candidate_id]["score"] += 0.3
                candidates[candidate_id]["reasons"].append(f"domain affinity: {domain}\u2192{related}")

    # 3. Tag overlap based recommendations
    current_tags = set()
    for sid in current_skills:
        info = _skill_info.get(sid, {})
        current_tags.update(info.get("tags", []))

    for candidate_id, info in _skill_info.items():
        if candidate_id in exclude_set:
            continue
        overlap = current_tags & set(info.get("tags", []))
        if len(overlap) >= 2:
            if candidate_id not in candidates:
                candidates[candidate_id] = {"score": 0.0, "reasons": []}
            candidates[candidate_id]["score"] += len(overlap) * 0.2
            candidates[candidate_id]["reasons"].append(f"shared tags: {', '.join(list(overlap)[:3])}")

    # Sort by score and return top_n
    sorted_candidates = sorted(candidates.items(), key=lambda x: x[1]["score"], reverse=True)

    return [
        {
            "skill_id": skill_id,
            "score": round(data["score"], 2),
            "reason": data["reasons"][0] if data["reasons"] else "related skill",
        }
        for skill_id, data in sorted_candidates[:top_n]
    ]


# ─── Skill Index (lazy loaded) ───

_skill_index: dict[str, list[str]] = {}  # domain -> [skill_ids]
_skill_info: dict[str, dict] = {}  # skill_id -> {tags, domain}
_index_loaded = False


def _ensure_skill_index() -> None:
    """Lazy-load skill index from YAML files."""
    global _index_loaded
    if _index_loaded:
        return

    import yaml
    from pathlib import Path
    import os

    skill_dir = Path(os.getenv("SKILL_DIR", Path(__file__).resolve().parent.parent.parent / "skills"))

    for path in skill_dir.rglob("*.yaml"):
        if "_archive" in str(path):
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if data and "id" in data:
                sid = data["id"]
                domain = data.get("domain", "")
                tags = data.get("tags", [])
                _skill_info[sid] = {"domain": domain, "tags": tags}
                if domain not in _skill_index:
                    _skill_index[domain] = []
                _skill_index[domain].append(sid)
        except Exception:
            continue

    _index_loaded = True


def get_recommendation_stats() -> dict:
    """Return recommendation engine stats."""
    with _cooccurrence_lock:
        total_pairs = sum(sum(c.values()) for c in _cooccurrence.values())
        unique_skills = len(_cooccurrence)

    return {
        "total_cooccurrence_pairs": total_pairs,
        "unique_skills_tracked": unique_skills,
        "skill_index_size": len(_skill_info),
        "domain_count": len(_skill_index),
    }
