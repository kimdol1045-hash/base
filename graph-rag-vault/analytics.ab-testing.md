---
id: "analytics.ab-testing"
domain: "analytics"
type: "pattern"
bloom_level: ""
tags: ["analytics", "ab-testing", "experiment"]
brain_region: "THALAMUS"
token_estimate: 450
---

# analytics.ab-testing

> #146 A/B Testing (Kohavi et al., 2009)

A/B 테스트 (데이터 기반으로 최적 변형을 선택한다):

### 실험 설계 7단계
1. **가설 수립**: "CTA 버튼 색상을 파란색→초록색으로 변경하면 클릭률이 10% 증가할 것이다"
2. **핵심 지표 정의**: 1차 지표(클릭률) + 가드레일 지표(이탈률)
3. **표본 크기 계산**: 유의수준 α=0.05, 검정력 1-β=0.8, 최소 감지 효과(MDE)
4. **무작위 배정**: 사용자를 A/B 그룹에 랜덤 할당
5. **실행 기간**: 최소 1-2주 (요일 효과 제거)
6. **분석**: p-value < 0.05 확인, 신뢰구간 확인
7. **의사결정**: 통계적 유의 + 실질적 의미 둘 다 확인

### 표본 크기 경험칙
| 기존 전환율 | MDE 10% | MDE 20% |
|------------|---------|---------|
| 1% | ~150,000/그룹 | ~40,000/그룹 |
| 5% | ~30,000/그룹 | ~8,000/그룹 |
| 10% | ~15,000/그룹 | ~4,000/그룹 |

### 흔한 실수
- 조기 종료: 초반 유의미해 보여도 표본 크기 채울 때까지 유지
- 다중 비교: A/B/C/D 테스트 시 Bonferroni 보정 필요
- 부정 결과 무시: "차이 없음"도 유효한 결과
- Novelty Effect: 새로움 때문에 초반 지표 왜곡

## Connections

- [[analytics.role]] — REQUIRES (weight: 0.9)
- [[analytics.verify]] — FEEDS (weight: 0.8)
- [[analytics.metrics]] — FEEDS (weight: 0.7)
- [[analytics.role]] — FEEDS (weight: 0.5)
- [[analytics.metrics]] — FEEDS (weight: 0.5)
- [[analytics.funnel-analysis]] — FEEDS (weight: 0.5)
- [[analytics.cohort-analysis]] — FEEDS (weight: 0.5)
- [[analytics.bayesian]] — FEEDS (weight: 0.5)
- [[analytics.simpsons-paradox]] — FEEDS (weight: 0.5)
- [[analytics.statistical-significance]] — FEEDS (weight: 0.5)
