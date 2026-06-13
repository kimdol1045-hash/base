"""Hook Engine 데이터 모델."""

from __future__ import annotations

import json
import logging
import os
import threading
import time
from dataclasses import asdict, dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class BloomLevel(Enum):
    REMEMBER = 1
    UNDERSTAND = 2
    APPLY = 3
    ANALYZE = 4
    EVALUATE = 5
    CREATE = 6


@dataclass
class SkillAssemblyPlan:
    """Hook 엔진의 최종 출력. Pipeline에 전달된다."""

    skill_ids: list[str]
    post_checks: list[str]
    domains: list[str]
    bloom_level: BloomLevel
    complexity: int
    executor_model: str  # haiku / sonnet / opus
    token_budget: int
    assembled_prompt: str
    is_followup: bool
    original_input: str = ""
    semantic_keywords: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class Session:
    """대화 세션. 연속 요청 시 컨텍스트를 유지한다."""

    session_id: str
    history: list[SkillAssemblyPlan] = field(default_factory=list)
    active_domains: list[str] = field(default_factory=list)
    previous_outputs: list[str] = field(default_factory=list)
    accumulated_skills: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    last_accessed: float = field(default_factory=time.time)


# ─── 세션 저장소 ───

MAX_SESSIONS = 1000
SESSION_TTL_SECONDS = 3600


def _session_to_dict(session: Session) -> dict:
    """Session → JSON-serializable dict (history 제외, 너무 큼)."""
    return {
        "session_id": session.session_id,
        "active_domains": session.active_domains,
        "previous_outputs": session.previous_outputs[-10:],
        "accumulated_skills": session.accumulated_skills[-50:],
        "created_at": session.created_at,
        "last_accessed": session.last_accessed,
    }


def _session_from_dict(data: dict) -> Session:
    """dict → Session 복원."""
    return Session(
        session_id=data["session_id"],
        active_domains=data.get("active_domains", []),
        previous_outputs=data.get("previous_outputs", []),
        accumulated_skills=data.get("accumulated_skills", []),
        created_at=data.get("created_at", time.time()),
        last_accessed=data.get("last_accessed", time.time()),
    )


class _InMemoryStore:
    """인메모리 세션 저장소 (폴백용)."""

    def __init__(self) -> None:
        self._sessions: dict[str, Session] = {}

    def get_or_create(self, session_id: str) -> Session:
        if session_id in self._sessions:
            self._sessions[session_id].last_accessed = time.time()
            return self._sessions[session_id]

        if len(self._sessions) >= MAX_SESSIONS:
            self._evict()

        self._sessions[session_id] = Session(session_id=session_id)
        return self._sessions[session_id]

    def save(self, session: Session) -> None:
        session.last_accessed = time.time()
        self._sessions[session.session_id] = session

    def _evict(self) -> None:
        now = time.time()
        expired = [
            sid for sid, s in self._sessions.items()
            if now - s.last_accessed > SESSION_TTL_SECONDS
        ]
        for sid in expired:
            del self._sessions[sid]

        if len(self._sessions) >= MAX_SESSIONS:
            sorted_sessions = sorted(
                self._sessions.items(), key=lambda kv: kv[1].last_accessed
            )
            to_remove = len(self._sessions) - MAX_SESSIONS + 1
            for sid, _ in sorted_sessions[:to_remove]:
                del self._sessions[sid]


class _RedisStore:
    """Redis 기반 세션 저장소."""

    def __init__(self, client) -> None:
        self._redis = client
        self._prefix = "session:"

    def get_or_create(self, session_id: str) -> Session:
        key = f"{self._prefix}{session_id}"
        raw = self._redis.get(key)
        if raw:
            data = json.loads(raw)
            session = _session_from_dict(data)
            session.last_accessed = time.time()
            return session

        return Session(session_id=session_id)

    def save(self, session: Session) -> None:
        key = f"{self._prefix}{session.session_id}"
        session.last_accessed = time.time()
        data = _session_to_dict(session)
        self._redis.set(key, json.dumps(data), ex=SESSION_TTL_SECONDS)


class _SQLiteStore:
    """SQLite 기반 세션 저장소 (Redis 없을 때 영속성 제공)."""

    def __init__(self, db_path: str) -> None:
        import sqlite3
        self._db_path = db_path
        os.makedirs(os.path.dirname(db_path) or ".", exist_ok=True)
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._lock = threading.Lock()
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS sessions "
            "(session_id TEXT PRIMARY KEY, data TEXT, last_accessed REAL)"
        )
        self._conn.commit()

    def get_or_create(self, session_id: str) -> Session:
        with self._lock:
            self._evict()
            row = self._conn.execute(
                "SELECT data FROM sessions WHERE session_id = ?",
                (session_id,),
            ).fetchone()
        if row:
            data = json.loads(row[0])
            session = _session_from_dict(data)
            session.last_accessed = time.time()
            return session
        return Session(session_id=session_id)

    def save(self, session: Session) -> None:
        session.last_accessed = time.time()
        data = json.dumps(_session_to_dict(session))
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO sessions (session_id, data, last_accessed) VALUES (?, ?, ?)",
                (session.session_id, data, session.last_accessed),
            )
            self._conn.commit()

    def _evict(self) -> None:
        now = time.time()
        self._conn.execute(
            "DELETE FROM sessions WHERE last_accessed < ?",
            (now - SESSION_TTL_SECONDS,),
        )
        count = self._conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        if count >= MAX_SESSIONS:
            self._conn.execute(
                "DELETE FROM sessions WHERE session_id IN "
                "(SELECT session_id FROM sessions ORDER BY last_accessed ASC LIMIT ?)",
                (count - MAX_SESSIONS + 1,),
            )
        self._conn.commit()


def _create_store():
    """Redis → SQLite → 인메모리 순서로 세션 저장소 선택."""
    redis_url = os.environ.get("REDIS_URL", "")
    if redis_url:
        try:
            import redis
            client = redis.from_url(redis_url, decode_responses=True)
            client.ping()
            logger.info("Session store: Redis (%s)", redis_url)
            return _RedisStore(client)
        except Exception as e:
            logger.warning("Redis unavailable (%s), trying SQLite", e)

    sqlite_path = os.environ.get("SQLITE_SESSION_DB", "")
    if sqlite_path:
        try:
            store = _SQLiteStore(sqlite_path)
            logger.info("Session store: SQLite (%s)", sqlite_path)
            return store
        except Exception as e:
            logger.warning("SQLite unavailable (%s), falling back to in-memory", e)

    logger.info("Session store: in-memory")
    return _InMemoryStore()


_store = None


def _get_store():
    global _store
    if _store is None:
        _store = _create_store()
    return _store


def get_or_create_session(session_id: str) -> Session:
    return _get_store().get_or_create(session_id)


def save_session(session: Session) -> None:
    """세션 상태를 저장소에 영속화."""
    _get_store().save(session)
