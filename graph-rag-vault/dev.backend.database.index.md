---
id: "dev.backend.database.index"
domain: "development.database"
type: "pattern"
bloom_level: ""
tags: ["database", "index", "btree", "gin", "explain-analyze", "performance"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.database.index

> #110 B-tree Index (Bayer & McCreight, 1972)

인덱싱 전략 (쿼리 성능을 O(n)에서 O(log n)으로 개선한다):

### 인덱스 종류와 사용 기준

**B-tree (기본, 가장 범용)**:
```sql
-- 등호(=), 범위(<, >, BETWEEN), ORDER BY, LIKE 'prefix%'
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_created_at ON orders(created_at);
```

**Hash (등호 비교만)**:
```sql
-- 정확한 값 매칭만 필요할 때 (범위 검색 불가)
CREATE INDEX idx_sessions_token ON sessions USING hash(token);
```

**GIN (배열, JSONB, 전문 검색)**:
```sql
-- JSONB 내부 검색
CREATE INDEX idx_products_metadata ON products USING gin(metadata);

-- 전문 검색 (Full Text Search)
ALTER TABLE posts ADD COLUMN search_vector tsvector
  GENERATED ALWAYS AS (
    setweight(to_tsvector('korean', coalesce(title, '')), 'A') ||
    setweight(to_tsvector('korean', coalesce(content, '')), 'B')
  ) STORED;
CREATE INDEX idx_posts_search ON posts USING gin(search_vector);
```

**GiST (지리 데이터, 범위 타입)**:
```sql
-- PostGIS 지리 데이터 인덱싱
CREATE INDEX idx_stores_location ON stores USING gist(location);
```

### 복합 인덱스 컬럼 순서
선택도(cardinality)가 높은 컬럼을 먼저 배치한다.

DO:
```sql
-- ✅ user_id(높은 선택도) → status(낮은 선택도) → created_at(범위)
CREATE INDEX idx_orders_user_status_date
  ON orders(user_id, status, created_at DESC);

-- 이 인덱스로 커버되는 쿼리들:
-- WHERE user_id = $1
-- WHERE user_id = $1 AND status = $2
-- WHERE user_id = $1 AND status = $2 ORDER BY created_at DESC
```

DON'T:
```sql
-- ❌ status(선택도 낮음: 5가지)를 먼저 → 효율 나쁨
CREATE INDEX idx_orders_bad ON orders(status, user_id, created_at);
```

### 부분 인덱스 (Partial Index)
조건부 데이터만 인덱싱하여 인덱스 크기를 줄인다.
```sql
-- active 사용자만 인덱싱 (전체의 20%만 해당)
CREATE INDEX idx_users_active_email
  ON users(email)
  WHERE deleted_at IS NULL AND status = 'active';
```

### EXPLAIN ANALYZE 읽는 법
```sql
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT id, title FROM posts
WHERE author_id = '550e8400-...' AND published = true
ORDER BY created_at DESC LIMIT 10;
```

핵심 확인 포인트:
```
-- ✅ 좋은 결과: Index Scan + 적은 행 처리
Index Scan using idx_posts_author on posts
  (cost=0.43..8.45 rows=10 width=48)
  (actual time=0.025..0.042 rows=10 loops=1)
  Buffers: shared hit=4

-- ❌ 나쁜 결과: Seq Scan + 전체 테이블 스캔
Seq Scan on posts
  (cost=0.00..125000.00 rows=500000 width=48)
  (actual time=0.015..1250.000 rows=10 loops=1)
  Filter: (author_id = '550e8400-...' AND published)
  Rows Removed by Filter: 499990
```

**체크 순서**:
1. `Seq Scan` 발견 → 인덱스 추가 필요
2. `actual rows` vs `rows` (estimated) 차이 10배+ → `ANALYZE` 실행
3. `Buffers: shared read` 높음 → 캐시 미스, 메모리 부족 가능
4. `Sort` 노드 발견 → ORDER BY 인덱스 커버 확인

### 인덱스 관리 규칙
- 테이블당 인덱스 5-7개 권장 상한 (쓰기 성능 저하 주의)
- 사용하지 않는 인덱스 정기 정리:
  ```sql
  SELECT indexrelname, idx_scan, idx_tup_read
  FROM pg_stat_user_indexes
  WHERE idx_scan = 0 AND schemaname = 'public'
  ORDER BY pg_relation_size(indexrelid) DESC;
  ```
- 프로덕션: CREATE INDEX CONCURRENTLY 사용 (테이블 락 방지)

### 흔한 실수
- 모든 컬럼에 인덱스 → INSERT/UPDATE 성능 50%+ 저하
- WHERE LOWER(email) 사용인데 일반 인덱스 → 함수 인덱스 필요
- LIKE '%keyword%' → B-tree 인덱스 사용 불가 (pg_trgm 또는 GIN 필요)
- 복합 인덱스의 중간 컬럼만 조건 → 인덱스 미사용

## Connections

- [[dev.backend.database.schema]] — CO_CREATES (weight: 0.6)
- [[dev.backend.database.query]] — CO_CREATES (weight: 0.6)
- [[dev.backend.database.transaction]] — CO_CREATES (weight: 0.6)
- [[dev.backend.api.search]] — CO_CREATES (weight: 0.6)
- [[dev.backend.api.filtering]] — CO_CREATES (weight: 0.6)
