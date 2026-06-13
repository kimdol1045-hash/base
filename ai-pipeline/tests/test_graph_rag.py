"""Graph RAG 유닛 테스트 — Neo4j/Qdrant 없이 로직 검증."""

from __future__ import annotations

import pytest

from packages.graph_rag.config import GraphRAGSettings
from packages.graph_rag.edge_extractor import (
    _get_domain_from_id,
    _infer_type,
    extract_all_edges,
    extract_base_edges,
    extract_keyword_edges,
)
from packages.graph_rag.embeddings import _content_hash, load_all_skills
from packages.graph_rag.models import (
    ActivatedSkill,
    EdgeType,
    HybridResult,
    SkillEdge,
    SkillNode,
)


# ─── Config 테스트 ───


class TestConfig:
    def test_default_settings(self):
        settings = GraphRAGSettings()
        assert settings.neo4j_uri == "bolt://localhost:7687"
        assert settings.qdrant_port == 6333
        assert settings.spread_decay == 0.85
        assert settings.weight_graph == 0.5
        assert settings.weight_vector == 0.3
        assert settings.weight_static == 0.2

    def test_weights_sum_to_one(self):
        settings = GraphRAGSettings()
        total = settings.weight_graph + settings.weight_vector + settings.weight_static
        assert abs(total - 1.0) < 1e-10


# ─── Models 테스트 ───


class TestModels:
    def test_skill_node_defaults(self):
        node = SkillNode(id="test.role", domain="test", skill_type="role")
        assert node.activation_value == 1.0
        assert node.execution_count == 0
        assert node.success_rate == 1.0

    def test_skill_edge(self):
        edge = SkillEdge(
            source_id="a.role",
            target_id="a.verify",
            edge_type=EdgeType.REQUIRES,
            weight=0.9,
        )
        assert edge.edge_type == EdgeType.REQUIRES
        assert edge.weight == 0.9
        assert not edge.auto_created

    def test_activated_skill(self):
        skill = ActivatedSkill(
            skill_id="test.role",
            activation_score=0.85,
            source="graph",
            hop_distance=1,
        )
        assert skill.activation_score == 0.85

    def test_hybrid_result_defaults(self):
        result = HybridResult()
        assert result.skills == []
        assert result.graph_count == 0


# ─── Edge Extractor 테스트 ───


class TestEdgeExtractor:
    def test_infer_type_role(self):
        assert _infer_type("dev.backend.api.role") == "role"

    def test_infer_type_verify(self):
        assert _infer_type("dev.backend.api.verify") == "verify"

    def test_infer_type_middle(self):
        assert _infer_type("dev.backend.api.rest") == "middle"

    def test_get_domain_from_id(self):
        assert _get_domain_from_id("dev.backend.api.role") == "dev.backend"
        assert _get_domain_from_id("analytics.role") == "analytics.role"

    def test_extract_base_edges(self):
        edges = extract_base_edges()
        assert len(edges) > 0

        # role → middle 엣지 존재 확인
        requires = [e for e in edges if e.edge_type == EdgeType.REQUIRES]
        assert len(requires) > 0

        # 모든 REQUIRES 가중치 >= 0.85
        for e in requires:
            assert e.weight >= 0.85

        # verify 엣지 존재 확인
        feeds = [e for e in edges if e.edge_type == EdgeType.FEEDS]
        assert len(feeds) > 0

    def test_extract_keyword_edges(self):
        edges = extract_keyword_edges()
        assert len(edges) > 0

        # CO_CREATES + FEEDS 존재
        types = {e.edge_type for e in edges}
        assert EdgeType.CO_CREATES in types or EdgeType.FEEDS in types

    def test_extract_all_edges_dedup(self):
        edges = extract_all_edges()
        # 중복 없는지 확인 (source+target+type 기준)
        keys = set()
        for e in edges:
            key = (e.source_id, e.target_id, e.edge_type.value)
            assert key not in keys, f"Duplicate edge: {key}"
            keys.add(key)

    def test_edge_counts_reasonable(self):
        """엣지 수가 합리적 범위인지 확인 (BASE 17도메인 * ~5엣지 + KEYWORD 80키워드)."""
        base = extract_base_edges()
        keyword = extract_keyword_edges()
        all_edges = extract_all_edges()

        assert len(base) >= 50, f"Too few base edges: {len(base)}"
        assert len(keyword) >= 50, f"Too few keyword edges: {len(keyword)}"
        assert len(all_edges) <= len(base) + len(keyword), "Dedup should reduce count"


# ─── Embeddings (오프라인 테스트) ───


class TestEmbeddings:
    def test_content_hash(self):
        h1 = _content_hash("hello world")
        h2 = _content_hash("hello world")
        h3 = _content_hash("different content")
        assert h1 == h2
        assert h1 != h3
        assert len(h1) == 16

    def test_load_all_skills(self):
        skills = load_all_skills("./skills")
        assert len(skills) > 0

        # 필수 필드 확인
        for skill in skills[:5]:
            assert "id" in skill
            assert "domain" in skill
            assert "content" in skill
            assert "content_hash" in skill

    def test_skill_ids_unique(self):
        skills = load_all_skills("./skills")
        ids = [s["id"] for s in skills]
        assert len(ids) == len(set(ids)), "Duplicate skill IDs found"


# ─── Hybrid Selector (로직만) ───


class TestHybridMerge:
    def test_merge_static_only(self):
        """정적 결과만 있을 때."""
        from packages.graph_rag.hybrid_selector import _merge_results

        settings = GraphRAGSettings()
        static = [
            ActivatedSkill(skill_id="a", activation_score=1.0, source="static"),
            ActivatedSkill(skill_id="b", activation_score=1.0, source="static"),
        ]

        result = _merge_results([], [], static, settings)
        assert len(result.skills) == 2
        # 정적만이면 정적 가중치(0.2)만 반영
        for s in result.skills:
            assert abs(s.activation_score - 0.2) < 1e-10

    def test_merge_all_sources(self):
        """세 소스 모두 있을 때."""
        from packages.graph_rag.hybrid_selector import _merge_results

        settings = GraphRAGSettings()
        graph = [ActivatedSkill(skill_id="a", activation_score=0.8, source="graph")]
        vector = [ActivatedSkill(skill_id="a", activation_score=0.9, source="vector")]
        static = [ActivatedSkill(skill_id="a", activation_score=1.0, source="static")]

        result = _merge_results(graph, vector, static, settings)
        assert len(result.skills) == 1

        skill = result.skills[0]
        # 0.5 * (0.8/0.8) + 0.3 * 0.9 + 0.2 * 1.0 = 0.5 + 0.27 + 0.2 = 0.97
        expected = 0.5 * 1.0 + 0.3 * 0.9 + 0.2 * 1.0
        assert abs(skill.activation_score - expected) < 1e-10

    def test_merge_preserves_order(self):
        """점수 내림차순 정렬."""
        from packages.graph_rag.hybrid_selector import _merge_results

        settings = GraphRAGSettings()
        graph = [
            ActivatedSkill(skill_id="low", activation_score=0.3, source="graph"),
            ActivatedSkill(skill_id="high", activation_score=0.9, source="graph"),
        ]

        result = _merge_results(graph, [], [], settings)
        assert result.skills[0].skill_id == "high"
        assert result.skills[1].skill_id == "low"


# ─── Selector Hybrid (폴백) ───


class TestSelectorHybrid:
    @pytest.mark.asyncio
    async def test_hybrid_falls_back_to_static(self):
        """Graph RAG 미가용 시 정적 결과로 폴백."""
        from packages.hook_engine.models import Session
        from packages.hook_engine.selector import select_skills, select_skills_hybrid

        session = Session(session_id="test")
        domains = ["development.backend"]
        keywords = ["auth"]
        complexity = 5

        static = select_skills(domains, keywords, complexity, session)
        hybrid = await select_skills_hybrid(
            "로그인 API 만들어줘", domains, keywords, complexity, session,
        )

        # Neo4j가 없으므로 정적과 동일하거나 포함 관계
        assert len(hybrid) > 0
        # 정적 결과의 모든 항목이 hybrid에 포함 (폴백이므로)
        # (hybrid가 graph/vector 결과를 추가할 수 있으므로 superset일 수 있음)
        for s in static:
            assert s in hybrid, f"Static skill {s} missing from hybrid result"
