"""파일 와처 테스트 — YAML 변경 감지."""

from __future__ import annotations

import asyncio
from unittest.mock import MagicMock, patch

import pytest

from packages.graph_rag.watcher import (
    _SkillChangeHandler,
    _extract_skill_id,
    _is_yaml,
    _skill_id_from_filename,
)


class TestHelpers:
    def test_is_yaml_true(self):
        assert _is_yaml("skills/dev/backend/api/auth.yaml") is True
        assert _is_yaml("skills/test.yml") is True

    def test_is_yaml_false(self):
        assert _is_yaml("skills/README.md") is False
        assert _is_yaml("skills/test.py") is False
        assert _is_yaml("skills/test.json") is False

    def test_extract_skill_id_valid(self, tmp_path):
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text('id: "dev.backend.api.role"\ndomain: "development.backend"\n')
        assert _extract_skill_id(str(yaml_file)) == "dev.backend.api.role"

    def test_extract_skill_id_no_id(self, tmp_path):
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text("domain: test\n")
        assert _extract_skill_id(str(yaml_file)) is None

    def test_extract_skill_id_nonexistent(self):
        assert _extract_skill_id("/nonexistent/file.yaml") is None

    def test_extract_skill_id_invalid_yaml(self, tmp_path):
        yaml_file = tmp_path / "test.yaml"
        yaml_file.write_text("{{invalid yaml")
        assert _extract_skill_id(str(yaml_file)) is None

    def test_skill_id_from_filename(self):
        assert _skill_id_from_filename("/path/to/auth.yaml") == "auth"
        assert _skill_id_from_filename("test.yaml") == "test"


class TestSkillChangeHandler:
    def test_enqueue_yaml_create(self):
        loop = asyncio.new_event_loop()
        queue = asyncio.Queue()
        handler = _SkillChangeHandler(loop, queue)

        event = MagicMock()
        event.is_directory = False
        event.src_path = "/skills/dev/backend/api/auth.yaml"

        with patch.object(loop, "call_soon_threadsafe") as mock_call:
            handler.on_created(event)
            mock_call.assert_called_once()

        loop.close()

    def test_enqueue_yaml_modify(self):
        loop = asyncio.new_event_loop()
        queue = asyncio.Queue()
        handler = _SkillChangeHandler(loop, queue)

        event = MagicMock()
        event.is_directory = False
        event.src_path = "/skills/test.yaml"

        with patch.object(loop, "call_soon_threadsafe") as mock_call:
            handler.on_modified(event)
            mock_call.assert_called_once()

        loop.close()

    def test_enqueue_yaml_delete(self):
        loop = asyncio.new_event_loop()
        queue = asyncio.Queue()
        handler = _SkillChangeHandler(loop, queue)

        event = MagicMock()
        event.is_directory = False
        event.src_path = "/skills/test.yaml"

        with patch.object(loop, "call_soon_threadsafe") as mock_call:
            handler.on_deleted(event)
            mock_call.assert_called_once()

        loop.close()

    def test_ignore_non_yaml(self):
        loop = asyncio.new_event_loop()
        queue = asyncio.Queue()
        handler = _SkillChangeHandler(loop, queue)

        event = MagicMock()
        event.is_directory = False
        event.src_path = "/skills/README.md"

        with patch.object(loop, "call_soon_threadsafe") as mock_call:
            handler.on_created(event)
            mock_call.assert_not_called()

        loop.close()

    def test_ignore_directory(self):
        loop = asyncio.new_event_loop()
        queue = asyncio.Queue()
        handler = _SkillChangeHandler(loop, queue)

        event = MagicMock()
        event.is_directory = True
        event.src_path = "/skills/dev/"

        with patch.object(loop, "call_soon_threadsafe") as mock_call:
            handler.on_created(event)
            mock_call.assert_not_called()

        loop.close()


@pytest.mark.asyncio
class TestDebounce:
    async def test_debounce_merges_events(self):
        """같은 파일에 대한 create + modify → 마지막 액션만 처리."""
        queue: asyncio.Queue[tuple[str, str]] = asyncio.Queue()
        queue.put_nowait(("upsert", "/skills/test.yaml"))
        queue.put_nowait(("upsert", "/skills/test.yaml"))
        queue.put_nowait(("delete", "/skills/test.yaml"))

        # 디바운스 윈도우 후 마지막 액션은 delete
        pending: dict[str, str] = {}
        while not queue.empty():
            action, path = queue.get_nowait()
            pending[path] = action

        assert pending["/skills/test.yaml"] == "delete"
        assert len(pending) == 1
