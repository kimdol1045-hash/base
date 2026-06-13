"""스킬 디렉토리 파일 와처 — YAML 변경 감지 → 자동 인제스트/삭제."""

from __future__ import annotations

import asyncio
import logging
from pathlib import Path
from typing import Any

import yaml
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from watchdog.observers import Observer

logger = logging.getLogger(__name__)

# 디바운스 간격 (초)
_DEBOUNCE_SEC = 0.5


def _is_yaml(path: str) -> bool:
    """YAML 파일 확장자 확인."""
    return path.endswith((".yaml", ".yml"))


def _extract_skill_id(path: str) -> str | None:
    """YAML 파일에서 skill id 추출. 파일이 없거나 파싱 실패 시 None."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data and isinstance(data, dict):
            return data.get("id")
    except Exception:
        pass
    return None


def _skill_id_from_filename(path: str) -> str:
    """파일명에서 skill id 추론 (삭제 시 파일을 읽을 수 없을 때 사용)."""
    return Path(path).stem


class _SkillChangeHandler(FileSystemEventHandler):
    """watchdog 이벤트 → 디바운스 큐 전달."""

    def __init__(self, loop: asyncio.AbstractEventLoop, queue: asyncio.Queue[tuple[str, str]]) -> None:
        super().__init__()
        self._loop = loop
        self._queue = queue

    def _enqueue(self, action: str, path: str) -> None:
        if _is_yaml(path):
            self._loop.call_soon_threadsafe(self._queue.put_nowait, (action, path))

    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self._enqueue("upsert", event.src_path)

    def on_modified(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self._enqueue("upsert", event.src_path)

    def on_deleted(self, event: FileSystemEvent) -> None:
        if not event.is_directory:
            self._enqueue("delete", event.src_path)


async def _debounce_worker(
    queue: asyncio.Queue[tuple[str, str]],
    skill_dir: str,
) -> None:
    """디바운스: 이벤트를 모아서 _DEBOUNCE_SEC 후 일괄 처리."""
    from .ingest import delete_skill, ingest_single_skill

    while True:
        # 첫 이벤트 대기
        action, path = await queue.get()
        pending: dict[str, str] = {path: action}

        # 디바운스 윈도우 동안 추가 이벤트 수집
        await asyncio.sleep(_DEBOUNCE_SEC)
        while not queue.empty():
            try:
                a, p = queue.get_nowait()
                pending[p] = a  # 같은 파일은 마지막 액션만
            except asyncio.QueueEmpty:
                break

        # 일괄 처리
        for filepath, act in pending.items():
            try:
                if act == "upsert":
                    skill_id = _extract_skill_id(filepath)
                    if skill_id:
                        logger.info("Watcher: ingesting skill %s (%s)", skill_id, filepath)
                        await ingest_single_skill(skill_id, skill_dir)
                    else:
                        logger.warning("Watcher: could not extract skill_id from %s", filepath)
                elif act == "delete":
                    skill_id = _skill_id_from_filename(filepath)
                    logger.info("Watcher: deleting skill %s (%s)", skill_id, filepath)
                    await delete_skill(skill_id)
            except Exception:
                logger.exception("Watcher: failed to process %s on %s", act, filepath)


async def start_watcher(skill_dir: str = "./skills") -> Observer:
    """스킬 디렉토리 감시 시작. Observer 반환 (stop 시 사용).

    Usage:
        observer = await start_watcher("./skills")
        # ... 서버 종료 시:
        observer.stop()
        observer.join()
    """
    watch_path = Path(skill_dir).resolve()
    if not watch_path.exists():
        watch_path.mkdir(parents=True, exist_ok=True)
        logger.info("Created skill directory: %s", watch_path)

    loop = asyncio.get_running_loop()
    queue: asyncio.Queue[tuple[str, str]] = asyncio.Queue()

    handler = _SkillChangeHandler(loop, queue)
    observer = Observer()
    observer.schedule(handler, str(watch_path), recursive=True)
    observer.start()

    # 디바운스 워커를 백그라운드 태스크로 실행
    asyncio.create_task(_debounce_worker(queue, str(watch_path)))

    logger.info("Skill watcher started: %s", watch_path)
    return observer
