"""Phase 11 feature tests — usage tracking, classifier domains, pipeline order, selector coverage, /api/usage."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

from packages.skill_store.server import (
    _MAX_TIMESTAMPS,
    _record_usage,
    _usage_counter,
    _usage_lock,
    _usage_timestamps,
    get_usage_stats,
)
from packages.hook_engine.classifier import CLASSIFY_PROMPT
from apps.server.pipeline import DOMAIN_EXECUTION_ORDER


# ─── 1. Usage Tracking ───


class TestUsageTracking:
    def test_record_usage_increments_counter(self):
        """_record_usage should increment the counter for each skill."""
        with _usage_lock:
            _usage_counter.clear()
        _record_usage(["dev.backend.api.role", "dev.backend.auth.jwt-auth"])
        with _usage_lock:
            assert _usage_counter["dev.backend.api.role"] >= 1
            assert _usage_counter["dev.backend.auth.jwt-auth"] >= 1

    def test_get_usage_stats_returns_correct_structure(self):
        """get_usage_stats should return dict with expected keys."""
        stats = get_usage_stats(top_n=5)
        assert "total_calls" in stats
        assert "unique_skills_used" in stats
        assert "top_skills" in stats
        assert isinstance(stats["top_skills"], list)

    def test_record_usage_caps_timestamps(self):
        """Should not exceed _MAX_TIMESTAMPS per skill."""
        with _usage_lock:
            _usage_timestamps.pop("test.cap.skill", None)
        _record_usage(["test.cap.skill"] * (_MAX_TIMESTAMPS + 50))
        with _usage_lock:
            assert len(_usage_timestamps.get("test.cap.skill", [])) <= _MAX_TIMESTAMPS


# ─── 2. Classifier Domain Tests ───


class TestClassifierDomains:
    def test_classify_prompt_contains_new_domains(self):
        """CLASSIFY_PROMPT should include wireframe, design-system, ux-audit."""
        assert "design.wireframe" in CLASSIFY_PROMPT
        assert "design.design-system" in CLASSIFY_PROMPT
        assert "qa.ux-audit" in CLASSIFY_PROMPT

    def test_classify_prompt_contains_new_keywords(self):
        """CLASSIFY_PROMPT should include new semantic_keywords."""
        for kw in [
            "ai-agent", "embedding", "guardrails", "ssr", "code-splitting",
            "serverless", "tdd", "chain-of-thought", "debounce",
        ]:
            assert kw in CLASSIFY_PROMPT, f"Missing keyword: {kw}"


# ─── 3. Pipeline DOMAIN_EXECUTION_ORDER ───


class TestDomainExecutionOrder:
    def test_order_contains_new_domains(self):
        """DOMAIN_EXECUTION_ORDER should include all new domains."""
        new_domains = [
            "design.wireframe", "design.design-system", "development.ai",
            "marketing.seo", "marketing.growth",
            "qa.code-review", "qa.testing", "qa.ux-audit",
        ]
        for d in new_domains:
            assert d in DOMAIN_EXECUTION_ORDER, f"Missing domain: {d}"

    def test_order_has_correct_sequence(self):
        """Design domains should come before development domains."""
        design_idx = DOMAIN_EXECUTION_ORDER.index("design")
        backend_idx = DOMAIN_EXECUTION_ORDER.index("development.backend")
        assert design_idx < backend_idx

    def test_order_has_25_domains(self):
        """Should have exactly 25 domains."""
        assert len(DOMAIN_EXECUTION_ORDER) == 25


# ─── 4. Selector Full Coverage ───


class TestSelectorFullCoverage:
    def test_all_yaml_skills_registered(self):
        """All YAML skills should be reachable through selector."""
        selector_path = Path("packages/hook_engine/selector.py")
        content = selector_path.read_text()
        registered = set(re.findall(r'"([a-z][a-z0-9\-]+(?:\.[a-z][a-z0-9\-]+)+)"', content))

        yaml_ids: set[str] = set()
        for p in Path("skills").rglob("*.yaml"):
            with open(p) as f:
                data = yaml.safe_load(f)
            if data and "id" in data:
                yaml_ids.add(data["id"])

        unregistered = yaml_ids - registered
        assert len(unregistered) == 0, f"Unregistered skills: {unregistered}"


# ─── 5. /api/usage Endpoint (mock via ASGI) ───


from httpx import ASGITransport, AsyncClient
from apps.server.main import app


class TestUsageEndpoint:
    @pytest.mark.asyncio
    async def test_usage_endpoint_returns_200(self):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            resp = await ac.get("/api/usage")
        assert resp.status_code == 200
        data = resp.json()
        assert "total_calls" in data
        assert "unique_skills_used" in data
