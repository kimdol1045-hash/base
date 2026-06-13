---
id: "dev.backend.queue.retry-strategy"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["queue", "retry", "backoff", "reliability"]
brain_region: "BRAINSTEM"
token_estimate: 400
---

# dev.backend.queue.retry-strategy

> #212 Exponential Backoff and Retry (AWS Architecture Blog, 2015)

# 메시지 재시도 전략 가이드

## 핵심 원칙
- 지수 백오프(Exponential Backoff)를 기본 재시도 전략으로 사용한다
- 지터(Jitter)를 추가하여 동시 재시도로 인한 부하 집중을 방지한다
- 재시도 가능한 에러와 불가능한 에러를 구분한다
- 최대 재시도 횟수를 반드시 설정한다

## DO
- 일시적 에러(네트워크, 타임아웃, 429)만 재시도한다
- 재시도 간격: `min(baseDelay * 2^attempt + jitter, maxDelay)`
- 재시도 횟수를 메시지 메타데이터에 기록한다
- Circuit Breaker와 조합하여 연쇄 실패를 방지한다

## DON'T
- 400 Bad Request 같은 클라이언트 에러를 재시도하지 않는다
- 고정 간격 재시도를 사용하지 않는다 (Thundering Herd 유발)
- 최대 재시도 없이 무한 재시도를 설정하지 않는다
- 재시도 중 원본 메시지를 변형하지 않는다

## 코드 예시
```typescript
interface RetryConfig {
  maxRetries: number;
  baseDelayMs: number;
  maxDelayMs: number;
  retryableErrors: string[];
}

const DEFAULT_CONFIG: RetryConfig = {
  maxRetries: 5,
  baseDelayMs: 1000,
  maxDelayMs: 60_000,
  retryableErrors: ["NETWORK_ERROR", "TIMEOUT", "RATE_LIMITED", "SERVICE_UNAVAILABLE"],
};

function calculateDelay(attempt: number, config: RetryConfig): number {
  const exponentialDelay = config.baseDelayMs * Math.pow(2, attempt);
  const jitter = Math.random() * config.baseDelayMs;
  return Math.min(exponentialDelay + jitter, config.maxDelayMs);
}

function isRetryable(error: AppError, config: RetryConfig): boolean {
  return config.retryableErrors.includes(error.code);
}

async function processWithRetry<T>(
  handler: () => Promise<T>,
  config = DEFAULT_CONFIG,
): Promise<T> {
  for (let attempt = 0; attempt <= config.maxRetries; attempt++) {
    try {
      return await handler();
    } catch (error) {
      if (attempt === config.maxRetries || !isRetryable(error, config)) throw error;
      await sleep(calculateDelay(attempt, config));
    }
  }
  throw new Error("Unreachable");
}
```
