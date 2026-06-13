---
id: "dev.backend.api.pagination"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#105 Cursor Pagination (Bickle, 2019)"
tags: [backend, api, pagination, cursor, performance, database]
---

# dev.backend.api.pagination

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #105 Cursor Pagination (Bickle, 2019)  
> **Tokens**: 500

## Content

페이지네이션 패턴 (대량 데이터를 한번에 반환하면 서버/클라이언트 모두 죽는다):

### Cursor vs Offset 비교
| 항목 | Cursor (커서) | Offset (오프셋) |
|------|--------------|-----------------|
| 성능 | O(1) -- 인덱스 탐색 | O(N) -- offset 증가 시 느려짐 |
| 일관성 | 중간 삽입/삭제에 안전 | 행이 추가되면 중복/누락 발생 |
| "N페이지로 이동" | 불가능 | 가능 |
| 사용 시점 | **무한 스크롤, 피드, 대용량** | 관리자 페이지, 소규모 데이터 |
| 구현 난이도 | 약간 복잡 | 단순 |

### Cursor 기반 페이지네이션 (권장)
```typescript
// schemas/pagination.ts
const CursorQuerySchema = z.object({
  cursor: z.string().optional(),  // 마지막 아이템의 ID 또는 인코딩 값
  limit: z.coerce.number().int().min(1).max(100).default(20),
});

// routes/posts.ts
app.get("/api/v1/posts", async (c) => {
  const { cursor, limit } = CursorQuerySchema.parse(c.req.query());

  const posts = await db.query.posts.findMany({
    where: cursor ? lt(posts.id, cursor) : undefined,  // id 기준 역순
    orderBy: [desc(posts.id)],
    limit: limit + 1,  // +1로 다음 페이지 존재 여부 확인
  });

  const hasMore = posts.length > limit;
  const items = hasMore ? posts.slice(0, -1) : posts;  // +1 항목 제거
  const nextCursor = hasMore ? items[items.length - 1].id : undefined;

  return c.json({
    data: items,
    meta: {
      hasMore,
      nextCursor,
    },
  });
});
```

클라이언트 사용:
```
GET /api/v1/posts?limit=20
→ { data: [...20개], meta: { hasMore: true, nextCursor: "abc123" } }

GET /api/v1/posts?limit=20&cursor=abc123
→ { data: [...20개], meta: { hasMore: true, nextCursor: "def456" } }

GET /api/v1/posts?limit=20&cursor=def456
→ { data: [...5개], meta: { hasMore: false } }
```

### 복합 커서 (정렬 기준이 unique하지 않을 때)
```typescript
// created_at이 같은 행이 여러 개일 수 있으므로 id를 보조 키로 사용
function encodeCursor(createdAt: Date, id: string): string {
  return Buffer.from(JSON.stringify({ createdAt, id })).toString("base64url");
}

function decodeCursor(cursor: string): { createdAt: Date; id: string } {
  return JSON.parse(Buffer.from(cursor, "base64url").toString());
}

app.get("/api/v1/posts", async (c) => {
  const { cursor, limit } = CursorQuerySchema.parse(c.req.query());

  let whereClause;
  if (cursor) {
    const { createdAt, id } = decodeCursor(cursor);
    whereClause = or(
      lt(posts.createdAt, createdAt),
      and(eq(posts.createdAt, createdAt), lt(posts.id, id)),
    );
  }

  const items = await db.query.posts.findMany({
    where: whereClause,
    orderBy: [desc(posts.createdAt), desc(posts.id)],
    limit: limit + 1,
  });

  const hasMore = items.length > limit;
  const result = hasMore ? items.slice(0, -1) : items;
  const nextCursor = hasMore
    ? encodeCursor(result.at(-1)!.createdAt, result.at(-1)!.id)
    : undefined;

  return c.json({ data: result, meta: { hasMore, nextCursor } });
});
```

### Offset 기반 페이지네이션 (관리자/소규모용)
```typescript
const OffsetQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});

app.get("/api/v1/admin/users", authMiddleware, requireRole("admin"), async (c) => {
  const { page, limit } = OffsetQuerySchema.parse(c.req.query());
  const offset = (page - 1) * limit;

  const [items, countResult] = await Promise.all([
    db.query.users.findMany({ limit, offset, orderBy: [desc(users.createdAt)] }),
    db.select({ count: count() }).from(users),
  ]);

  const total = countResult[0].count;

  return c.json({
    data: items,
    meta: {
      page,
      limit,
      total,
      totalPages: Math.ceil(total / limit),
    },
  });
});
```

DON'T:
```typescript
// ❌ limit 없이 전체 조회
const allPosts = await db.query.posts.findMany(); // 100만 행이면?

// ❌ offset이 커지면 성능 급락
// OFFSET 100000 → DB가 100000행을 읽고 버림
const posts = await db.query.posts.findMany({ offset: 100000, limit: 20 });

// ❌ cursor를 id가 아닌 변경 가능한 값으로 사용
const cursor = post.title; // 제목이 바뀌면 페이지네이션 깨짐
```

### 선택 가이드
- 피드/타임라인/채팅: **Cursor** (무한 스크롤, 실시간 데이터 추가)
- 검색 결과: **Cursor** (결과가 많을 수 있음)
- 관리자 대시보드: **Offset** (페이지 번호 필요, 데이터 수만 건 이하)
- 내보내기/일괄처리: **Cursor** (대량 데이터 순회)

### 흔한 실수
- limit에 최대값 미설정 -> `?limit=999999`로 전체 데이터 노출
- `hasMore` 판단을 위해 `COUNT(*)` 별도 쿼리 -> cursor에서는 `limit+1`로 판단
- cursor 값을 클라이언트가 조작 가능하다고 가정하지 않음 -> base64 디코딩 후 검증 필요
- 정렬 기준 컬럼에 인덱스 없음 -> 대용량에서 full table scan 발생

## Connections

### CO_CREATES (2)

- ← [[dev.backend.api.rest]] `w=0.6`
- ← [[dev.backend.api.versioning]] `w=0.6`
