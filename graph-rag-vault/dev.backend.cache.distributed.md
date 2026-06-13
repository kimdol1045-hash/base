---
id: "dev.backend.cache.distributed"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["cache", "distributed", "redis", "cluster"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.cache.distributed

> #215 Distributed Caching (Redis University, 2023)

# 분산 캐시 설계 가이드

## 핵심 원칙
- 분산 캐시는 여러 서버 인스턴스가 동일한 캐시 데이터를 공유한다
- Redis Cluster 또는 Memcached로 분산 캐시를 구현한다
- 캐시 노드 장애 시에도 서비스가 정상 동작하도록 설계한다
- 로컬 캐시(L1)와 분산 캐시(L2)를 조합하여 성능을 극대화한다

## DO
- 2단계 캐시를 구현한다: 로컬 메모리(L1) → Redis(L2) → DB
- Redis Cluster를 사용하여 자동 샤딩과 고가용성을 확보한다
- 캐시 연결 풀링을 설정하여 연결 오버헤드를 줄인다
- 직렬화 형식을 최적화한다 (MessagePack, Protocol Buffers)

## DON'T
- 캐시를 주 데이터 저장소로 사용하지 않는다
- 단일 Redis 인스턴스에 모든 데이터를 집중시키지 않는다
- 네트워크 지연을 무시하고 모든 데이터를 분산 캐시에 넣지 않는다
- L1 캐시의 일관성 문제를 무시하지 않는다

## 코드 예시
```typescript
import { LRUCache } from "lru-cache";
import Redis from "ioredis";

class TwoLevelCache {
  private l1 = new LRUCache<string, unknown>({
    max: 1000,
    ttl: 60_000, // 로컬 캐시 1분
  });
  private l2: Redis;

  constructor(redisUrl: string) {
    this.l2 = new Redis(redisUrl);
  }

  async get<T>(key: string): Promise<T | null> {
    // L1 조회
    const local = this.l1.get(key) as T | undefined;
    if (local !== undefined) return local;

    // L2 조회
    const remote = await this.l2.get(key);
    if (remote) {
      const parsed = JSON.parse(remote) as T;
      this.l1.set(key, parsed); // L1에 승격
      return parsed;
    }
    return null;
  }

  async set<T>(key: string, value: T, ttlSeconds: number): Promise<void> {
    this.l1.set(key, value);
    await this.l2.set(key, JSON.stringify(value), "EX", ttlSeconds);
  }

  async invalidate(key: string): Promise<void> {
    this.l1.delete(key);
    await this.l2.del(key);
    // 다른 인스턴스의 L1 무효화를 위해 이벤트 발행
    await this.l2.publish("cache:invalidate", key);
  }
}
```
