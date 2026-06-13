---
id: "qa.test-gen.bdd"
domain: "qa"
type: "pattern"
bloom_level: ""
tags: ["qa", "bdd", "test", "given-when-then"]
brain_region: "CEREBELLUM"
token_estimate: 430
---

# qa.test-gen.bdd

> #153 Behavior-Driven Development (Dan North, 2006)

BDD (비즈니스 요구사항을 실행 가능한 테스트로 전환한다):

### Given-When-Then 패턴
```gherkin
Feature: 장바구니

Scenario: 상품 추가
  Given 빈 장바구니가 있다
  When "맥북 프로" 상품을 추가한다
  Then 장바구니에 1개 상품이 있어야 한다
  And 총 금액이 2,490,000원이어야 한다

Scenario: 재고 부족 시 추가 실패
  Given "한정판 키보드"의 재고가 0개이다
  When "한정판 키보드"를 장바구니에 추가한다
  Then "재고가 부족합니다" 에러가 표시되어야 한다
```

### 코드 구현 (Vitest)
```typescript
describe('장바구니', () => {
  describe('상품 추가', () => {
    it('빈 장바구니에 상품 추가 시 수량 1, 총액 반영', () => {
      // Given
      const cart = new Cart();
      const product = { id: '1', name: '맥북 프로', price: 2490000 };

      // When
      cart.addItem(product);

      // Then
      expect(cart.items).toHaveLength(1);
      expect(cart.totalAmount).toBe(2490000);
    });
  });
});
```

### 좋은 시나리오 작성법
- 비즈니스 언어 사용 (구현 디테일 X)
- 시나리오 하나에 검증 포인트 하나
- Edge case도 시나리오로 작성
- "~해야 한다" 형식으로 기대 결과 명시

### BDD vs TDD
| 구분 | TDD | BDD |
|------|-----|-----|
| 관점 | 개발자 | 사용자/비즈니스 |
| 단위 | 함수/모듈 | 기능/시나리오 |
| 언어 | 코드 | 자연어 + 코드 |

## Connections

- [[qa.test-gen.e2e]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.role]] — CO_CREATES (weight: 0.6)
