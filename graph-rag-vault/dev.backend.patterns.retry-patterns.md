---
id: "dev.backend.patterns.retry-patterns"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "patterns", "retry", "backoff", "resilience"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.patterns.retry-patterns

> #125 Release It! Stability Patterns

재시도 패턴 (일시적 장애를 자동 복구하되 시스템을 과부하하지 않는다):

### Exponential Backoff + Jitter 공식
`delay = min(base * 2^attempt + random(0, jitter), maxDelay)`

### 재시도 지연 테이블
| 시도 | 기본 지연 | + Jitter (0~1s) | 최대 제한 |
|------|-----------|-----------------|-----------|
| 1회 | 1s | 1.0~2.0s | — |
| 2회 | 2s | 2.0~3.0s | — |
| 3회 | 4s | 4.0~5.0s | — |
| 4회 | 8s | 8.0~9.0s | 10s (cap) |
| 최대 재시도: 3회 (총 4회 시도) |

### 구현
```typescript
// DO: exponential backoff + jitter, 재시도 가능 에러만 구분
interface RetryConfig {
  maxRetries: number;
  baseDelay: number;    // ms
  maxDelay: number;     // ms
  jitterMax: number;    // ms
}

const DEFAULT_RETRY: RetryConfig = {
  maxRetries: 3,
  baseDelay: 1000,
  maxDelay: 10000,
  jitterMax: 1000,
};

async function withRetry<T>(
  fn: () => Promise<T>,
  config: RetryConfig = DEFAULT_RETRY,
  isRetryable: (err: Error) => boolean = defaultRetryable,
): Promise<T> {
  let lastError: Error;
  for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err as Error;
      if (attempt === config.maxRetries || !isRetryable(lastError)) throw lastError;
      const delay = Math.min(
        config.baseDelay * Math.pow(2, attempt) + Math.random() * config.jitterMax,
        config.maxDelay,
      );
      await sleep(delay);
    }
  }
  throw lastError!;
}

// 재시도 가능 여부 판단
function defaultRetryable(err: Error): boolean {
  if (err instanceof HttpError) {
    // 5xx, 408(Timeout), 429(Too Many Requests)만 재시도
    return err.status >= 500 || err.status === 408 || err.status === 429;
  }
  // 네트워크 에러는 재시도
  return err.message.includes('ECONNRESET') || err.message.includes('ETIMEDOUT');
}

// 사용 예시
const result = await withRetry(
  () => externalApi.fetchData(id),
  { maxRetries: 3, baseDelay: 1000, maxDelay: 10000, jitterMax: 500 },
);
```

DON'T:
```typescript
// ❌ 고정 지연 — Thundering Herd 유발 (모든 클라이언트가 동시에 재시도)
async function retryFixed(fn: () => Promise<any>) {
  for (let i = 0; i < 10; i++) {  // ❌ 무한에 가까운 재시도
    try { return await fn(); }
    catch { await sleep(1000); }  // ❌ 고정 1초, jitter 없음
  }
}

// ❌ 비멱등 POST 요청을 무조건 재시도 — 중복 결제 발생!
await withRetry(() => fetch('/api/payments', { method: 'POST', body }));

// ❌ 모든 에러 재시도 — 400 Bad Request도 재시도 (의미 없음)
```

### 재시도 가능 vs 불가
| 재시도 가능 | 재시도 불가 |
|-------------|-------------|
| 503 Service Unavailable | 400 Bad Request |
| 429 Too Many Requests | 401 Unauthorized |
| 408 Request Timeout | 403 Forbidden |
| ECONNRESET, ETIMEDOUT | 404 Not Found |
| DB deadlock | 422 Validation Error |

### 흔한 실수
- 비멱등 연산(결제, 주문)에 Idempotency Key 없이 재시도
- maxRetries가 너무 높아(10+) 장애 지속 시 큐 적체
- Circuit Breaker와 함께 사용하지 않아 불필요한 재시도 반복

## Connections

- [[dev.backend.patterns.circuit-breaker]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.timeout-patterns]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.health-check]] — CO_CREATES (weight: 0.6)
