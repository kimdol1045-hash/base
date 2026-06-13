---
id: "qa.test-gen.unit"
domain: "qa"
type: "pattern"
bloom_level: ""
tags: ["qa", "test", "unit-test", "vitest"]
brain_region: "CEREBELLUM"
token_estimate: 420
---

# qa.test-gen.unit

> #123 AAA Pattern (Arrange-Act-Assert)

단위 테스트 (개별 함수/모듈의 정확성을 검증한다):

### AAA 패턴
```typescript
import { describe, it, expect } from 'vitest';
import { calculateDiscount } from './pricing';

describe('calculateDiscount', () => {
  it('10만원 이상 구매 시 10% 할인 적용', () => {
    // Arrange
    const price = 150000;
    const memberLevel = 'standard';

    // Act
    const result = calculateDiscount(price, memberLevel);

    // Assert
    expect(result).toBe(135000);
  });

  it('음수 금액 시 에러 발생', () => {
    expect(() => calculateDiscount(-1000, 'standard'))
      .toThrow('금액은 0 이상이어야 합니다');
  });

  it('VIP 회원은 추가 5% 할인', () => {
    const result = calculateDiscount(100000, 'vip');
    expect(result).toBe(85000); // 10% + 5%
  });
});
```

### 좋은 테스트의 조건
- 독립적: 다른 테스트에 의존하지 않음
- 반복 가능: 몇 번이든 같은 결과
- 빠름: 단위 테스트 전체 10초 이내
- 의미 있는 이름: "~할 때 ~해야 한다" 형식

### Mock/Stub 기준
- 외부 의존성(DB, API, 파일)만 mock
- 내부 구현 mock 금지 (리팩토링 시 테스트 깨짐)
- vi.fn()으로 호출 횟수/인자 검증

### 테스트 커버리지
- 행복 경로 (정상 동작) + 에지 케이스 (경계값, null, 빈 배열)
- 목표: 80% 라인 커버리지 (100% 추구 금지 — 유지보수 비용)

## Connections

- [[qa.test-gen.role]] — REQUIRES (weight: 0.9)
- [[qa.test-gen.verify]] — FEEDS (weight: 0.8)
- [[qa.test-gen.integration]] — FEEDS (weight: 0.7)
- [[qa.code-review.role]] — FEEDS (weight: 0.5)
- [[qa.code-review.priority]] — FEEDS (weight: 0.5)
- [[qa.code-review.performance]] — FEEDS (weight: 0.5)
- [[qa.test-gen.role]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.integration]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.component-test]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.testing-trophy]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.verify]] — CO_CREATES (weight: 0.6)
