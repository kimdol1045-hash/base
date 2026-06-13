---
id: "dev.backend.patterns.bulkhead"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["patterns", "bulkhead", "resilience", "isolation"]
brain_region: "BRAINSTEM"
token_estimate: 400
---

# dev.backend.patterns.bulkhead

> #221 Bulkhead Pattern (Nygard, Release It! 2007)

# Bulkhead 패턴 가이드

## 핵심 원칙
- 선박의 격벽처럼 시스템을 격리된 구획으로 나누어 장애 전파를 방지한다
- 하나의 서비스/기능 장애가 전체 시스템에 영향을 미치지 않도록 한다
- 리소스 풀(스레드, 커넥션, 메모리)을 기능별로 분리한다
- Circuit Breaker와 함께 사용하면 효과가 극대화된다

## DO
- HTTP 클라이언트 연결 풀을 서비스별로 분리한다
- DB 커넥션 풀을 읽기/쓰기, 중요도별로 분리한다
- 큐 워커를 작업 유형별로 분리한다
- 각 격벽의 리소스 사용량을 모니터링한다

## DON'T
- 모든 외부 서비스 호출에 동일한 HTTP 클라이언트를 공유하지 않는다
- 격벽을 너무 세분화하여 리소스를 낭비하지 않는다
- 격벽 크기를 정적으로만 설정하지 않는다 (동적 조절 고려)
- 격벽 간 의존성을 만들지 않는다

## 코드 예시
```typescript
import { Agent } from "undici";

// 서비스별 HTTP 클라이언트 격벽
const paymentClient = new Agent({
  connect: { timeout: 5_000 },
  connections: 20,      // 결제 서비스 전용 20개 커넥션
  pipelining: 1,
});

const notificationClient = new Agent({
  connect: { timeout: 10_000 },
  connections: 5,       // 알림 서비스 전용 5개 커넥션
  pipelining: 1,
});

// DB 커넥션 풀 격벽
const criticalPool = createPool({ max: 30, connectionString: DB_URL });
const analyticsPool = createPool({ max: 10, connectionString: DB_URL });

// 사용: 결제 장애가 알림 서비스에 영향을 주지 않음
async function processPayment(data: PaymentInput) {
  return fetch(PAYMENT_URL, { dispatcher: paymentClient, /* ... */ });
}

async function sendNotification(data: NotificationInput) {
  return fetch(NOTIFICATION_URL, { dispatcher: notificationClient, /* ... */ });
}
```
