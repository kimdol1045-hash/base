---
id: "dev.frontend.testing.accessibility-testing"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "testing", "accessibility", "a11y", "wcag"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.testing.accessibility-testing

> #259 Web Accessibility Testing (WCAG 2.1, W3C 2018)

# 접근성(Accessibility) 테스트 가이드

## 핵심 원칙
- WCAG 2.1 AA 수준을 최소 준수 기준으로 한다
- 자동 검사와 수동 검사를 병행한다 (자동 검사는 30% 정도만 커버)
- 키보드 네비게이션, 스크린리더 호환성을 필수 검증한다
- CI에서 자동 접근성 검사를 실행한다

## DO
- `axe-core`를 테스트 파이프라인에 통합한다
- 시맨틱 HTML 요소를 사용한다 (div 대신 button, nav, main)
- 모든 이미지에 의미 있는 alt 텍스트를 제공한다
- 색상 대비를 4.5:1 이상으로 유지한다
- 키보드 탭 순서가 논리적인지 확인한다

## DON'T
- `div`에 onClick을 직접 달지 않는다 (button 사용)
- aria 속성을 잘못 사용하는 것보다 안 쓰는 게 낫다
- 자동 테스트 통과만으로 접근성을 보장한다고 판단하지 않는다
- 포커스 아웃라인(outline)을 제거하지 않는다

## 코드 예시
```tsx
// vitest + axe-core 접근성 테스트
import { render } from "@testing-library/react";
import { axe, toHaveNoViolations } from "jest-axe";

expect.extend(toHaveNoViolations);

describe("LoginForm 접근성", () => {
  it("접근성 위반이 없어야 한다", async () => {
    const { container } = render(<LoginForm onSubmit={vi.fn()} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
```

```typescript
// Playwright 접근성 테스트
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("홈페이지 접근성", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page })
    .withTags(["wcag2a", "wcag2aa"])
    .analyze();

  expect(results.violations).toEqual([]);
});

// 키보드 네비게이션 테스트
test("탭 순서가 올바르다", async ({ page }) => {
  await page.goto("/login");
  await page.keyboard.press("Tab");
  await expect(page.getByRole("textbox", { name: /이메일/i })).toBeFocused();
  await page.keyboard.press("Tab");
  await expect(page.getByLabelText(/비밀번호/i)).toBeFocused();
  await page.keyboard.press("Tab");
  await expect(page.getByRole("button", { name: /로그인/i })).toBeFocused();
});
```
