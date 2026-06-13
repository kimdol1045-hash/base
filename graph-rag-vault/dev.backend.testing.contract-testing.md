---
id: "dev.backend.testing.contract-testing"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["testing", "contract", "pact", "microservices"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.testing.contract-testing

> #228 Consumer-Driven Contract Testing (Pact Foundation, 2013)

# 계약 테스트(Contract Testing) 가이드

## 핵심 원칙
- 서비스 간 API 계약을 소비자(Consumer) 관점에서 검증한다
- 통합 테스트 없이도 서비스 간 호환성을 보장한다
- 소비자가 기대하는 요청/응답 형식을 계약으로 정의한다
- Provider가 계약을 만족하는지 독립적으로 검증한다

## DO
- Consumer-Driven 방식으로 소비자가 먼저 계약을 정의한다
- Pact 또는 Spring Cloud Contract를 활용한다
- CI/CD 파이프라인에 계약 검증을 포함한다
- 계약 변경 시 모든 소비자에게 알린다

## DON'T
- E2E 테스트를 계약 테스트 대신 사용하지 않는다 (느리고 불안정)
- 내부 구현 세부사항을 계약에 포함하지 않는다
- 계약 브로커(Pact Broker) 없이 파일로만 공유하지 않는다
- 모든 API 호출을 계약 테스트하지 않는다 (핵심 인터페이스만)

## 코드 예시
```typescript
// Consumer 측 계약 정의 (Pact)
import { PactV3, MatchersV3 } from "@pact-foundation/pact";
const { like, eachLike, string } = MatchersV3;

const provider = new PactV3({
  consumer: "OrderService",
  provider: "UserService",
});

describe("UserService 계약", () => {
  it("사용자 조회 API", async () => {
    await provider
      .given("사용자 ID=123이 존재함")
      .uponReceiving("GET /users/123 요청")
      .withRequest({ method: "GET", path: "/users/123" })
      .willRespondWith({
        status: 200,
        body: {
          data: {
            id: like("123"),
            email: string("user@example.com"),
            displayName: string("홍길동"),
          },
        },
      })
      .executeTest(async (mockServer) => {
        const client = new UserClient(mockServer.url);
        const user = await client.getById("123");
        expect(user.email).toBeDefined();
      });
  });
});

// Provider 측 검증
const { Verifier } = require("@pact-foundation/pact");
await new Verifier({
  providerBaseUrl: "http://localhost:3000",
  pactBrokerUrl: PACT_BROKER_URL,
  providerVersionBranch: "main",
  stateHandlers: {
    "사용자 ID=123이 존재함": async () => {
      await seedUser({ id: "123", email: "user@example.com" });
    },
  },
}).verifyProvider();
```
