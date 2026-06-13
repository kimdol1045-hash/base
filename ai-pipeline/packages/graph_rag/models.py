"""Graph RAG 데이터 모델 — 노드, 엣지, 활성화 결과."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class EdgeType(str, Enum):
    """그래프 엣지 유형."""
    REQUIRES = "REQUIRES"       # role → rules (0.90)
    FEEDS = "FEEDS"             # rules → verify (0.80), 크로스 도메인
    CO_CREATES = "CO_CREATES"   # 같은 키워드 그룹 내 동일 도메인
    CO_OCCURS = "CO_OCCURS"     # 자동 생성 (3회+ 동시 활성화)


class SkillType(str, Enum):
    """Atomic Skill 유형."""
    ROLE = "role"
    RULE = "rule"
    PATTERN = "pattern"
    VERIFY = "verify"
    STACK = "stack"


@dataclass
class SkillNode:
    """Neo4j Skill 노드 데이터."""
    id: str
    domain: str
    skill_type: str
    bloom_level: str = ""
    theory: str = ""
    tags: list[str] = field(default_factory=list)
    token_estimate: int = 400
    content: str = ""
    content_hash: str = ""

    # 동적 속성 (자가 발전)
    activation_value: float = 1.0
    execution_count: int = 0
    success_rate: float = 1.0
    last_used: str = ""


@dataclass
class SkillEdge:
    """Neo4j Skill 엣지 데이터."""
    source_id: str
    target_id: str
    edge_type: EdgeType
    weight: float = 1.0
    auto_created: bool = False


@dataclass
class ActivatedSkill:
    """확산 활성화 결과."""
    skill_id: str
    activation_score: float
    source: str  # "graph", "vector", "static"
    hop_distance: int = 0


@dataclass
class HybridResult:
    """하이브리드 선택 최종 결과."""
    skills: list[ActivatedSkill] = field(default_factory=list)
    graph_count: int = 0
    vector_count: int = 0
    static_count: int = 0
    total_score: float = 0.0


@dataclass
class EvolutionEvent:
    """자가 발전 이벤트."""
    skill_ids: list[str]
    status: str  # "PASS" / "FAIL"
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
