"""엣지 추출기 — selector.py의 BASE_SKILLS/KEYWORD_SKILLS에서 초기 엣지 생성."""

from __future__ import annotations

import logging
from itertools import combinations

from .models import SkillEdge, EdgeType

logger = logging.getLogger(__name__)

# selector.py에서 가져옴 (순환 참조 방지를 위해 지연 임포트)


def _get_skill_dicts() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """selector.py에서 BASE_SKILLS, KEYWORD_SKILLS 가져오기."""
    from packages.hook_engine.selector import BASE_SKILLS, KEYWORD_SKILLS
    return BASE_SKILLS, KEYWORD_SKILLS


# ─── Skill Type 추론 ───

# id 끝부분으로 skill type 추론
TYPE_SUFFIXES = {
    "role": "role",
    "verify": "verify",
    "stack": "stack",
}

MIDDLE_TYPES = {"rule", "pattern", "rest", "validation", "error", "middleware",
                "schema", "query", "transaction", "index", "solid", "gestalt",
                "typography", "spacing", "responsive", "accessibility",
                "aida", "headline", "storytelling", "cta",
                "hook-model", "social-proof", "reciprocity", "authority", "scarcity",
                "ab-testing", "metrics", "bayesian",
                "inverted-pyramid", "readability", "structure",
                "priority", "readability", "security", "integration",
                "confirmation-bias", "availability-bias", "planning-fallacy"}


def _infer_type(skill_id: str) -> str:
    """Skill ID에서 타입 추론."""
    last_part = skill_id.rsplit(".", 1)[-1] if "." in skill_id else skill_id
    if last_part in TYPE_SUFFIXES:
        return TYPE_SUFFIXES[last_part]
    return "middle"  # rule/pattern 등 중간 단계


def _get_domain_from_id(skill_id: str) -> str:
    """Skill ID에서 도메인 추출. e.g., dev.backend.api.role → dev.backend"""
    parts = skill_id.split(".")
    if len(parts) >= 2:
        return ".".join(parts[:2])
    return parts[0]


# ─── BASE_SKILLS 엣지 추출 ───

def extract_base_edges() -> list[SkillEdge]:
    """BASE_SKILLS에서 도메인 내 role→middle→verify 순서 엣지 추출.

    규칙:
    - role → 모든 middle: REQUIRES (0.90)
    - middle → verify: FEEDS (0.80)
    - middle → middle (순서상 인접): FEEDS (0.70)
    """
    base_skills, _ = _get_skill_dicts()
    edges: list[SkillEdge] = []

    for domain, skill_ids in base_skills.items():
        roles: list[str] = []
        middles: list[str] = []
        verifies: list[str] = []

        for sid in skill_ids:
            t = _infer_type(sid)
            if t == "role":
                roles.append(sid)
            elif t == "verify":
                verifies.append(sid)
            else:
                middles.append(sid)

        # role → middle (REQUIRES, 0.90)
        for role in roles:
            for mid in middles:
                edges.append(SkillEdge(
                    source_id=role,
                    target_id=mid,
                    edge_type=EdgeType.REQUIRES,
                    weight=0.90,
                ))

        # role → verify (REQUIRES, 0.85)
        for role in roles:
            for verify in verifies:
                edges.append(SkillEdge(
                    source_id=role,
                    target_id=verify,
                    edge_type=EdgeType.REQUIRES,
                    weight=0.85,
                ))

        # middle → verify (FEEDS, 0.80)
        for mid in middles:
            for verify in verifies:
                edges.append(SkillEdge(
                    source_id=mid,
                    target_id=verify,
                    edge_type=EdgeType.FEEDS,
                    weight=0.80,
                ))

        # middle → middle 순서 (FEEDS, 0.70)
        for i in range(len(middles) - 1):
            edges.append(SkillEdge(
                source_id=middles[i],
                target_id=middles[i + 1],
                edge_type=EdgeType.FEEDS,
                weight=0.70,
            ))

    logger.info("Extracted %d edges from BASE_SKILLS", len(edges))
    return edges


# ─── KEYWORD_SKILLS 엣지 추출 ───

def extract_keyword_edges() -> list[SkillEdge]:
    """KEYWORD_SKILLS에서 같은 키워드 그룹 내 스킬 쌍 엣지 추출.

    규칙:
    - 같은 도메인: CO_CREATES (0.60)
    - 다른 도메인: FEEDS (0.50)
    """
    _, keyword_skills = _get_skill_dicts()
    edges: list[SkillEdge] = []
    seen: set[tuple[str, str]] = set()

    for keyword, skill_ids in keyword_skills.items():
        for a, b in combinations(skill_ids, 2):
            # 방향 정규화 (중복 방지)
            pair = (min(a, b), max(a, b))
            if pair in seen:
                continue
            seen.add(pair)

            domain_a = _get_domain_from_id(a)
            domain_b = _get_domain_from_id(b)

            if domain_a == domain_b:
                edges.append(SkillEdge(
                    source_id=a,
                    target_id=b,
                    edge_type=EdgeType.CO_CREATES,
                    weight=0.60,
                ))
            else:
                edges.append(SkillEdge(
                    source_id=a,
                    target_id=b,
                    edge_type=EdgeType.FEEDS,
                    weight=0.50,
                ))

    logger.info("Extracted %d edges from KEYWORD_SKILLS", len(edges))
    return edges


def extract_all_edges() -> list[SkillEdge]:
    """모든 초기 엣지 추출."""
    base = extract_base_edges()
    keyword = extract_keyword_edges()
    all_edges = base + keyword

    # 중복 제거 (source+target+type 기준으로 높은 weight 유지)
    edge_map: dict[tuple[str, str, str], SkillEdge] = {}
    for edge in all_edges:
        key = (edge.source_id, edge.target_id, edge.edge_type.value)
        if key not in edge_map or edge.weight > edge_map[key].weight:
            edge_map[key] = edge

    deduped = list(edge_map.values())
    logger.info("Total unique edges: %d (base=%d, keyword=%d)", len(deduped), len(base), len(keyword))
    return deduped
