---
id: "dev.performance.caching"
domain: "development.performance"
type: "pattern"
bloom_level: ""
tags: ["performance", "caching", "redis", "http"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.performance.caching

> #102 HTTP Caching (Fielding, 1999)

캐싱 전략 (반복 요청의 비용을 줄인다):

### 캐시 레이어별 전략
| 레이어 | 도구 | TTL | 대상 |
|--------|------|-----|------|
| 브라우저 | Cache-Control | 1h~1y | 정적 에셋(JS/CSS/이미지) |
| CDN | CloudFlare/Vercel | 5m~1h | HTML, API 응답 |
| 서버 메모리 | Map/LRU | 1m~5m | 자주 조회되는 데이터 |
| Redis | Redis | 5m~1h | 세션, 인기 데이터, 계산 결과 |
| DB | 쿼리 캐시 | 자동 | 동일 쿼리 반복 |

### HTTP Cache-Control
```typescript
// 정적 에셋: 1년 캐시 + 해시 기반 무효화
// next.config.js가 자동 처리 (_next/static/*)

// API 응답: 상황별
// 공개 데이터 (제품 목록)
res.headers.set('Cache-Control', 'public, max-age=300, stale-while-revalidate=60');

// 개인 데이터 (프로필)
res.headers.set('Cache-Control', 'private, max-age=0, must-revalidate');

// 절대 캐시 금지 (결제, 인증)
res.headers.set('Cache-Control', 'no-store');
```

### Redis 캐싱 패턴
```typescript
async function getCachedOrFetch<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttlSeconds = 300,
): Promise<T> {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);

  const data = await fetcher();
  await redis.set(key, JSON.stringify(data), 'EX', ttlSeconds);
  return data;
}

// 사용
const products = await getCachedOrFetch(
  'products:popular',
  () => db.query('SELECT ... ORDER BY sales DESC LIMIT 20'),
  600,  // 10분
);
```

### 캐시 무효화 (가장 어려운 부분)
- 데이터 변경 시 관련 캐시 키 삭제
- 패턴: Write-through (쓰기 시 캐시 갱신) 또는 Cache-aside (삭제 후 다음 읽기 시 재생성)
- 절대 하지 말 것: 캐시만 업데이트하고 DB 미반영

## Connections

- [[dev.performance.role]] — REQUIRES (weight: 0.9)
- [[dev.performance.verify]] — FEEDS (weight: 0.8)
- [[dev.performance.web-vitals]] — FEEDS (weight: 0.7)
- [[dev.performance.budget]] — FEEDS (weight: 0.7)
- [[dev.performance.role]] — CO_CREATES (weight: 0.6)
- [[dev.performance.web-vitals]] — CO_CREATES (weight: 0.6)
- [[dev.performance.budget]] — CO_CREATES (weight: 0.6)
- [[dev.performance.amdahl]] — CO_CREATES (weight: 0.6)
- [[dev.performance.littles-law]] — CO_CREATES (weight: 0.6)
- [[dev.frontend.component.performance]] — FEEDS (weight: 0.5)
- [[dev.backend.api.caching]] — FEEDS (weight: 0.5)
