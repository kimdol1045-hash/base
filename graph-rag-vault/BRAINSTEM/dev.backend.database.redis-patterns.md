---
id: "dev.backend.database.redis-patterns"
domain: "development.database"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#108 CAP Theorem (Brewer, 2000)"
tags: [database, redis, caching, pubsub, distributed-lock, sorted-set, session]
---

# dev.backend.database.redis-patterns

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.database`  
> **Type**: `pattern`  
> **Theory**: #108 CAP Theorem (Brewer, 2000)  
> **Tokens**: 500

## Content

Redis 고급 패턴 (캐싱, 실시간 통신, 분산 락을 위한 인메모리 데이터 구조):

### 1. Cache-Aside 패턴
읽기 시 캐시 확인 → miss면 DB 조회 → 캐시 저장. 쓰기 시 DB 갱신 → 캐시 삭제.

DO:
```typescript
// ✅ Cache-Aside with TTL
async function getUser(id: string): Promise<User> {
  const cached = await redis.get(`user:${id}`);
  if (cached) return JSON.parse(cached);

  const user = await db.user.findUnique({ where: { id } });
  if (user) {
    await redis.set(`user:${id}`, JSON.stringify(user), "EX", 3600); // TTL 1시간
  }
  return user;
}

// ✅ 쓰기 시 캐시 무효화 (Write-Through 아님)
async function updateUser(id: string, data: UpdateUserDto) {
  const user = await db.user.update({ where: { id }, data });
  await redis.del(`user:${id}`);  // 캐시 삭제 (갱신 아님)
  return user;
}
```

### 2. Pub/Sub — 실시간 이벤트 브로드캐스트
```typescript
// ✅ 채널 기반 Pub/Sub (1:N 브로드캐스트)
const subscriber = redis.duplicate();
await subscriber.subscribe("notifications:user:123");
subscriber.on("message", (channel, message) => {
  const event = JSON.parse(message);
  ws.send(event); // WebSocket으로 전달
});

// Publisher
await redis.publish("notifications:user:123", JSON.stringify({
  type: "NEW_MESSAGE",
  payload: { from: "alice", text: "Hello" },
}));
```

### 3. Sorted Set — 리더보드, 랭킹
```typescript
// ✅ 리더보드: O(log N) 삽입, O(log N + M) 범위 조회
await redis.zadd("leaderboard:weekly", score, `user:${userId}`);

// 상위 10명 조회 (높은 점수순)
const top10 = await redis.zrevrange("leaderboard:weekly", 0, 9, "WITHSCORES");

// 특정 유저 순위 조회 (0-based)
const rank = await redis.zrevrank("leaderboard:weekly", `user:${userId}`);
```

### 4. 분산 락 (Redlock 알고리즘)
DO:
```typescript
// ✅ SET NX + EX 로 원자적 락 획득 (단일 인스턴스)
const lockKey = `lock:order:${orderId}`;
const lockValue = crypto.randomUUID(); // 소유권 식별
const acquired = await redis.set(lockKey, lockValue, "NX", "EX", 30); // 30초 TTL

if (acquired) {
  try {
    await processOrder(orderId);
  } finally {
    // ✅ Lua 스크립트로 원자적 해제 (소유자만 해제)
    await redis.eval(
      `if redis.call("get", KEYS[1]) == ARGV[1] then
         return redis.call("del", KEYS[1])
       end return 0`,
      1, lockKey, lockValue
    );
  }
}
```

### 5. 세션 스토어
- TTL: 30분 (sliding window), `EXPIRE` 갱신
- Hash 타입으로 필드별 접근: `HSET session:abc userId "123" role "admin"`
- 최대 메모리 정책: `maxmemory-policy allkeys-lru`

DON'T:
```typescript
// ❌ KEYS * 프로덕션 사용 — O(N) 전체 스캔, 블로킹
const allKeys = await redis.keys("user:*"); // 서버 멈춤 위험

// ❌ TTL 없는 캐시 — 메모리 무한 증가
await redis.set(`user:${id}`, JSON.stringify(user)); // TTL 미설정

// ❌ 단일 Redis로 Redlock — 최소 5개 독립 인스턴스 필요
// 단일 인스턴스 장애 시 락 보장 불가 (CP 위반)
```

### 운영 수치
- 단일 인스턴스 처리량: ~100,000 ops/sec (GET/SET)
- Pub/Sub 지연: < 1ms (같은 인스턴스)
- 권장 최대 키 크기: 512MB (실무 1MB 이하 권장)
- Cluster 최소 구성: 3 master + 3 replica
