---
id: "dev.backend.testing.snapshot-testing"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["testing", "snapshot", "regression", "backend"]
brain_region: "BRAINSTEM"
token_estimate: 400
---

# dev.backend.testing.snapshot-testing

> #229 Snapshot Testing (Jest Documentation, Meta 2016)

# 스냅샷 테스트 가이드

## 핵심 원칙
- API 응답, 설정 파일, 직렬화된 데이터의 예상치 못한 변경을 감지한다
- 첫 실행 시 스냅샷을 생성하고, 이후 실행에서 비교한다
- 의도적 변경 시 스냅샷을 명시적으로 업데이트한다
- 스냅샷 파일을 버전 관리에 포함하여 코드 리뷰 시 변경 사항을 확인한다

## DO
- API 응답 구조의 변경 감지에 활용한다
- 스냅샷 업데이트는 PR 리뷰에서 변경 사유를 확인한다
- 날짜, ID 등 동적 값은 스냅샷 전에 고정(mock)한다
- 인라인 스냅샷을 짧은 데이터에 활용한다

## DON'T
- 거대한 객체를 통째로 스냅샷하지 않는다 (핵심 필드만 선택)
- 무의미하게 스냅샷을 업데이트(`-u`)하지 않는다 (변경 원인 확인)
- 동적 값(타임스탬프, UUID)을 포함한 스냅샷을 생성하지 않는다
- 스냅샷 테스트로 로직 검증을 대체하지 않는다

## 코드 예시
```typescript
import { describe, it, expect } from "vitest";

describe("User API 응답", () => {
  it("사용자 목록 응답 구조가 변경되지 않아야 한다", async () => {
    const response = await request(app).get("/api/v1/users");
    // 동적 값 제거
    const sanitized = response.body.data.map((user: any) => ({
      ...user,
      id: "[ID]",
      createdAt: "[DATE]",
    }));
    expect(sanitized).toMatchSnapshot();
  });

  it("에러 응답 형식이 일관되어야 한다", async () => {
    const response = await request(app).get("/api/v1/users/invalid");
    expect(response.body).toMatchInlineSnapshot(`
      {
        "error": {
          "code": "NOT_FOUND",
          "message": "사용자를 찾을 수 없습니다",
        },
      }
    `);
  });
});

// 스냅샷 업데이트 명령어
// npx vitest --update  (변경 원인 확인 후에만 실행)
```
