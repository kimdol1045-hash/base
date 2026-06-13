"""Dashboard API 테스트 — Skill/Domain/Stats 엔드포인트."""

from __future__ import annotations

from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from apps.server.main import app


def _mock_skills():
    """테스트용 스킬 데이터 생성."""
    skills = []
    for i in range(510):
        domain = "development.backend" if i % 3 == 0 else (
            "design" if i % 3 == 1 else "analytics"
        )
        skills.append({
            "id": f"skill.{domain}.{i}",
            "domain": domain,
            "type": "role" if i % 5 == 0 else "rule",
            "tags": ["test"],
            "token_estimate": 400,
            "content": f"Test content {i}",
            "content_hash": f"hash{i}",
        })
    return skills


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.mark.anyio
class TestListSkills:
    async def test_get_all_skills(self):
        with patch("apps.server.main._get_cached_skills", return_value=_mock_skills()):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                resp = await ac.get("/api/skills")

        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] == 510

    async def test_filter_by_domain(self):
        with patch("apps.server.main._get_cached_skills", return_value=_mock_skills()):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                resp = await ac.get("/api/skills?domain=development.backend")

        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] > 0
        for s in data["skills"]:
            assert s["domain"] == "development.backend"

    async def test_filter_by_type(self):
        with patch("apps.server.main._get_cached_skills", return_value=_mock_skills()):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                resp = await ac.get("/api/skills?type=role")

        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] > 0
        for s in data["skills"]:
            assert s["type"] == "role"

    async def test_search_skills(self):
        with patch("apps.server.main._get_cached_skills", return_value=_mock_skills()):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                resp = await ac.get("/api/skills?search=test")

        assert resp.status_code == 200
        data = resp.json()
        assert data["total"] > 0


@pytest.mark.anyio
class TestGetSkill:
    async def test_existing_skill(self):
        skills = _mock_skills()
        with patch("apps.server.main._get_cached_skills", return_value=skills):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                resp = await ac.get(f"/api/skills/{skills[0]['id']}")

        assert resp.status_code == 200

    async def test_nonexistent_skill(self):
        with patch("apps.server.main._get_cached_skills", return_value=_mock_skills()):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                resp = await ac.get("/api/skills/nonexistent.skill")

        assert resp.status_code == 404
        assert "error" in resp.json()


@pytest.mark.anyio
class TestListDomains:
    async def test_domains_with_counts(self):
        with patch("apps.server.main._get_cached_skills", return_value=_mock_skills()):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                resp = await ac.get("/api/domains")

        assert resp.status_code == 200
        data = resp.json()
        assert data["total_domains"] == 3
        assert len(data["domains"]) == 3
        for d in data["domains"]:
            assert "domain" in d
            assert "count" in d
            assert d["count"] > 0


@pytest.mark.anyio
class TestGetStats:
    async def test_overall_stats(self):
        with patch("apps.server.main._get_cached_skills", return_value=_mock_skills()):
            async with AsyncClient(
                transport=ASGITransport(app=app), base_url="http://test"
            ) as ac:
                resp = await ac.get("/api/stats")

        assert resp.status_code == 200
        data = resp.json()
        assert data["total_skills"] >= 500
        assert data["total_domains"] >= 1
        assert data["total_types"] >= 1
        assert "domains" in data
        assert "types" in data
