"""하이브리드 선택기 — 그래프(0.5) + 벡터(0.3) + 정적(0.2) 병합."""

from __future__ import annotations

import json
import logging
from pathlib import Path

from .config import GraphRAGSettings, get_settings
from .embeddings import embed_query
from .models import ActivatedSkill, HybridResult
from .neo4j_client import Neo4jClient
from .spread_activation import spread_activation
from .vector_client import VectorClient

WEIGHT_HISTORY_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "weight_history.json"

logger = logging.getLogger(__name__)

# 도메인별 가중치 오버라이드 — 도메인 특성에 맞게 하이브리드 가중치 조절
DOMAIN_WEIGHT_OVERRIDES: dict[str, dict[str, float]] = {
    # AI 도메인: 시맨틱 유사도(벡터) 중요
    "development.ai": {"weight_graph": 0.3, "weight_vector": 0.5, "weight_static": 0.2},
    # 메타 도메인: 그래프 관계(편향 체크 등) 중요
    "meta": {"weight_graph": 0.6, "weight_vector": 0.2, "weight_static": 0.2},
    # 보안: 그래프 관계 + 정적 규칙 중요
    "development.security": {"weight_graph": 0.5, "weight_vector": 0.2, "weight_static": 0.3},
    # UX 심리학: 시맨틱 유사도 + 그래프 관계
    "design.ux-psychology": {"weight_graph": 0.4, "weight_vector": 0.4, "weight_static": 0.2},
    # QA: 정적 규칙 중요
    "qa.testing": {"weight_graph": 0.3, "weight_vector": 0.3, "weight_static": 0.4},
    "qa.code-review": {"weight_graph": 0.3, "weight_vector": 0.3, "weight_static": 0.4},
}


def get_domain_weights(domain: str, settings) -> tuple[float, float, float]:
    """도메인에 맞는 하이브리드 가중치를 반환.

    DOMAIN_WEIGHT_OVERRIDES에 도메인이 있으면 오버라이드 사용.
    없으면 settings 기본값 사용.
    부분 매칭 지원 (e.g., "development.ai.rag" → "development.ai").
    """
    # Exact match first
    if domain in DOMAIN_WEIGHT_OVERRIDES:
        w = DOMAIN_WEIGHT_OVERRIDES[domain]
        return w["weight_graph"], w["weight_vector"], w["weight_static"]

    # Partial match (parent domain)
    parts = domain.split(".")
    for i in range(len(parts) - 1, 0, -1):
        parent = ".".join(parts[:i])
        if parent in DOMAIN_WEIGHT_OVERRIDES:
            w = DOMAIN_WEIGHT_OVERRIDES[parent]
            return w["weight_graph"], w["weight_vector"], w["weight_static"]

    return settings.weight_graph, settings.weight_vector, settings.weight_static


def _load_weight_history() -> list[dict]:
    """Load weight adjustment history."""
    if WEIGHT_HISTORY_FILE.exists():
        try:
            return json.loads(WEIGHT_HISTORY_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return []


def _save_weight_history(history: list[dict]) -> None:
    """Save weight adjustment history."""
    WEIGHT_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    WEIGHT_HISTORY_FILE.write_text(
        json.dumps(history[-500:], indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def tune_weights(domain: str, validation_status: str) -> None:
    """검증 결과 기반 가중치 자동 조정.

    PASS → 현재 가중치 유지 (기록만)
    FAIL → 벡터 가중치 +0.05, 그래프 가중치 -0.05 (시맨틱 강화)
    """
    from datetime import datetime, timezone

    history = _load_weight_history()

    current = DOMAIN_WEIGHT_OVERRIDES.get(domain)

    if validation_status == "FAIL" and current:
        # Shift towards vector (semantic) when failing
        delta = 0.05
        new_graph = max(0.1, current["weight_graph"] - delta)
        new_vector = min(0.7, current["weight_vector"] + delta)
        new_static = current["weight_static"]

        # Normalize to sum to 1.0
        total = new_graph + new_vector + new_static
        DOMAIN_WEIGHT_OVERRIDES[domain] = {
            "weight_graph": round(new_graph / total, 2),
            "weight_vector": round(new_vector / total, 2),
            "weight_static": round(new_static / total, 2),
        }

    history.append({
        "domain": domain,
        "status": validation_status,
        "weights": DOMAIN_WEIGHT_OVERRIDES.get(domain, {"weight_graph": 0.5, "weight_vector": 0.3, "weight_static": 0.2}),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })

    _save_weight_history(history)


def get_weight_stats() -> dict:
    """현재 가중치 및 히스토리 반환."""
    history = _load_weight_history()
    return {
        "current_overrides": DOMAIN_WEIGHT_OVERRIDES,
        "total_adjustments": len(history),
        "recent_history": history[-20:],
    }


CONVERGENCE_FILE = Path(__file__).resolve().parent.parent.parent / "data" / "weight_convergence.json"
_ROLLING_WINDOW = 50  # last N results per domain
_LOCK_THRESHOLD = 0.9  # lock weights when pass rate > 90%
_BOOST_THRESHOLD = 0.7  # increase delta when pass rate < 70%
_BOOST_DELTA = 0.08
_NORMAL_DELTA = 0.05

# In-memory rolling results
_domain_results: dict[str, list[str]] = {}  # domain -> [PASS/FAIL/...]
_locked_domains: set[str] = set()


def record_validation_result(domain: str, status: str) -> None:
    """Record validation result for convergence tracking.

    Called after each validation to track pass/fail rates per domain.
    """
    if domain not in _domain_results:
        _domain_results[domain] = []
    _domain_results[domain].append(status)

    # Keep only rolling window
    if len(_domain_results[domain]) > _ROLLING_WINDOW:
        _domain_results[domain] = _domain_results[domain][-_ROLLING_WINDOW:]

    # Check convergence
    results = _domain_results[domain]
    if len(results) >= 10:  # minimum sample size
        pass_rate = sum(1 for r in results if r == "PASS") / len(results)

        if pass_rate >= _LOCK_THRESHOLD:
            _locked_domains.add(domain)
        elif domain in _locked_domains and pass_rate < _LOCK_THRESHOLD - 0.05:
            # Unlock if performance degrades
            _locked_domains.discard(domain)

    # Auto-tune if not locked
    if domain not in _locked_domains and domain in DOMAIN_WEIGHT_OVERRIDES:
        _auto_tune(domain)

    # Save convergence state
    _save_convergence()


def _auto_tune(domain: str) -> None:
    """Auto-tune weights based on rolling results."""
    results = _domain_results.get(domain, [])
    if len(results) < 5:
        return

    pass_rate = sum(1 for r in results[-20:] if r == "PASS") / len(results[-20:])
    current = DOMAIN_WEIGHT_OVERRIDES.get(domain)
    if not current:
        return

    # Determine delta
    delta = _BOOST_DELTA if pass_rate < _BOOST_THRESHOLD else _NORMAL_DELTA

    if pass_rate < _LOCK_THRESHOLD:
        # Shift towards vector when struggling
        new_graph = max(0.1, current["weight_graph"] - delta)
        new_vector = min(0.7, current["weight_vector"] + delta)
        new_static = current["weight_static"]

        total = new_graph + new_vector + new_static
        DOMAIN_WEIGHT_OVERRIDES[domain] = {
            "weight_graph": round(new_graph / total, 3),
            "weight_vector": round(new_vector / total, 3),
            "weight_static": round(new_static / total, 3),
        }


def _save_convergence() -> None:
    """Save convergence state to JSON."""
    CONVERGENCE_FILE.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "domain_results": {d: r[-_ROLLING_WINDOW:] for d, r in _domain_results.items()},
        "locked_domains": list(_locked_domains),
    }
    try:
        CONVERGENCE_FILE.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except OSError:
        pass


def _load_convergence() -> None:
    """Load convergence state from JSON."""
    global _domain_results, _locked_domains
    if CONVERGENCE_FILE.exists():
        try:
            data = json.loads(CONVERGENCE_FILE.read_text(encoding="utf-8"))
            _domain_results = data.get("domain_results", {})
            _locked_domains = set(data.get("locked_domains", []))
        except (json.JSONDecodeError, OSError):
            pass


def get_convergence_status() -> dict:
    """Get convergence status for all tracked domains."""
    status = {}
    for domain, results in _domain_results.items():
        if not results:
            continue
        pass_count = sum(1 for r in results if r == "PASS")
        pass_rate = pass_count / len(results) if results else 0
        status[domain] = {
            "pass_rate": round(pass_rate, 3),
            "sample_size": len(results),
            "locked": domain in _locked_domains,
            "current_weights": DOMAIN_WEIGHT_OVERRIDES.get(domain, {}),
        }
    return {
        "domains": status,
        "total_locked": len(_locked_domains),
        "total_tracked": len(_domain_results),
    }


# Load convergence state on module import
_load_convergence()


async def _graph_search(
    neo4j: Neo4jClient,
    seed_ids: list[str],
    settings: GraphRAGSettings,
) -> list[ActivatedSkill]:
    """그래프 확산 활성화 검색."""
    return await spread_activation(neo4j, seed_ids, settings)


async def _vector_search(
    vector: VectorClient,
    query: str,
    limit: int = 30,
    settings: GraphRAGSettings | None = None,
) -> list[ActivatedSkill]:
    """벡터 유사도 검색."""
    settings = settings or get_settings()
    try:
        query_embedding = await embed_query(query, settings)
        results = await vector.search(query_embedding, limit=limit)
        return [
            ActivatedSkill(
                skill_id=r["skill_id"],
                activation_score=r["score"],
                source="vector",
            )
            for r in results
        ]
    except Exception as e:
        logger.error("Vector search failed: %s", e)
        return []


def _static_search(
    static_ids: list[str],
) -> list[ActivatedSkill]:
    """정적 선택 결과 → ActivatedSkill 변환."""
    return [
        ActivatedSkill(
            skill_id=sid,
            activation_score=1.0,
            source="static",
        )
        for sid in static_ids
    ]


def _merge_results(
    graph_results: list[ActivatedSkill],
    vector_results: list[ActivatedSkill],
    static_results: list[ActivatedSkill],
    settings: GraphRAGSettings,
    domain: str = "",
) -> HybridResult:
    """세 소스의 결과를 가중 병합.

    최종 점수 = graph_weight * graph_score + vector_weight * vector_score + static_weight * static_score
    도메인이 지정되면 도메인별 가중치 오버라이드 적용.
    """
    w_graph, w_vector, w_static = get_domain_weights(domain, settings)

    score_map: dict[str, dict[str, float]] = {}

    # 그래프 점수 정규화 + 가중
    if graph_results:
        max_graph = max(r.activation_score for r in graph_results)
        for r in graph_results:
            if r.skill_id not in score_map:
                score_map[r.skill_id] = {"graph": 0.0, "vector": 0.0, "static": 0.0}
            normalized = r.activation_score / max_graph if max_graph > 0 else 0
            score_map[r.skill_id]["graph"] = max(
                score_map[r.skill_id]["graph"], normalized
            )

    # 벡터 점수 (이미 0-1 범위)
    for r in vector_results:
        if r.skill_id not in score_map:
            score_map[r.skill_id] = {"graph": 0.0, "vector": 0.0, "static": 0.0}
        score_map[r.skill_id]["vector"] = max(
            score_map[r.skill_id]["vector"], r.activation_score
        )

    # 정적 점수
    for r in static_results:
        if r.skill_id not in score_map:
            score_map[r.skill_id] = {"graph": 0.0, "vector": 0.0, "static": 0.0}
        score_map[r.skill_id]["static"] = 1.0

    # 가중 병합
    merged: list[ActivatedSkill] = []
    for skill_id, scores in score_map.items():
        final_score = (
            w_graph * scores["graph"]
            + w_vector * scores["vector"]
            + w_static * scores["static"]
        )

        # 주요 소스 결정
        source = "static"
        max_contrib = scores["static"] * w_static
        if scores["graph"] * w_graph > max_contrib:
            source = "graph"
            max_contrib = scores["graph"] * w_graph
        if scores["vector"] * w_vector > max_contrib:
            source = "vector"

        merged.append(ActivatedSkill(
            skill_id=skill_id,
            activation_score=final_score,
            source=source,
        ))

    merged.sort(key=lambda x: x.activation_score, reverse=True)

    return HybridResult(
        skills=merged,
        graph_count=len(graph_results),
        vector_count=len(vector_results),
        static_count=len(static_results),
        total_score=sum(s.activation_score for s in merged),
    )


async def hybrid_select(
    query: str,
    seed_ids: list[str],
    static_ids: list[str],
    neo4j: Neo4jClient | None = None,
    vector: VectorClient | None = None,
    settings: GraphRAGSettings | None = None,
    domain: str = "",
) -> HybridResult:
    """하이브리드 스킬 선택.

    Args:
        query: 사용자 입력 (벡터 검색용)
        seed_ids: 그래프 확산 시드 (정적 선택 결과의 핵심 스킬)
        static_ids: 정적 선택 결과
        neo4j: Neo4j 클라이언트 (None이면 자동 생성)
        vector: Qdrant 클라이언트 (None이면 자동 생성)
        settings: 설정
        domain: 도메인 (도메인별 가중치 오버라이드용)

    Returns:
        HybridResult
    """
    settings = settings or get_settings()

    graph_results: list[ActivatedSkill] = []
    vector_results: list[ActivatedSkill] = []
    static_results = _static_search(static_ids)

    # 그래프 검색
    if neo4j:
        graph_results = await _graph_search(neo4j, seed_ids, settings)
    else:
        try:
            async with Neo4jClient(settings) as n:
                graph_results = await _graph_search(n, seed_ids, settings)
        except Exception as e:
            logger.warning("Graph search unavailable, using fallback: %s", e)

    # 벡터 검색
    if vector:
        vector_results = await _vector_search(vector, query, settings=settings)
    else:
        try:
            async with VectorClient(settings) as v:
                vector_results = await _vector_search(v, query, settings=settings)
        except Exception as e:
            logger.warning("Vector search unavailable, using fallback: %s", e)

    # 병합
    result = _merge_results(graph_results, vector_results, static_results, settings, domain)

    logger.info(
        "Hybrid select: graph=%d, vector=%d, static=%d → merged=%d",
        result.graph_count,
        result.vector_count,
        result.static_count,
        len(result.skills),
    )

    return result


# ─── Cache Warmup ───

_warmup_cache: dict[str, HybridResult] = {}
_WARMUP_CACHE_SIZE = 50


def warmup_cache(common_combinations: list[list[str]]) -> int:
    """Pre-compute and cache results for common skill combinations.

    Args:
        common_combinations: List of skill_id lists to precompute

    Returns:
        Number of combinations cached
    """
    cached = 0
    for combo in common_combinations[:_WARMUP_CACHE_SIZE]:
        key = "|".join(sorted(combo))
        if key not in _warmup_cache:
            # Store a placeholder result with static scores
            _warmup_cache[key] = HybridResult(
                skills=[
                    ActivatedSkill(skill_id=sid, activation_score=1.0, source="cache")
                    for sid in combo
                ],
                graph_count=0,
                vector_count=0,
                static_count=len(combo),
                total_score=float(len(combo)),
            )
            cached += 1
    return cached


def get_cached_result(skill_ids: list[str]) -> HybridResult | None:
    """Check if a combination is in the warmup cache."""
    key = "|".join(sorted(skill_ids))
    return _warmup_cache.get(key)
