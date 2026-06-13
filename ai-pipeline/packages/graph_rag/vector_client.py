"""Qdrant async 벡터 DB 클라이언트."""

from __future__ import annotations

import logging
from typing import Any

from qdrant_client import AsyncQdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
    Filter,
    FieldCondition,
    MatchValue,
)

from .config import GraphRAGSettings, get_settings

logger = logging.getLogger(__name__)


class VectorClient:
    """Qdrant async 클라이언트.

    Usage:
        async with VectorClient() as client:
            results = await client.search("JWT 인증", vector)
    """

    def __init__(self, settings: GraphRAGSettings | None = None) -> None:
        self._settings = settings or get_settings()
        self._client: AsyncQdrantClient | None = None
        self._collection = self._settings.qdrant_collection

    async def connect(self) -> None:
        """클라이언트 연결."""
        if self._client is not None:
            return
        self._client = AsyncQdrantClient(
            host=self._settings.qdrant_host,
            port=self._settings.qdrant_port,
        )
        logger.info(
            "Qdrant connected: %s:%s",
            self._settings.qdrant_host,
            self._settings.qdrant_port,
        )

    async def close(self) -> None:
        """클라이언트 종료."""
        if self._client:
            await self._client.close()
            self._client = None
            logger.info("Qdrant disconnected")

    async def __aenter__(self) -> VectorClient:
        await self.connect()
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()

    async def ensure_collection(self) -> None:
        """컬렉션이 없으면 생성."""
        assert self._client is not None
        collections = await self._client.get_collections()
        names = [c.name for c in collections.collections]

        if self._collection not in names:
            await self._client.create_collection(
                collection_name=self._collection,
                vectors_config=VectorParams(
                    size=self._settings.embedding_dimensions,
                    distance=Distance.COSINE,
                ),
            )
            logger.info("Created collection: %s", self._collection)
        else:
            logger.info("Collection exists: %s", self._collection)

    async def upsert_batch(
        self,
        points: list[dict[str, Any]],
    ) -> None:
        """벡터 배치 업서트.

        Args:
            points: [{"id": int, "skill_id": str, "vector": [...], "payload": {...}}]
        """
        assert self._client is not None
        structs = [
            PointStruct(
                id=p["id"],
                vector=p["vector"],
                payload=p.get("payload", {}),
            )
            for p in points
        ]

        # 100개씩 배치
        batch_size = 100
        for i in range(0, len(structs), batch_size):
            batch = structs[i : i + batch_size]
            await self._client.upsert(
                collection_name=self._collection,
                points=batch,
            )
        logger.info("Upserted %d vectors to %s", len(structs), self._collection)

    async def delete_point(self, skill_id: str) -> None:
        """스킬 ID 기반 포인트 삭제 (결정적 ID 사용)."""
        from .ingest import skill_id_to_qdrant_id

        assert self._client is not None
        point_id = skill_id_to_qdrant_id(skill_id)
        await self._client.delete(
            collection_name=self._collection,
            points_selector=[point_id],
        )
        logger.info("Deleted point %d (skill: %s) from %s", point_id, skill_id, self._collection)

    async def search(
        self,
        query_vector: list[float],
        limit: int = 20,
        domain_filter: str | None = None,
    ) -> list[dict[str, Any]]:
        """벡터 유사도 검색.

        Returns:
            [{"skill_id": str, "score": float, "payload": dict}]
        """
        assert self._client is not None

        query_filter = None
        if domain_filter:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="domain",
                        match=MatchValue(value=domain_filter),
                    )
                ]
            )

        results = await self._client.search(
            collection_name=self._collection,
            query_vector=query_vector,
            limit=limit,
            query_filter=query_filter,
        )

        return [
            {
                "skill_id": hit.payload.get("skill_id", ""),
                "score": hit.score,
                "payload": hit.payload,
            }
            for hit in results
        ]

    async def get_count(self) -> int:
        """컬렉션 포인트 수."""
        assert self._client is not None
        info = await self._client.get_collection(self._collection)
        return info.points_count or 0

    async def verify_connection(self) -> bool:
        """연결 상태 확인."""
        try:
            assert self._client is not None
            collections = await self._client.get_collections()
            return collections is not None
        except Exception as e:
            logger.error("Qdrant connection failed: %s", e)
            return False

    async def delete_collection(self) -> None:
        """컬렉션 삭제 (리셋용)."""
        assert self._client is not None
        try:
            await self._client.delete_collection(self._collection)
            logger.info("Deleted collection: %s", self._collection)
        except Exception:
            logger.debug("Collection %s not found for deletion", self._collection)
