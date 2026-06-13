---
id: "dev.backend.testing.api-testing"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["testing", "api", "integration", "supertest"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.testing.api-testing

> #232 API Testing Pyramid (Cohn, Succeeding with Agile 2009)

# API 통합 테스트 가이드

## 핵심 원칙
- API 테스트는 HTTP 레벨에서 엔드포인트의 전체 동작을 검증한다
- 인증, 유효성 검사, 비즈니스 로직, 에러 처리를 모두 포함한다
- 실제 서버를 시작하여 E2E에 가까운 테스트를 수행한다
- 외부 서비스는 Mock하되, DB는 실제 사용한다

## DO
- 각 엔드포인트의 성공/실패 케이스를 모두 테스트한다
- 인증 토큰을 테스트 헬퍼로 자동 생성한다
- 응답 스키마(status code, 구조)를 검증한다
- 사이드 이펙트(DB 변경, 이벤트 발행)를 확인한다

## DON'T
- 테스트 간 상태를 공유하지 않는다 (각 테스트가 독립적)
- 구현 세부사항(내부 함수 호출)을 테스트하지 않는다
- 테스트에서 실제 외부 API를 호출하지 않는다
- 하드코딩된 포트를 사용하지 않는다

## 코드 예시
```typescript
import { describe, it, expect, beforeAll, afterAll } from "vitest";
import request from "supertest";
import { createApp } from "../src/app";

let app: Express;
let authToken: string;

beforeAll(async () => {
  app = await createApp({ database: testDb });
  const admin = await createUser({ role: "admin" });
  authToken = await generateTestToken(admin.id);
});

describe("POST /api/v1/users", () => {
  it("유효한 데이터로 사용자를 생성한다", async () => {
    const res = await request(app)
      .post("/api/v1/users")
      .set("Authorization", `Bearer ${authToken}`)
      .send({ email: "new@test.com", displayName: "신규" });

    expect(res.status).toBe(201);
    expect(res.body.data).toMatchObject({
      email: "new@test.com",
      displayName: "신규",
    });

    // DB에 실제로 저장되었는지 확인
    const user = await testDb.users.findByEmail("new@test.com");
    expect(user).toBeDefined();
  });

  it("중복 이메일은 409를 반환한다", async () => {
    await createUser({ email: "dup@test.com" });
    const res = await request(app)
      .post("/api/v1/users")
      .set("Authorization", `Bearer ${authToken}`)
      .send({ email: "dup@test.com", displayName: "중복" });

    expect(res.status).toBe(409);
    expect(res.body.error.code).toBe("ALREADY_EXISTS");
  });

  it("인증 없이 요청하면 401을 반환한다", async () => {
    const res = await request(app)
      .post("/api/v1/users")
      .send({ email: "no-auth@test.com" });

    expect(res.status).toBe(401);
  });
});
```
