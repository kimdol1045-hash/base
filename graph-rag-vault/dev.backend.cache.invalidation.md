---
id: "dev.backend.cache.invalidation"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["cache", "invalidation", "consistency", "backend"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.cache.invalidation

> #214 Cache Invalidation (Phil Karlton, 'Two Hard Things in CS')

# 캐시 무효화 가이드

## 핵심 원칙
- 캐시 무효화는 캐싱에서 가장 어려운 문제이다
- 데이터 변경 시 관련된 모든 캐시 키를 식별하고 무효화한다
- 태그 기반 무효화로 관련 캐시를 그룹으로 관리한다
- 무효화 실패에 대비하여 TTL을 안전장치로 설정한다

## DO
- 쓰기 작업 후 해당 엔티티 관련 캐시를 즉시 삭제한다
- 캐시 키에 버전을 포함하여 스키마 변경 시 자동 무효화한다
- 태그 기반 캐시 그룹핑으로 관련 캐시를 일괄 무효화한다
- 이벤트 기반 무효화를 구현하여 서비스 간 캐시 일관성을 유지한다

## DON'T
- 캐시 무효화를 누락하여 stale 데이터가 노출되도록 하지 않는다
- 전체 캐시를 flush하는 방식으로 무효화하지 않는다
- 캐시 삭제 실패를 무시하지 않는다
- 복잡한 캐시 의존성 그래프를 만들지 않는다

## 코드 예시
```typescript
// 태그 기반 캐시 무효화
class TaggedCache {
  async set(key: string, value: unknown, tags: string[], ttl: number) {
    await redis.set(key, JSON.stringify(value), "EX", ttl);
    for (const tag of tags) {
      await redis.sadd(`tag:${tag}`, key);
    }
  }

  async invalidateByTag(tag: string) {
    const keys = await redis.smembers(`tag:${tag}`);
    if (keys.length > 0) {
      await redis.del(...keys);
    }
    await redis.del(`tag:${tag}`);
  }
}

// 사용 예: 사용자 수정 시 관련 캐시 모두 무효화
async function updateUser(id: string, data: UpdateUserInput) {
  const user = await db.users.update(id, data);
  await taggedCache.invalidateByTag(`user:${id}`);
  // user:123 태그가 붙은 모든 캐시가 삭제됨
  // 예: user:123:profile, user:123:posts, team:456:members 등
  return user;
}

// 캐시 저장 시 태그 지정
await taggedCache.set(
  `user:${id}:profile`, profile,
  [`user:${id}`, `team:${profile.teamId}`],
  3600,
);
```
