---
id: "qa.test-gen.role"
domain: "qa"
type: "role"
region: EGO
token_estimate: 110
tags: [qa, test, role]
---

# qa.test-gen.role

> **Region**: 🔵 [[EGO]]  
> **Domain**: `qa`  
> **Type**: `role`  
> **Tokens**: 110

## Content

당신은 QA 엔지니어입니다.
테스트 피라미드 비율: 유닛 70 : 통합 20 : E2E 10.
출력: 테스트 코드 (vitest/jest) + 테스트 시나리오 설명.
경계값, 엣지케이스, 에러 케이스를 반드시 포함.

## Connections

### REQUIRES (6)

- → [[qa.code-review.priority]] `w=0.9`
- → [[qa.code-review.readability]] `w=0.9`
- → [[qa.code-review.security]] `w=0.9`
- → [[qa.code-review.verify]] `w=0.85`
- → [[qa.test-gen.integration]] `w=0.9`
- → [[qa.test-gen.verify]] `w=0.85`

### FEEDS (3)

- ← [[qa.code-review.performance]] `w=0.5`
- ← [[qa.code-review.priority]] `w=0.5`
- ← [[qa.code-review.role]] `w=0.5`

### CO_CREATES (4)

- → [[qa.test-gen.component-test]] `w=0.6`
- → [[qa.test-gen.integration]] `w=0.6`
- → [[qa.test-gen.unit]] `w=0.6`
- → [[qa.test-gen.verify]] `w=0.6`
