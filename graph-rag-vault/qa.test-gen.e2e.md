---
id: "qa.test-gen.e2e"
domain: "qa"
type: "pattern"
bloom_level: ""
tags: ["qa", "test", "e2e", "playwright", "page-object-model"]
brain_region: "CEREBELLUM"
token_estimate: 480
---

# qa.test-gen.e2e

> #126 Testing Trophy (Dodds, 2019)

E2E 테스트 (사용자 관점에서 전체 시스템의 핵심 경로를 검증한다):

### Testing Trophy에서의 E2E 위치
단위 < 통합 < **E2E** (피라미드 최상단)
E2E는 수가 적되, 핵심 사용자 여정(Critical Path)만 집중한다.

### Page Object Model (POM)
```typescript
// DO: POM으로 페이지 로직 캡슐화
class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto('/login');
  }

  async login(email: string, password: string) {
    await this.page.getByLabel('이메일').fill(email);
    await this.page.getByLabel('비밀번호').fill(password);
    await this.page.getByRole('button', { name: '로그인' }).click();
  }

  async expectError(message: string) {
    await expect(this.page.getByRole('alert')).toHaveText(message);
  }
}
```

### Critical Path 테스트 (로그인→행동→검증)
```typescript
import { test, expect } from '@playwright/test';

test.describe('주문 플로우', () => {
  test('로그인 → 상품 추가 → 결제 완료', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('user@test.com', 'password123');

    // 상품 추가
    await page.getByRole('link', { name: '상품 목록' }).click();
    await page.getByRole('button', { name: '장바구니 추가' }).first().click();
    await expect(page.getByTestId('cart-count')).toHaveText('1');

    // 결제
    await page.getByRole('link', { name: '장바구니' }).click();
    await page.getByRole('button', { name: '결제하기' }).click();
    await expect(page.getByText('주문 완료')).toBeVisible();
  });
});
```

### 테스트 격리 (Fixtures)
```typescript
// DO: fixture로 테스트 데이터 격리
test.beforeEach(async ({ page, request }) => {
  // API로 테스트 데이터 직접 생성 (UI 클릭 최소화)
  await request.post('/api/test/seed', { data: { scenario: 'checkout' } });
});

test.afterEach(async ({ request }) => {
  await request.post('/api/test/cleanup');
});
```

DON'T:
```typescript
// ❌ 구현 상세에 의존하는 셀렉터
await page.locator('.MuiButton-root > div:nth-child(2)').click();
await page.locator('#__next > main > div:nth-child(3)').click();

// ❌ 테스트 간 상태 공유
let orderId: string; // 이전 테스트에서 생성된 ID에 의존
test('주문 확인', async ({ page }) => {
  await page.goto(`/orders/${orderId}`); // 이전 테스트 실패 시 연쇄 실패
});
```

### Visual Comparison (CI)
```typescript
// 스크린샷 비교로 시각적 회귀 검출
await expect(page).toHaveScreenshot('checkout-page.png', {
  maxDiffPixelRatio: 0.01,
});
```

### CI 통합 규칙
- Playwright 전용 Docker 이미지 사용 (playwright:v1.40.0)
- 병렬 실행: `workers: 4` (CI에서 속도 최적화)
- 실패 시 trace/screenshot 자동 저장: `retries: 1`, `trace: 'on-first-retry'`
- E2E는 전체 테스트의 10-20%만 유지 (유지보수 비용 관리)

## Connections

- [[qa.test-gen.bdd]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.role]] — CO_CREATES (weight: 0.6)
