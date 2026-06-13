"""Pipeline Orchestrator — Hook Engine → Skill Assembly → Plan 반환.

코드 생성은 Claude Code가 수행. 이 모듈은 Plan 준비와 POST 검증만 담당.
"""

from __future__ import annotations

import asyncio
import logging
import uuid

import anthropic

from packages.hook_engine.engine import run_hook_engine
from packages.hook_engine.models import SkillAssemblyPlan, get_or_create_session, save_session
from packages.hook_engine.selector import MODEL_CONTEXT_LIMITS
from packages.post_validator.validator import validate_output
from packages.skill_store.server import assemble_prompt

logger = logging.getLogger(__name__)

MAX_RETRIES = 2
# 복잡도 2 이하인 요청은 POST 검증 스킵 (비용 최적화)
POST_VALIDATION_SKIP_THRESHOLD = 2
# 세션 컨텍스트 최대 크기 (출력 저장 최대 수)
MAX_SESSION_OUTPUTS = 10
# 세션 누적 스킬 최대 수
MAX_SESSION_SKILLS = 50


def _get_max_tokens(complexity: int) -> int:
    """복잡도 기반 max_tokens 동적 조절."""
    if complexity <= 3:
        return 2048
    if complexity <= 6:
        return 4096
    return 8192


# ─── 도메인별 실행 순서 ───

DOMAIN_EXECUTION_ORDER = [
    "planning",
    "planning.business",
    "planning.project-mgmt",
    "design",
    "design.ux-psychology",
    "design.wireframe",
    "design.design-system",
    "development.database",
    "development.backend",
    "development.security",
    "development.frontend",
    "development.performance",
    "development.ai",
    "development.infra",
    "marketing",
    "marketing.persuasion",
    "marketing.seo",
    "marketing.growth",
    "analytics",
    "content",
    "qa",
    "qa.code-review",
    "qa.testing",
    "qa.ux-audit",
    "meta",
]


async def prepare_plan(
    user_input: str,
    session_id: str | None = None,
    client: anthropic.AsyncAnthropic | None = None,
) -> dict:
    """Hook Engine → Skill Assembly → Plan 반환.

    코드 생성은 하지 않는다. Claude Code가 이 Plan의
    system_prompt를 받아서 직접 코드를 생성한다.

    Returns:
        단일 실행:
        {
            mode: "single",
            session_id, system_prompt, post_checks,
            model_hint, max_tokens, plan, skip_validation, warnings
        }

        분할 실행:
        {
            mode: "split",
            session_id, plans: [...], warnings
        }
    """
    if client is None:
        client = anthropic.AsyncAnthropic()

    if session_id is None:
        session_id = str(uuid.uuid4())

    # ─── Hook Engine ───
    plan = await run_hook_engine(
        user_input=user_input,
        session_id=session_id,
        assemble_fn=assemble_prompt,
        client=client,
    )

    # 토큰 초과 + 다중 도메인 → 분할 계획 반환
    if plan.token_budget > 3000 and len(plan.domains) > 1:
        return await _prepare_split_plans(user_input, session_id, plan, client)

    skip_validation = plan.complexity <= POST_VALIDATION_SKIP_THRESHOLD

    return {
        "mode": "single",
        "session_id": session_id,
        "system_prompt": plan.assembled_prompt or "당신은 시니어 엔지니어입니다.",
        "post_checks": plan.post_checks,
        "model_hint": plan.executor_model,
        "max_tokens": _get_max_tokens(plan.complexity),
        "plan": _plan_to_dict(plan),
        "skip_validation": skip_validation,
        "warnings": plan.warnings,
        "token_budget_used": plan.token_budget,
        "token_budget_limit": MODEL_CONTEXT_LIMITS.get(plan.executor_model, 16000),
    }


async def _prepare_split_plans(
    user_input: str,
    session_id: str,
    plan: SkillAssemblyPlan,
    client: anthropic.AsyncAnthropic,
) -> dict:
    """다중 도메인 요청을 도메인별 Plan으로 분할 준비."""
    sorted_domains = sorted(
        plan.domains,
        key=lambda d: (
            DOMAIN_EXECUTION_ORDER.index(d)
            if d in DOMAIN_EXECUTION_ORDER
            else len(DOMAIN_EXECUTION_ORDER)
        ),
    )

    plans: list[dict] = []
    all_warnings = list(plan.warnings)
    all_warnings.append(f"자동 분할 실행: {sorted_domains}")

    for domain in sorted_domains:
        # 도메인별 사전 분류 — Haiku 재호출 방지
        sub_classification = {
            "domains": [domain],
            "bloom": plan.bloom_level,
            "complexity": plan.complexity,
            "semantic_keywords": plan.semantic_keywords,
            "is_followup": False,
        }
        sub_result = await run_hook_engine(
            user_input=f"[도메인: {domain}] {user_input}",
            session_id=session_id,
            assemble_fn=assemble_prompt,
            client=client,
            pre_classification=sub_classification,
        )

        skip_validation = sub_result.complexity <= POST_VALIDATION_SKIP_THRESHOLD

        plans.append({
            "domain": domain,
            "system_prompt": sub_result.assembled_prompt or "당신은 시니어 엔지니어입니다.",
            "post_checks": sub_result.post_checks,
            "model_hint": sub_result.executor_model,
            "max_tokens": _get_max_tokens(sub_result.complexity),
            "skip_validation": skip_validation,
            "skill_ids": sub_result.skill_ids,
        })

    return {
        "mode": "split",
        "session_id": session_id,
        "plans": plans,
        "overall_plan": _plan_to_dict(plan),
        "warnings": all_warnings,
    }


async def validate_and_record(
    output: str,
    plan_result: dict,
    client: anthropic.AsyncAnthropic | None = None,
) -> dict:
    """Claude Code가 생성한 출력을 POST 검증 + evolution 피드백 기록.

    Args:
        output: Claude Code가 생성한 코드/텍스트
        plan_result: prepare_plan()이 반환한 dict
        client: Anthropic 클라이언트 (검증용 Haiku 호출)

    Returns:
        { status, issues, pass_count, fail_count, check_details }
    """
    if client is None:
        client = anthropic.AsyncAnthropic()

    # 검증 스킵 판단
    skip_validation = plan_result.get("skip_validation", False)
    post_checks = plan_result.get("post_checks", [])
    session_id = plan_result.get("session_id", "")

    if skip_validation or not post_checks:
        status = "PASS"
        result = {"status": status, "issues": "", "pass_count": 0, "fail_count": 0, "check_details": []}
    else:
        validation = await validate_output(
            output=output,
            post_checks=post_checks,
            client=client,
        )
        result = {
            "status": validation.status,
            "issues": validation.issues,
            "pass_count": validation.pass_count,
            "fail_count": validation.fail_count,
            "check_details": validation.check_details,
        }
        status = validation.status

    # 세션에 출력 기록
    if session_id:
        session = get_or_create_session(session_id)
        session.previous_outputs.append(output[:2000])
        if len(session.previous_outputs) > MAX_SESSION_OUTPUTS:
            session.previous_outputs = session.previous_outputs[-MAX_SESSION_OUTPUTS:]
        if len(session.accumulated_skills) > MAX_SESSION_SKILLS:
            session.accumulated_skills = session.accumulated_skills[-MAX_SESSION_SKILLS:]
        save_session(session)

    # Evolution 피드백 (fire-and-forget)
    skill_ids = plan_result.get("plan", {}).get("skill_ids", [])
    if skill_ids:
        asyncio.create_task(_record_evolution_feedback(skill_ids, status))

    return result


async def _record_evolution_feedback(skill_ids: list[str], status: str) -> None:
    """자가 발전 피드백 기록 (Graph RAG 미가용 시 무시)."""
    try:
        from packages.graph_rag.neo4j_client import Neo4jClient
        from packages.graph_rag.self_evolution import record_execution

        async with Neo4jClient() as neo4j:
            if await neo4j.verify_connection():
                await record_execution(neo4j, skill_ids, status)
    except ImportError:
        pass  # graph_rag 미설치
    except Exception as e:
        logger.debug("Evolution feedback skipped: %s", e)


def _plan_to_dict(plan: SkillAssemblyPlan) -> dict:
    """SkillAssemblyPlan → JSON 직렬화 가능 dict."""
    return {
        "skill_ids": plan.skill_ids,
        "domains": plan.domains,
        "bloom_level": plan.bloom_level.name,
        "complexity": plan.complexity,
        "executor_model": plan.executor_model,
        "token_budget": plan.token_budget,
        "post_checks": plan.post_checks,
        "is_followup": plan.is_followup,
        "warnings": plan.warnings,
    }
