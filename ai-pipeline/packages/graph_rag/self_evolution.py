"""자가 발전 루프 — 실행 결과 기반 가중치 업데이트, 자동 엣지, 감쇠."""

from __future__ import annotations

import logging
from collections import Counter
from datetime import datetime
from itertools import combinations
from typing import Any

from .config import GraphRAGSettings, get_settings
from .models import EvolutionEvent
from .neo4j_client import Neo4jClient
from .schema import (
    CREATE_CO_OCCURS_EDGE,
    DECAY_ALL_WEIGHTS,
    UPDATE_EDGE_WEIGHT,
    UPDATE_SKILL_STATS,
)

logger = logging.getLogger(__name__)

# 동시 활성화 추적 (메모리 내, 프로덕션에서는 Redis/DB)
_co_occurrence_counter: Counter[tuple[str, str]] = Counter()


async def record_execution(
    neo4j: Neo4jClient,
    skill_ids: list[str],
    status: str,
    settings: GraphRAGSettings | None = None,
) -> EvolutionEvent:
    """실행 결과 기록 + 가중치 업데이트.

    Args:
        neo4j: Neo4j 클라이언트
        skill_ids: 실행된 스킬 ID 목록
        status: "PASS" 또는 "FAIL"
        settings: 설정

    Returns:
        EvolutionEvent
    """
    settings = settings or get_settings()
    timestamp = datetime.now().isoformat()
    delta = (
        settings.evolution_success_delta
        if status == "PASS"
        else settings.evolution_failure_delta
    )

    # 1. 각 스킬 통계 업데이트
    for skill_id in skill_ids:
        try:
            await neo4j.run_void(
                UPDATE_SKILL_STATS,
                {"skill_id": skill_id, "status": status, "timestamp": timestamp},
            )
        except Exception as e:
            logger.debug("Failed to update stats for %s: %s", skill_id, e)

    # 2. 스킬 간 엣지 가중치 업데이트
    for i, src in enumerate(skill_ids):
        for tgt in skill_ids[i + 1:]:
            for edge_type in ["REQUIRES", "FEEDS", "CO_CREATES", "CO_OCCURS"]:
                try:
                    await neo4j.run_void(
                        UPDATE_EDGE_WEIGHT,
                        {
                            "source_id": src,
                            "target_id": tgt,
                            "edge_type": edge_type,
                            "status": status,
                            "delta": delta,
                        },
                    )
                except Exception as e:
                    logger.debug("Edge weight update skipped %s→%s: %s", src, tgt, e)

    # 3. 동시 활성화 추적 + 자동 엣지 생성
    await _track_co_occurrence(neo4j, skill_ids, settings)

    event = EvolutionEvent(
        skill_ids=skill_ids,
        status=status,
        timestamp=timestamp,
    )

    logger.info(
        "Evolution recorded: %s, %d skills, delta=%.3f",
        status, len(skill_ids), delta,
    )

    return event


async def _track_co_occurrence(
    neo4j: Neo4jClient,
    skill_ids: list[str],
    settings: GraphRAGSettings,
) -> None:
    """동시 활성화 추적. threshold(기본 3) 이상이면 CO_OCCURS 엣지 자동 생성."""
    for a, b in combinations(sorted(skill_ids), 2):
        pair = (a, b)
        _co_occurrence_counter[pair] += 1

        if _co_occurrence_counter[pair] >= settings.evolution_co_occur_threshold:
            try:
                await neo4j.run_void(
                    CREATE_CO_OCCURS_EDGE,
                    {
                        "source_id": a,
                        "target_id": b,
                        "threshold": settings.evolution_co_occur_threshold,
                    },
                )
                logger.info("Auto CO_OCCURS edge: %s → %s (count=%d)", a, b, _co_occurrence_counter[pair])
            except Exception as e:
                logger.debug("CO_OCCURS creation failed %s→%s: %s", a, b, e)


async def apply_decay(
    neo4j: Neo4jClient,
    settings: GraphRAGSettings | None = None,
) -> None:
    """전체 엣지 가중치 감쇠 (decay_factor=0.95).

    주기적으로 실행하여 오래된 연결의 영향력을 줄인다.
    """
    settings = settings or get_settings()
    try:
        await neo4j.run_void(
            DECAY_ALL_WEIGHTS,
            {"decay_factor": settings.evolution_decay_factor},
        )
        logger.info("Applied decay factor %.3f to all edges", settings.evolution_decay_factor)
    except Exception as e:
        logger.error("Decay failed: %s", e)


async def get_evolution_stats(neo4j: Neo4jClient) -> dict[str, Any]:
    """자가 발전 통계 조회."""
    # 실행 횟수 상위
    top_executed = await neo4j.run(
        """
        MATCH (s:Skill)
        WHERE s.executionCount > 0
        RETURN s.id AS id, s.executionCount AS count, s.successRate AS rate
        ORDER BY s.executionCount DESC
        LIMIT 10
        """
    )

    # 자동 생성 엣지
    auto_edges = await neo4j.run(
        """
        MATCH ()-[r:CO_OCCURS]->()
        WHERE r.autoCreated = true
        RETURN count(r) AS count
        """
    )

    # 가중치 분포
    weight_stats = await neo4j.run(
        """
        MATCH ()-[r]->()
        RETURN type(r) AS type, avg(r.weight) AS avgWeight, min(r.weight) AS minWeight, max(r.weight) AS maxWeight
        """
    )

    return {
        "top_executed": top_executed,
        "auto_edges": auto_edges[0]["count"] if auto_edges else 0,
        "weight_distribution": weight_stats,
        "co_occurrence_tracking": len(_co_occurrence_counter),
    }
