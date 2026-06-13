"""자동 인제스트 테스트 — Neo4j/Qdrant mock 기반."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from packages.graph_rag.ingest import (
    delete_skill,
    ingest_single_skill,
    skill_id_to_qdrant_id,
)


class TestSkillIdToQdrantId:
    def test_deterministic(self):
        """같은 skill_id는 항상 같은 Qdrant ID를 반환."""
        id1 = skill_id_to_qdrant_id("dev.backend.api.role")
        id2 = skill_id_to_qdrant_id("dev.backend.api.role")
        assert id1 == id2

    def test_different_ids(self):
        """다른 skill_id는 다른 Qdrant ID를 반환."""
        id1 = skill_id_to_qdrant_id("dev.backend.api.role")
        id2 = skill_id_to_qdrant_id("dev.frontend.component.role")
        assert id1 != id2

    def test_returns_positive_int(self):
        result = skill_id_to_qdrant_id("test.skill")
        assert isinstance(result, int)
        assert result > 0


@pytest.mark.asyncio
class TestIngestSingleSkill:
    async def test_new_skill_ingested(self, tmp_path):
        """신규 스킬 인제스트 성공."""
        skill_dir = tmp_path / "skills" / "dev" / "backend" / "api"
        skill_dir.mkdir(parents=True)
        yaml_file = skill_dir / "test-skill.yaml"
        yaml_file.write_text(
            'id: "dev.backend.api.test-skill"\n'
            'domain: "development.backend"\n'
            'type: "rule"\n'
            'tags: ["test"]\n'
            'token_estimate: 400\n'
            'content: "Test content"\n'
        )

        mock_neo4j = AsyncMock()
        mock_neo4j.run = AsyncMock(return_value=[])  # no existing hash
        mock_neo4j.run_void = AsyncMock()
        mock_neo4j.init_schema = AsyncMock()
        mock_neo4j.__aenter__ = AsyncMock(return_value=mock_neo4j)
        mock_neo4j.__aexit__ = AsyncMock(return_value=False)

        mock_vector = AsyncMock()
        mock_vector.ensure_collection = AsyncMock()
        mock_vector.upsert_batch = AsyncMock()
        mock_vector.__aenter__ = AsyncMock(return_value=mock_vector)
        mock_vector.__aexit__ = AsyncMock(return_value=False)

        mock_settings = MagicMock()

        with patch("packages.graph_rag.ingest.Neo4jClient", return_value=mock_neo4j):
            with patch("packages.graph_rag.ingest.VectorClient", return_value=mock_vector):
                with patch("packages.graph_rag.ingest.get_settings", return_value=mock_settings):
                    with patch("packages.graph_rag.ingest.generate_embeddings", new_callable=AsyncMock, return_value=[[0.1] * 1536]):
                        result = await ingest_single_skill(
                            "dev.backend.api.test-skill",
                            str(tmp_path / "skills"),
                        )

        assert result is True
        mock_neo4j.run_void.assert_called_once()
        mock_vector.upsert_batch.assert_called_once()

    async def test_unchanged_skill_skipped(self, tmp_path):
        """해시가 같으면 인제스트 스킵."""
        skill_dir = tmp_path / "skills" / "dev" / "backend"
        skill_dir.mkdir(parents=True)
        yaml_file = skill_dir / "unchanged.yaml"
        yaml_file.write_text(
            'id: "dev.backend.unchanged"\n'
            'domain: "development.backend"\n'
            'type: "rule"\n'
            'content: "Same content"\n'
        )

        from packages.graph_rag.embeddings import _content_hash
        expected_hash = _content_hash("Same content")

        mock_neo4j = AsyncMock()
        mock_neo4j.run = AsyncMock(return_value=[{"hash": expected_hash}])
        mock_neo4j.__aenter__ = AsyncMock(return_value=mock_neo4j)
        mock_neo4j.__aexit__ = AsyncMock(return_value=False)

        with patch("packages.graph_rag.ingest.Neo4jClient", return_value=mock_neo4j):
            result = await ingest_single_skill(
                "dev.backend.unchanged",
                str(tmp_path / "skills"),
            )

        assert result is False

    async def test_nonexistent_skill_returns_false(self, tmp_path):
        """존재하지 않는 스킬 → False."""
        skill_dir = tmp_path / "skills"
        skill_dir.mkdir(parents=True)

        result = await ingest_single_skill("nonexistent.skill", str(skill_dir))
        assert result is False


@pytest.mark.asyncio
class TestDeleteSkill:
    async def test_deletes_from_neo4j_and_qdrant(self):
        """Neo4j + Qdrant 양쪽에서 삭제 확인."""
        mock_neo4j = AsyncMock()
        mock_neo4j.run_void = AsyncMock()
        mock_neo4j.__aenter__ = AsyncMock(return_value=mock_neo4j)
        mock_neo4j.__aexit__ = AsyncMock(return_value=False)

        mock_vector = AsyncMock()
        mock_vector.connect = AsyncMock()
        mock_vector.delete_point = AsyncMock()
        mock_vector.__aenter__ = AsyncMock(return_value=mock_vector)
        mock_vector.__aexit__ = AsyncMock(return_value=False)

        with patch("packages.graph_rag.ingest.Neo4jClient", return_value=mock_neo4j):
            with patch("packages.graph_rag.ingest.VectorClient", return_value=mock_vector):
                await delete_skill("dev.backend.api.test")

        mock_neo4j.run_void.assert_called_once()
        mock_vector.delete_point.assert_called_once_with("dev.backend.api.test")
