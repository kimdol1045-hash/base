"""Phase 13 feature tests — classifier few-shot, cost tracking, Prometheus metrics,
SQLite session, skill generation, Obsidian bidirectional sync, dynamic weights."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
import yaml


# ─── 1. Classifier Few-Shot Examples ───


class TestClassifierFewShot:
    def test_classify_prompt_has_few_shot_examples(self):
        """CLASSIFY_PROMPT should contain few-shot examples."""
        from packages.hook_engine.classifier import CLASSIFY_PROMPT

        assert "## 분류 예시" in CLASSIFY_PROMPT
        assert "예시 1:" in CLASSIFY_PROMPT
        assert "예시 8:" in CLASSIFY_PROMPT

    def test_few_shot_covers_diverse_domains(self):
        """Few-shot examples should cover multiple domains."""
        from packages.hook_engine.classifier import CLASSIFY_PROMPT

        domains_in_examples = [
            "development.backend",
            "development.frontend",
            "development.ai",
            "marketing.seo",
            "qa.code-review",
            "analytics",
            "design.wireframe",
            "qa.testing",
        ]
        for domain in domains_in_examples:
            assert domain in CLASSIFY_PROMPT, f"Missing domain in few-shot: {domain}"

    def test_few_shot_has_followup_example(self):
        """At least one few-shot example should be a followup."""
        from packages.hook_engine.classifier import CLASSIFY_PROMPT

        assert '"is_followup": true' in CLASSIFY_PROMPT


# ─── 2. Cost Tracking ───


class TestCostTracking:
    def test_model_pricing_has_required_models(self):
        """MODEL_PRICING should have haiku, sonnet, opus."""
        from packages.skill_store.server import MODEL_PRICING

        assert "haiku" in MODEL_PRICING
        assert "sonnet" in MODEL_PRICING
        assert "opus" in MODEL_PRICING

    def test_model_pricing_has_input_output(self):
        """Each model should have input and output pricing."""
        from packages.skill_store.server import MODEL_PRICING

        for model, pricing in MODEL_PRICING.items():
            assert "input" in pricing, f"{model} missing input pricing"
            assert "output" in pricing, f"{model} missing output pricing"
            assert pricing["input"] > 0
            assert pricing["output"] > 0

    def test_record_cost_adds_record(self):
        """_record_cost should add to _cost_records."""
        from packages.skill_store.server import (
            _cost_lock,
            _cost_records,
            _record_cost,
        )

        with _cost_lock:
            initial_len = len(_cost_records)

        _record_cost("test-session", "haiku", 1000, 500)

        with _cost_lock:
            assert len(_cost_records) > initial_len
            last = _cost_records[-1]
            assert last["session_id"] == "test-session"
            assert last["model"] == "haiku"
            assert last["input_tokens"] == 1000
            assert last["output_tokens"] == 500
            assert last["cost_usd"] > 0

    def test_get_cost_stats_schema(self):
        """get_cost_stats should return expected schema."""
        from packages.skill_store.server import get_cost_stats

        stats = get_cost_stats()
        assert "total_cost_usd" in stats
        assert "total_requests" in stats
        assert "per_model" in stats
        assert "recent_records" in stats
        assert isinstance(stats["total_cost_usd"], (int, float))


# ─── 3. Prometheus Metrics ───


class TestPrometheusMetrics:
    def test_prometheus_import_guard(self):
        """main.py should handle missing prometheus_client gracefully."""
        # The import guard exists in main.py
        from apps.server import main

        assert hasattr(main, "PROMETHEUS_AVAILABLE")

    def test_metrics_endpoint_exists(self):
        """FastAPI app should have /metrics route."""
        from apps.server.main import app

        routes = [r.path for r in app.routes]
        assert "/metrics" in routes


# ─── 4. SQLite Session Backend ───


class TestSQLiteSession:
    def test_sqlite_store_create_and_get(self):
        """_SQLiteStore should create and retrieve sessions."""
        from packages.hook_engine.models import _SQLiteStore

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_sessions.db")
            store = _SQLiteStore(db_path)

            # Create session
            session = store.get_or_create("test-123")
            assert session.session_id == "test-123"

            # Modify and save
            session.active_domains = ["development.backend"]
            store.save(session)

            # Retrieve
            retrieved = store.get_or_create("test-123")
            assert retrieved.session_id == "test-123"
            assert "development.backend" in retrieved.active_domains

    def test_sqlite_store_different_sessions(self):
        """_SQLiteStore should maintain separate sessions."""
        from packages.hook_engine.models import _SQLiteStore

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = os.path.join(tmpdir, "test_sessions.db")
            store = _SQLiteStore(db_path)

            s1 = store.get_or_create("session-1")
            s1.active_domains = ["qa"]
            store.save(s1)

            s2 = store.get_or_create("session-2")
            s2.active_domains = ["design"]
            store.save(s2)

            r1 = store.get_or_create("session-1")
            r2 = store.get_or_create("session-2")
            assert r1.active_domains == ["qa"]
            assert r2.active_domains == ["design"]

    def test_create_store_priority(self):
        """_create_store should try Redis → SQLite → in-memory."""
        from packages.hook_engine.models import _InMemoryStore, _create_store

        # No env vars → in-memory
        with patch.dict(os.environ, {}, clear=True):
            store = _create_store()
            assert isinstance(store, _InMemoryStore)


# ─── 5. Skill Auto-Generation ───


class TestSkillGeneration:
    def test_generate_skill_creates_file(self):
        """generate_skill should create a valid YAML file."""
        from scripts.generate_skill import generate_skill, SKILLS_DIR

        with tempfile.TemporaryDirectory() as tmpdir:
            # Temporarily override SKILLS_DIR
            import scripts.generate_skill as gen_module

            original_dir = gen_module.SKILLS_DIR
            gen_module.SKILLS_DIR = Path(tmpdir)

            try:
                result = gen_module.generate_skill("dev.backend", "test-cache", "rule")
                assert result is not None
                assert result.exists()

                data = yaml.safe_load(result.read_text(encoding="utf-8"))
                assert data["id"] == "dev.backend.test-cache"
                assert data["type"] == "rule"
                assert "content" in data
                assert "token_estimate" in data
                assert data["token_estimate"] > 0
            finally:
                gen_module.SKILLS_DIR = original_dir

    def test_generate_skill_skip_existing(self):
        """generate_skill should skip existing files without --force."""
        import scripts.generate_skill as gen_module

        with tempfile.TemporaryDirectory() as tmpdir:
            original_dir = gen_module.SKILLS_DIR
            gen_module.SKILLS_DIR = Path(tmpdir)

            try:
                # Create first time
                gen_module.generate_skill("dev.backend", "test-skip", "rule")
                # Second call should return None (skip)
                result = gen_module.generate_skill("dev.backend", "test-skip", "rule")
                assert result is None
            finally:
                gen_module.SKILLS_DIR = original_dir

    def test_generate_skill_valid_types(self):
        """Only valid types should be accepted."""
        from scripts.generate_skill import VALID_TYPES

        assert "role" in VALID_TYPES
        assert "rule" in VALID_TYPES
        assert "pattern" in VALID_TYPES
        assert "verify" in VALID_TYPES


# ─── 6. Obsidian Bidirectional Sync ───


class TestObsidianSync:
    def test_sync_state_read_write(self):
        """Sync state should be readable and writable."""
        from scripts.sync_obsidian import _load_sync_state, _save_sync_state, SYNC_STATE_FILE

        with tempfile.TemporaryDirectory() as tmpdir:
            import scripts.sync_obsidian as sync_module

            original_file = sync_module.SYNC_STATE_FILE
            sync_module.SYNC_STATE_FILE = Path(tmpdir) / "test-state.json"

            try:
                state = {"md:test.md": "abc123", "yaml:test.yaml": "def456"}
                _save_sync_state(state)

                loaded = _load_sync_state()
                assert loaded["md:test.md"] == "abc123"
                assert loaded["yaml:test.yaml"] == "def456"
            finally:
                sync_module.SYNC_STATE_FILE = original_file

    def test_parse_obsidian_to_skill(self):
        """_parse_obsidian_to_skill should extract skill from markdown."""
        from scripts.sync_obsidian import _parse_obsidian_to_skill

        with tempfile.TemporaryDirectory() as tmpdir:
            md_path = Path(tmpdir) / "test.md"
            md_path.write_text(
                "---\n"
                "id: dev.backend.auth\n"
                "domain: development.backend\n"
                "type: rule\n"
                "tags:\n"
                "  - auth\n"
                "  - jwt\n"
                "---\n"
                "# Auth Rules\n\n"
                "## DO\n"
                "- Use JWT with short expiry\n",
                encoding="utf-8",
            )

            skill = _parse_obsidian_to_skill(md_path)
            assert skill is not None
            assert skill["id"] == "dev.backend.auth"
            assert skill["domain"] == "development.backend"
            assert "Auth Rules" in skill["content"]


# ─── 7. Dynamic Weights ───


class TestDynamicWeights:
    def test_domain_weight_overrides_structure(self):
        """DOMAIN_WEIGHT_OVERRIDES should have valid structure."""
        from packages.graph_rag.hybrid_selector import DOMAIN_WEIGHT_OVERRIDES

        assert len(DOMAIN_WEIGHT_OVERRIDES) >= 4

        for domain, weights in DOMAIN_WEIGHT_OVERRIDES.items():
            assert "weight_graph" in weights
            assert "weight_vector" in weights
            assert "weight_static" in weights
            total = weights["weight_graph"] + weights["weight_vector"] + weights["weight_static"]
            assert abs(total - 1.0) < 0.01, f"{domain} weights don't sum to 1.0: {total}"

    def test_get_domain_weights_exact_match(self):
        """get_domain_weights should return overrides for known domains."""
        from packages.graph_rag.hybrid_selector import get_domain_weights
        from packages.graph_rag.config import get_settings

        settings = get_settings()
        w_g, w_v, w_s = get_domain_weights("development.ai", settings)
        # AI domain should have higher vector weight
        assert w_v > w_g

    def test_get_domain_weights_fallback(self):
        """get_domain_weights should fallback to settings for unknown domains."""
        from packages.graph_rag.hybrid_selector import get_domain_weights
        from packages.graph_rag.config import get_settings

        settings = get_settings()
        w_g, w_v, w_s = get_domain_weights("unknown.domain", settings)
        assert w_g == settings.weight_graph
        assert w_v == settings.weight_vector
        assert w_s == settings.weight_static

    def test_get_weight_stats_returns_dict(self):
        """get_weight_stats should return expected schema."""
        from packages.graph_rag.hybrid_selector import get_weight_stats

        stats = get_weight_stats()
        assert "current_overrides" in stats
        assert "total_adjustments" in stats
        assert "recent_history" in stats
