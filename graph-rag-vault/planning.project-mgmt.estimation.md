---
id: "planning.project-mgmt.estimation"
domain: "planning"
type: "pattern"
bloom_level: ""
tags: ["planning", "project-management", "estimation", "story-points", "velocity"]
brain_region: "PREFRONTAL"
token_estimate: 500
---

# planning.project-mgmt.estimation

> #142 스크럼 추정 기법 + A9 계획 오류 방지 (Buehler et al., 1994)

추정 기법 (과거 데이터 기반의 현실적 추정):

### 왜 추정이 어려운가?
계획 오류(Planning Fallacy, A9)에 의해 인간은 소요 시간을 체계적으로
과소 추정한다. "이번에는 다를 것이다"라는 내부 관점(Inside View) 대신
과거 유사 프로젝트 데이터에 기반한 외부 관점(Outside View)을 사용해야 한다.

### 추정 기법 1: Story Points
```
피보나치 수열 기준: 1, 2, 3, 5, 8, 13, 21

기준점 설정 (Calibration):
- 1SP: 경험 있는 팀원이 반나절 내 완료 가능한 단순 작업
       예: 버튼 텍스트 변경, 환경 변수 추가
- 3SP: 하루 정도 소요. 명확한 구현 방법이 있는 작업
       예: CRUD API 엔드포인트 1개 추가
- 5SP: 2-3일 소요. 약간의 불확실성이 있는 작업
       예: 외부 API 연동, 새로운 UI 컴포넌트 개발
- 8SP: 3-5일 소요. 기술적 불확실성 존재
       예: 결제 시스템 연동, 복잡한 상태 관리
- 13SP+: 분해 필요. 이 크기의 스토리는 반드시 하위 스토리로 분리
```

### 추정 기법 2: T-shirt Sizing
```
빠른 초기 추정에 적합. 로드맵 수준 계획에 사용:

| 사이즈 | SP 범위 | 기간 | 예시 |
|--------|---------|------|------|
| XS | 1-2 SP | 반나절 | 설정값 변경, 문구 수정 |
| S  | 3-5 SP | 1-3일 | API 엔드포인트, 단순 UI |
| M  | 5-8 SP | 3-5일 | 기능 모듈 1개 |
| L  | 8-13 SP | 1-2주 | 복합 기능, 외부 연동 |
| XL | 13+ SP | 2주+ | 분해 필수, 에픽 수준 |
```

### 추정 기법 3: Planning Poker
```
진행 절차:
1. PO가 스토리를 설명 (5분)
2. 팀원 질문 및 토론 (5분)
3. 각자 카드를 동시에 공개
4. 최대-최소 추정자가 근거 설명
5. 재투표 (1-2회)
6. 합의 도출 또는 최대값 채택

규칙:
- 3번 이상 재투표 금지 (시간 낭비 방지)
- 편차가 3배 이상이면 스토리 정의 재검토
  예: 2SP vs 8SP → 스토리의 범위가 모호한 신호
```

### 계획 오류 방지: 범위 추정 (Three-Point Estimation)
```
단일 숫자 추정 대신 범위로 추정한다:

공식: 기대값 = (최소 + 4×최빈 + 최대) / 6

예시: 결제 연동 작업
- 최소(Optimistic): 3일 (모든 것이 순조로울 때)
- 최빈(Most Likely): 5일 (일반적 상황)
- 최대(Pessimistic): 12일 (API 문서 부정확, 인증 문제 등)
- 기대값: (3 + 20 + 12) / 6 = 5.8일

→ 단일 추정치 "5일"보다 현실적. 이해관계자에게는 "5-12일, 기대값 6일"로 보고
```

### Velocity 기반 계획
```
과거 3-5 스프린트의 velocity 평균을 사용:

| 스프린트 | 완료 SP | 비고 |
|----------|---------|------|
| S1 | 18 | 온보딩 기간 |
| S2 | 22 | |
| S3 | 25 | |
| S4 | 20 | 팀원 1명 휴가 |
| S5 | 23 | |

평균 velocity: 21.6SP → 다음 스프린트 계획: 20-22SP
절대 최대값(25SP)으로 계획하지 않는다.
```

### DO / DON'T
DO: "과거 5개 스프린트 평균 velocity가 21SP이므로 이번 스프린트도
     20SP로 계획한다. 결제 연동은 5-12일(기대 6일)로 범위 추정했다."
DON'T: "이번에는 팀이 의욕이 높으니 30SP를 목표로 하자"
       → 내부 관점에 의한 계획 오류. 데이터 기반 추정을 사용할 것

## Connections

- [[planning.project-mgmt.role]] — REQUIRES (weight: 0.9)
- [[planning.project-mgmt.verify]] — FEEDS (weight: 0.8)
- [[planning.project-mgmt.kanban]] — FEEDS (weight: 0.7)
- [[planning.project-mgmt.tech-debt]] — FEEDS (weight: 0.7)
