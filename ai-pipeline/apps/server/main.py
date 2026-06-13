"""FastAPI Server — AI Pipeline API.

Plan 준비 + POST 검증 API. 코드 생성은 Claude Code가 수행.
"""

from __future__ import annotations

import asyncio
import logging
import os
import uuid
from collections import defaultdict
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .pipeline import prepare_plan, validate_and_record

try:
    from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
    PROMETHEUS_AVAILABLE = True
except ImportError:
    PROMETHEUS_AVAILABLE = False

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)

_DECAY_INTERVAL_HOURS = int(os.environ.get("EVOLUTION_DECAY_INTERVAL_HOURS", "24"))
_AUTO_INGEST = os.environ.get("AUTO_INGEST", "").lower() in ("true", "1", "yes")


async def _decay_loop() -> None:
    """백그라운드 감쇠 루프 — Neo4j 가용 시에만 실행."""
    from packages.graph_rag.config import get_settings
    from packages.graph_rag.neo4j_client import Neo4jClient
    from packages.graph_rag.self_evolution import apply_decay

    interval = _DECAY_INTERVAL_HOURS * 3600
    while True:
        await asyncio.sleep(interval)
        try:
            async with Neo4jClient() as neo4j:
                if await neo4j.verify_connection():
                    settings = get_settings()
                    await apply_decay(neo4j, settings)
                    logger.info("Scheduled decay completed")
                else:
                    logger.warning("Decay skipped — Neo4j unavailable")
        except Exception as e:
            logger.error("Decay loop error: %s", e)


async def _start_auto_ingest_watcher() -> Any:
    """AUTO_INGEST=true 시 스킬 파일 와처 시작. Observer 또는 None 반환."""
    if not _AUTO_INGEST:
        return None
    try:
        from packages.graph_rag.watcher import start_watcher
        from packages.graph_rag.config import get_settings

        settings = get_settings()
        observer = await start_watcher(settings.skill_dir)
        logger.info("Auto-ingest watcher started (skill_dir=%s)", settings.skill_dir)
        return observer
    except Exception as e:
        logger.error("Failed to start auto-ingest watcher: %s", e)
        return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """애플리케이션 lifespan — 스케줄러 + 와처 시작/종료."""
    decay_task = asyncio.create_task(_decay_loop())
    logger.info(
        "Evolution decay scheduler started (interval=%dh)", _DECAY_INTERVAL_HOURS
    )

    observer = await _start_auto_ingest_watcher()

    if PROMETHEUS_AVAILABLE:
        try:
            from packages.skill_store.server import get_pipeline_status
            status = get_pipeline_status()
            SKILLS_TOTAL.set(status.get("total_skills", 0))
        except Exception:
            pass

    yield

    # 와처 종료
    if observer is not None:
        observer.stop()
        observer.join()
        logger.info("Auto-ingest watcher stopped")

    decay_task.cancel()
    try:
        await decay_task
    except asyncio.CancelledError:
        pass
    logger.info("Evolution decay scheduler stopped")


app = FastAPI(
    title="AI Pipeline",
    description="Atomic Skill 기반 AI 파이프라인 — Plan 준비 + POST 검증 API",
    version="0.2.0",
    lifespan=lifespan,
)

# ─── Prometheus Metrics ───
if PROMETHEUS_AVAILABLE:
    PIPELINE_REQUESTS = Counter(
        "pipeline_requests_total",
        "Total pipeline requests",
        ["mode", "status"],
    )
    PIPELINE_DURATION = Histogram(
        "pipeline_request_duration_seconds",
        "Pipeline request duration",
        ["endpoint"],
    )
    SKILLS_TOTAL = Gauge(
        "skills_total",
        "Total number of skills loaded",
    )
    VALIDATION_RESULTS = Counter(
        "validation_results_total",
        "Validation results",
        ["status"],
    )


# ─── Request / Response ───


class PlanRequest(BaseModel):
    input: str = Field(..., min_length=1, description="사용자 요구사항")
    session_id: str | None = Field(
        default=None, description="세션 ID (없으면 자동 생성)"
    )


class PlanResponse(BaseModel):
    mode: str  # "single" or "split"
    session_id: str
    system_prompt: str | None = None
    post_checks: list[str] | None = None
    model_hint: str | None = None
    max_tokens: int | None = None
    plan: dict | None = None
    overall_plan: dict | None = None
    plans: list[dict] | None = None
    skip_validation: bool = False
    warnings: list[str] = []


class ValidateRequest(BaseModel):
    output: str = Field(..., description="Claude Code가 생성한 출력")
    plan_result: dict = Field(..., description="prepare_plan이 반환한 결과")


class ValidateResponse(BaseModel):
    status: str
    issues: str = ""
    pass_count: int = 0
    fail_count: int = 0
    check_details: list[dict] = []


# ─── Endpoints ───


@app.post("/api/plan", response_model=PlanResponse)
async def plan(req: PlanRequest) -> PlanResponse:
    """요구사항 → Hook Engine → Skill 조립 → Plan 반환.

    코드 생성은 하지 않는다. Claude Code가 이 Plan을 받아 직접 코드를 생성.
    """
    session_id = req.session_id or str(uuid.uuid4())

    _start = time.time()
    try:
        result = await prepare_plan(
            user_input=req.input,
            session_id=session_id,
        )
    except Exception as e:
        if PROMETHEUS_AVAILABLE:
            PIPELINE_REQUESTS.labels(mode="error", status="500").inc()
        raise HTTPException(status_code=500, detail=str(e))

    if PROMETHEUS_AVAILABLE:
        PIPELINE_REQUESTS.labels(mode=result.get("mode", "single"), status="200").inc()
        PIPELINE_DURATION.labels(endpoint="/api/plan").observe(time.time() - _start)

    return PlanResponse(**result)


@app.post("/api/validate", response_model=ValidateResponse)
async def validate(req: ValidateRequest) -> ValidateResponse:
    """Claude Code가 생성한 출력을 POST 검증.

    plan_result는 /api/plan이 반환한 결과를 그대로 전달.
    """
    try:
        result = await validate_and_record(
            output=req.output,
            plan_result=req.plan_result,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    if PROMETHEUS_AVAILABLE:
        VALIDATION_RESULTS.labels(status=result.get("status", "UNKNOWN")).inc()

    return ValidateResponse(**result)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


@app.get("/metrics")
async def metrics():
    if not PROMETHEUS_AVAILABLE:
        return JSONResponse(
            status_code=501,
            content={"error": "prometheus_client not installed"},
        )
    from starlette.responses import Response
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


# ─── Evolution Endpoints ───


@app.get("/api/evolution/stats")
async def evolution_stats() -> JSONResponse:
    """자가 발전 통계 조회."""
    from packages.graph_rag.neo4j_client import Neo4jClient
    from packages.graph_rag.self_evolution import get_evolution_stats

    try:
        async with Neo4jClient() as neo4j:
            if not await neo4j.verify_connection():
                return JSONResponse(
                    status_code=503,
                    content={"error": "Neo4j is unavailable"},
                )
            stats = await get_evolution_stats(neo4j)
            return JSONResponse(content=stats)
    except Exception as e:
        logger.error("evolution/stats error: %s", e)
        return JSONResponse(
            status_code=503,
            content={"error": f"Neo4j connection failed: {e}"},
        )


@app.post("/api/evolution/decay")
async def evolution_decay() -> JSONResponse:
    """수동 감쇠 실행."""
    from packages.graph_rag.config import get_settings
    from packages.graph_rag.neo4j_client import Neo4jClient
    from packages.graph_rag.self_evolution import apply_decay

    try:
        async with Neo4jClient() as neo4j:
            if not await neo4j.verify_connection():
                return JSONResponse(
                    status_code=503,
                    content={"error": "Neo4j is unavailable"},
                )
            settings = get_settings()
            await apply_decay(neo4j, settings)
            return JSONResponse(
                content={
                    "status": "ok",
                    "decay_factor": settings.evolution_decay_factor,
                },
            )
    except Exception as e:
        logger.error("evolution/decay error: %s", e)
        return JSONResponse(
            status_code=503,
            content={"error": f"Neo4j connection failed: {e}"},
        )


# ─── Skill / Domain / Stats Endpoints ───

import time

_skill_cache: dict[str, Any] = {"data": None, "ts": 0.0}
_SKILL_CACHE_TTL = 300  # 5 minutes


def _get_cached_skills() -> list[dict[str, Any]]:
    """Load skills with simple TTL cache."""
    now = time.time()
    if _skill_cache["data"] is None or (now - _skill_cache["ts"]) > _SKILL_CACHE_TTL:
        from packages.graph_rag.embeddings import load_all_skills

        _skill_cache["data"] = load_all_skills()
        _skill_cache["ts"] = now
    return _skill_cache["data"]


@app.get("/api/skills")
async def list_skills(
    domain: str | None = None,
    type: str | None = None,
    search: str | None = None,
) -> JSONResponse:
    """List all skills with optional filters."""
    skills = _get_cached_skills()
    filtered = skills
    if domain:
        filtered = [s for s in filtered if s.get("domain", "") == domain]
    if type:
        filtered = [s for s in filtered if s.get("type", "") == type]
    if search:
        q = search.lower()
        filtered = [
            s for s in filtered
            if q in s.get("id", "").lower()
            or q in s.get("content", "").lower()
            or q in " ".join(s.get("tags", [])).lower()
        ]
    # Return without full content for listing (include content_hash for change detection)
    items = [
        {
            "id": s["id"],
            "domain": s.get("domain", ""),
            "type": s.get("type", ""),
            "tags": s.get("tags", []),
            "token_estimate": s.get("token_estimate", 0),
            "content_hash": s.get("content_hash", ""),
        }
        for s in filtered
    ]
    return JSONResponse(content={"skills": items, "total": len(items)})


@app.get("/api/skills/{skill_id:path}")
async def get_skill(skill_id: str) -> JSONResponse:
    """Get single skill detail."""
    skills = _get_cached_skills()
    for s in skills:
        if s["id"] == skill_id:
            return JSONResponse(content=s)
    return JSONResponse(status_code=404, content={"error": f"Skill not found: {skill_id}"})


@app.get("/api/domains")
async def list_domains() -> JSONResponse:
    """Domain-wise skill count."""
    skills = _get_cached_skills()
    counts: dict[str, int] = defaultdict(int)
    for s in skills:
        d = s.get("domain", "unknown")
        counts[d] += 1
    items = [{"domain": k, "count": v} for k, v in sorted(counts.items())]
    return JSONResponse(content={"domains": items, "total_domains": len(items)})


@app.get("/api/stats")
async def get_stats() -> JSONResponse:
    """Overall statistics."""
    skills = _get_cached_skills()
    domains: set[str] = set()
    types: set[str] = set()
    total_tokens = 0
    for s in skills:
        domains.add(s.get("domain", ""))
        types.add(s.get("type", ""))
        total_tokens += s.get("token_estimate", 0)
    return JSONResponse(
        content={
            "total_skills": len(skills),
            "total_domains": len(domains),
            "total_types": len(types),
            "total_token_estimate": total_tokens,
            "domains": sorted(domains),
            "types": sorted(types),
        }
    )


@app.get("/api/usage")
async def usage_stats(top_n: int = 20) -> JSONResponse:
    """Skill usage statistics."""
    from packages.skill_store.server import get_usage_stats
    stats = get_usage_stats(top_n)
    return JSONResponse(content=stats)


@app.get("/api/costs")
async def cost_stats() -> JSONResponse:
    """API cost statistics."""
    from packages.skill_store.server import get_cost_stats
    stats = get_cost_stats()
    return JSONResponse(content=stats)


@app.get("/api/recommendations")
async def recommendations(skill_ids: str = "", top_n: int = 5) -> JSONResponse:
    """Skill recommendations based on usage patterns."""
    from packages.skill_store.server import get_recommendations
    ids = [s.strip() for s in skill_ids.split(",") if s.strip()]
    if not ids:
        return JSONResponse(content={"recommendations": [], "message": "No skill_ids provided"})
    recs = get_recommendations(ids, top_n)
    return JSONResponse(content={"recommendations": recs})


@app.get("/api/evolution/health")
async def evolution_health() -> JSONResponse:
    """Neo4j 스키마 유효성 검사 (제약조건/인덱스 존재 확인)."""
    from packages.graph_rag.neo4j_client import Neo4jClient
    from packages.graph_rag.schema import CONSTRAINTS, INDEXES

    try:
        async with Neo4jClient() as neo4j:
            if not await neo4j.verify_connection():
                return JSONResponse(
                    status_code=503,
                    content={"error": "Neo4j is unavailable"},
                )

            # 현재 제약조건 조회
            existing_constraints = await neo4j.run(
                "SHOW CONSTRAINTS YIELD name RETURN collect(name) AS names"
            )
            constraint_names = (
                existing_constraints[0]["names"] if existing_constraints else []
            )

            # 현재 인덱스 조회
            existing_indexes = await neo4j.run(
                "SHOW INDEXES YIELD name RETURN collect(name) AS names"
            )
            index_names = existing_indexes[0]["names"] if existing_indexes else []

            # 노드/엣지 카운트
            counts = await neo4j.get_counts()

            return JSONResponse(
                content={
                    "status": "ok",
                    "neo4j_connected": True,
                    "constraints": constraint_names,
                    "indexes": index_names,
                    "expected_constraints": len(CONSTRAINTS),
                    "expected_indexes": len(INDEXES),
                    "counts": counts,
                },
            )
    except Exception as e:
        logger.error("evolution/health error: %s", e)
        return JSONResponse(
            status_code=503,
            content={"error": f"Neo4j connection failed: {e}"},
        )
