"""3홉 확산 활성화 엔진 — 시드 스킬에서 관련 스킬을 그래프 탐색으로 발견."""

from __future__ import annotations

import logging

from .config import GraphRAGSettings, get_settings
from .models import ActivatedSkill
from .neo4j_client import Neo4jClient

logger = logging.getLogger(__name__)

# 확산 활성화를 위한 최적화된 Cypher 쿼리
# - 3홉까지 탐색하되, 각 홉에서 decay와 threshold 적용
# - 시드 노드 자체는 결과에서 제외
SPREAD_QUERY = """
// 시드 노드들
MATCH (seed:Skill)
WHERE seed.id IN $seed_ids

// 1홉
WITH seed
OPTIONAL MATCH (seed)-[r1]->(h1:Skill)
WHERE type(r1) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
  AND NOT h1.id IN $seed_ids
WITH seed, h1, r1.weight * $decay AS score1
WHERE score1 >= $threshold_initial AND h1 IS NOT NULL

// 결과 1홉 수집
WITH collect({id: h1.id, score: score1, hop: 1, seed: seed.id}) AS hop1_results,
     collect(DISTINCT h1) AS hop1_nodes

// 2홉
UNWIND hop1_nodes AS h1
WITH hop1_results, h1
OPTIONAL MATCH (h1)-[r2]->(h2:Skill)
WHERE type(r2) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
  AND NOT h2.id IN $seed_ids
  AND NOT h2.id = h1.id
WITH hop1_results, h1, h2, r2
// h1의 최고 점수를 hop1_results에서 찾기
WITH hop1_results, h2,
     [x IN hop1_results WHERE x.id = h1.id | x.score][0] * r2.weight * $decay AS score2
WHERE score2 >= $threshold_hop AND h2 IS NOT NULL

WITH hop1_results,
     collect({id: h2.id, score: score2, hop: 2}) AS hop2_results,
     collect(DISTINCT h2) AS hop2_nodes

// 3홉
UNWIND hop2_nodes AS h2
WITH hop1_results, hop2_results, h2
OPTIONAL MATCH (h2)-[r3]->(h3:Skill)
WHERE type(r3) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
  AND NOT h3.id IN $seed_ids
WITH hop1_results, hop2_results, h3, r3, h2,
     [x IN hop2_results WHERE x.id = h2.id | x.score][0] * r3.weight * $decay AS score3
WHERE score3 >= $threshold_hop AND h3 IS NOT NULL

WITH hop1_results + hop2_results +
     collect({id: h3.id, score: score3, hop: 3}) AS all_results

// 중복 제거 (같은 id에서 최고 score, 최저 hop)
UNWIND all_results AS r
WITH r.id AS skillId, max(r.score) AS activationScore, min(r.hop) AS hopDistance
RETURN skillId, activationScore, hopDistance
ORDER BY activationScore DESC
"""

# 더 단순하고 안정적인 쿼리 (홉별 분리)
HOP1_QUERY = """
MATCH (seed:Skill)-[r]->(target:Skill)
WHERE seed.id IN $seed_ids
  AND type(r) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
  AND NOT target.id IN $seed_ids
WITH target.id AS skillId,
     max(r.weight * $decay * seed.activationValue) AS activationScore
WHERE activationScore >= $threshold
RETURN skillId, activationScore, 1 AS hopDistance
ORDER BY activationScore DESC
"""

HOP2_QUERY = """
MATCH (seed:Skill)-[r1]->(h1:Skill)-[r2]->(target:Skill)
WHERE seed.id IN $seed_ids
  AND type(r1) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
  AND type(r2) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
  AND NOT target.id IN $seed_ids
  AND NOT target.id = seed.id
WITH target.id AS skillId,
     max(r1.weight * r2.weight * $decay * $decay * seed.activationValue) AS activationScore
WHERE activationScore >= $threshold
RETURN skillId, activationScore, 2 AS hopDistance
ORDER BY activationScore DESC
"""

HOP3_QUERY = """
MATCH (seed:Skill)-[r1]->(h1:Skill)-[r2]->(h2:Skill)-[r3]->(target:Skill)
WHERE seed.id IN $seed_ids
  AND type(r1) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
  AND type(r2) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
  AND type(r3) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
  AND NOT target.id IN $seed_ids
  AND target.id <> h1.id
  AND target.id <> seed.id
WITH target.id AS skillId,
     max(r1.weight * r2.weight * r3.weight * $decay * $decay * $decay * seed.activationValue) AS activationScore
WHERE activationScore >= $threshold
RETURN skillId, activationScore, 3 AS hopDistance
ORDER BY activationScore DESC
"""


async def spread_activation(
    neo4j: Neo4jClient,
    seed_ids: list[str],
    settings: GraphRAGSettings | None = None,
) -> list[ActivatedSkill]:
    """시드 스킬에서 3홉 확산 활성화.

    Args:
        neo4j: Neo4j 클라이언트
        seed_ids: 시드 스킬 ID 목록
        settings: 확산 파라미터

    Returns:
        활성화된 스킬 목록 (score 내림차순)
    """
    if not seed_ids:
        return []

    settings = settings or get_settings()

    params_hop1 = {
        "seed_ids": seed_ids,
        "decay": settings.spread_decay,
        "threshold": settings.spread_threshold_initial,
    }
    params_hop23 = {
        "seed_ids": seed_ids,
        "decay": settings.spread_decay,
        "threshold": settings.spread_threshold_hop,
    }

    # 각 홉별 쿼리 실행
    results_map: dict[str, ActivatedSkill] = {}

    try:
        # 1홉
        hop1 = await neo4j.run(HOP1_QUERY, params_hop1)
        for row in hop1:
            sid = row["skillId"]
            results_map[sid] = ActivatedSkill(
                skill_id=sid,
                activation_score=row["activationScore"],
                source="graph",
                hop_distance=1,
            )

        # 2홉
        hop2 = await neo4j.run(HOP2_QUERY, params_hop23)
        for row in hop2:
            sid = row["skillId"]
            if sid not in results_map or row["activationScore"] > results_map[sid].activation_score:
                results_map[sid] = ActivatedSkill(
                    skill_id=sid,
                    activation_score=row["activationScore"],
                    source="graph",
                    hop_distance=2,
                )

        # 3홉 (max_hops >= 3일 때만)
        if settings.spread_max_hops >= 3:
            hop3 = await neo4j.run(HOP3_QUERY, params_hop23)
            for row in hop3:
                sid = row["skillId"]
                if sid not in results_map or row["activationScore"] > results_map[sid].activation_score:
                    results_map[sid] = ActivatedSkill(
                        skill_id=sid,
                        activation_score=row["activationScore"],
                        source="graph",
                        hop_distance=3,
                    )

    except Exception as e:
        logger.error("Spread activation failed: %s", e)
        return []

    activated = sorted(results_map.values(), key=lambda x: x.activation_score, reverse=True)

    logger.info(
        "Spread activation: %d seeds → %d activated (hop1=%d, hop2=%d, hop3=%d)",
        len(seed_ids),
        len(activated),
        sum(1 for a in activated if a.hop_distance == 1),
        sum(1 for a in activated if a.hop_distance == 2),
        sum(1 for a in activated if a.hop_distance == 3),
    )

    return activated
