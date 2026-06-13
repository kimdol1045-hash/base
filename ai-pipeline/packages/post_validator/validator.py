"""POST Validator — Haiku 기반 출력 검증."""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field

import anthropic

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    status: str  # "PASS", "FAIL", or "INCONCLUSIVE"
    output: str
    issues: str = ""
    pass_count: int = 0
    fail_count: int = 0
    check_details: list[dict] = field(default_factory=list)


def _parse_validation_response(text: str) -> tuple[str, str, list[dict]]:
    """검증 응답을 파싱하여 (status, issues, details) 반환.

    여러 형식을 지원:
    - "최종 판정: PASS" / "최종 판정: FAIL"
    - "최종 판정:PASS" (공백 없음)
    - JSON 형식 {"verdict": "PASS", ...}
    - [PASS] / [FAIL] 항목별 매칭
    """
    details: list[dict] = []

    # 항목별 [PASS] / [FAIL] 파싱
    for match in re.finditer(r'\[(PASS|FAIL)\]\s*(.+)', text):
        details.append({
            "status": match.group(1),
            "reason": match.group(2).strip(),
        })

    # 1) "최종 판정" 텍스트 매칭 (가장 일반적)
    verdict_match = re.search(r'최종\s*판정\s*[:：]\s*(PASS|FAIL)', text)
    if verdict_match:
        status = verdict_match.group(1)
        issues = text if status == "FAIL" else ""
        return status, issues, details

    # 2) JSON 형식 시도
    try:
        # JSON 블록 추출
        json_text = text
        if "```" in text:
            for block in text.split("```"):
                block = block.strip()
                if block.startswith("json"):
                    block = block[4:].strip()
                try:
                    data = json.loads(block)
                    if "verdict" in data or "status" in data:
                        status = str(data.get("verdict", data.get("status", ""))).upper()
                        if status in ("PASS", "FAIL"):
                            issues = data.get("issues", data.get("reason", ""))
                            if isinstance(issues, list):
                                issues = "\n".join(issues)
                            return status, issues if status == "FAIL" else "", details
                except (json.JSONDecodeError, ValueError):
                    continue
        else:
            data = json.loads(json_text.strip())
            status = str(data.get("verdict", data.get("status", ""))).upper()
            if status in ("PASS", "FAIL"):
                issues = data.get("issues", data.get("reason", ""))
                if isinstance(issues, list):
                    issues = "\n".join(issues)
                return status, issues if status == "FAIL" else "", details
    except (json.JSONDecodeError, ValueError, AttributeError):
        pass

    # 3) FAIL 항목이 있으면 FAIL
    fail_items = [d for d in details if d["status"] == "FAIL"]
    if fail_items:
        issues = "\n".join(f"[FAIL] {d['reason']}" for d in fail_items)
        return "FAIL", issues, details

    # 4) PASS 항목만 있으면 PASS
    if details and all(d["status"] == "PASS" for d in details):
        return "PASS", "", details

    # 5) 마지막 수단: "PASS" / "FAIL" 단어경계 매칭
    upper_text = text.upper()
    pass_count = len(re.findall(r'\bPASS\b', upper_text))
    fail_count = len(re.findall(r'\bFAIL\b', upper_text))
    if fail_count > 0 and fail_count >= pass_count:
        return "FAIL", text, details

    # 기본: 판정 불가 시 INCONCLUSIVE
    logger.warning("Cannot determine verdict from validation response: %s", text[:200])
    return "INCONCLUSIVE", "", details


async def validate_output(
    output: str,
    post_checks: list[str],
    client: anthropic.AsyncAnthropic | None = None,
) -> ValidationResult:
    """Claude 출력을 POST 체크리스트로 검증.

    Args:
        output: Claude가 생성한 출력
        post_checks: 검증 체크리스트 항목 리스트
        client: Anthropic 클라이언트

    Returns:
        ValidationResult (PASS/FAIL/INCONCLUSIVE + issues + details)
    """
    if not post_checks:
        return ValidationResult(status="PASS", output=output)

    if client is None:
        client = anthropic.AsyncAnthropic()

    checklist_str = "\n".join(f"- [ ] {check}" for check in post_checks)

    validation_prompt = f"""다음 출력을 아래 체크리스트로 검증하세요.
각 항목에 PASS/FAIL과 사유를 적으세요.

## 출력
{output[:8000]}

## 체크리스트
{checklist_str}

## 응답 형식 (정확히 이 형식으로)
각 항목: [PASS] 또는 [FAIL] 사유
최종 판정: PASS 또는 FAIL
실패 항목이 있으면: 구체적 수정 사항 나열"""

    try:
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1500,
            messages=[{"role": "user", "content": validation_prompt}],
        )
        validation_text = response.content[0].text

        status, issues, details = _parse_validation_response(validation_text)
        pass_count = sum(1 for d in details if d["status"] == "PASS")
        fail_count = sum(1 for d in details if d["status"] == "FAIL")

        return ValidationResult(
            status=status,
            output=output,
            issues=issues,
            pass_count=pass_count,
            fail_count=fail_count,
            check_details=details,
        )
    except Exception as e:
        logger.error("POST validation failed: %s", e)
        return ValidationResult(
            status="INCONCLUSIVE",
            output=output,
            issues=f"검증 실패: {e}",
        )
