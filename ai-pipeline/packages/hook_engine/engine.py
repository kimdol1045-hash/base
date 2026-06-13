"""Hook Engine 메인 — 요구사항 → SkillAssemblyPlan 반환."""

from __future__ import annotations

import logging

import anthropic

from .classifier import classify_with_haiku
from .models import SkillAssemblyPlan, get_or_create_session, save_session
from .post_checks import generate_post_checks
from .selector import select_skills_hybrid, _trim_to_budget

logger = logging.getLogger(__name__)

# 평균 Atomic Skill 토큰 수 (추정) — 이론+예제 보강 후 상향
AVG_TOKENS_PER_SKILL = 400

# 모델 선택 복잡도 임계값
COMPLEXITY_THRESHOLD_HAIKU = 3
COMPLEXITY_THRESHOLD_SONNET = 6

# 경고 임계값
TOKEN_WARNING_THRESHOLD = 3000
DOMAIN_WARNING_THRESHOLD = 3


async def run_hook_engine(
    user_input: str,
    session_id: str,
    assemble_fn=None,
    client: anthropic.AsyncAnthropic | None = None,
    pre_classification: dict | None = None,
) -> SkillAssemblyPlan:
    """Hook 엔진 메인.

    Args:
        user_input: 사용자 요구사항
        session_id: 세션 ID
        assemble_fn: 프롬프트 조립 함수 (skill_ids → prompt str).
                     None이면 빈 문자열.
        client: Anthropic 클라이언트 (테스트 시 mock 주입)
        pre_classification: 이미 분류된 결과 (분할 실행 시 Haiku 재호출 방지)

    Returns:
        SkillAssemblyPlan
    """
    session = get_or_create_session(session_id)

    # ─── Phase 1: Haiku 분류 (~200ms) ───
    if pre_classification:
        classification = pre_classification
    else:
        classification = await classify_with_haiku(user_input, session, client)

    domains: list[str] = classification["domains"]
    bloom = classification["bloom"]
    complexity: int = classification["complexity"]
    semantic_keywords: list[str] = classification["semantic_keywords"]
    is_followup: bool = classification["is_followup"]

    # 후속 요청이면 이전 도메인 유지 + 새 도메인 추가
    if is_followup and session.active_domains:
        merged = list(dict.fromkeys(session.active_domains + domains))
        domains = merged

    # 모델 선택 (complexity 기반)
    if complexity <= COMPLEXITY_THRESHOLD_HAIKU:
        executor_model = "haiku"
    elif complexity <= COMPLEXITY_THRESHOLD_SONNET:
        executor_model = "sonnet"
    else:
        executor_model = "opus"

    # ─── Phase 2: Skill 선택 (<1ms) ───
    skill_ids = await select_skills_hybrid(
        user_input, domains, semantic_keywords, complexity, session,
    )

    # ─── Phase 2.5: Token budget trim ───
    skill_ids, dropped = _trim_to_budget(skill_ids, executor_model)

    # 토큰 예산 추정
    token_budget = len(skill_ids) * AVG_TOKENS_PER_SKILL

    # ─── Phase 3: POST 체크리스트 + 프롬프트 조립 ───
    post_checks = generate_post_checks(domains, semantic_keywords)

    # 프롬프트 조립
    assembled_prompt = ""
    if assemble_fn:
        try:
            result = assemble_fn(skill_ids)
            if isinstance(result, dict):
                assembled_prompt = result.get("prompt", "")
                token_budget = result.get("total_tokens", token_budget)
            else:
                assembled_prompt = str(result)
        except Exception as e:
            logger.error("Prompt assembly failed: %s", e)

    # 경고 생성
    warnings: list[str] = []
    if dropped:
        warnings.append(f"토큰 예산 초과로 {len(dropped)}개 스킬 제외: {dropped[:3]}")
    if token_budget > TOKEN_WARNING_THRESHOLD:
        warnings.append(f"토큰 예산 {token_budget} 초과. Skill 수 줄이기 권장.")
    if len(domains) > DOMAIN_WARNING_THRESHOLD:
        warnings.append("도메인 4개 이상. 작업 분할 권장.")

    plan = SkillAssemblyPlan(
        skill_ids=skill_ids,
        post_checks=post_checks,
        domains=domains,
        bloom_level=bloom,
        complexity=complexity,
        executor_model=executor_model,
        token_budget=token_budget,
        assembled_prompt=assembled_prompt,
        is_followup=is_followup,
        original_input=user_input,
        semantic_keywords=semantic_keywords,
        warnings=warnings,
    )

    # 세션 업데이트
    session.history.append(plan)
    session.active_domains = domains
    session.accumulated_skills = list(dict.fromkeys(
        session.accumulated_skills + skill_ids
    ))
    save_session(session)

    return plan
