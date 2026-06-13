---
id: "dev.frontend.testing.interaction-testing"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "testing", "e2e", "playwright", "interaction"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.testing.interaction-testing

> #260 Interaction Testing (Playwright, Microsoft 2020)

# E2E 인터랙션 테스트 가이드

## 핵심 원칙
- 실제 브라우저에서 사용자 시나리오를 재현하여 검증한다
- 핵심 사용자 플로우(Critical User Journey)만 E2E로 테스트한다
- Playwright를 기본 도구로 사용한다
- 테스트 격리를 보장하고, 안정적으로 유지한다

## DO
- 로그인 → 주요 기능 → 로그아웃 같은 핵심 플로우를 테스트한다
- `page.getByRole()`, `page.getByText()` 등 사용자 중심 로케이터를 사용한다
- 테스트마다 독립적인 데이터를 생성한다
- `expect(locator).toBeVisible()`처럼 자동 대기하는 어서션을 사용한다

## DON'T
- 모든 기능을 E2E로 테스트하지 않는다 (느리고 비용이 크다)
- `page.waitForTimeout()`으로 고정 대기하지 않는다
- CSS 셀렉터로 요소를 찾지 않는다 (변경에 취약)
- 테스트 간 상태를 공유하지 않는다

## 코드 예시
```typescript
import { test, expect } from "@playwright/test";

test.describe("주문 플로우", () => {
  test.beforeEach(async ({ page }) => {
    // 테스트용 계정으로 로그인
    await page.goto("/login");
    await page.getByRole("textbox", { name: /이메일/i }).fill("test@test.com");
    await page.getByLabel(/비밀번호/i).fill("password123");
    await page.getByRole("button", { name: /로그인/i }).click();
    await expect(page).toHaveURL("/dashboard");
  });

  test("상품을 장바구니에 추가하고 주문할 수 있다", async ({ page }) => {
    // 1. 상품 페이지로 이동
    await page.goto("/products");
    await page.getByRole("heading", { name: "프리미엄 플랜" }).click();

    // 2. 장바구니에 추가
    await page.getByRole("button", { name: /장바구니/i }).click();
    await expect(page.getByRole("status")).toHaveText("장바구니에 추가되었습니다");

    // 3. 장바구니로 이동
    await page.getByRole("link", { name: /장바구니/i }).click();
    await expect(page.getByRole("row")).toHaveCount(1);

    // 4. 주문하기
    await page.getByRole("button", { name: /주문하기/i }).click();
    await page.getByLabel(/카드 번호/i).fill("4242424242424242");
    await page.getByRole("button", { name: /결제/i }).click();

    // 5. 주문 완료 확인
    await expect(page.getByRole("heading")).toHaveText("주문이 완료되었습니다");
  });
});
```
