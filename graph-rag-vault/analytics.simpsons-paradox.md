---
id: "analytics.simpsons-paradox"
domain: "analytics"
type: "rule"
bloom_level: ""
tags: ["analytics", "statistics", "simpsons-paradox"]
brain_region: "THALAMUS"
token_estimate: 400
---

# analytics.simpsons-paradox

> #148 Simpson's Paradox (Simpson, 1951)

심슨의 역설 (전체 데이터와 세그먼트별 데이터가 반대 결론):

### 실제 예시
전체 전환율: A안 45%, B안 42% → A안 승리?

세그먼트별:
| | 모바일 | 데스크톱 |
|--|--------|---------|
| A안 | 30% (3000명) | 60% (1000명) |
| B안 | 35% (1000명) | 65% (3000명) |

B안이 모바일/데스크톱 모두에서 더 높다!
A안이 전체에서 높은 이유: 모바일(전환율 낮은) 트래픽 비중이 더 큼.

### 방지 규칙
1. **항상 세그먼트별 분석 병행**
   주요 세그먼트: 디바이스, 신규/기존, 유입 채널, 국가, 시간대
2. **전체 수치만으로 결론 내지 않기**
   "전체 전환율 상승"이어도 특정 세그먼트에서 하락할 수 있음
3. **공변량(Confounding Variable) 확인**
   "A/B 그룹 간 트래픽 구성이 동일한가?"

### 체크리스트
- [ ] 전체 결과와 세그먼트 결과가 같은 방향인가?
- [ ] 그룹 간 세그먼트 구성 비율이 유사한가?
- [ ] 숨겨진 교란 변수가 없는가?

## Connections

- [[analytics.role]] — FEEDS (weight: 0.5)
- [[analytics.metrics]] — FEEDS (weight: 0.5)
- [[analytics.ab-testing]] — FEEDS (weight: 0.5)
- [[analytics.funnel-analysis]] — FEEDS (weight: 0.5)
- [[analytics.cohort-analysis]] — FEEDS (weight: 0.5)
- [[analytics.bayesian]] — FEEDS (weight: 0.5)
