---
id: "planning.prd.metrics"
domain: "planning"
type: "pattern"
region: PREFRONTAL
token_estimate: 500
theory: "#80 HEART Framework (Google, 2010), Pirate Metrics AARRR (McClure, 2007)"
tags: [planning, prd, metrics, kpi, pattern]
---

# planning.prd.metrics

> **Region**: 🧠 [[PREFRONTAL]]  
> **Domain**: `planning`  
> **Type**: `pattern`  
> **Theory**: #80 HEART Framework (Google, 2010), Pirate Metrics AARRR (McClure, 2007)  
> **Tokens**: 500

## Content

Product Metrics 설계 (측정하지 않으면 개선할 수 없다):

### 왜 지표 설계가 중요한가?
지표 없는 제품은 나침반 없는 항해와 같다. 하지만 잘못된 지표는
팀을 잘못된 방향으로 이끈다. 허영 지표(Vanity Metric)에 빠지지 않고,
실행 가능한 지표(Actionable Metric)를 선정해야 한다.

### HEART Framework (사용자 경험 지표)
Google이 개발한 UX 품질 측정 프레임워크:

| 차원 | 의미 | 지표 예시 |
|------|------|-----------|
| Happiness | 사용자 만족도 | NPS, CSAT, 앱스토어 평점 |
| Engagement | 참여 깊이 | 세션당 체류 시간, 핵심 기능 사용 빈도 |
| Adoption | 신규 채택 | 신규 가입 수, 온보딩 완료율 |
| Retention | 재방문 | D1/D7/D30 리텐션, 주간 활성 사용자 |
| Task Success | 태스크 완료 | 핵심 플로우 완료율, 에러율, 소요 시간 |

각 차원별 GSM(Goals-Signals-Metrics) 작성:
```
차원: [HEART 중 택1]
Goal: [달성하고 싶은 것]
Signal: [목표 달성을 나타내는 사용자 행동]
Metric: [Signal을 측정하는 구체적 수치]
```

### AARRR (Pirate Metrics, 비즈니스 퍼널 지표)
사용자 라이프사이클 전체를 측정하는 프레임워크:

| 단계 | 질문 | 핵심 지표 예시 |
|------|------|----------------|
| Acquisition | 어떻게 사용자가 오는가? | 채널별 유입 수, CAC |
| Activation | 첫 경험이 좋은가? | 온보딩 완료율, "Aha Moment" 도달율 |
| Retention | 다시 돌아오는가? | D1/D7/D30 리텐션, DAU/MAU |
| Revenue | 돈을 내는가? | 전환율, ARPU, LTV |
| Referral | 추천하는가? | 추천 코드 사용율, K-factor |

### North Star Metric (NSM) 선정

NSM은 제품의 핵심 가치를 하나의 숫자로 대표하는 지표이다.

**좋은 NSM의 조건:**
- 고객 가치를 반영한다 (매출이 아닌 사용자 성공)
- 장기 비즈니스 성과와 상관관계가 있다
- 팀 전체가 이해하고 영향을 줄 수 있다
- 주기적으로 측정 가능하다

**NSM 예시:**
| 제품 유형 | NSM 예시 | 이유 |
|-----------|----------|------|
| 콘텐츠 플랫폼 | 주당 콘텐츠 소비 시간 | 가치 전달량 반영 |
| SaaS 도구 | 주간 활성 팀 수 | 핵심 사용 패턴 반영 |
| 이커머스 | 월간 반복 구매 고객 수 | 고객 만족+비즈니스 연결 |
| 커뮤니티 | 주간 의미 있는 인터랙션 수 | 네트워크 효과 반영 |

### 허영 지표 vs 실행 가능 지표

| 허영 지표 (피할 것) | 실행 가능 지표 (사용할 것) |
|---------------------|---------------------------|
| 총 다운로드 수 | 월간 활성 사용자(MAU) |
| 총 가입자 수 | 온보딩 완료율 |
| 페이지뷰 | 세션당 핵심 액션 수 |
| 총 매출 | 코호트별 LTV |
| 앱스토어 평점 (단독) | NPS + 정성 피드백 조합 |

DO: "D7 리텐션 40% 달성을 목표로 하며, 주간 코호트별 추적.
     현재 업계 벤치마크는 20-30% 수준 [출처: Mixpanel 2023 Report]"
DON'T: "다운로드 100만 달성"
  → 다운로드 후 한 번도 안 열면 의미 없는 수치

### 지표 설계 템플릿
```
┌─────────────────────────────────────────┐
│ North Star Metric: ____________________ │
│ 정의: _________________________________ │
│ 측정 주기: 일간 / 주간 / 월간           │
│ 현재 값: ______ 목표 값: ______         │
├─────────────────────────────────────────┤
│ Supporting Metrics (3-5개)              │
│ 1. ____________ (측정: _____, 목표: ___)│
│ 2. ____________ (측정: _____, 목표: ___)│
│ 3. ____________ (측정: _____, 목표: ___)│
├─────────────────────────────────────────┤
│ 가드레일 Metric (악화되면 안 되는 것)   │
│ - ____________ (하한선: ___)            │
└─────────────────────────────────────────┘
```

### 주의사항
- 지표가 10개를 넘으면 집중이 분산된다 → NSM 1개 + Supporting 3-5개로 제한
- 목표값은 업계 벤치마크 또는 과거 데이터에 기반. 근거 없으면 [추정치] 태그
- 지표 측정을 위한 로깅/분석 구현이 MVP에 포함되어야 한다

## Connections

### FEEDS (1)

- → [[analytics.metrics]] `w=0.5`

### CO_CREATES (1)

- ← [[planning.prd.feature-prioritization]] `w=0.6`
