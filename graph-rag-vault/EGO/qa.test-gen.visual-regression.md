---
id: "qa.test-gen.visual-regression"
domain: "qa"
type: "pattern"
region: EGO
token_estimate: 490
theory: "#33 Aesthetic-Usability Effect"
tags: [qa, test, visual-regression, screenshot, playwright, chromatic]
---

# qa.test-gen.visual-regression

> **Region**: 🔵 [[EGO]]  
> **Domain**: `qa`  
> **Type**: `pattern`  
> **Theory**: #33 Aesthetic-Usability Effect  
> **Tokens**: 490

## Content

시각적 회귀 테스트 (UI의 의도치 않은 시각적 변경을 감지한다):

### 이론 배경
Aesthetic-Usability Effect: 시각적으로 보기 좋은 디자인이 더 사용하기 쉽다고 인지된다.
→ 시각적 회귀는 사용성 인식에 직접 영향을 미치므로 자동 감지가 필수적이다.

### Playwright 스크린샷 비교
```typescript
import { test, expect } from '@playwright/test';

// DO: 핵심 페이지를 주요 브레이크포인트에서 검증
const breakpoints = [
  { name: 'mobile', width: 375, height: 812 },
  { name: 'tablet', width: 768, height: 1024 },
  { name: 'desktop', width: 1440, height: 900 },
];

for (const bp of breakpoints) {
  test(`홈페이지 — ${bp.name}`, async ({ page }) => {
    await page.setViewportSize({ width: bp.width, height: bp.height });
    await page.goto('/');

    // 동적 콘텐츠 안정화
    await page.evaluate(() => {
      document.querySelectorAll('[data-animated]')
        .forEach(el => el.style.animation = 'none');
    });

    // DO: 0.1% 픽셀 차이 허용 (안티앨리어싱, 폰트 렌더링 차이)
    await expect(page).toHaveScreenshot(`home-${bp.name}.png`, {
      maxDiffPixelRatio: 0.001,
      animations: 'disabled',
    });
  });
}
```

### 동적 콘텐츠 Mocking
```typescript
// DO: 날짜, 광고, 랜덤 콘텐츠는 mock 처리
test('대시보드 스크린샷', async ({ page }) => {
  // 시간 고정
  await page.clock.setFixedTime(new Date('2024-01-15T09:00:00'));

  // API 응답 고정
  await page.route('/api/dashboard', (route) => {
    route.fulfill({
      status: 200,
      body: JSON.stringify(fixedDashboardData),
    });
  });

  await page.goto('/dashboard');
  await expect(page).toHaveScreenshot('dashboard.png', {
    maxDiffPixelRatio: 0.001,
  });
});
```

### Chromatic + Storybook
```typescript
// .storybook/main.ts
// Chromatic은 Storybook 스토리를 자동으로 스크린샷 비교
// 장점: 컴포넌트 단위 시각적 테스트, 브라우저 환경 일관성

// 스토리별 threshold 설정
export const Primary: Story = {
  parameters: {
    chromatic: {
      diffThreshold: 0.063, // 6.3% 허용 (애니메이션 있는 컴포넌트)
      viewports: [375, 768, 1440],
    },
  },
};

// 특정 스토리 제외
export const Animated: Story = {
  parameters: {
    chromatic: { disableSnapshot: true },
  },
};
```

DON'T:
```typescript
// ❌ 픽셀 퍼펙트 비교 (0% 차이 허용) → 환경 차이로 항상 실패
await expect(page).toHaveScreenshot('home.png', {
  maxDiffPixelRatio: 0, // 안티앨리어싱만으로도 실패
});

// ❌ 동적 콘텐츠 mock 없이 스크린샷 → 매번 달라서 항상 실패
await page.goto('/feed'); // 실시간 피드 → 매번 다른 콘텐츠
await expect(page).toHaveScreenshot('feed.png');

// ❌ 전체 페이지 스크린샷만 (특정 컴포넌트 변경 추적 불가)
// → 핵심 컴포넌트별 개별 스크린샷도 추가
```

### CI 워크플로우
- PR마다 자동 스크린샷 비교 실행
- 차이 발생 시 PR 코멘트에 diff 이미지 첨부
- 의도된 변경: baseline 업데이트 (`npx playwright test --update-snapshots`)
- 검증 대상: 핵심 5-10 페이지 × 3 브레이크포인트 = 15-30 스크린샷
