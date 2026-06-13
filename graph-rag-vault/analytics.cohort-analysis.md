---
id: "analytics.cohort-analysis"
domain: "analytics"
type: "pattern"
bloom_level: ""
tags: ["analytics", "cohort", "retention", "metrics"]
brain_region: "THALAMUS"
token_estimate: 420
---

# analytics.cohort-analysis

> #141 Cohort Analysis (리텐션 측정의 표준 방법론)

코호트 분석 (동일 시점 사용자 그룹의 행동 변화를 추적한다):

### 코호트 정의
- 시간 코호트: 가입 주/월 기준 (가장 일반적)
- 행동 코호트: 특정 행동 완료 기준 (온보딩 완료 여부)
- 크기 코호트: 구매 금액/사용량 기준

### 리텐션 테이블
```
       Week 0  Week 1  Week 2  Week 3  Week 4
Jan    100%    40%     25%     20%     18%
Feb    100%    45%     30%     24%     22%
Mar    100%    50%     35%     28%     25%
```
→ Feb, Mar 코호트 개선 = 온보딩 변경 효과 입증

### 핵심 리텐션 지표
| 지표 | 공식 | 좋은 기준 (B2C SaaS) |
|------|------|-------------------|
| Day 1 | D1 활성 / 가입자 | > 40% |
| Day 7 | D7 활성 / 가입자 | > 20% |
| Day 30 | D30 활성 / 가입자 | > 10% |
| 스마일 커브 | 하락 후 반등 | 존재 시 PMF 신호 |

### 분석 시 주의사항
- 최소 코호트 크기: 통계적 유의성 위해 100명 이상
- 시즌 효과 보정: 연말/명절 코호트는 별도 취급
- 생존 편향: 초기 이탈자 데이터도 반드시 포함
- Incomplete cohort: 아직 안 끝난 코호트에 결론 금지

## Connections

- [[analytics.role]] — REQUIRES (weight: 0.9)
- [[analytics.verify]] — FEEDS (weight: 0.8)
- [[analytics.funnel-analysis]] — FEEDS (weight: 0.7)
- [[analytics.bayesian]] — FEEDS (weight: 0.7)
- [[analytics.role]] — FEEDS (weight: 0.5)
- [[analytics.metrics]] — FEEDS (weight: 0.5)
- [[analytics.ab-testing]] — FEEDS (weight: 0.5)
- [[analytics.simpsons-paradox]] — FEEDS (weight: 0.5)
