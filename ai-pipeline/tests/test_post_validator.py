"""POST Validator 단위 테스트 — Haiku 기반 출력 검증."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from packages.post_validator.validator import (
    ValidationResult,
    _parse_validation_response,
    validate_output,
)


class TestValidationResult:
    def test_pass_result(self):
        r = ValidationResult(status="PASS", output="test output")
        assert r.status == "PASS"
        assert r.issues == ""

    def test_fail_result_with_issues(self):
        r = ValidationResult(status="FAIL", output="bad output", issues="missing auth")
        assert r.status == "FAIL"
        assert "missing auth" in r.issues


class TestValidateOutput:
    @pytest.mark.asyncio
    async def test_empty_checklist_pass(self):
        """체크리스트 비어있으면 즉시 PASS."""
        result = await validate_output(output="anything", post_checks=[])
        assert result.status == "PASS"

    @pytest.mark.asyncio
    async def test_pass_verdict(self):
        """Haiku가 '최종 판정: PASS' 반환 시 PASS."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(
            text="[PASS] 모든 검증 통과\n최종 판정: PASS"
        )]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        result = await validate_output(
            output="잘 만든 코드",
            post_checks=["Zod 검증", "에러 처리"],
            client=mock_client,
        )
        assert result.status == "PASS"

    @pytest.mark.asyncio
    async def test_fail_verdict_with_issues(self):
        """Haiku가 FAIL 반환 시 issues 포함."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(
            text="[FAIL] Zod 검증 누락\n[PASS] 에러 처리 OK\n최종 판정: FAIL\n수정사항: Zod 스키마 추가 필요"
        )]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        result = await validate_output(
            output="미완성 코드",
            post_checks=["Zod 검증", "에러 처리"],
            client=mock_client,
        )
        assert result.status == "FAIL"
        assert len(result.issues) > 0
        assert "Zod" in result.issues

    @pytest.mark.asyncio
    async def test_api_error_graceful_pass(self):
        """API 에러 시 INCONCLUSIVE (검증 불가 ≠ 품질 불량)."""
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(side_effect=Exception("API timeout"))

        result = await validate_output(
            output="어떤 출력",
            post_checks=["체크1", "체크2"],
            client=mock_client,
        )
        assert result.status == "INCONCLUSIVE"
        assert "검증 실패" in result.issues

    @pytest.mark.asyncio
    async def test_pass_without_space(self):
        """'최종 판정:PASS' (공백 없음)도 인식."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(
            text="모든 항목 OK\n최종 판정:PASS"
        )]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        result = await validate_output(
            output="출력",
            post_checks=["체크1"],
            client=mock_client,
        )
        assert result.status == "PASS"

    @pytest.mark.asyncio
    async def test_output_preserved_in_result(self):
        """원본 output이 결과에 보존."""
        result = await validate_output(output="원본 출력 텍스트", post_checks=[])
        assert result.output == "원본 출력 텍스트"

    @pytest.mark.asyncio
    async def test_long_output_truncated_in_prompt(self):
        """8000자 초과 출력은 잘려서 검증 프롬프트에 전달."""
        long_output = "A" * 10000

        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="최종 판정: PASS")]

        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        result = await validate_output(
            output=long_output,
            post_checks=["체크1"],
            client=mock_client,
        )
        assert result.status == "PASS"

        # 호출된 프롬프트에 전체 10000자가 아닌 8000자만 포함되는지 확인
        call_args = mock_client.messages.create.call_args
        prompt_text = call_args.kwargs["messages"][0]["content"]
        assert len(prompt_text) < 10000 + 500  # 프롬프트 오버헤드 포함


# ─── 8-3: 파싱 안정화 테스트 ───


class TestParseValidationResponse:
    def test_standard_pass(self):
        text = "[PASS] 모든 검증 통과\n최종 판정: PASS"
        status, issues, details = _parse_validation_response(text)
        assert status == "PASS"
        assert issues == ""
        assert len(details) == 1

    def test_standard_fail(self):
        text = "[FAIL] Zod 누락\n[PASS] 에러 처리\n최종 판정: FAIL\nZod 추가 필요"
        status, issues, details = _parse_validation_response(text)
        assert status == "FAIL"
        assert len(issues) > 0
        assert len(details) == 2

    def test_no_space_verdict(self):
        text = "최종 판정:PASS"
        status, issues, _ = _parse_validation_response(text)
        assert status == "PASS"

    def test_korean_colon_verdict(self):
        text = "최종 판정： PASS"
        status, issues, _ = _parse_validation_response(text)
        assert status == "PASS"

    def test_json_verdict(self):
        text = '{"verdict": "PASS", "issues": []}'
        status, issues, _ = _parse_validation_response(text)
        assert status == "PASS"

    def test_json_fail_verdict(self):
        text = '{"verdict": "FAIL", "issues": ["Zod 누락", "에러 처리 미흡"]}'
        status, issues, _ = _parse_validation_response(text)
        assert status == "FAIL"
        assert "Zod" in issues

    def test_json_in_code_block(self):
        text = '```json\n{"verdict": "PASS"}\n```'
        status, issues, _ = _parse_validation_response(text)
        assert status == "PASS"

    def test_all_fail_items_no_verdict(self):
        """최종 판정 없이 [FAIL] 항목만 있으면 FAIL."""
        text = "[FAIL] Zod 검증 누락\n[FAIL] SQL 인젝션 방어 미흡"
        status, issues, details = _parse_validation_response(text)
        assert status == "FAIL"
        assert len(details) == 2

    def test_all_pass_items_no_verdict(self):
        """최종 판정 없이 [PASS] 항목만 있으면 PASS."""
        text = "[PASS] Zod 적용됨\n[PASS] 에러 처리 OK"
        status, issues, details = _parse_validation_response(text)
        assert status == "PASS"
        assert len(details) == 2

    def test_ambiguous_text_defaults_inconclusive(self):
        """판정 불가 텍스트는 INCONCLUSIVE."""
        text = "검증을 수행했습니다. 결과는 양호합니다."
        status, issues, _ = _parse_validation_response(text)
        assert status == "INCONCLUSIVE"

    def test_check_details_populated(self):
        """항목별 PASS/FAIL 상세가 details에 기록."""
        text = "[PASS] Zod OK\n[FAIL] 에러 처리 부족\n최종 판정: FAIL"
        status, issues, details = _parse_validation_response(text)
        assert status == "FAIL"
        assert details[0]["status"] == "PASS"
        assert details[1]["status"] == "FAIL"

    @pytest.mark.asyncio
    async def test_fail_response_has_counts(self):
        """FAIL 응답에 pass_count, fail_count 포함."""
        mock_response = MagicMock()
        mock_response.content = [MagicMock(
            text="[FAIL] Zod 누락\n[PASS] 에러 OK\n[PASS] SQL OK\n최종 판정: FAIL"
        )]
        mock_client = AsyncMock()
        mock_client.messages.create = AsyncMock(return_value=mock_response)

        result = await validate_output(
            output="코드", post_checks=["Zod", "에러", "SQL"], client=mock_client,
        )
        assert result.fail_count == 1
        assert result.pass_count == 2
