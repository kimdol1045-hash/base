"""Graph RAG 설정 — Neo4j / Qdrant / OpenAI 연결 정보."""

from __future__ import annotations


from pydantic_settings import BaseSettings


class GraphRAGSettings(BaseSettings):
    """환경 변수 기반 설정. .env 파일 자동 로드."""

    # Neo4j
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""

    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "skills"

    # OpenAI Embedding
    openai_api_key: str = ""
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536

    # Skill YAML 디렉토리
    skill_dir: str = "./skills"

    # 확산 활성화 파라미터
    spread_decay: float = 0.85
    spread_threshold_initial: float = 0.50
    spread_threshold_hop: float = 0.40
    spread_max_hops: int = 3

    # 하이브리드 선택기 가중치
    weight_graph: float = 0.5
    weight_vector: float = 0.3
    weight_static: float = 0.2

    # 자가 발전
    evolution_success_delta: float = 0.05
    evolution_failure_delta: float = -0.05
    evolution_decay_factor: float = 0.95
    evolution_co_occur_threshold: int = 3

    model_config = {"env_prefix": "GRAPH_RAG_", "env_file": ".env", "extra": "ignore"}


def get_settings() -> GraphRAGSettings:
    """싱글턴 설정 반환."""
    return GraphRAGSettings()
