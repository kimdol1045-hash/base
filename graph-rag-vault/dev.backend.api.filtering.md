---
id: "dev.backend.api.filtering"
domain: "development.backend"
type: "rule"
bloom_level: ""
tags: ["backend", "api", "filtering", "sorting", "query-builder", "drizzle", "security"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.api.filtering

> #102 RESTful Design

필터링/정렬 쿼리 설계 (동적 필터는 화이트리스트 기반으로만 허용한다 -- 사용자 입력을 쿼리에 직접 넣는 것은 SQL Injection의 시작이다):

### 쿼리 파라미터 컨벤션
```
GET /api/v1/products?status=active&minPrice=100&maxPrice=500&category=electronics&sort=-createdAt&limit=20&cursor=abc123
```

| 파라미터 | 형식 | 예시 | 설명 |
|----------|------|------|------|
| 필터 | `field=value` | `status=active` | 정확한 일치 |
| 범위 | `minField`, `maxField` | `minPrice=100` | 범위 필터 |
| 다중 값 | `field=a,b,c` | `status=active,pending` | IN 연산 |
| 정렬 | `sort=field` / `sort=-field` | `sort=-createdAt` | -는 DESC |
| 검색 | `search=term` | `search=키보드` | 텍스트 검색 |

### 필터 연산자 설계
| 연산자 | URL 형식 | SQL 매핑 | 예시 |
|--------|----------|----------|------|
| eq | `field=value` | `= value` | `status=active` |
| gt | `minField=value` | `> value` | `minPrice=100` |
| gte | `minField=value` | `>= value` | `minCreatedAt=2024-01-01` |
| lt | `maxField=value` | `< value` | `maxPrice=500` |
| lte | `maxField=value` | `<= value` | `maxAge=30` |
| in | `field=a,b` | `IN (a, b)` | `category=a,b` |
| contains | `search=term` | `ILIKE %term%` | 텍스트 검색 |

DO:
```typescript
// 1. 화이트리스트 기반 필터 스키마 정의
const FILTERABLE_FIELDS = {
  status: { type: "enum", values: ["active", "pending", "archived"] },
  category: { type: "enum", values: ["electronics", "clothing", "food"] },
  minPrice: { type: "number", column: "price", operator: ">=" },
  maxPrice: { type: "number", column: "price", operator: "<=" },
  minCreatedAt: { type: "date", column: "created_at", operator: ">=" },
  maxCreatedAt: { type: "date", column: "created_at", operator: "<=" },
} as const;

const SORTABLE_FIELDS = ["createdAt", "updatedAt", "price", "name"] as const;

const ProductFilterSchema = z.object({
  status: z.enum(["active", "pending", "archived"]).optional(),
  category: z.string().optional(),
  minPrice: z.coerce.number().min(0).optional(),
  maxPrice: z.coerce.number().max(1_000_000).optional(),
  minCreatedAt: z.coerce.date().optional(),
  maxCreatedAt: z.coerce.date().optional(),
  search: z.string().max(100).optional(),
  sort: z.string().regex(/^-?(createdAt|updatedAt|price|name)$/).default("-createdAt"),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  cursor: z.string().optional(),
});

// 2. 동적 쿼리 빌더 (Drizzle)
import { and, eq, gte, lte, ilike, desc, asc, SQL } from "drizzle-orm";

function buildProductQuery(filters: z.infer<typeof ProductFilterSchema>) {
  const conditions: SQL[] = [];

  // 화이트리스트 필드만 조건 추가
  if (filters.status) conditions.push(eq(products.status, filters.status));
  if (filters.category) conditions.push(eq(products.category, filters.category));
  if (filters.minPrice != null) conditions.push(gte(products.price, filters.minPrice));
  if (filters.maxPrice != null) conditions.push(lte(products.price, filters.maxPrice));
  if (filters.minCreatedAt) conditions.push(gte(products.createdAt, filters.minCreatedAt));
  if (filters.maxCreatedAt) conditions.push(lte(products.createdAt, filters.maxCreatedAt));
  if (filters.search) conditions.push(ilike(products.name, `%${filters.search}%`));

  // 정렬 파싱
  const isDesc = filters.sort.startsWith("-");
  const sortField = filters.sort.replace(/^-/, "") as keyof typeof products;
  const sortColumn = products[sortField];
  const orderBy = isDesc ? desc(sortColumn) : asc(sortColumn);

  return { where: conditions.length > 0 ? and(...conditions) : undefined, orderBy };
}

// 3. API 핸들러
app.get("/api/v1/products", async (c) => {
  const filters = ProductFilterSchema.parse(c.req.query());
  const { where, orderBy } = buildProductQuery(filters);

  const results = await db.query.products.findMany({
    where,
    orderBy,
    limit: filters.limit + 1,  // +1로 다음 페이지 존재 여부 확인
    ...(filters.cursor ? { offset: decodeCursor(filters.cursor) } : {}),
  });

  const hasNext = results.length > filters.limit;
  const data = hasNext ? results.slice(0, -1) : results;

  return c.json({
    data,
    meta: {
      hasNext,
      nextCursor: hasNext ? encodeCursor(data[data.length - 1]) : null,
    },
  });
});
```

DON'T:
```typescript
// ❌ eval() 또는 문자열 보간으로 동적 필터 -- SQL Injection / 코드 실행
app.get("/products", async (c) => {
  const { filter } = c.req.query();
  const where = eval(filter);  // 치명적 보안 취약점
});

// ❌ 사용자 입력을 직접 컬럼명으로 사용
const sortColumn = c.req.query("sort");  // "price; DROP TABLE products--"
await db.execute(`SELECT * FROM products ORDER BY ${sortColumn}`);

// ❌ 필터 가능 필드 제한 없음 -- 내부 필드(password_hash 등) 노출
const filters = c.req.query();
Object.entries(filters).forEach(([key, value]) => {
  conditions.push(eq(products[key], value));  // 모든 컬럼 필터 허용
});

// ❌ 정렬 방향을 검증하지 않음
const order = c.req.query("order");  // "ASC; DROP TABLE--"
```

### 흔한 실수
- 필터 가능 필드를 화이트리스트로 관리하지 않음 -> 민감한 컬럼 노출
- 숫자 범위 필터에 최대값 제한 없음 -> maxPrice=999999999로 풀스캔 유도
- sort 파라미터에 여러 컬럼 허용 시 인덱스 미스 -> 복합 인덱스 설계 필요
- 검색어에 SQL 와일드카드(%, _) 이스케이프 누락 -> 의도치 않은 패턴 매칭
- 날짜 필터에 타임존 처리 누락 -> UTC 기준 통일 필수

## Connections

- [[dev.backend.api.search]] — CO_CREATES (weight: 0.6)
- [[dev.backend.database.query]] — CO_CREATES (weight: 0.6)
- [[dev.backend.database.index]] — CO_CREATES (weight: 0.6)
