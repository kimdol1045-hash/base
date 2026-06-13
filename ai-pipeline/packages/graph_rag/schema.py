"""Neo4j Cypher 스키마 — 제약조건, 인덱스, 쿼리 상수."""

from __future__ import annotations

# ─── 스키마 초기화 (제약조건 + 인덱스) ───

CONSTRAINTS = [
    "CREATE CONSTRAINT skill_id IF NOT EXISTS FOR (s:Skill) REQUIRE s.id IS UNIQUE",
]

INDEXES = [
    "CREATE INDEX skill_domain IF NOT EXISTS FOR (s:Skill) ON (s.domain)",
    "CREATE INDEX skill_type IF NOT EXISTS FOR (s:Skill) ON (s.skillType)",
    "CREATE INDEX skill_tags IF NOT EXISTS FOR (s:Skill) ON (s.tags)",
]

# ─── 노드 CRUD ───

UPSERT_SKILLS = """
UNWIND $skills AS s
MERGE (sk:Skill {id: s.id})
SET sk.domain       = s.domain,
    sk.skillType    = s.skillType,
    sk.bloomLevel   = s.bloomLevel,
    sk.theory       = s.theory,
    sk.tags         = s.tags,
    sk.tokenEstimate = s.tokenEstimate,
    sk.content      = s.content,
    sk.contentHash  = s.contentHash,
    sk.activationValue = coalesce(sk.activationValue, 1.0),
    sk.executionCount  = coalesce(sk.executionCount, 0),
    sk.successRate     = coalesce(sk.successRate, 1.0),
    sk.lastUsed        = coalesce(sk.lastUsed, '')
"""

DELETE_SKILL = """
MATCH (s:Skill {id: $skill_id})
DETACH DELETE s
"""

# ─── 엣지 CRUD ───

UPSERT_EDGES = """
UNWIND $edges AS e
MATCH (src:Skill {id: e.source})
MATCH (tgt:Skill {id: e.target})
CALL apoc.merge.relationship(src, e.type, {}, {weight: e.weight, autoCreated: e.autoCreated}, tgt, {}) YIELD rel
RETURN count(rel)
"""

# APOC 없이도 동작하는 엣지 생성 (타입별 분리)
UPSERT_REQUIRES = """
UNWIND $edges AS e
MATCH (src:Skill {id: e.source})
MATCH (tgt:Skill {id: e.target})
MERGE (src)-[r:REQUIRES]->(tgt)
SET r.weight = e.weight, r.autoCreated = e.autoCreated
"""

UPSERT_FEEDS = """
UNWIND $edges AS e
MATCH (src:Skill {id: e.source})
MATCH (tgt:Skill {id: e.target})
MERGE (src)-[r:FEEDS]->(tgt)
SET r.weight = e.weight, r.autoCreated = e.autoCreated
"""

UPSERT_CO_CREATES = """
UNWIND $edges AS e
MATCH (src:Skill {id: e.source})
MATCH (tgt:Skill {id: e.target})
MERGE (src)-[r:CO_CREATES]->(tgt)
SET r.weight = e.weight, r.autoCreated = e.autoCreated
"""

UPSERT_CO_OCCURS = """
UNWIND $edges AS e
MATCH (src:Skill {id: e.source})
MATCH (tgt:Skill {id: e.target})
MERGE (src)-[r:CO_OCCURS]->(tgt)
SET r.weight = e.weight, r.autoCreated = e.autoCreated
"""

EDGE_UPSERT_MAP = {
    "REQUIRES": UPSERT_REQUIRES,
    "FEEDS": UPSERT_FEEDS,
    "CO_CREATES": UPSERT_CO_CREATES,
    "CO_OCCURS": UPSERT_CO_OCCURS,
}

# ─── 확산 활성화 쿼리 ───

SPREAD_ACTIVATION_QUERY = """
// 시드 노드에서 3홉 확산 활성화
MATCH (seed:Skill)
WHERE seed.id IN $seed_ids
WITH seed, 1.0 AS activation

// 1홉: 직접 연결
OPTIONAL MATCH (seed)-[r1]->(hop1:Skill)
WHERE type(r1) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
WITH seed, hop1, r1,
     activation * r1.weight * $decay AS hop1_activation
WHERE hop1_activation >= $threshold_initial

// 2홉
OPTIONAL MATCH (hop1)-[r2]->(hop2:Skill)
WHERE type(r2) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
  AND hop2.id <> seed.id
WITH seed, hop1, hop1_activation, hop2, r2,
     hop1_activation * r2.weight * $decay AS hop2_activation
WHERE hop2_activation >= $threshold_hop

// 3홉
OPTIONAL MATCH (hop2)-[r3]->(hop3:Skill)
WHERE type(r3) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
  AND hop3.id <> seed.id
  AND hop3.id <> hop1.id
WITH collect(DISTINCT {id: hop1.id, score: hop1_activation, hop: 1}) +
     collect(DISTINCT {id: hop2.id, score: hop2_activation, hop: 2}) +
     collect(DISTINCT {id: hop3.id, score: hop2_activation * r3.weight * $decay, hop: 3}) AS all_results

UNWIND all_results AS r
WITH r WHERE r.id IS NOT NULL AND r.score >= $threshold_hop
RETURN r.id AS skillId, max(r.score) AS activationScore, min(r.hop) AS hopDistance
ORDER BY activationScore DESC
"""

# ─── 자가 발전 쿼리 ───

UPDATE_SKILL_STATS = """
MATCH (s:Skill {id: $skill_id})
SET s.executionCount = s.executionCount + 1,
    s.successRate = CASE
        WHEN $status = 'PASS'
        THEN (s.successRate * s.executionCount + 1.0) / (s.executionCount + 1)
        ELSE (s.successRate * s.executionCount) / (s.executionCount + 1)
    END,
    s.lastUsed = $timestamp
"""

UPDATE_EDGE_WEIGHT = """
MATCH (src:Skill {id: $source_id})-[r]->(tgt:Skill {id: $target_id})
WHERE type(r) = $edge_type
SET r.weight = CASE
    WHEN $status = 'PASS' THEN toFloat(r.weight) + $delta
    ELSE toFloat(r.weight) + $delta
END
"""

DECAY_ALL_WEIGHTS = """
MATCH ()-[r]->()
WHERE type(r) IN ['REQUIRES', 'FEEDS', 'CO_CREATES', 'CO_OCCURS']
SET r.weight = r.weight * $decay_factor
"""

CREATE_CO_OCCURS_EDGE = """
MATCH (a:Skill {id: $source_id})
MATCH (b:Skill {id: $target_id})
MERGE (a)-[r:CO_OCCURS]->(b)
ON CREATE SET r.weight = 0.5, r.autoCreated = true, r.coOccurCount = 1
ON MATCH SET r.coOccurCount = r.coOccurCount + 1,
             r.weight = CASE WHEN r.coOccurCount >= $threshold THEN r.weight + 0.05 ELSE r.weight END
"""

# ─── 통계 쿼리 ───

COUNT_SKILLS = "MATCH (s:Skill) RETURN count(s) AS count"
COUNT_EDGES = "MATCH ()-[r]->() RETURN type(r) AS type, count(r) AS count"

GET_SKILL_BY_ID = "MATCH (s:Skill {id: $id}) RETURN s"

# ─── Louvain 커뮤니티 탐지 (GDS) ───

GDS_PROJECT_GRAPH = """
CALL gds.graph.project(
    'skill-graph',
    'Skill',
    {
        REQUIRES: {orientation: 'UNDIRECTED', properties: 'weight'},
        FEEDS: {orientation: 'UNDIRECTED', properties: 'weight'},
        CO_CREATES: {orientation: 'UNDIRECTED', properties: 'weight'},
        CO_OCCURS: {orientation: 'UNDIRECTED', properties: 'weight'}
    }
)
"""

GDS_DROP_GRAPH = "CALL gds.graph.drop('skill-graph', false)"

GDS_LOUVAIN = """
CALL gds.louvain.write('skill-graph', {
    writeProperty: 'community',
    relationshipWeightProperty: 'weight'
})
YIELD communityCount, modularity
RETURN communityCount, modularity
"""

GET_COMMUNITIES = """
MATCH (s:Skill)
WHERE s.community IS NOT NULL
RETURN s.community AS community, collect(s.id) AS skills, count(s) AS size
ORDER BY size DESC
"""

# ─── 전체 초기화 / 리셋 ───

DELETE_ALL = """
MATCH (n)
DETACH DELETE n
"""
