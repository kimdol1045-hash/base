---
id: "dev.backend.cache.strategy"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["cache", "strategy", "performance", "backend"]
brain_region: "BRAINSTEM"
token_estimate: 430
---

# dev.backend.cache.strategy

> #213 Caching Strategies (Martin Fowler, Patterns of Enterprise Application Architecture 2002)

# 캐시 전략 가이드

## 핵심 원칙
- 읽기가 쓰기보다 압도적으로 많은 데이터에 캐시를 적용한다
- 캐시 전략은 데이터 특성에 따라 선택한다
- TTL(Time To Live)을 반드시 설정하여 stale 데이터를 방지한다
- 캐시 히트율을 모니터링하여 효과를 검증한다

## 주요 캐시 전략
| 전략 | 설명 | 적합한 경우 |
|------|------|-------------|
| Cache-Aside | 앱이 캐시 관리, 미스 시 DB 조회 후 캐시 저장 | 범용, 읽기 많은 워크로드 |
| Write-Through | 쓰기 시 캐시+DB 동시 업데이트 | 일관성이 중요한 경우 |
| Write-Behind | 쓰기 시 캐시만 업데이트, 비동기로 DB 반영 | 쓰기 성능이 중요한 경우 |
| Read-Through | 캐시가 DB 조회를 대행 | ORM/프레임워크 통합 시 |

## DO
- Cache-Aside 패턴을 기본으로 사용한다
- 캐시 키를 일관된 네이밍 규칙으로 설계한다
- TTL에 약간의 랜덤값을 추가하여 동시 만료(Cache Stampede)를 방지한다
- 캐시 히트율 메트릭을 수집한다

## DON'T
- 자주 변경되는 데이터를 긴 TTL로 캐시하지 않는다
- 캐시에만 존재하는 데이터를 만들지 않는다 (캐시는 언제든 사라질 수 있다)
- 캐시 실패 시 전체 서비스가 중단되도록 하지 않는다
- 모든 데이터를 무조건 캐시하지 않는다

## 코드 예시
```typescript
// Cache-Aside 패턴
async function getUserById(id: string): Promise<User> {
  const cacheKey = `user:${id}`;
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  const user = await db.users.findById(id);
  if (user) {
    const ttl = 3600 + Math.floor(Math.random() * 300); // TTL jitter
    await redis.set(cacheKey, JSON.stringify(user), "EX", ttl);
  }
  return user;
}
```
