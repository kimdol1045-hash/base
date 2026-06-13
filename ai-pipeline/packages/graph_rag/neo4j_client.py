"""Neo4j async 드라이버 래퍼."""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import Any

from neo4j import AsyncGraphDatabase, AsyncDriver, AsyncSession

from .config import GraphRAGSettings, get_settings
from .schema import CONSTRAINTS, INDEXES

logger = logging.getLogger(__name__)


class Neo4jClient:
    """Neo4j async 클라이언트.

    Usage:
        async with Neo4jClient() as client:
            result = await client.run("MATCH (n) RETURN count(n)")
    """

    def __init__(self, settings: GraphRAGSettings | None = None) -> None:
        self._settings = settings or get_settings()
        self._driver: AsyncDriver | None = None

    async def connect(self) -> None:
        """드라이버 연결."""
        if self._driver is not None:
            return
        self._driver = AsyncGraphDatabase.driver(
            self._settings.neo4j_uri,
            auth=(self._settings.neo4j_user, self._settings.neo4j_password),
        )
        logger.info("Neo4j connected: %s", self._settings.neo4j_uri)

    async def close(self) -> None:
        """드라이버 종료."""
        if self._driver:
            await self._driver.close()
            self._driver = None
            logger.info("Neo4j disconnected")

    async def __aenter__(self) -> Neo4jClient:
        await self.connect()
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    @asynccontextmanager
    async def session(self) -> Any:
        """Neo4j 세션 컨텍스트 매니저."""
        if not self._driver:
            await self.connect()
        assert self._driver is not None
        session: AsyncSession = self._driver.session()
        try:
            yield session
        finally:
            await session.close()

    async def run(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """단일 Cypher 쿼리 실행 → 결과 목록 반환."""
        async with self.session() as session:
            result = await session.run(query, parameters or {})
            records = [record.data() for record in await result.fetch(1000)]
            return records

    async def run_void(
        self,
        query: str,
        parameters: dict[str, Any] | None = None,
    ) -> None:
        """결과 없는 Cypher 쿼리 실행 (DDL, 업데이트 등)."""
        async with self.session() as session:
            await session.run(query, parameters or {})

    async def init_schema(self) -> None:
        """제약조건 + 인덱스 생성."""
        for constraint in CONSTRAINTS:
            try:
                await self.run_void(constraint)
                logger.info("Created constraint: %s", constraint[:60])
            except Exception as e:
                logger.debug("Constraint already exists or error: %s", e)

        for index in INDEXES:
            try:
                await self.run_void(index)
                logger.info("Created index: %s", index[:60])
            except Exception as e:
                logger.debug("Index already exists or error: %s", e)

    async def verify_connection(self) -> bool:
        """연결 상태 확인."""
        try:
            result = await self.run("RETURN 1 AS ok")
            return len(result) > 0 and result[0].get("ok") == 1
        except Exception as e:
            logger.error("Neo4j connection failed: %s", e)
            return False

    async def get_counts(self) -> dict[str, Any]:
        """노드/엣지 카운트 반환."""
        nodes = await self.run("MATCH (s:Skill) RETURN count(s) AS count")
        edges = await self.run(
            "MATCH ()-[r]->() RETURN type(r) AS type, count(r) AS count"
        )
        return {
            "nodes": nodes[0]["count"] if nodes else 0,
            "edges": {row["type"]: row["count"] for row in edges},
        }
