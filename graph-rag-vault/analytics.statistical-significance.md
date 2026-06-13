---
id: "analytics.statistical-significance"
domain: "analytics"
type: "rule"
bloom_level: ""
tags: ["analytics", "statistics", "significance"]
brain_region: "THALAMUS"
token_estimate: 420
---

# analytics.statistical-significance

> #147 Statistical Significance (Fisher, 1925)

통계적 유의성 (우연이 아닌 실제 차이인지 판단한다):

### 핵심 개념
- **p-value**: 귀무가설이 참일 때 이 결과가 나올 확률. 0.05 미만이면 유의.
- **신뢰구간 (CI)**: 95% CI가 0을 포함하지 않으면 유의.
- **효과 크기 (Effect Size)**: 통계적 유의 ≠ 실질적 의미. 효과 크기도 확인.

### 1종/2종 오류
| | 실제 차이 있음 | 실제 차이 없음 |
|--|-------------|-------------|
| 유의하다 판단 | ✅ 정탐 | ❌ 1종 오류 (α) |
| 유의하지 않다 판단 | ❌ 2종 오류 (β) | ✅ 정탐 |

- α = 0.05 (5% 확률로 없는 효과를 있다고 잘못 판단)
- β = 0.2 (20% 확률로 있는 효과를 놓침)
- 검정력 = 1 - β = 0.8

### 흔한 실수 (p-hacking)
- 데이터 보면서 가설 변경 (HARKing)
- 유의미한 결과 나올 때까지 표본 추가
- 여러 지표 중 유의미한 것만 보고
- 하위 그룹 분석에서 우연히 유의미한 것 선택

### 올바른 해석
- DO: "p=0.03이므로 95% 신뢰수준에서 통계적으로 유의한 차이가 있다. 효과 크기는 +5%p."
- DON'T: "p=0.03이므로 B안이 확실히 더 좋다."

## Connections

- [[analytics.ab-testing]] — FEEDS (weight: 0.5)
