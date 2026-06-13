"""skill-store MCP Server — Atomic Skill YAML 서빙."""

import logging
import os
import re
import sys
import threading
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import yaml
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

SKILL_DIR = Path(os.getenv("SKILL_DIR", Path(__file__).resolve().parent.parent.parent / "skills"))

store = FastMCP("ai-pipeline")

# ─── Usage Tracking ───
_usage_lock = threading.Lock()
_usage_counter: Counter = Counter()
_usage_timestamps: dict[str, list[str]] = {}  # skill_id -> [iso timestamps]
_MAX_TIMESTAMPS = 100  # per skill


def _record_usage(skill_ids: list[str]) -> None:
    """Record skill usage for tracking."""
    now = datetime.now(timezone.utc).isoformat()
    with _usage_lock:
        for sid in skill_ids:
            _usage_counter[sid] += 1
            if sid not in _usage_timestamps:
                _usage_timestamps[sid] = []
            _usage_timestamps[sid].append(now)
            if len(_usage_timestamps[sid]) > _MAX_TIMESTAMPS:
                _usage_timestamps[sid] = _usage_timestamps[sid][-_MAX_TIMESTAMPS:]


# ─── Cost Tracking ───
MODEL_PRICING = {
    # USD per 1M tokens (input, output)
    "haiku": {"input": 0.80, "output": 4.00},
    "sonnet": {"input": 3.00, "output": 15.00},
    "opus": {"input": 15.00, "output": 75.00},
}

_cost_lock = threading.Lock()
_cost_records: list[dict] = []  # [{session_id, model, input_tokens, output_tokens, cost, timestamp}]
_MAX_COST_RECORDS = 1000


def _record_cost(session_id: str, model: str, input_tokens: int, output_tokens: int) -> None:
    pricing = MODEL_PRICING.get(model, MODEL_PRICING["haiku"])
    cost = (input_tokens * pricing["input"] + output_tokens * pricing["output"]) / 1_000_000
    record = {
        "session_id": session_id,
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cost_usd": round(cost, 6),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    with _cost_lock:
        _cost_records.append(record)
        if len(_cost_records) > _MAX_COST_RECORDS:
            _cost_records[:] = _cost_records[-_MAX_COST_RECORDS:]


# 인메모리 캐시
_skill_cache: dict[str, dict | None] = {}


def _resolve_path(skill_id: str) -> Path | None:
    """skill_id를 파일 경로로 변환.
    예: dev.backend.api.auth → skills/dev/backend/api/auth.yaml
    """
    parts = skill_id.split(".")
    if len(parts) < 2:
        return None
    path = SKILL_DIR / "/".join(parts[:-1]) / f"{parts[-1]}.yaml"
    return path if path.exists() else None


def _load_skill(skill_id: str) -> dict | None:
    """YAML 파일에서 Atomic Skill 로드 (캐시 적용)."""
    if skill_id in _skill_cache:
        return _skill_cache[skill_id]

    path = _resolve_path(skill_id)
    if not path:
        _skill_cache[skill_id] = None
        return None

    try:
        with open(path, encoding="utf-8") as f:
            skill = yaml.safe_load(f)
        _skill_cache[skill_id] = skill
        return skill
    except (yaml.YAMLError, OSError) as e:
        logger.warning("Failed to load skill %s: %s", skill_id, e)
        _skill_cache[skill_id] = None
        return None


def _estimate_tokens(content: str) -> int:
    """토큰 수 추정. 한국어 포함 시 len//2, 영어만 len//4."""
    if re.search(r'[\uac00-\ud7af\u3130-\u318f]', content):
        return len(content) // 2
    return len(content) // 4


# ─── Tools ───


@store.tool()
def get_skill(skill_id: str) -> dict:
    """단일 Atomic Skill 조회.

    Args:
        skill_id: Skill ID (예: dev.backend.api.auth)

    Returns:
        Skill 데이터 (id, domain, type, theory, content, tags, token_estimate)
    """
    skill = _load_skill(skill_id)
    if not skill:
        return {"error": f"Skill not found: {skill_id}"}
    return skill


@store.tool()
def get_skills_batch(skill_ids: list[str]) -> list[dict]:
    """여러 Atomic Skill 일괄 조회. Hook 엔진이 결정한 목록을 한 번에 가져온다.

    Args:
        skill_ids: Skill ID 목록

    Returns:
        찾은 Skill 데이터 리스트 (존재하지 않는 ID는 건너뜀)
    """
    results = []
    for sid in skill_ids:
        skill = _load_skill(sid)
        if skill:
            results.append(skill)
    return results


@store.tool()
def search_skills(
    domain: str = "",
    tags: list[str] | None = None,
    skill_type: str = "",
) -> list[dict]:
    """조건 기반 Atomic Skill 검색. content 제외, 메타데이터만 반환.

    Args:
        domain: 도메인 필터 (예: development.backend). 빈 문자열이면 전체.
        tags: 태그 필터. 하나라도 매칭되면 포함.
        skill_type: 타입 필터 (role/rule/pattern/verify). 빈 문자열이면 전체.

    Returns:
        매칭된 Skill 메타데이터 리스트 (id, domain, type, tags, token_estimate)
    """
    tags = tags or []
    results = []

    for path in SKILL_DIR.rglob("*.yaml"):
        try:
            with open(path, encoding="utf-8") as f:
                skill = yaml.safe_load(f)
        except (yaml.YAMLError, OSError):
            continue

        if not skill or "id" not in skill:
            continue
        if domain and not skill.get("domain", "").startswith(domain):
            continue
        if skill_type and skill.get("type") != skill_type:
            continue
        if tags and not set(tags).intersection(set(skill.get("tags", []))):
            continue

        results.append({
            "id": skill["id"],
            "domain": skill.get("domain"),
            "type": skill.get("type"),
            "tags": skill.get("tags", []),
            "token_estimate": skill.get("token_estimate", 0),
        })

    return results


# ─── 프롬프트 조립 템플릿 ───

ASSEMBLY_TEMPLATE = """{role}

## 기술 스택
{stack}

## 이 작업에서 반드시 지켜야 할 규칙
{rules}

## 작성 후 스스로 검증할 것
{verification}"""


@store.tool()
def assemble_prompt(skill_ids: list[str]) -> dict:
    """Atomic Skill들을 하나의 시스템 프롬프트로 조립.
    type별로 분류하여 자연스러운 구조를 만든다.

    Args:
        skill_ids: 조립할 Skill ID 목록 (순서 무관, type별 자동 정렬)

    Returns:
        { prompt: str, total_tokens: int, skill_count: int }
    """
    skills = get_skills_batch(skill_ids)

    role_parts: list[str] = []
    stack_parts: list[str] = []
    rule_parts: list[str] = []
    verify_parts: list[str] = []
    total_tokens = 0

    for skill in skills:
        content = skill.get("content", "").strip()
        skill_type = skill.get("type", "rule")

        # 미분류 타입 → rule로 폴백
        if skill_type not in ("role", "stack", "rule", "pattern", "verify"):
            skill_type = "rule"

        total_tokens += skill.get("token_estimate", _estimate_tokens(content))

        if skill_type == "role":
            role_parts.append(content)
        elif skill_type == "stack":
            stack_parts.append(content)
        elif skill_type in ("rule", "pattern"):
            theory = skill.get("theory", "")
            label = skill["id"].split(".")[-1]
            header = f"### {label}" + (f" ({theory})" if theory else "")
            rule_parts.append(f"{header}\n{content}")
        elif skill_type == "verify":
            verify_parts.append(content)

    prompt = ASSEMBLY_TEMPLATE.format(
        role="\n".join(role_parts) if role_parts else "당신은 시니어 엔지니어입니다.",
        stack="\n".join(stack_parts) if stack_parts else "프로젝트 기술 스택에 맞춰 작업하세요.",
        rules="\n\n".join(rule_parts) if rule_parts else "일반적인 베스트 프랙티스를 따르세요.",
        verification="\n".join(verify_parts) if verify_parts else "출력의 정확성을 스스로 검증하세요.",
    )

    _record_usage(skill_ids)

    from packages.skill_store.recommender import record_cooccurrence
    record_cooccurrence(skill_ids)

    # Estimate cost based on token budget
    # Assume output tokens ≈ 2x input tokens for generation tasks
    _record_cost(
        session_id="assemble",
        model="haiku",  # classification model
        input_tokens=total_tokens,
        output_tokens=0,
    )

    return {
        "prompt": prompt,
        "total_tokens": total_tokens,
        "skill_count": len(skills),
    }


# ─── 신규 도구 ───


@store.tool()
async def prepare_plan(input: str, session_id: str = "") -> dict:
    """전체 파이프라인 실행: 사용자 입력 → 분류 → 스킬 선택 → 프롬프트 조립.

    Hook Engine을 통해 요구사항을 분석하고, 최적의 Atomic Skill을 선택하여
    시스템 프롬프트로 조립한 Plan을 반환한다.

    Args:
        input: 사용자 요구사항 (예: "로그인 API 만들어줘")
        session_id: 세션 ID (빈 문자열이면 자동 생성)

    Returns:
        Plan dict (mode, session_id, system_prompt, post_checks, model_hint, ...)
    """
    from apps.server.pipeline import prepare_plan as _prepare_plan

    result = await _prepare_plan(
        user_input=input,
        session_id=session_id or None,
    )
    plan_skills = result.get("plan", {}).get("skill_ids", [])
    if plan_skills:
        _record_usage(plan_skills)
    return result


@store.tool()
async def validate(output: str, plan_result: dict) -> dict:
    """Claude가 생성한 출력을 POST 검증 체크리스트로 검증.

    Args:
        output: Claude가 생성한 코드/텍스트
        plan_result: prepare_plan이 반환한 결과 dict

    Returns:
        { status: PASS|FAIL|INCONCLUSIVE, issues, pass_count, fail_count, check_details }
    """
    from apps.server.pipeline import validate_and_record

    result = await validate_and_record(
        output=output,
        plan_result=plan_result,
    )
    return result


@store.tool()
async def get_evolution_stats() -> dict:
    """자가 진화 통계 조회 — Neo4j 그래프 DB의 스킬 관계 통계.

    Returns:
        { total_nodes, total_edges, avg_weight, ... } 또는 { error }
    """
    try:
        from packages.graph_rag.neo4j_client import Neo4jClient
        from packages.graph_rag.self_evolution import get_evolution_stats as _get_stats

        async with Neo4jClient() as neo4j:
            if not await neo4j.verify_connection():
                return {"error": "Neo4j is unavailable"}
            return await _get_stats(neo4j)
    except ImportError:
        return {"error": "graph_rag module not available"}
    except Exception as e:
        return {"error": f"Neo4j connection failed: {e}"}


@store.tool()
async def run_decay() -> dict:
    """가중치 감쇠 실행 — 사용되지 않는 스킬 관계의 가중치를 점진적으로 낮춤.

    Returns:
        { status: ok, decay_factor } 또는 { error }
    """
    try:
        from packages.graph_rag.config import get_settings
        from packages.graph_rag.neo4j_client import Neo4jClient
        from packages.graph_rag.self_evolution import apply_decay

        async with Neo4jClient() as neo4j:
            if not await neo4j.verify_connection():
                return {"error": "Neo4j is unavailable"}
            settings = get_settings()
            await apply_decay(neo4j, settings)
            return {"status": "ok", "decay_factor": settings.evolution_decay_factor}
    except ImportError:
        return {"error": "graph_rag module not available"}
    except Exception as e:
        return {"error": f"Decay failed: {e}"}


@store.tool()
def get_pipeline_status() -> dict:
    """파이프라인 상태 조회 — 스킬 수, 도메인, Neo4j 상태 등.

    Returns:
        { total_skills, domains, skill_types, neo4j_available }
    """
    skills = []
    for path in SKILL_DIR.rglob("*.yaml"):
        try:
            with open(path, encoding="utf-8") as f:
                skill = yaml.safe_load(f)
            if skill and "id" in skill:
                skills.append(skill)
        except (yaml.YAMLError, OSError):
            continue

    domains = sorted(set(s.get("domain", "") for s in skills))
    types = sorted(set(s.get("type", "") for s in skills))
    total_tokens = sum(s.get("token_estimate", 0) for s in skills)

    # Neo4j 가용성 체크 (동기)
    neo4j_available = False
    try:
        import importlib
        importlib.import_module("packages.graph_rag.neo4j_client")
        neo4j_available = True  # 모듈 존재 = 설정은 되어있음
    except ImportError:
        pass

    return {
        "total_skills": len(skills),
        "total_domains": len(domains),
        "domains": domains,
        "total_types": len(types),
        "types": types,
        "total_token_estimate": total_tokens,
        "neo4j_available": neo4j_available,
    }


@store.tool()
def get_domain_skills(domain: str) -> list[dict]:
    """특정 도메인의 모든 스킬 목록 조회.

    Args:
        domain: 도메인 이름 (예: "development.backend", "design")

    Returns:
        해당 도메인의 스킬 메타데이터 리스트
    """
    results = []
    for path in SKILL_DIR.rglob("*.yaml"):
        try:
            with open(path, encoding="utf-8") as f:
                skill = yaml.safe_load(f)
        except (yaml.YAMLError, OSError):
            continue

        if not skill or "id" not in skill:
            continue
        if not skill.get("domain", "").startswith(domain):
            continue

        results.append({
            "id": skill["id"],
            "domain": skill.get("domain"),
            "type": skill.get("type"),
            "tags": skill.get("tags", []),
            "token_estimate": skill.get("token_estimate", 0),
        })

    return results


@store.tool()
def get_usage_stats(top_n: int = 20) -> dict:
    """스킬 사용 통계 조회.

    Args:
        top_n: 상위 N개 스킬 반환 (기본: 20)

    Returns:
        { total_calls, unique_skills, top_skills, least_used }
    """
    with _usage_lock:
        total = sum(_usage_counter.values())
        top = _usage_counter.most_common(top_n)
        least = _usage_counter.most_common()[:-top_n-1:-1] if len(_usage_counter) > top_n else []

    return {
        "total_calls": total,
        "unique_skills_used": len(_usage_counter),
        "top_skills": [{"skill_id": k, "count": v} for k, v in top],
        "least_used": [{"skill_id": k, "count": v} for k, v in least],
    }


@store.tool()
def get_cost_stats() -> dict:
    """API 비용 통계 조회.

    Returns:
        { total_cost_usd, total_requests, per_model, recent_records }
    """
    with _cost_lock:
        records = list(_cost_records)

    total_cost = sum(r["cost_usd"] for r in records)
    per_model: dict[str, dict] = {}
    for r in records:
        m = r["model"]
        if m not in per_model:
            per_model[m] = {"requests": 0, "cost_usd": 0.0, "input_tokens": 0, "output_tokens": 0}
        per_model[m]["requests"] += 1
        per_model[m]["cost_usd"] = round(per_model[m]["cost_usd"] + r["cost_usd"], 6)
        per_model[m]["input_tokens"] += r["input_tokens"]
        per_model[m]["output_tokens"] += r["output_tokens"]

    return {
        "total_cost_usd": round(total_cost, 6),
        "total_requests": len(records),
        "per_model": per_model,
        "recent_records": records[-20:],
    }


@store.tool()
def get_recommendations(skill_ids: list[str], top_n: int = 5) -> list[dict]:
    """현재 스킬 기반 추천.

    Args:
        skill_ids: 현재 선택된 스킬 ID 목록
        top_n: 추천할 스킬 수 (기본: 5)

    Returns:
        [{skill_id, score, reason}] 리스트
    """
    from packages.skill_store.recommender import recommend_skills
    return recommend_skills(skill_ids, top_n)


@store.tool()
def get_ab_tests(status: str = "") -> list[dict]:
    """A/B 테스트 목록 조회.

    Args:
        status: 필터 (active/completed/paused). 빈 문자열이면 전체.

    Returns:
        테스트 목록
    """
    from packages.hook_engine.ab_test import get_ab_manager
    return get_ab_manager().list_tests(status)


if __name__ == "__main__":
    if "--sse" in sys.argv:
        store.run(transport="sse")
    elif "--streamable-http" in sys.argv:
        store.run(transport="streamable-http")
    else:
        store.run()
