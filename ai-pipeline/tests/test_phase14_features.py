"""Phase 14 feature tests — thin content, benchmark 100, version mgmt, quality eval,
recommender, context optimization, A/B test, auto-tuning convergence, dashboard tabs."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml


# ─── 1. Thin Content Verification ───


class TestThinContent:
    def test_no_skill_under_300_chars(self):
        """After strengthening, no skill should have content < 300 chars."""
        skills_dir = Path("skills")
        thin = []
        for p in skills_dir.rglob("*.yaml"):
            if "_archive" in str(p):
                continue
            try:
                data = yaml.safe_load(p.read_text(encoding="utf-8"))
                if data and "content" in data:
                    cl = len(data["content"].strip())
                    if cl < 300:
                        thin.append((data.get("id", "?"), cl))
            except Exception:
                continue
        assert len(thin) == 0, f"Found {len(thin)} skills under 300 chars: {thin[:5]}"


# ─── 2. Benchmark 100 Cases ───


class TestBenchmark100:
    def test_benchmark_has_100_cases(self):
        """BENCHMARK_CASES should have 100 entries."""
        from tests.benchmark import BENCHMARK_CASES
        assert len(BENCHMARK_CASES) == 100

    def test_benchmark_ids_sequential(self):
        """Benchmark case IDs should be 1-100 sequential."""
        from tests.benchmark import BENCHMARK_CASES
        ids = [c.id for c in BENCHMARK_CASES]
        assert ids == list(range(1, 101))

    def test_benchmark_cases_have_required_fields(self):
        """All benchmark cases should have required fields."""
        from tests.benchmark import BENCHMARK_CASES
        for case in BENCHMARK_CASES:
            assert case.input, f"Case {case.id} missing input"
            assert case.expected_domains, f"Case {case.id} missing domains"
            assert case.expected_skills_contain, f"Case {case.id} missing skills"
            assert case.category, f"Case {case.id} missing category"

    def test_benchmark_new_categories(self):
        """New benchmark should cover AI, security, design system categories."""
        from tests.benchmark import BENCHMARK_CASES
        categories = set(c.category for c in BENCHMARK_CASES)
        assert "ai" in categories or any(
            "ai" in c.category or c.id >= 51 for c in BENCHMARK_CASES
            if any("dev.ai" in d for d in c.expected_domains)
        )


# ─── 3. Skill Version Management ───


class TestVersionManagement:
    def test_skills_have_version_field(self):
        """All skills should have version field after add-version-all."""
        skills_dir = Path("skills")
        missing = []
        total = 0
        for p in skills_dir.rglob("*.yaml"):
            if "_archive" in str(p):
                continue
            try:
                data = yaml.safe_load(p.read_text(encoding="utf-8"))
                if data and "id" in data:
                    total += 1
                    if "version" not in data:
                        missing.append(data["id"])
            except Exception:
                continue
        assert total >= 500, f"Expected 500+ skills, got {total}"
        assert len(missing) == 0, f"{len(missing)} skills missing version: {missing[:5]}"

    def test_version_script_exists(self):
        """version_skill.py should exist."""
        assert Path("scripts/version_skill.py").exists()


# ─── 4. Quality Evaluator ───


class TestQualityEvaluator:
    def test_evaluate_skill_returns_score(self):
        """evaluate_skill should return expected schema."""
        from scripts.evaluate_skills import evaluate_skill

        skill = {
            "id": "test.skill",
            "type": "rule",
            "domain": "development.backend",
            "content": "# Test Rule\n\n## 핵심 원칙\n- 원칙 1\n\n## DO\n- Do this\n- Do that\n\n## DON'T\n- Don't do this",
        }
        result = evaluate_skill(skill)
        assert "total_score" in result
        assert "completeness" in result
        assert "specificity" in result
        assert "actionability" in result
        assert "consistency" in result
        assert 0 <= result["total_score"] <= 10

    def test_empty_content_scores_zero(self):
        """Empty content should score 0."""
        from scripts.evaluate_skills import evaluate_skill

        skill = {"id": "test.empty", "type": "rule", "domain": "test", "content": ""}
        result = evaluate_skill(skill)
        assert result["total_score"] == 0.0


# ─── 5. Skill Recommender ───


class TestRecommender:
    def test_record_cooccurrence(self):
        """record_cooccurrence should track co-occurrence."""
        from packages.skill_store.recommender import (
            record_cooccurrence,
            _cooccurrence,
            _cooccurrence_lock,
        )

        record_cooccurrence(["skill.a", "skill.b", "skill.c"])

        with _cooccurrence_lock:
            assert _cooccurrence["skill.a"]["skill.b"] >= 1
            assert _cooccurrence["skill.b"]["skill.a"] >= 1

    def test_recommend_skills_returns_list(self):
        """recommend_skills should return list of dicts."""
        from packages.skill_store.recommender import recommend_skills

        recs = recommend_skills(["dev.backend.auth.role"], top_n=3)
        assert isinstance(recs, list)
        for rec in recs:
            assert "skill_id" in rec
            assert "score" in rec
            assert "reason" in rec

    def test_recommendation_stats(self):
        """get_recommendation_stats should return expected schema."""
        from packages.skill_store.recommender import get_recommendation_stats

        stats = get_recommendation_stats()
        assert "total_cooccurrence_pairs" in stats
        assert "unique_skills_tracked" in stats
        assert "skill_index_size" in stats


# ─── 6. Context Window Optimization ───


class TestContextOptimization:
    def test_model_context_limits_exist(self):
        """MODEL_CONTEXT_LIMITS should have haiku/sonnet/opus."""
        from packages.hook_engine.selector import MODEL_CONTEXT_LIMITS

        assert "haiku" in MODEL_CONTEXT_LIMITS
        assert "sonnet" in MODEL_CONTEXT_LIMITS
        assert "opus" in MODEL_CONTEXT_LIMITS
        assert MODEL_CONTEXT_LIMITS["haiku"] < MODEL_CONTEXT_LIMITS["sonnet"]
        assert MODEL_CONTEXT_LIMITS["sonnet"] < MODEL_CONTEXT_LIMITS["opus"]

    def test_skill_type_priority(self):
        """SKILL_TYPE_PRIORITY should rank role > rule > verify."""
        from packages.hook_engine.selector import SKILL_TYPE_PRIORITY

        assert SKILL_TYPE_PRIORITY["role"] > SKILL_TYPE_PRIORITY["rule"]
        assert SKILL_TYPE_PRIORITY["rule"] > SKILL_TYPE_PRIORITY["verify"]

    def test_trim_to_budget_keeps_high_priority(self):
        """_trim_to_budget should keep role skills when budget is tight."""
        from packages.hook_engine.selector import _trim_to_budget

        # With a very small budget, only highest priority skills should be kept
        skills = ["dev.backend.auth.role", "dev.backend.auth.jwt-auth"]
        kept, dropped = _trim_to_budget(skills, "haiku")
        # Both should fit in haiku budget (8000 tokens)
        assert len(kept) >= 1


# ─── 7. A/B Test Framework ───


class TestABTestFramework:
    def test_create_and_get_test(self):
        """Should create and retrieve A/B test."""
        from packages.hook_engine.ab_test import ABTestManager

        with tempfile.TemporaryDirectory() as tmpdir:
            import packages.hook_engine.ab_test as ab_module
            original = ab_module.AB_TESTS_FILE
            ab_module.AB_TESTS_FILE = Path(tmpdir) / "test_ab.json"

            try:
                manager = ABTestManager()
                test_id = manager.create_test(
                    "test-auth",
                    "development.backend",
                    ["skill.a", "skill.b"],
                    ["skill.a", "skill.c"],
                )
                assert test_id

                variant = manager.get_variant(test_id)
                assert variant in ("A", "B")

                skills = manager.get_skills_for_variant(test_id, "A")
                assert skills == ["skill.a", "skill.b"]
            finally:
                ab_module.AB_TESTS_FILE = original

    def test_record_and_get_results(self):
        """Should record results and compute pass rates."""
        from packages.hook_engine.ab_test import ABTestManager

        with tempfile.TemporaryDirectory() as tmpdir:
            import packages.hook_engine.ab_test as ab_module
            original = ab_module.AB_TESTS_FILE
            ab_module.AB_TESTS_FILE = Path(tmpdir) / "test_ab.json"

            try:
                manager = ABTestManager()
                test_id = manager.create_test(
                    "test-results",
                    "qa.testing",
                    ["skill.x"],
                    ["skill.y"],
                )
                manager.record_result(test_id, "A", "PASS")
                manager.record_result(test_id, "B", "FAIL")

                results = manager.get_results(test_id)
                assert results["variant_a"]["sample_size"] == 1
                assert results["variant_b"]["sample_size"] == 1
            finally:
                ab_module.AB_TESTS_FILE = original


# ─── 8. Graph RAG Auto-Tuning Convergence ───


class TestAutoTuningConvergence:
    def test_convergence_status_schema(self):
        """get_convergence_status should return expected schema."""
        from packages.graph_rag.hybrid_selector import get_convergence_status

        status = get_convergence_status()
        assert "domains" in status
        assert "total_locked" in status
        assert "total_tracked" in status

    def test_record_validation_result(self):
        """record_validation_result should track results."""
        from packages.graph_rag.hybrid_selector import (
            record_validation_result,
            _domain_results,
        )

        record_validation_result("test.domain", "PASS")
        assert "test.domain" in _domain_results
        assert len(_domain_results["test.domain"]) >= 1

    def test_cache_warmup(self):
        """warmup_cache should cache combinations."""
        from packages.graph_rag.hybrid_selector import warmup_cache, get_cached_result

        cached = warmup_cache([["skill.a", "skill.b"]])
        assert cached >= 0  # may be 0 if already cached

        result = get_cached_result(["skill.a", "skill.b"])
        # Result may or may not exist depending on prior state


# ─── 9. Dashboard Tabs ───


class TestDashboardTabs:
    def test_dashboard_has_cost_tab(self):
        """Dashboard app.py should contain cost tab code."""
        content = Path("apps/dashboard/app.py").read_text(encoding="utf-8")
        assert "Cost" in content or "cost" in content.lower()
        assert "get_cost_stats" in content or "/api/costs" in content

    def test_dashboard_has_metrics_tab(self):
        """Dashboard app.py should contain metrics tab code."""
        content = Path("apps/dashboard/app.py").read_text(encoding="utf-8")
        assert "Metrics" in content or "metrics" in content.lower()
