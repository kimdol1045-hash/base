---
id: "qa.test-gen.verify"
domain: "qa"
type: "verify"
region: EGO
token_estimate: 90
tags: [qa, test, verification]
---

# qa.test-gen.verify

> **Region**: 🔵 [[EGO]]  
> **Domain**: `qa`  
> **Type**: `verify`  
> **Tokens**: 90

## Content

자기 검증 체크리스트:
- [ ] 정상 케이스와 에러 케이스를 모두 커버하는가?
- [ ] 경계값 테스트가 포함되었는가? (min, max, 0, null, empty)
- [ ] 테스트가 독립적으로 실행 가능한가? (다른 테스트에 의존하지 않는가)

## Connections

### REQUIRES (2)

- ← [[qa.code-review.role]] `w=0.85`
- ← [[qa.test-gen.role]] `w=0.85`

### FEEDS (6)

- ← [[qa.code-review.performance]] `w=0.5`
- ← [[qa.code-review.priority]] `w=0.8`
- ← [[qa.code-review.readability]] `w=0.8`
- ← [[qa.code-review.role]] `w=0.5`
- ← [[qa.code-review.security]] `w=0.8`
- ← [[qa.test-gen.integration]] `w=0.8`

### CO_CREATES (4)

- ← [[qa.test-gen.component-test]] `w=0.6`
- ← [[qa.test-gen.integration]] `w=0.6`
- ← [[qa.test-gen.role]] `w=0.6`
- ← [[qa.test-gen.unit]] `w=0.6`
