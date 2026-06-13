---
id: "qa.test-gen.mutation"
domain: "qa"
type: "pattern"
region: EGO
token_estimate: 420
theory: "#171 Mutation Testing (Richard Lipton, 1971 / Stryker Mutator)"
tags: [qa, mutation-testing, test-quality, stryker]
---

# qa.test-gen.mutation

> **Region**: 🔵 [[EGO]]  
> **Domain**: `qa`  
> **Type**: `pattern`  
> **Theory**: #171 Mutation Testing (Richard Lipton, 1971 / Stryker Mutator)  
> **Tokens**: 420

## Content

뮤테이션 테스트 (테스트의 품질 자체를 검증한다):

### 핵심 개념
코드에 의도적 버그(mutant)를 주입 → 테스트가 이를 잡는지 확인
- Killed: 테스트가 mutant를 감지 ✅
- Survived: 테스트가 mutant를 놓침 ❌ (테스트 보강 필요)

### 뮤테이션 유형
| 유형 | 원본 | 뮤턴트 |
|------|------|--------|
| 조건 반전 | `if (a > b)` | `if (a <= b)` |
| 산술 변경 | `a + b` | `a - b` |
| 반환값 변경 | `return true` | `return false` |
| 삭제 | `validateInput()` | (삭제) |
| 경계값 | `i < n` | `i <= n` |

### Stryker (JavaScript/TypeScript)
```bash
npx stryker run
```
```
Mutation score: 85% (170 killed / 200 total)
Survived mutants:
  - src/pricing.ts:23  a > b → a >= b  (boundary mutant)
  - src/auth.ts:45     return true → return false
```

### 뮤테이션 스코어
```
Score = (Killed + Timeout) / Total Mutants × 100%
```
- 목표: 80%+ (100%는 비현실적)
- 낮은 스코어 = 테스트가 있지만 실질적 검증이 부족

### 적용 가이드
- ✅ 적용: 비즈니스 크리티컬 로직, 금융/의료 코드
- ❌ 부적합: UI 코드, 외부 API 호출 코드 (느리고 비결정적)
- 전체 코드가 아닌 핵심 모듈에만 적용 (비용 대비 효과)

## Connections

*Connections will be populated by Graph RAG ingest.*
