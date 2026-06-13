---
id: "dev.backend.patterns.circuit-breaker"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "patterns", "circuit-breaker", "resilience"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.patterns.circuit-breaker

> #125 Release It! Stability Patterns

Circuit Breaker 패턴 (외부 서비스 장애가 내 시스템으로 전파되는 것을 차단한다):

### 3가지 상태
| 상태 | 동작 | 전환 조건 |
|------|------|-----------|
| Closed (정상) | 모든 요청 통과, 실패 횟수 카운트 | 실패 5회 → Open |
| Open (차단) | 즉시 fallback 반환, 요청 차단 | 30초 경과 → HalfOpen |
| HalfOpen (시험) | 1개 요청만 통과시켜 테스트 | 성공 → Closed, 실패 → Open |

### opossum 라이브러리 구현
```typescript
// DO: 외부 호출을 Circuit Breaker로 감싸고 fallback 제공
import CircuitBreaker from 'opossum';

const paymentBreaker = new CircuitBreaker(
  async (orderId: string) => {
    const res = await fetch('https://payment-api.com/charge', {
      method: 'POST',
      body: JSON.stringify({ orderId }),
      signal: AbortSignal.timeout(5000),  // 개별 요청 타임아웃
    });
    if (!res.ok) throw new Error(`Payment API: ${res.status}`);
    return res.json();
  },
  {
    timeout: 10000,           // 함수 실행 타임아웃 (10초)
    errorThresholdPercentage: 50,  // 50% 실패 시 Open
    resetTimeout: 30000,      // Open → HalfOpen 전환 시간 (30초)
    volumeThreshold: 5,       // 최소 5회 요청 후 판단
    rollingCountTimeout: 60000, // 1분 윈도우 내 집계
  }
);

// Fallback: 서킷 Open 시 대체 응답
paymentBreaker.fallback((orderId: string) => ({
  status: 'pending',
  message: '결제 서비스 일시 불가 — 잠시 후 자동 재시도됩니다.',
  orderId,
}));

// 모니터링 이벤트
paymentBreaker.on('open', () => logger.warn('Payment circuit OPEN'));
paymentBreaker.on('halfOpen', () => logger.info('Payment circuit HALF-OPEN'));
paymentBreaker.on('close', () => logger.info('Payment circuit CLOSED'));

// 사용
async function chargeOrder(orderId: string) {
  return paymentBreaker.fire(orderId);
}
```

DON'T:
```typescript
// ❌ Circuit Breaker 없이 외부 API 직접 호출 — 장애 전파
async function chargeOrder(orderId: string) {
  const res = await fetch('https://payment-api.com/charge', {
    method: 'POST',
    body: JSON.stringify({ orderId }),
    // 타임아웃 없음! 외부 서비스 응답 없으면 무한 대기
  });
  return res.json(); // 연쇄 실패로 내 서비스도 다운
}

// ❌ Fallback 없음 — 서킷 Open 시 사용자에게 500 에러만 반환
// ❌ 모든 에러를 동일 취급 — 4xx(클라이언트 오류)까지 서킷 카운트
```

### 적용 대상
- ✅ 필수: 외부 결제 API, 이메일 서비스, 서드파티 API
- ✅ 권장: 마이크로서비스 간 통신, DB 커넥션
- ❌ 불필요: 로컬 함수 호출, 인메모리 캐시

### 흔한 실수
- threshold가 너무 낮아(1회) 일시적 오류에도 서킷 Open
- resetTimeout이 너무 길어(5분) 서비스 복구 후에도 오래 차단
- 4xx 에러(잘못된 요청)를 서킷 실패로 카운트
- 서킷 상태를 모니터링/알림하지 않음

## Connections

- [[dev.backend.patterns.event-driven]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.cqrs]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.cap-theorem]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.twelve-factor]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.saga-pattern]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.conways-law]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.strangler-fig]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.retry-patterns]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.timeout-patterns]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.health-check]] — CO_CREATES (weight: 0.6)
- [[dev.backend.api.third-party]] — CO_CREATES (weight: 0.6)
