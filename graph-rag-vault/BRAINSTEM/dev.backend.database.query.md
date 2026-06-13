---
id: "dev.backend.database.query"
domain: "development.database"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#108 쿼리 최적화 (Query Optimization)"
tags: [database, query, optimization, n+1, pagination]
---

# dev.backend.database.query

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.database`  
> **Type**: `pattern`  
> **Theory**: #108 쿼리 최적화 (Query Optimization)  
> **Tokens**: 500

## Content

쿼리 최적화 규칙 (불필요한 DB 부하를 방지한다):

### SELECT * 금지
필요한 컬럼만 명시적으로 선택한다. 네트워크 전송량과 메모리 사용량을 줄인다.

DO:
```sql
SELECT id, name, email, created_at
FROM users
WHERE status = 'active'
ORDER BY created_at DESC
LIMIT 20;
```

DON'T:
```sql
-- ❌ 불필요한 컬럼까지 전부 가져옴 (BLOB/TEXT 포함 시 치명적)
SELECT * FROM users WHERE status = 'active';
```

### N+1 쿼리 방지
연관 데이터는 JOIN 또는 서브쿼리로 한 번에 가져온다.

DO:
```sql
-- ✅ JOIN으로 1회 쿼리
SELECT p.id, p.title, u.name AS author_name, u.avatar_url
FROM posts p
JOIN users u ON p.author_id = u.id
WHERE p.published = true
ORDER BY p.created_at DESC
LIMIT 20;
```

DON'T:
```typescript
// ❌ 루프 안에서 개별 쿼리 → N+1 (20개 포스트 = 21회 쿼리)
const posts = await db.query('SELECT * FROM posts WHERE published = true');
for (const post of posts) {
  const author = await db.query(
    'SELECT name FROM users WHERE id = $1',
    [post.author_id]
  );
  post.authorName = author.rows[0].name;
}
```

### 페이지네이션
대량 데이터에서 OFFSET은 뒤로 갈수록 느려진다. cursor 기반을 우선 사용한다.

DO:
```sql
-- ✅ Cursor 기반: 일정한 성능 (O(1))
SELECT id, title, created_at
FROM posts
WHERE created_at < $1  -- 마지막 항목의 created_at
ORDER BY created_at DESC
LIMIT 20;
```

DON'T:
```sql
-- ❌ OFFSET 기반: 페이지 100 = 2000행 스캔 후 버림
SELECT id, title FROM posts
ORDER BY created_at DESC
LIMIT 20 OFFSET 2000;
```

### Prepared Statement 필수
동적 쿼리도 반드시 parameterized query를 사용한다.

DO:
```typescript
// ✅ parameterized query → SQL Injection 방지
const result = await db.query(
  'SELECT id, email FROM users WHERE email = $1 AND status = $2',
  [userEmail, 'active']
);
```

DON'T:
```typescript
// ❌ 문자열 연결 → SQL Injection 취약
const result = await db.query(
  `SELECT * FROM users WHERE email = '${userEmail}'`
);
```

### EXPLAIN ANALYZE 활용
복잡한 쿼리는 반드시 실행 계획을 확인한다.
```sql
EXPLAIN ANALYZE
SELECT p.id, p.title, u.name
FROM posts p
JOIN users u ON p.author_id = u.id
WHERE p.category_id = '550e8400-e29b-41d4-a716-446655440000'
ORDER BY p.created_at DESC
LIMIT 20;

-- 확인 포인트:
-- 1. Seq Scan이 보이면 → 인덱스 추가 필요
-- 2. Nested Loop이 대량 데이터에 보이면 → Hash/Merge Join 검토
-- 3. actual rows vs. estimated rows 차이가 10배 이상 → ANALYZE 실행
```

### 벌크 INSERT 최적화
```sql
-- ✅ 한 번의 INSERT로 다수 행 삽입
INSERT INTO tags (name, slug) VALUES
  ('typescript', 'typescript'),
  ('postgresql', 'postgresql'),
  ('react', 'react')
ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name;
```

### 흔한 실수
- WHERE 절에 함수 사용 → 인덱스 무효화 (`WHERE LOWER(email) = ...` 대신 함수 인덱스 사용)
- LIKE '%keyword%' → Full Table Scan (pg_trgm 또는 Full Text Search 사용)
- COUNT(*) 남용 → 대량 테이블에서 매우 느림 (approximate count 고려)
- 트랜잭션 내 외부 API 호출 → 커넥션 점유 시간 증가, 데드락 위험

## Connections

### REQUIRES (1)

- ← [[dev.backend.database.role]] `w=0.9`

### FEEDS (3)

- ← [[dev.backend.database.schema]] `w=0.7`
- → [[dev.backend.database.transaction]] `w=0.7`
- → [[dev.backend.database.verify]] `w=0.8`

### CO_CREATES (5)

- ← [[dev.backend.api.filtering]] `w=0.6`
- ← [[dev.backend.api.search]] `w=0.6`
- → [[dev.backend.database.index]] `w=0.6`
- ← [[dev.backend.database.schema]] `w=0.6`
- → [[dev.backend.database.transaction]] `w=0.6`
