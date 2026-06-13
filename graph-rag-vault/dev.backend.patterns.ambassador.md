---
id: "dev.backend.patterns.ambassador"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["patterns", "ambassador", "proxy", "microservices"]
brain_region: "BRAINSTEM"
token_estimate: 400
---

# dev.backend.patterns.ambassador

> #223 Ambassador Pattern (Burns, Designing Distributed Systems 2018)

# Ambassador 패턴 가이드

## 핵심 원칙
- 애플리케이션 대신 외부 서비스와의 통신을 대리(proxy)하는 패턴이다
- 재시도, 로깅, 라우팅, 인증 등을 Ambassador가 처리한다
- 주 애플리케이션은 localhost로만 통신하여 외부 서비스의 복잡성을 감춘다
- Sidecar 패턴의 특수한 형태로, 네트워크 프록시 역할에 집중한다

## DO
- 외부 API 호출의 재시도, Circuit Breaker를 Ambassador에서 처리한다
- TLS 종료를 Ambassador에서 수행한다
- 요청/응답 로깅을 Ambassador 레벨에서 일괄 처리한다
- Ambassador를 통해 서비스 디스커버리를 추상화한다

## DON'T
- 단순한 직접 호출만 필요한 경우 Ambassador를 도입하지 않는다
- Ambassador에 비즈니스 로직을 넣지 않는다
- Ambassador의 지연시간 오버헤드를 무시하지 않는다
- 모든 서비스에 무조건 Ambassador를 적용하지 않는다

## 코드 예시
```typescript
// Ambassador 프록시 서버 (로컬 포트에서 실행)
import { Hono } from "hono";

const ambassador = new Hono();

// 외부 결제 API Ambassador
ambassador.all("/payment/*", async (c) => {
  const path = c.req.path.replace("/payment", "");
  const maxRetries = 3;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      const response = await fetch(`${PAYMENT_API_URL}${path}`, {
        method: c.req.method,
        headers: {
          "Authorization": `Bearer ${await getServiceToken()}`,
          "Content-Type": "application/json",
          "X-Request-Id": c.req.header("x-request-id") ?? generateId(),
        },
        body: c.req.method !== "GET" ? await c.req.text() : undefined,
        signal: AbortSignal.timeout(5_000),
      });

      // 로깅
      logger.info("외부 API 호출", {
        service: "payment", path, status: response.status, attempt,
      });

      if (response.ok || response.status < 500) {
        return c.json(await response.json(), response.status);
      }
    } catch (err) {
      logger.warn("외부 API 호출 실패", { attempt, error: err });
      if (attempt === maxRetries - 1) throw err;
      await sleep(1000 * Math.pow(2, attempt));
    }
  }
});

// 앱에서는 localhost로 호출
// fetch("http://localhost:9000/payment/charge", { ... })
```
