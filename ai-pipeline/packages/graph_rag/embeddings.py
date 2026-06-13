"""스킬 content → 임베딩 벡터 생성 (OpenAI text-embedding-3-small)."""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

import yaml
from openai import AsyncOpenAI

from .config import GraphRAGSettings, get_settings

logger = logging.getLogger(__name__)


def _content_hash(content: str) -> str:
    """content의 SHA-256 해시 (변경 감지용)."""
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def load_all_skills(skill_dir: str | None = None) -> list[dict[str, Any]]:
    """모든 YAML 스킬 파일 로드.

    Returns:
        [{"id": str, "domain": str, "type": str, "content": str,
          "tags": list, "token_estimate": int, "theory": str, "content_hash": str}]
    """
    settings = get_settings()
    base_dir = Path(skill_dir or settings.skill_dir)

    skills: list[dict[str, Any]] = []
    for yaml_path in sorted(base_dir.rglob("*.yaml")):
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)

            if not data or "id" not in data:
                logger.warning("Skipping invalid YAML: %s", yaml_path)
                continue

            content = data.get("content", "")
            skills.append({
                "id": data["id"],
                "domain": data.get("domain", ""),
                "type": data.get("type", ""),
                "content": content,
                "tags": data.get("tags", []),
                "token_estimate": data.get("token_estimate", 400),
                "theory": data.get("theory", ""),
                "content_hash": _content_hash(content),
            })
        except Exception as e:
            logger.error("Failed to load %s: %s", yaml_path, e)

    logger.info("Loaded %d skills from %s", len(skills), base_dir)
    return skills


async def generate_embeddings(
    texts: list[str],
    settings: GraphRAGSettings | None = None,
) -> list[list[float]]:
    """텍스트 목록 → 임베딩 벡터 생성.

    Args:
        texts: 임베딩할 텍스트 목록
        settings: 설정 (None이면 기본값)

    Returns:
        임베딩 벡터 목록 (len(texts) == len(result))
    """
    settings = settings or get_settings()
    client = AsyncOpenAI(api_key=settings.openai_api_key)

    all_embeddings: list[list[float]] = []

    # OpenAI 배치 제한: 2048개, 각 8191 토큰
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        try:
            response = await client.embeddings.create(
                model=settings.embedding_model,
                input=batch,
            )
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)
            logger.info("Embedded batch %d-%d (%d texts)", i, i + len(batch), len(batch))
        except Exception as e:
            logger.error("Embedding failed for batch %d: %s", i, e)
            # 실패 시 제로 벡터로 대체
            all_embeddings.extend(
                [[0.0] * settings.embedding_dimensions] * len(batch)
            )

    return all_embeddings


async def embed_query(
    query: str,
    settings: GraphRAGSettings | None = None,
) -> list[float]:
    """단일 쿼리 텍스트 → 임베딩 벡터."""
    result = await generate_embeddings([query], settings)
    return result[0]
