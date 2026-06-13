---
id: "dev.backend.api.caching"
domain: "development.backend"
type: "rule"
region: BRAINSTEM
token_estimate: 500
theory: "#102 HTTP Caching (Fielding, 1999)"
tags: [backend, api, caching, http, redis, performance]
---

# dev.backend.api.caching

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `rule`  
> **Theory**: #102 HTTP Caching (Fielding, 1999)  
> **Tokens**: 500

## Content

HTTP 캐싱 전략 (같은 데이터를 반복 요청하는 것은 서버와 사용자 모두에게 낭비다):

### Cache-Control 헤더 기본
| 디렉티브 | 의미 | 사용 시점 |
|----------|------|-----------|
| `no-store` | 캐시 절대 금지 | 민감한 데이터 (인증 정보, 결제) |
| `no-cache` | 캐시하되 매번 재검증 | 자주 변하는 데이터 |
| `private` | 브라우저만 캐시 (CDN 금지) | 사용자별 데이터 |
| `public, max-age=N` | N초 동안 캐시 | 정적/공유 데이터 |
| `s-maxage=N` | CDN에서 N초 캐시 | CDN 활용 시 |
| `stale-while-revalidate=N` | 만료 후 N초간 캐시 제공하며 백그라운드 갱신 | 준실시간 데이터 |

### 엔드포인트별 캐싱 전략
```typescript
// 1. 공개 목록 (변경 빈도 낮음) -- CDN + 브라우저 캐시
app.get("/api/v1/categories", async (c) => {
  const categories = await getCategories();
  c.header("Cache-Control", "public, max-age=3600, s-maxage=86400, stale-while-revalidate=60");
  return c.json({ data: categories });
});

// 2. 사용자별 데이터 -- 브라우저만 캐시, CDN 금지
app.get("/api/v1/me/profile", authMiddleware, async (c) => {
  const profile = await getProfile(c.get("userId"));
  c.header("Cache-Control", "private, max-age=60");
  return c.json({ data: profile });
});

// 3. 민감한 데이터 -- 캐시 완전 금지
app.get("/api/v1/me/payment-methods", authMiddleware, async (c) => {
  const methods = await getPaymentMethods(c.get("userId"));
  c.header("Cache-Control", "no-store");
  return c.json({ data: methods });
});
```

### ETag를 이용한 조건부 요청
동일한 데이터를 반복 전송하지 않고, 변경 여부만 확인한다.

```typescript
import { createHash } from "crypto";

app.get("/api/v1/posts/:id", async (c) => {
  const post = await getPost(c.req.param("id"));
  if (!post) throw Errors.notFound("게시글");

  // ETag 생성 (콘텐츠 해시 기반)
  const etag = `"${createHash("md5").update(JSON.stringify(post)).digest("hex")}"`;

  // 클라이언트가 보낸 If-None-Match와 비교
  if (c.req.header("If-None-Match") === etag) {
    return c.body(null, 304);  // Not Modified -- body 전송 안 함
  }

  c.header("ETag", etag);
  c.header("Cache-Control", "private, no-cache");  // 매번 재검증
  return c.json({ data: post });
});
```

### 서버 사이드 캐싱 (Redis)
DB 부하를 줄이기 위해 자주 조회되는 데이터를 Redis에 캐싱한다.

```typescript
async function getCachedOrFetch<T>(
  key: string,
  ttlSeconds: number,
  fetcher: () => Promise<T>,
): Promise<T> {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached) as T;

  const data = await fetcher();
  await redis.set(key, JSON.stringify(data), "EX", ttlSeconds);
  return data;
}

// 사용
app.get("/api/v1/posts/:id", async (c) => {
  const id = c.req.param("id");
  const post = await getCachedOrFetch(
    `post:${id}`,
    300,  // 5분 TTL
    () => db.query.posts.findFirst({ where: eq(posts.id, id) }),
  );
  return c.json({ data: post });
});
```

### 캐시 무효화 (Cache Invalidation)
```typescript
// 데이터 변경 시 관련 캐시 삭제
app.patch("/api/v1/posts/:id", authMiddleware, async (c) => {
  const id = c.req.param("id");
  const updated = await updatePost(id, body);

  // 관련 캐시 무효화
  await redis.del(`post:${id}`);
  await redis.del("posts:list:*");  // 목록 캐시도 무효화

  return c.json({ data: updated });
});
```

DON'T:
```typescript
// ❌ 인증된 사용자 데이터에 public 캐시
c.header("Cache-Control", "public, max-age=3600");  // CDN이 캐시하면 다른 유저에게 노출

// ❌ POST/PATCH/DELETE 응답을 캐시
app.post("/api/v1/posts", async (c) => {
  c.header("Cache-Control", "max-age=60");  // 쓰기 요청은 캐시하면 안 됨
});

// ❌ 캐시 무효화 없이 데이터 수정
await updatePost(id, data);  // Redis 캐시는 여전히 옛날 데이터...
```

### 흔한 실수
- `private` 데이터에 `public` 캐시 설정 -> 다른 사용자에게 데이터 유출
- 캐시 무효화 누락 -> 사용자가 수정해도 이전 데이터가 계속 보임
- Redis 캐시 TTL을 너무 길게 설정 -> 데이터 일관성 문제
- ETag 비교 시 따옴표(`"`) 포함 여부 불일치
- `stale-while-revalidate`를 모든 엔드포인트에 적용 -> 실시간 데이터에 부적절

## Connections

### FEEDS (1)

- → [[dev.performance.caching]] `w=0.5`
