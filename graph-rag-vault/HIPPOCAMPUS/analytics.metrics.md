---
id: "analytics.metrics"
domain: "analytics"
type: "rule"
region: HIPPOCAMPUS
token_estimate: 450
theory: "#80 AARRR Pirate Metrics (McClure, 2007) + HEART (Google, 2010)"
tags: [analytics, metrics, aarrr, heart]
---

# analytics.metrics

> **Region**: 🌿 [[HIPPOCAMPUS]]  
> **Domain**: `analytics`  
> **Type**: `rule`  
> **Theory**: #80 AARRR Pirate Metrics (McClure, 2007) + HEART (Google, 2010)  
> **Tokens**: 450

## Content

제품 지표 프레임워크 (무엇을 측정할지 결정한다):

### AARRR (Pirate Metrics)
| 단계 | 지표 예시 | 허영 지표 ❌ | 실행 지표 ✅ |
|------|----------|------------|------------|
| Acquisition | 방문자 수 | 페이지뷰 | 채널별 CAC |
| Activation | 가입/온보딩 | 가입자 수 | 핵심 기능 도달률 |
| Retention | 재방문 | 총 방문수 | Day 7/30 리텐션 |
| Revenue | 매출 | 총 매출 | ARPU, LTV |
| Referral | 공유 | 공유 수 | 바이럴 계수 (K-factor) |

### North Star Metric
제품의 핵심 가치를 하나의 지표로:
- Slack: "주간 메시지 전송 수" (소통 가치)
- Airbnb: "예약된 숙박 일수" (거래 가치)
- 선정 기준: 고객 가치 반영 + 선행 지표 + 팀 전체 정렬 가능

### HEART Framework (Google)
| 차원 | 설명 | 지표 예시 |
|------|------|----------|
| Happiness | 사용자 만족 | NPS, CSAT |
| Engagement | 참여도 | DAU/MAU, 세션 시간 |
| Adoption | 신규 채택 | 신규 사용자 비율 |
| Retention | 유지 | D7, D30 리텐션 |
| Task Success | 작업 성공 | 완료율, 에러율 |

### 흔한 실수
- 허영 지표에 집중 (총 가입자 수 100만! → 근데 DAU 1000명)
- 지표 과다 (20개 지표 추적 → 집중력 분산)
- 후행 지표만 (매출은 결과. 선행 지표를 찾아야)

## Connections

### REQUIRES (1)

- ← [[analytics.role]] `w=0.9`

### FEEDS (7)

- ← [[analytics.ab-testing]] `w=0.7`
- → [[analytics.ab-testing]] `w=0.5`
- → [[analytics.bayesian]] `w=0.7`
- ← [[analytics.role]] `w=0.5`
- → [[analytics.simpsons-paradox]] `w=0.5`
- → [[analytics.verify]] `w=0.8`
- ← [[planning.prd.metrics]] `w=0.5`
