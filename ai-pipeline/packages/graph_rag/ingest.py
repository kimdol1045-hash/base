"""YAML → Neo4j + Qdrant 인제스트."""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import Any

import yaml

from .config import get_settings
from .edge_extractor import extract_all_edges
from .embeddings import load_all_skills, generate_embeddings, _content_hash
from .models import SkillEdge
from .neo4j_client import Neo4jClient
from .schema import DELETE_SKILL, EDGE_UPSERT_MAP, UPSERT_SKILLS
from .vector_client import VectorClient

logger = logging.getLogger(__name__)


def skill_id_to_qdrant_id(skill_id: str) -> int:
    """스킬 ID → 결정적 Qdrant point ID (MD5 기반)."""
    return int(hashlib.md5(skill_id.encode()).hexdigest()[:15], 16)


def _skill_to_neo4j(skill: dict[str, Any]) -> dict[str, Any]:
    """스킬 dict → Neo4j 파라미터 형식."""
    return {
        "id": skill["id"],
        "domain": skill["domain"],
        "skillType": skill["type"],
        "bloomLevel": "",
        "theory": skill.get("theory", ""),
        "tags": skill.get("tags", []),
        "tokenEstimate": skill.get("token_estimate", 400),
        "content": skill.get("content", ""),
        "contentHash": skill.get("content_hash", ""),
    }


def _edges_to_params(edges: list[SkillEdge]) -> dict[str, list[dict[str, Any]]]:
    """엣지 목록을 타입별로 그룹화 → Cypher 파라미터."""
    grouped: dict[str, list[dict[str, Any]]] = {
        "REQUIRES": [],
        "FEEDS": [],
        "CO_CREATES": [],
        "CO_OCCURS": [],
    }

    for edge in edges:
        grouped[edge.edge_type.value].append({
            "source": edge.source_id,
            "target": edge.target_id,
            "weight": edge.weight,
            "autoCreated": edge.auto_created,
        })

    return grouped


async def ingest_skills_to_neo4j(
    neo4j: Neo4jClient,
    skill_dir: str | None = None,
) -> dict[str, int]:
    """스킬 YAML → Neo4j 노드 + 엣지 인제스트.

    Returns:
        {"nodes": int, "edges": {"REQUIRES": int, ...}}
    """
    # 1. 스킬 로드
    skills = load_all_skills(skill_dir)
    if not skills:
        logger.warning("No skills found")
        return {"nodes": 0, "edges": {}}

    # 2. 스키마 초기화
    await neo4j.init_schema()

    # 3. 노드 업서트 (100개씩 배치)
    neo4j_params = [_skill_to_neo4j(s) for s in skills]
    batch_size = 100
    for i in range(0, len(neo4j_params), batch_size):
        batch = neo4j_params[i : i + batch_size]
        await neo4j.run_void(UPSERT_SKILLS, {"skills": batch})
        logger.info("Upserted nodes %d-%d", i, i + len(batch))

    # 4. 엣지 추출 + 업서트
    edges = extract_all_edges()
    grouped = _edges_to_params(edges)
    edge_counts: dict[str, int] = {}

    for edge_type, params in grouped.items():
        if not params:
            continue
        cypher = EDGE_UPSERT_MAP.get(edge_type)
        if not cypher:
            logger.warning("No upsert query for edge type: %s", edge_type)
            continue

        # 배치 처리
        for i in range(0, len(params), batch_size):
            batch = params[i : i + batch_size]
            try:
                await neo4j.run_void(cypher, {"edges": batch})
            except Exception as e:
                # 누락된 노드 참조 시 개별 처리
                logger.warning("Batch edge upsert failed, trying individual: %s", e)
                for edge_param in batch:
                    try:
                        await neo4j.run_void(cypher, {"edges": [edge_param]})
                    except Exception as ie:
                        logger.debug(
                            "Skipping edge %s → %s: %s",
                            edge_param["source"], edge_param["target"], ie,
                        )

        edge_counts[edge_type] = len(params)
        logger.info("Upserted %d %s edges", len(params), edge_type)

    total_edges = sum(edge_counts.values())
    logger.info(
        "Ingest complete: %d nodes, %d edges (%s)",
        len(skills), total_edges, edge_counts,
    )
    return {"nodes": len(skills), "edges": edge_counts}


async def ingest_skills_to_qdrant(
    vector: VectorClient,
    skill_dir: str | None = None,
) -> int:
    """스킬 content → 임베딩 → Qdrant 업서트.

    Returns:
        업서트된 포인트 수
    """
    settings = get_settings()
    skills = load_all_skills(skill_dir)
    if not skills:
        logger.warning("No skills found")
        return 0

    # 컬렉션 생성
    await vector.ensure_collection()

    # 임베딩 텍스트 준비: id + domain + tags + content
    texts = []
    for s in skills:
        tags_str = ", ".join(s.get("tags", []))
        text = f"[{s['id']}] domain={s['domain']} tags={tags_str}\n{s['content'][:500]}"
        texts.append(text)

    # 임베딩 생성
    embeddings = await generate_embeddings(texts, settings)

    # Qdrant 포인트 생성 (결정적 ID)
    points = []
    for skill, embedding in zip(skills, embeddings):
        points.append({
            "id": skill_id_to_qdrant_id(skill["id"]),
            "vector": embedding,
            "payload": {
                "skill_id": skill["id"],
                "domain": skill["domain"],
                "skill_type": skill["type"],
                "tags": skill.get("tags", []),
                "token_estimate": skill.get("token_estimate", 400),
                "content_preview": skill["content"][:200],
            },
        })

    # 업서트
    await vector.upsert_batch(points)

    logger.info("Qdrant ingest complete: %d vectors", len(points))
    return len(points)


async def ingest_single_skill(
    skill_id: str,
    skill_dir: str = "./skills",
) -> bool:
    """단일 스킬 인제스트/업데이트 (변경 감지 포함).

    Returns:
        True if the skill was updated, False if unchanged.
    """
    settings = get_settings()
    base_dir = Path(skill_dir)

    # 스킬 YAML 파일 찾기
    yaml_path: Path | None = None
    for p in base_dir.rglob("*.yaml"):
        try:
            with open(p, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data and data.get("id") == skill_id:
                yaml_path = p
                break
        except Exception:
            continue

    if yaml_path is None:
        # .yml 확장자도 탐색
        for p in base_dir.rglob("*.yml"):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                if data and data.get("id") == skill_id:
                    yaml_path = p
                    break
            except Exception:
                continue

    if yaml_path is None:
        logger.warning("Skill YAML not found for id: %s", skill_id)
        return False

    with open(yaml_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data or "id" not in data:
        logger.warning("Invalid YAML: %s", yaml_path)
        return False

    content = data.get("content", "")
    new_hash = _content_hash(content)

    # Neo4j에서 기존 contentHash 확인
    async with Neo4jClient() as neo4j:
        records = await neo4j.run(
            "MATCH (s:Skill {id: $id}) RETURN s.contentHash AS hash",
            {"id": skill_id},
        )
        old_hash = records[0]["hash"] if records else None

        if old_hash == new_hash:
            logger.info("Skill %s unchanged (hash=%s), skipping", skill_id, new_hash)
            return False

        # Neo4j 노드 업서트
        skill_data = {
            "id": data["id"],
            "domain": data.get("domain", ""),
            "type": data.get("type", ""),
            "content": content,
            "tags": data.get("tags", []),
            "token_estimate": data.get("token_estimate", 400),
            "theory": data.get("theory", ""),
            "content_hash": new_hash,
        }
        await neo4j.init_schema()
        await neo4j.run_void(UPSERT_SKILLS, {"skills": [_skill_to_neo4j(skill_data)]})
        logger.info("Neo4j upserted skill: %s", skill_id)

    # Qdrant 포인트 업서트
    tags_str = ", ".join(data.get("tags", []))
    text = f"[{skill_id}] domain={data.get('domain', '')} tags={tags_str}\n{content[:500]}"
    embeddings = await generate_embeddings([text], settings)

    point = {
        "id": skill_id_to_qdrant_id(skill_id),
        "vector": embeddings[0],
        "payload": {
            "skill_id": skill_id,
            "domain": data.get("domain", ""),
            "skill_type": data.get("type", ""),
            "tags": data.get("tags", []),
            "token_estimate": data.get("token_estimate", 400),
            "content_preview": content[:200],
        },
    }

    async with VectorClient() as vector:
        await vector.ensure_collection()
        await vector.upsert_batch([point])
        logger.info("Qdrant upserted skill: %s (point_id=%d)", skill_id, point["id"])

    return True


async def delete_skill(skill_id: str) -> None:
    """스킬 삭제: Neo4j + Qdrant."""
    async with Neo4jClient() as neo4j:
        await neo4j.run_void(DELETE_SKILL, {"skill_id": skill_id})
        logger.info("Neo4j deleted skill: %s", skill_id)

    async with VectorClient() as vector:
        await vector.connect()
        await vector.delete_point(skill_id)
        logger.info("Qdrant deleted skill: %s", skill_id)


async def full_ingest(skill_dir: str | None = None) -> dict[str, Any]:
    """Neo4j + Qdrant 전체 인제스트."""
    settings = get_settings()
    skill_dir = skill_dir or settings.skill_dir

    results: dict[str, Any] = {}

    async with Neo4jClient() as neo4j:
        neo4j_result = await ingest_skills_to_neo4j(neo4j, skill_dir)
        results["neo4j"] = neo4j_result

    async with VectorClient() as vector:
        qdrant_count = await ingest_skills_to_qdrant(vector, skill_dir)
        results["qdrant"] = {"vectors": qdrant_count}

    return results
