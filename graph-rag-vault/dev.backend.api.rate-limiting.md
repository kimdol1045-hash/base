---
id: "dev.backend.api.rate-limiting"
domain: "development.backend"
type: "rule"
bloom_level: ""
tags: ["backend", "api", "rate-limiting", "redis", "security", "throttling"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.api.rate-limiting

> #115 Saltzer Least Privilege

Rate Limiting 전략 (모든 엔드포인트는 요청 한도가 있어야 한다 -- 제한 없는 API는 남용의 초대장이다):

### 알고리즘 비교
| 알고리즘 | 장점 | 단점 | 사용 시점 |
|----------|------|------|-----------|
| Token Bucket | 버스트 허용, 평균 속도 제어 | 구현 복잡 | 일반 API |
| Sliding Window Counter | 정확한 윈도우, 경계 문제 없음 | 메모리 사용 높음 | 인증 엔드포인트 |
| Fixed Window | 구현 간단 | 윈도우 경계 버스트 | 간단한 제한 |
| Leaky Bucket | 일정한 처리 속도 | 버스트 불허 | 외부 API 호출 |

### 엔드포인트별 제한 기준
| 엔드포인트 | 제한 | 키 | 이유 |
|------------|------|----|------|
| POST /auth/login | 5/min | IP | 브루트포스 방지 |
| POST /auth/register | 3/min | IP | 스팸 계정 방지 |
| POST /auth/forgot-password | 3/hour | IP+Email | 이메일 폭탄 방지 |
| GET /api/* (인증) | 100/min | User ID | 남용 방지 |
| GET /api/* (비인증) | 30/min | IP | 스크래핑 방지 |
| POST /api/search | 30/min | User ID | 검색 남용 방지 |
| POST /api/uploads | 5/min | User ID | 스토리지 남용 방지 |

DO:
```typescript
// Redis 기반 Sliding Window Counter (Lua 스크립트로 원자성 보장)
const SLIDING_WINDOW_SCRIPT = `
  local key = KEYS[1]
  local now = tonumber(ARGV[1])
  local window = tonumber(ARGV[2])
  local limit = tonumber(ARGV[3])

  -- 윈도우 밖의 오래된 요청 제거
  redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
  -- 현재 윈도우 내 요청 수 확인
  local count = redis.call('ZCARD', key)

  if count < limit then
    -- 요청 허용: 현재 타임스탬프 추가
    redis.call('ZADD', key, now, now .. '-' .. math.random(1000000))
    redis.call('EXPIRE', key, window / 1000)
    return {1, limit - count - 1}  -- {허용, 남은 횟수}
  else
    return {0, 0}  -- {거부, 남은 횟수 0}
  end
`;

async function checkRateLimit(
  key: string,
  limit: number,
  windowMs: number,
): Promise<{ allowed: boolean; remaining: number }> {
  const now = Date.now();
  const [allowed, remaining] = await redis.eval(
    SLIDING_WINDOW_SCRIPT, 1, key, now, windowMs, limit,
  ) as [number, number];

  return { allowed: allowed === 1, remaining };
}

// 미들웨어로 적용
function rateLimitMiddleware(config: { limit: number; windowMs: number; keyPrefix: string }) {
  return async (c: Context, next: Next) => {
    const identifier = c.get("userId") ?? c.req.header("x-forwarded-for") ?? "unknown";
    const key = `ratelimit:${config.keyPrefix}:${identifier}`;
    const { allowed, remaining } = await checkRateLimit(key, config.limit, config.windowMs);

    // 표준 Rate Limit 헤더 설정
    c.header("X-RateLimit-Limit", String(config.limit));
    c.header("X-RateLimit-Remaining", String(remaining));
    c.header("X-RateLimit-Reset", String(Math.ceil(Date.now() / 1000) + config.windowMs / 1000));

    if (!allowed) {
      c.header("Retry-After", String(Math.ceil(config.windowMs / 1000)));
      return c.json({
        error: { code: "RATE_LIMITED", message: "요청 한도를 초과했습니다" }
      }, 429);
    }

    await next();
  };
}

// 엔드포인트 적용
app.post("/auth/login", rateLimitMiddleware({ limit: 5, windowMs: 60_000, keyPrefix: "login" }), loginHandler);
app.use("/api/*", rateLimitMiddleware({ limit: 100, windowMs: 60_000, keyPrefix: "api" }));
```

DON'T:
```typescript
// ❌ 인메모리 Rate Limiting -- 분산 환경에서 서버별 독립 카운트
const requestCounts = new Map<string, number>();  // 서버 재시작 시 초기화, 서버 간 공유 불가

// ❌ IP만으로 제한 -- 프록시/NAT 뒤의 사용자 전체가 차단됨
const key = c.req.header("x-forwarded-for");  // 같은 IP의 다른 사용자도 차단

// ❌ Rate Limit 헤더 미제공 -- 클라이언트가 남은 횟수를 알 수 없음
if (!allowed) return c.json({ error: "Too many requests" }, 429);
// X-RateLimit-* 헤더 없이 429만 반환

// ❌ Redis 없이 Fixed Window만 사용 -- 윈도우 경계에서 2배 버스트 가능
// 59초에 100회 + 61초에 100회 = 2초 동안 200회 통과
```

### 흔한 실수
- x-forwarded-for 헤더를 스푸핑 가능한 환경에서 신뢰 -> 프록시 설정 확인 필수
- Rate Limit을 인증 미들웨어 뒤에 배치 -> 인증 전 엔드포인트(로그인)가 보호되지 않음
- 429 응답에 Retry-After 헤더 미포함 -> 클라이언트가 즉시 재시도하여 상황 악화
- 관리자 API에 Rate Limit 미적용 -> 탈취된 관리자 토큰으로 무제한 요청 가능
- 분산 환경에서 각 서버가 독립적으로 카운트 -> Redis 중앙 집중식 저장소 필수

## Connections

- [[dev.backend.api.verify]] — FEEDS (weight: 0.8)
- [[dev.backend.patterns.rag-pattern]] — FEEDS (weight: 0.7)
- [[dev.backend.api.caching]] — FEEDS (weight: 0.7)
