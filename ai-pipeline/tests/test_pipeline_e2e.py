"""Pipeline E2E 통합 테스트 — prepare_plan + validate_and_record mock 기반 검증."""

from __future__ import annotations

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


def _make_classify_response(
    domains: list[str],
    complexity: int = 5,
    keywords: list[str] | None = None,
    bloom: str = "APPLY",
    is_followup: bool = False,
) -> MagicMock:
    """분류 응답 mock 생성."""
    resp = MagicMock()
    resp.content = [MagicMock(text=json.dumps({
        "domains": domains,
        "bloom": bloom,
        "complexity": complexity,
        "semantic_keywords": keywords or [],
        "is_followup": is_followup,
    }))]
    return resp


def _make_validation_response(text: str) -> MagicMock:
    """검증 응답 mock."""
    resp = MagicMock()
    resp.content = [MagicMock(text=text)]
    return resp


class TestPreparePlan:
    @pytest.mark.asyncio
    async def test_login_api_plan(self):
        """'로그인 API 만들어줘' → backend 도메인 + auth 스킬 포함 Plan."""
        from apps.server.pipeline import prepare_plan

        classify_resp = _make_classify_response(
            domains=["development.backend"],
            complexity=5,
            keywords=["auth", "jwt"],
        )

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=classify_resp)

        result = await prepare_plan(
            user_input="로그인 API 만들어줘",
            session_id="test-login",
            client=mock_client,
        )

        assert result["mode"] == "single"
        assert result["session_id"] == "test-login"
        assert result["system_prompt"]  # 비어있지 않음
        assert len(result["plan"]["skill_ids"]) > 0
        assert "development.backend" in result["plan"]["domains"]
        assert result["model_hint"] == "sonnet"  # complexity 5
        assert result["max_tokens"] == 4096  # complexity 5

    @pytest.mark.asyncio
    async def test_planning_request(self):
        """'SaaS MVP 기획해줘' → planning Skill만 사용."""
        from apps.server.pipeline import prepare_plan

        classify_resp = _make_classify_response(
            domains=["planning"],
            complexity=4,
            keywords=[],
        )

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=classify_resp)

        result = await prepare_plan(
            user_input="SaaS MVP 기획해줘",
            session_id="test-planning",
            client=mock_client,
        )

        assert result["mode"] == "single"
        plan = result["plan"]
        assert "planning" in plan["domains"]
        assert any("planning" in s for s in plan["skill_ids"])

    @pytest.mark.asyncio
    async def test_model_hint_haiku_for_low_complexity(self):
        """complexity ≤ 3 → haiku hint."""
        from apps.server.pipeline import prepare_plan

        classify_resp = _make_classify_response(
            domains=["content"], complexity=2,
        )

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=classify_resp)

        result = await prepare_plan("블로그 작성", "test-model", client=mock_client)
        assert result["model_hint"] == "haiku"
        assert result["max_tokens"] == 2048

    @pytest.mark.asyncio
    async def test_high_complexity_opus(self):
        """complexity > 6 → opus hint + 8192 tokens."""
        from apps.server.pipeline import prepare_plan

        classify_resp = _make_classify_response(
            domains=["development.backend"], complexity=8,
        )

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=classify_resp)

        result = await prepare_plan("MSA 설계", "test-opus", client=mock_client)
        assert result["model_hint"] == "opus"
        assert result["max_tokens"] == 8192

    @pytest.mark.asyncio
    async def test_skip_validation_flag(self):
        """complexity ≤ 2 → skip_validation=True."""
        from apps.server.pipeline import prepare_plan

        classify_resp = _make_classify_response(
            domains=["content"], complexity=1,
        )

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=classify_resp)

        result = await prepare_plan("간단한 질문", "test-skip", client=mock_client)
        assert result["skip_validation"] is True

    @pytest.mark.asyncio
    async def test_no_skip_validation_for_complex(self):
        """complexity > 2 → skip_validation=False."""
        from apps.server.pipeline import prepare_plan

        classify_resp = _make_classify_response(
            domains=["development.backend"], complexity=5,
        )

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=classify_resp)

        result = await prepare_plan("API 만들어줘", "test-no-skip", client=mock_client)
        assert result["skip_validation"] is False

    @pytest.mark.asyncio
    async def test_session_id_auto_generated(self):
        """session_id 미제공 시 자동 생성."""
        from apps.server.pipeline import prepare_plan

        classify_resp = _make_classify_response(["content"], complexity=1)

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=classify_resp)

        result = await prepare_plan("테스트", client=mock_client)
        assert result["session_id"] is not None
        assert len(result["session_id"]) > 0

    @pytest.mark.asyncio
    async def test_only_one_api_call(self):
        """prepare_plan은 분류 Haiku 1회만 호출 (코드 생성 X)."""
        from apps.server.pipeline import prepare_plan

        classify_resp = _make_classify_response(
            domains=["development.backend"], complexity=5,
        )

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=classify_resp)

        await prepare_plan("API 만들어줘", "test-calls", client=mock_client)
        assert mock_client.messages.create.call_count == 1


class TestPrepareSplitPlans:
    @pytest.mark.asyncio
    async def test_auto_split_on_multi_domain(self):
        """토큰 초과 + 다중 도메인 → 분할 Plan 반환."""
        from apps.server.pipeline import prepare_plan

        # 메인 분류: 다중 도메인 + 높은 복잡도
        classify_main = _make_classify_response(
            domains=["planning", "development.backend", "design"],
            complexity=8,
            keywords=["auth", "payment"],
        )
        sub_classify = _make_classify_response(["planning"], complexity=4)

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            side_effect=[classify_main, sub_classify, sub_classify, sub_classify]
        )

        result = await prepare_plan(
            "풀스택 SaaS 만들어줘", "test-split", client=mock_client,
        )

        assert result["mode"] == "split"
        assert len(result["plans"]) == 3
        for plan in result["plans"]:
            assert "domain" in plan
            assert "system_prompt" in plan
            assert "post_checks" in plan
            assert "model_hint" in plan
            assert "max_tokens" in plan

    @pytest.mark.asyncio
    async def test_split_has_domain_order(self):
        """분할 시 도메인 순서가 DOMAIN_EXECUTION_ORDER를 따른다."""
        from apps.server.pipeline import prepare_plan

        classify_main = _make_classify_response(
            domains=["development.backend", "planning"],
            complexity=8,
            keywords=["auth"],
        )
        sub_classify = _make_classify_response(["planning"], complexity=4)

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(
            side_effect=[classify_main, sub_classify, sub_classify]
        )

        result = await prepare_plan("만들어줘", "test-order", client=mock_client)
        domains = [p["domain"] for p in result["plans"]]
        assert domains[0] == "planning"  # planning이 backend보다 먼저


class TestValidateAndRecord:
    @pytest.mark.asyncio
    async def test_validation_pass(self):
        """POST 검증 PASS."""
        from apps.server.pipeline import validate_and_record

        validate_resp = _make_validation_response("최종 판정: PASS")

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=validate_resp)

        plan_result = {
            "session_id": "test-val",
            "skip_validation": False,
            "post_checks": ["체크1", "체크2"],
            "plan": {"skill_ids": ["dev.backend.api.role"]},
        }

        result = await validate_and_record(
            output="좋은 코드", plan_result=plan_result, client=mock_client,
        )
        assert result["status"] == "PASS"

    @pytest.mark.asyncio
    async def test_validation_fail(self):
        """POST 검증 FAIL."""
        from apps.server.pipeline import validate_and_record

        validate_resp = _make_validation_response(
            "[FAIL] Zod 검증 누락\n최종 판정: FAIL"
        )

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=validate_resp)

        plan_result = {
            "session_id": "test-fail",
            "skip_validation": False,
            "post_checks": ["체크1"],
            "plan": {"skill_ids": ["dev.backend.api.role"]},
        }

        result = await validate_and_record(
            output="나쁜 코드", plan_result=plan_result, client=mock_client,
        )
        assert result["status"] == "FAIL"
        assert result["issues"]

    @pytest.mark.asyncio
    async def test_skip_validation(self):
        """skip_validation=True → 검증 없이 PASS."""
        from apps.server.pipeline import validate_and_record

        mock_client = AsyncMock()

        plan_result = {
            "session_id": "test-skip",
            "skip_validation": True,
            "post_checks": ["체크1"],
            "plan": {"skill_ids": ["content.role"]},
        }

        result = await validate_and_record(
            output="간단한 출력", plan_result=plan_result, client=mock_client,
        )
        assert result["status"] == "PASS"
        # API 호출 없음
        mock_client.messages.create.assert_not_called()

    @pytest.mark.asyncio
    async def test_evolution_feedback_called(self):
        """검증 후 evolution 피드백이 호출."""
        from apps.server.pipeline import validate_and_record

        validate_resp = _make_validation_response("최종 판정: PASS")

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=validate_resp)

        plan_result = {
            "session_id": "test-evolve",
            "skip_validation": False,
            "post_checks": ["체크1"],
            "plan": {"skill_ids": ["dev.backend.api.role"]},
        }

        with patch("apps.server.pipeline._record_evolution_feedback") as mock_evolve:
            mock_evolve.return_value = None
            result = await validate_and_record(
                output="코드", plan_result=plan_result, client=mock_client,
            )

            assert result["status"] == "PASS"
            mock_evolve.assert_called_once()
            call_args = mock_evolve.call_args[0]
            assert call_args[0] == ["dev.backend.api.role"]  # skill_ids
            assert call_args[1] == "PASS"  # status

    @pytest.mark.asyncio
    async def test_session_output_recorded(self):
        """검증 후 세션에 출력이 기록된다."""
        from apps.server.pipeline import validate_and_record
        from packages.hook_engine.models import get_or_create_session

        mock_client = AsyncMock()

        plan_result = {
            "session_id": "test-session-record",
            "skip_validation": True,
            "post_checks": [],
            "plan": {"skill_ids": []},
        }

        await validate_and_record(
            output="기록될 출력", plan_result=plan_result, client=mock_client,
        )

        session = get_or_create_session("test-session-record")
        assert "기록될 출력" in session.previous_outputs[-1]
