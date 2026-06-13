"""Evolution API 테스트 — Neo4j mock 기반."""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from httpx import ASGITransport, AsyncClient

from apps.server.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


# 엔드포인트 내부에서 lazy import하므로 원본 모듈 경로를 패치해야 한다.
_NEO4J = "packages.graph_rag.neo4j_client.Neo4jClient"
_EVOLUTION_STATS = "packages.graph_rag.self_evolution.get_evolution_stats"
_APPLY_DECAY = "packages.graph_rag.self_evolution.apply_decay"
_GET_SETTINGS = "packages.graph_rag.config.get_settings"


@pytest.mark.anyio
class TestEvolutionStats:
    async def test_stats_success(self):
        mock_neo4j = AsyncMock()
        mock_neo4j.verify_connection = AsyncMock(return_value=True)
        mock_neo4j.__aenter__ = AsyncMock(return_value=mock_neo4j)
        mock_neo4j.__aexit__ = AsyncMock(return_value=False)

        mock_stats = {"total_nodes": 500, "total_edges": 1200, "avg_weight": 0.85}

        with patch(_NEO4J, return_value=mock_neo4j):
            with patch(_EVOLUTION_STATS, new_callable=AsyncMock, return_value=mock_stats):
                async with AsyncClient(
                    transport=ASGITransport(app=app), base_url="http://test"
                ) as ac:
                    resp = await ac.get("/api/evolution/stats")

        assert resp.status_code == 200
        data = resp.json()
        assert "total_nodes" in data

    async def test_stats_neo4j_unavailable(self):
        mock_neo4j = AsyncMock()
        mock_neo4j.verify_connection = AsyncMock(return_value=False)
        mock_neo4j.__aenter__ = AsyncMock(return_value=mock_neo4j)
        mock_neo4j.__aexit__ = AsyncMock(return_value=False)

        with patch(_NEO4J, return_value=mock_neo4j):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                resp = await ac.get("/api/evolution/stats")

        assert resp.status_code == 503
        assert "error" in resp.json()


@pytest.mark.anyio
class TestEvolutionDecay:
    async def test_decay_success(self):
        mock_neo4j = AsyncMock()
        mock_neo4j.verify_connection = AsyncMock(return_value=True)
        mock_neo4j.__aenter__ = AsyncMock(return_value=mock_neo4j)
        mock_neo4j.__aexit__ = AsyncMock(return_value=False)

        mock_settings = MagicMock()
        mock_settings.evolution_decay_factor = 0.95

        with patch(_NEO4J, return_value=mock_neo4j):
            with patch(_APPLY_DECAY, new_callable=AsyncMock):
                with patch(_GET_SETTINGS, return_value=mock_settings):
                    async with AsyncClient(
                        transport=ASGITransport(app=app), base_url="http://test"
                    ) as ac:
                        resp = await ac.post("/api/evolution/decay")

        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "decay_factor" in data

    async def test_decay_neo4j_unavailable(self):
        mock_neo4j = AsyncMock()
        mock_neo4j.verify_connection = AsyncMock(return_value=False)
        mock_neo4j.__aenter__ = AsyncMock(return_value=mock_neo4j)
        mock_neo4j.__aexit__ = AsyncMock(return_value=False)

        with patch(_NEO4J, return_value=mock_neo4j):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                resp = await ac.post("/api/evolution/decay")

        assert resp.status_code == 503


@pytest.mark.anyio
class TestEvolutionHealth:
    async def test_health_returns_schema_info(self):
        mock_neo4j = AsyncMock()
        mock_neo4j.verify_connection = AsyncMock(return_value=True)
        mock_neo4j.run = AsyncMock(side_effect=[
            [{"names": ["constraint1", "constraint2"]}],
            [{"names": ["index1", "index2"]}],
        ])
        mock_neo4j.get_counts = AsyncMock(return_value={"nodes": 500, "edges": 1200})
        mock_neo4j.__aenter__ = AsyncMock(return_value=mock_neo4j)
        mock_neo4j.__aexit__ = AsyncMock(return_value=False)

        with patch(_NEO4J, return_value=mock_neo4j):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                resp = await ac.get("/api/evolution/health")

        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert data["neo4j_connected"] is True
        assert "constraints" in data
        assert "indexes" in data
        assert "counts" in data
