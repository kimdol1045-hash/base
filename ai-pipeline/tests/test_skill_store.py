"""skill-store 단위 테스트 — YAML 로드, 배치 조회, 프롬프트 조립, 검색."""

from __future__ import annotations


from packages.skill_store.server import (
    _resolve_path,
    assemble_prompt,
    get_skill,
    get_skills_batch,
    search_skills,
)


class TestGetSkill:
    def test_existing_skill(self):
        result = get_skill("dev.backend.api.role")
        assert "error" not in result
        assert result["id"] == "dev.backend.api.role"
        assert result["domain"] == "development.backend"
        assert "content" in result

    def test_nonexistent_skill(self):
        result = get_skill("nonexistent.skill.xyz")
        assert "error" in result

    def test_auth_role_skill(self):
        result = get_skill("dev.backend.auth.role")
        assert result["id"] == "dev.backend.auth.role"
        assert "auth" in result.get("tags", []) or "security" in result.get("tags", [])


class TestGetSkillsBatch:
    def test_batch_returns_correct_count(self):
        """backend 6개 Skill batch 조회 → 6개 반환."""
        ids = [
            "dev.backend.api.role",
            "dev.backend.api.rest",
            "dev.backend.api.validation",
            "dev.backend.api.error",
            "dev.backend.api.middleware",
            "dev.backend.api.verify",
        ]
        results = get_skills_batch(ids)
        assert len(results) == 6

    def test_batch_skips_nonexistent(self):
        """존재하지 않는 ID는 건너뜀."""
        ids = ["dev.backend.api.role", "nonexistent.xyz", "dev.backend.api.verify"]
        results = get_skills_batch(ids)
        assert len(results) == 2

    def test_batch_empty_input(self):
        results = get_skills_batch([])
        assert results == []

    def test_batch_all_have_id(self):
        ids = ["dev.backend.api.role", "dev.backend.api.rest"]
        results = get_skills_batch(ids)
        for skill in results:
            assert "id" in skill


class TestAssemblePrompt:
    def test_returns_valid_prompt(self):
        """assemble_prompt → 유효한 프롬프트 반환."""
        ids = [
            "dev.backend.api.role",
            "dev.backend.api.rest",
            "dev.backend.api.verify",
        ]
        result = assemble_prompt(ids)
        assert "prompt" in result
        assert "total_tokens" in result
        assert "skill_count" in result
        assert result["skill_count"] == 3
        assert result["total_tokens"] > 0
        assert len(result["prompt"]) > 100

    def test_prompt_has_all_sections(self):
        """role + rule + verify → 4섹션 모두 포함."""
        ids = ["dev.backend.api.role", "dev.backend.api.rest", "dev.backend.api.verify"]
        result = assemble_prompt(ids)
        prompt = result["prompt"]
        assert "기술 스택" in prompt
        assert "규칙" in prompt
        assert "검증" in prompt

    def test_empty_ids_returns_defaults(self):
        result = assemble_prompt([])
        assert result["skill_count"] == 0
        assert "시니어 엔지니어" in result["prompt"]

    def test_token_count_scales(self):
        small = assemble_prompt(["dev.backend.api.role"])
        large = assemble_prompt([
            "dev.backend.api.role", "dev.backend.api.rest",
            "dev.backend.api.validation", "dev.backend.api.error",
        ])
        assert large["total_tokens"] > small["total_tokens"]


class TestSearchSkills:
    def test_search_by_domain(self):
        results = search_skills(domain="development.backend")
        assert len(results) > 0
        for r in results:
            assert r["domain"].startswith("development.backend")

    def test_search_by_type(self):
        results = search_skills(skill_type="role")
        assert len(results) > 0
        for r in results:
            assert r["type"] == "role"

    def test_search_by_tags(self):
        results = search_skills(tags=["auth"])
        assert len(results) > 0
        for r in results:
            assert "auth" in r["tags"]

    def test_search_no_filter_returns_all(self):
        results = search_skills()
        assert len(results) >= 500

    def test_search_results_have_metadata(self):
        results = search_skills(domain="development.backend")
        for r in results[:3]:
            assert "id" in r
            assert "domain" in r
            assert "type" in r
            assert "tags" in r
            assert "token_estimate" in r
            # content는 포함되지 않아야 함
            assert "content" not in r


class TestResolvePath:
    def test_valid_skill_id(self):
        path = _resolve_path("dev.backend.api.role")
        assert path is not None
        assert path.exists()

    def test_invalid_skill_id(self):
        path = _resolve_path("nonexistent.foo.bar")
        assert path is None

    def test_short_skill_id(self):
        path = _resolve_path("x")
        assert path is None
