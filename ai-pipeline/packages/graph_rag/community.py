"""Louvain 커뮤니티 탐지 — GDS 기반 스킬 클러스터링."""

from __future__ import annotations

import logging
from typing import Any

from .neo4j_client import Neo4jClient
from .schema import GDS_DROP_GRAPH, GDS_LOUVAIN, GDS_PROJECT_GRAPH, GET_COMMUNITIES

logger = logging.getLogger(__name__)


async def detect_communities(neo4j: Neo4jClient) -> dict[str, Any]:
    """Louvain 커뮤니티 탐지 실행.

    Returns:
        {
            "community_count": int,
            "modularity": float,
            "communities": [{"community": int, "skills": [...], "size": int}]
        }
    """
    # 1. 기존 프로젝션 삭제 (있으면)
    try:
        await neo4j.run_void(GDS_DROP_GRAPH)
    except Exception:
        pass  # 프로젝션이 없으면 무시

    # 2. 그래프 프로젝션 생성
    try:
        await neo4j.run_void(GDS_PROJECT_GRAPH)
        logger.info("Graph projection created: skill-graph")
    except Exception as e:
        logger.error("Graph projection failed: %s", e)
        return _fallback_communities(neo4j)

    # 3. Louvain 실행
    try:
        result = await neo4j.run(GDS_LOUVAIN)
        if not result:
            logger.warning("Louvain returned no results")
            return {"community_count": 0, "modularity": 0.0, "communities": []}

        community_count = result[0]["communityCount"]
        modularity = result[0]["modularity"]
        logger.info(
            "Louvain complete: %d communities, modularity=%.4f",
            community_count, modularity,
        )
    except Exception as e:
        logger.error("Louvain failed (GDS not installed?): %s", e)
        return await _fallback_communities(neo4j)

    # 4. 커뮤니티 결과 조회
    communities = await neo4j.run(GET_COMMUNITIES)

    # 5. 프로젝션 정리
    try:
        await neo4j.run_void(GDS_DROP_GRAPH)
    except Exception:
        pass

    return {
        "community_count": community_count,
        "modularity": modularity,
        "communities": communities,
    }


async def _fallback_communities(neo4j: Neo4jClient) -> dict[str, Any]:
    """GDS 미설치 시 도메인 기반 폴백 커뮤니티.

    도메인별로 스킬을 그룹화하여 의사(pseudo) 커뮤니티를 생성한다.
    """
    logger.info("Using domain-based fallback community detection")

    result = await neo4j.run(
        """
        MATCH (s:Skill)
        RETURN s.domain AS domain, collect(s.id) AS skills, count(s) AS size
        ORDER BY size DESC
        """
    )

    # 도메인을 커뮤니티 번호로 매핑
    communities = []
    for i, row in enumerate(result):
        communities.append({
            "community": i,
            "skills": row["skills"],
            "size": row["size"],
            "domain": row["domain"],
        })

        # 각 노드에 community 속성 설정
        for skill_id in row["skills"]:
            try:
                await neo4j.run_void(
                    "MATCH (s:Skill {id: $id}) SET s.community = $community",
                    {"id": skill_id, "community": i},
                )
            except Exception:
                pass

    return {
        "community_count": len(communities),
        "modularity": 0.0,  # 폴백은 modularity 계산 불가
        "communities": communities,
        "fallback": True,
    }


async def get_community_for_skill(
    neo4j: Neo4jClient,
    skill_id: str,
) -> list[str]:
    """특정 스킬이 속한 커뮤니티의 모든 스킬 ID 반환."""
    result = await neo4j.run(
        """
        MATCH (s:Skill {id: $id})
        WITH s.community AS comm
        MATCH (peer:Skill {community: comm})
        RETURN peer.id AS id
        """,
        {"id": skill_id},
    )
    return [row["id"] for row in result]
