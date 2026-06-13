---
id: "dev.backend.api.search"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "api", "search", "postgres", "tsvector", "full-text-search", "performance"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.api.search

> #110 Query Optimization

Full-text Search 패턴 (검색은 LIKE가 아니라 tsvector로 한다 -- 인덱싱 없는 검색은 테이블 풀스캔이다):

### Postgres tsvector 기본 설정

DO:
```typescript
// 1. 마이그레이션: tsvector 컬럼 + GIN 인덱스
import { sql } from "drizzle-orm";

export async function up(db: Database) {
  // 검색용 tsvector 컬럼 추가
  await db.execute(sql`
    ALTER TABLE posts ADD COLUMN search_vector tsvector
      GENERATED ALWAYS AS (
        setweight(to_tsvector('korean', coalesce(title, '')), 'A') ||
        setweight(to_tsvector('korean', coalesce(summary, '')), 'B') ||
        setweight(to_tsvector('korean', coalesce(body, '')), 'C')
      ) STORED;
  `);

  // GIN 인덱스 (검색 속도 핵심)
  await db.execute(sql`
    CREATE INDEX idx_posts_search ON posts USING GIN (search_vector);
  `);

  // trigram 인덱스 (오타 허용 퍼지 검색용)
  await db.execute(sql`
    CREATE EXTENSION IF NOT EXISTS pg_trgm;
    CREATE INDEX idx_posts_title_trgm ON posts USING GIN (title gin_trgm_ops);
  `);
}

// 2. 검색 API 구현
const SearchQuerySchema = z.object({
  q: z.string().min(1).max(100).trim(),
  category: z.string().optional(),
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(50).default(20),
});

app.get("/api/v1/posts/search", async (c) => {
  const { q, category, page, limit } = SearchQuerySchema.parse(c.req.query());

  // tsquery로 변환 (공백을 & 연산자로)
  const tsquery = q
    .split(/\s+/)
    .filter(Boolean)
    .map((term) => `${term}:*`)  // prefix 매칭
    .join(" & ");

  const offset = (page - 1) * limit;

  const results = await db.execute(sql`
    SELECT
      id, title, summary,
      ts_rank(search_vector, to_tsquery('korean', ${tsquery})) AS relevance,
      ts_headline('korean', body, to_tsquery('korean', ${tsquery}),
        'StartSel=<mark>, StopSel=</mark>, MaxWords=35, MinWords=15'
      ) AS highlight
    FROM posts
    WHERE search_vector @@ to_tsquery('korean', ${tsquery})
      ${category ? sql`AND category = ${category}` : sql``}
    ORDER BY relevance DESC, created_at DESC
    LIMIT ${limit} OFFSET ${offset}
  `);

  const total = await db.execute(sql`
    SELECT count(*) FROM posts
    WHERE search_vector @@ to_tsquery('korean', ${tsquery})
      ${category ? sql`AND category = ${category}` : sql``}
  `);

  return c.json({
    data: results.rows,
    meta: { total: total.rows[0].count, page, limit },
  });
});
```

### 퍼지 검색 (Trigram Similarity)
```typescript
// 오타 허용 검색 (예: "프로그래밍" -> "프로그레밍")
app.get("/api/v1/posts/suggest", async (c) => {
  const { q } = z.object({ q: z.string().min(2).max(50) }).parse(c.req.query());

  const suggestions = await db.execute(sql`
    SELECT title, similarity(title, ${q}) AS sim
    FROM posts
    WHERE similarity(title, ${q}) > 0.3
    ORDER BY sim DESC
    LIMIT 5
  `);

  return c.json({ data: suggestions.rows });
});

// similarity threshold 설정
await db.execute(sql`SET pg_trgm.similarity_threshold = 0.3`);
```

### 검색 가중치 전략
| 가중치 | 대상 필드 | 배수 | 이유 |
|--------|-----------|------|------|
| A (1.0) | title | 기본 x1.0 | 제목 일치가 가장 중요 |
| B (0.4) | summary | 기본 x0.4 | 요약은 보조 |
| C (0.2) | body | 기본 x0.2 | 본문은 노이즈가 많음 |
| D (0.1) | tags | 기본 x0.1 | 태그는 부가 정보 |

DON'T:
```typescript
// ❌ LIKE '%검색어%' -- 인덱스 사용 불가, 풀 테이블 스캔
const results = await db.execute(sql`
  SELECT * FROM posts WHERE body LIKE ${'%' + query + '%'}
`);  // 100만 행이면 매 검색마다 풀스캔

// ❌ 모든 컬럼에 동일 가중치 -- 제목과 본문의 중요도가 같을 수 없음
to_tsvector(title || ' ' || body)  // 가중치 없이 합침

// ❌ 검색어 sanitize 없이 직접 tsquery 전달
to_tsquery(${userInput})  // 특수문자(&, |, !) 포함 시 구문 오류

// ❌ search_vector를 매 쿼리마다 계산
WHERE to_tsvector('korean', title || body) @@ to_tsquery(${q})
// GENERATED STORED 컬럼이면 사전 계산됨
```

### 검색 성능 기준
| 데이터 규모 | 응답 시간 목표 | 권장 전략 |
|-------------|----------------|-----------|
| < 10만 행 | < 50ms | Postgres tsvector |
| 10만~100만 | < 100ms | tsvector + 파티셔닝 |
| 100만~1000만 | < 200ms | Elasticsearch/Meilisearch 고려 |
| > 1000만 | < 500ms | 전용 검색 엔진 필수 |

### 흔한 실수
- GIN 인덱스 없이 tsvector 검색 -> 인덱스가 성능의 핵심
- 한국어 검색 시 기본 'english' 설정 사용 -> 'korean' 또는 적절한 설정 필요
- ts_headline에 MinWords/MaxWords 미설정 -> 하이라이트 스니펫이 너무 길거나 짧음
- 검색어를 split 후 prefix 매칭(:*) 미적용 -> 부분 단어 매칭 불가
- 검색 결과 캐싱 미적용 -> 인기 검색어는 Redis 캐싱 (TTL 60초) 권장

## Connections

- [[dev.backend.api.filtering]] — CO_CREATES (weight: 0.6)
- [[dev.backend.database.query]] — CO_CREATES (weight: 0.6)
- [[dev.backend.database.index]] — CO_CREATES (weight: 0.6)
