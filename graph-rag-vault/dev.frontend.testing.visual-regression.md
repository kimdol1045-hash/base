---
id: "dev.frontend.testing.visual-regression"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "testing", "visual-regression", "screenshot"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.testing.visual-regression

> #257 Visual Regression Testing (Chromatic, Storybook 2019)

# 비주얼 리그레션 테스트 가이드

## 핵심 원칙
- UI의 시각적 변화를 스크린샷 비교로 자동 감지한다
- 의도치 않은 스타일 변경이나 레이아웃 깨짐을 방지한다
- Playwright 또는 Chromatic으로 구현한다
- CI에서 자동으로 실행하고 PR에 결과를 첨부한다

## DO
- 주요 페이지와 핵심 컴포넌트에 비주얼 테스트를 적용한다
- 다양한 뷰포트 크기(모바일, 태블릿, 데스크탑)에서 캡처한다
- 다크 모드/라이트 모드 양쪽을 테스트한다
- 동적 콘텐츠(날짜, 랜덤 데이터)를 고정하여 안정적인 스냅샷을 확보한다

## DON'T
- 모든 컴포넌트에 비주얼 테스트를 적용하지 않는다 (핵심 UI만)
- 애니메이션이 진행 중인 상태를 캡처하지 않는다
- 외부 리소스(이미지, 폰트) 로딩을 기다리지 않고 캡처하지 않는다
- 허용 임계값(threshold)을 너무 민감하게 설정하지 않는다

## 코드 예시
```typescript
// Playwright 비주얼 리그레션 테스트
import { test, expect } from "@playwright/test";

test.describe("랜딩 페이지 비주얼", () => {
  test.beforeEach(async ({ page }) => {
    // 동적 콘텐츠 고정
    await page.clock.setFixedTime(new Date("2024-01-15T10:00:00"));
  });

  const viewports = [
    { name: "mobile", width: 375, height: 812 },
    { name: "tablet", width: 768, height: 1024 },
    { name: "desktop", width: 1440, height: 900 },
  ];

  for (const vp of viewports) {
    test(`히어로 섹션 - ${vp.name}`, async ({ page }) => {
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await page.goto("/");
      await page.waitForLoadState("networkidle");

      await expect(page.locator("[data-testid=hero]")).toHaveScreenshot(
        `hero-${vp.name}.png`,
        { maxDiffPixelRatio: 0.01 },
      );
    });
  }

  test("다크 모드", async ({ page }) => {
    await page.emulateMedia({ colorScheme: "dark" });
    await page.goto("/");
    await expect(page).toHaveScreenshot("landing-dark.png");
  });
});
```
