"""Hook Engine 단위 테스트 — 분류, 선택, POST 체크, 통합."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock
import json

import pytest

from packages.hook_engine.classifier import _parse_json_response, classify_with_haiku
from packages.hook_engine.engine import run_hook_engine
from packages.hook_engine.models import BloomLevel, Session, SkillAssemblyPlan
from packages.hook_engine.post_checks import generate_post_checks
from packages.hook_engine.selector import (
    BASE_SKILLS,
    KEYWORD_SKILLS,
    select_skills,
    select_skills_hybrid,
)


# ─── Classifier 테스트 ───


class TestClassifier:
    def test_parse_valid_json(self):
        text = '{"domains": ["development.backend"], "bloom": "CREATE", "complexity": 5, "semantic_keywords": ["auth"], "is_followup": false}'
        result = _parse_json_response(text)
        assert result["domains"] == ["development.backend"]
        assert result["complexity"] == 5

    def test_parse_json_in_code_block(self):
        text = '```json\n{"domains": ["planning"], "bloom": "ANALYZE", "complexity": 3, "semantic_keywords": [], "is_followup": false}\n```'
        result = _parse_json_response(text)
        assert result["domains"] == ["planning"]

    def test_parse_invalid_json_fallback(self):
        result = _parse_json_response("not json at all")
        assert result["domains"] == ["planning"]  # 기본값
        assert result["reasoning"] == "parse_failed"

    @pytest.mark.asyncio
    async def test_classify_backend_request(self):
        """백엔드 요청 → development.backend 도메인."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "domains": ["development.backend"],
            "bloom": "CREATE",
            "complexity": 5,
            "semantic_keywords": ["auth", "jwt"],
            "is_followup": False,
        }))]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        session = Session(session_id="test")
        result = await classify_with_haiku("로그인 API 만들어줘", session, mock_client)

        assert "development.backend" in result["domains"]
        assert result["bloom"] == BloomLevel.CREATE
        assert result["complexity"] == 5
        assert "auth" in result["semantic_keywords"]

    @pytest.mark.asyncio
    async def test_classify_followup_detection(self):
        """후속 요청 감지."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "domains": ["development.backend"],
            "bloom": "CREATE",
            "complexity": 4,
            "semantic_keywords": ["oauth"],
            "is_followup": True,
        }))]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        session = Session(session_id="test", active_domains=["development.backend"])
        result = await classify_with_haiku("소셜 로그인도 추가해줘", session, mock_client)
        assert result["is_followup"] is True

    @pytest.mark.asyncio
    async def test_classify_api_failure_fallback(self):
        """API 실패 시 기본값 반환."""
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(side_effect=Exception("API error"))

        session = Session(session_id="test")
        result = await classify_with_haiku("테스트", session, mock_client)

        assert result["domains"] == ["planning"]
        assert result["bloom"] == BloomLevel.APPLY
        assert result["complexity"] == 3

    @pytest.mark.asyncio
    async def test_classify_complexity_capped_at_10(self):
        """복잡도 최대 10 제한."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "domains": ["planning"],
            "bloom": "CREATE",
            "complexity": 99,
            "semantic_keywords": [],
            "is_followup": False,
        }))]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        session = Session(session_id="test")
        result = await classify_with_haiku("test", session, mock_client)
        assert result["complexity"] == 10


# ─── Selector 테스트 ───


class TestSelector:
    def test_backend_domain_skills(self):
        session = Session(session_id="test")
        skills = select_skills(["development.backend"], [], 3, session)
        assert len(skills) > 0
        assert "dev.backend.api.role" in skills

    def test_keyword_skills_added(self):
        session = Session(session_id="test")
        skills = select_skills(["development.backend"], ["auth"], 3, session)
        assert "dev.backend.auth.role" in skills
        assert "dev.backend.auth.jwt-auth" in skills

    def test_high_complexity_adds_security(self):
        """복잡도 >= 5이고 dev 도메인이면 보안 Skill 추가."""
        session = Session(session_id="test")
        skills = select_skills(["development.backend"], [], 5, session)
        assert "dev.security.owasp" in skills
        assert "qa.code-review.security" in skills

    def test_high_complexity_adds_bias_for_planning(self):
        session = Session(session_id="test")
        skills = select_skills(["planning"], [], 5, session)
        assert "meta.bias-prevention.confirmation-bias" in skills
        assert "meta.bias-prevention.planning-fallacy" in skills

    def test_deduplication(self):
        session = Session(session_id="test")
        skills = select_skills(
            ["development.backend", "development.security"],
            ["security"],
            5,
            session,
        )
        assert len(skills) == len(set(skills)), "중복 발견"

    def test_followup_preserves_previous_skills(self):
        """후속 요청 시 이전 Skill 유지."""
        session = Session(
            session_id="test",
            accumulated_skills=["dev.backend.api.role", "dev.backend.api.rest"],
        )
        skills = select_skills(["development.backend"], [], 3, session)
        assert "dev.backend.api.role" in skills
        assert "dev.backend.api.rest" in skills

    def test_unknown_domain_returns_empty_base(self):
        session = Session(session_id="test")
        skills = select_skills(["unknown.domain"], [], 3, session)
        # 알 수 없는 도메인이면 BASE가 없으나 키워드로 추가 가능
        assert isinstance(skills, list)

    def test_all_base_domains_have_skills(self):
        """모든 BASE_SKILLS 도메인이 1개 이상 스킬을 가짐."""
        for domain, skill_list in BASE_SKILLS.items():
            assert len(skill_list) >= 1, f"Domain {domain} has no skills"

    def test_all_keyword_entries_have_skills(self):
        """모든 KEYWORD_SKILLS 키워드가 1개 이상 스킬을 가짐."""
        for kw, skill_list in KEYWORD_SKILLS.items():
            assert len(skill_list) >= 1, f"Keyword {kw} has no skills"


class TestSelectorHybrid:
    @pytest.mark.asyncio
    async def test_hybrid_returns_list(self):
        session = Session(session_id="test")
        result = await select_skills_hybrid(
            "로그인 API 만들어줘",
            ["development.backend"],
            ["auth"],
            5,
            session,
        )
        assert isinstance(result, list)
        assert len(result) > 0

    @pytest.mark.asyncio
    async def test_hybrid_superset_of_static(self):
        """하이브리드 결과는 정적 결과를 포함."""
        session = Session(session_id="test")
        static = select_skills(["development.backend"], ["auth"], 5, session)

        session2 = Session(session_id="test2")
        hybrid = await select_skills_hybrid(
            "로그인 API 만들어줘",
            ["development.backend"],
            ["auth"],
            5,
            session2,
        )
        for s in static:
            assert s in hybrid


# ─── POST Checks 테스트 ───


class TestPostChecks:
    def test_backend_checks(self):
        checks = generate_post_checks(["development.backend"], [])
        assert len(checks) > 0
        assert any("Zod" in c for c in checks)
        assert any("SQL" in c or "sql" in c.lower() for c in checks)

    def test_auth_keyword_checks(self):
        checks = generate_post_checks([], ["auth"])
        assert any("OWASP" in c for c in checks)
        assert any("토큰" in c for c in checks)

    def test_payment_keyword_checks(self):
        checks = generate_post_checks([], ["payment"])
        assert any("멱등" in c for c in checks)

    def test_deduplication(self):
        """같은 도메인+키워드에서 중복 체크 제거."""
        checks = generate_post_checks(
            ["development.backend", "development.security"],
            ["auth", "security"],
        )
        assert len(checks) == len(set(checks))

    def test_empty_inputs(self):
        checks = generate_post_checks([], [])
        assert checks == []

    def test_multiple_domains(self):
        checks = generate_post_checks(
            ["development.backend", "planning", "design"],
            [],
        )
        assert any("Zod" in c for c in checks)  # backend
        assert any("MVP" in c for c in checks)   # planning
        assert any("CTA" in c for c in checks)   # design


# ─── Engine 통합 테스트 ───


class TestEngine:
    @pytest.mark.asyncio
    async def test_run_hook_engine_basic(self):
        """기본 파이프라인 실행."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "domains": ["development.backend"],
            "bloom": "CREATE",
            "complexity": 5,
            "semantic_keywords": ["auth"],
            "is_followup": False,
        }))]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        plan = await run_hook_engine(
            user_input="로그인 API 만들어줘",
            session_id="test-engine",
            client=mock_client,
        )

        assert isinstance(plan, SkillAssemblyPlan)
        assert len(plan.skill_ids) > 0
        assert len(plan.domains) > 0
        assert plan.complexity == 5
        assert plan.bloom_level == BloomLevel.CREATE

    @pytest.mark.asyncio
    async def test_engine_model_selection_haiku(self):
        """복잡도 <= 3 → haiku 모델."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "domains": ["content"],
            "bloom": "APPLY",
            "complexity": 2,
            "semantic_keywords": [],
            "is_followup": False,
        }))]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        plan = await run_hook_engine("간단한 블로그 작성", "test-haiku", client=mock_client)
        assert plan.executor_model == "haiku"

    @pytest.mark.asyncio
    async def test_engine_model_selection_opus(self):
        """복잡도 >= 7 → opus 모델."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "domains": ["development.backend", "development.frontend", "planning"],
            "bloom": "CREATE",
            "complexity": 8,
            "semantic_keywords": ["auth", "payment", "microservice"],
            "is_followup": False,
        }))]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        plan = await run_hook_engine("대규모 결제 시스템", "test-opus", client=mock_client)
        assert plan.executor_model == "opus"

    @pytest.mark.asyncio
    async def test_engine_warnings_on_large_budget(self):
        """토큰 예산 초과 시 경고."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "domains": ["development.backend", "development.security"],
            "bloom": "CREATE",
            "complexity": 7,
            "semantic_keywords": ["auth", "payment", "security", "microservice"],
            "is_followup": False,
        }))]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        plan = await run_hook_engine("대규모 시스템", "test-warn", client=mock_client)
        # 다수의 스킬 → 토큰 경고 또는 도메인 경고 가능
        assert isinstance(plan.warnings, list)

    @pytest.mark.asyncio
    async def test_engine_post_checks_included(self):
        """POST 체크리스트 생성 확인."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "domains": ["development.backend"],
            "bloom": "CREATE",
            "complexity": 5,
            "semantic_keywords": ["auth"],
            "is_followup": False,
        }))]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        plan = await run_hook_engine("로그인", "test-checks", client=mock_client)
        assert len(plan.post_checks) > 0

    @pytest.mark.asyncio
    async def test_engine_session_accumulation(self):
        """세션에 스킬 누적."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text=json.dumps({
            "domains": ["development.backend"],
            "bloom": "CREATE",
            "complexity": 3,
            "semantic_keywords": [],
            "is_followup": False,
        }))]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        from packages.hook_engine.models import get_or_create_session

        plan = await run_hook_engine("API 만들어줘", "test-session-acc", client=mock_client)
        session = get_or_create_session("test-session-acc")

        assert len(session.history) == 1
        assert len(session.accumulated_skills) > 0
        assert session.active_domains == plan.domains
