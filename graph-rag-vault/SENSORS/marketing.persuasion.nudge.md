---
id: "marketing.persuasion.nudge"
domain: "marketing"
type: "pattern"
region: SENSORS
token_estimate: 500
theory: "#59 넛지 이론 (Thaler & Sunstein, 2008)"
tags: [marketing, persuasion, nudge, choice-architecture, default, framing]
---

# marketing.persuasion.nudge

> **Region**: 📡 [[SENSORS]]  
> **Domain**: `marketing`  
> **Type**: `pattern`  
> **Theory**: #59 넛지 이론 (Thaler & Sunstein, 2008)  
> **Tokens**: 500

## Content

넛지 이론 — 선택의 자유를 유지하면서 더 나은 의사결정을 유도하는 설계:

### 1. 기본값 설정 (Default Option)
사람은 기본값을 그대로 수용하는 경향이 있다 (옵트아웃 비율 < 10%).

**구독 설계 예시**:
- 연간 결제를 기본 선택: "연간 결제 (20% 할인)" ← 기본 선택됨
- 프로 요금제를 기본 하이라이트: "가장 인기 있는 플랜"
- 뉴스레터 수신 기본 체크: "유용한 팁을 이메일로 받겠습니다" ✓

**결제 페이지 예시**:
```
┌─────────────────────────────────────┐
│  결제 주기 선택                        │
│  ○ 월간 결제  ₩49,000/월              │
│  ● 연간 결제  ₩39,000/월 (20% 절약)   │  ← 기본 선택
│    "연 120,000원을 절약합니다"          │
└─────────────────────────────────────┘
```

### 2. 사회적 규범 활용 (Social Norms)
"다수의 행동"을 보여주면 같은 행동을 따르게 된다.

- "이 플랜을 선택한 고객의 78%가 연간 결제를 이용합니다"
- "같은 업종 기업의 92%가 프로 플랜을 사용합니다"
- "지난달 1,247명이 이 기능을 활성화했습니다"
- 호텔 타월 재사용: "이 방의 이전 투숙객 75%가 타월을 재사용했습니다" (Goldstein et al., 2008)

### 3. 선택 아키텍처 (Choice Architecture)
선택지의 배치, 순서, 프레이밍이 결정을 좌우한다.

**요금제 배치**:
```
┌──────────┐  ┌──────────────┐  ┌──────────┐
│  Basic   │  │  ★ Pro ★     │  │ Enterprise│
│  ₩29,000 │  │  ₩49,000     │  │  ₩99,000  │
│          │  │  가장 인기     │  │           │
│  5GB     │  │  50GB        │  │  무제한    │
│  3명     │  │  15명        │  │  무제한    │
│          │  │  ───────────  │  │           │
│  [선택]  │  │  [시작하기]   │  │  [문의]   │
└──────────┘  └──────────────┘  └──────────┘
     작게          크게+강조          보통
```
- 추천 플랜을 시각적으로 강조 (크기, 색상, 배지)
- 3개 선택지일 때 중간이 가장 많이 선택됨 (타협 효과)

### 4. 프레이밍 효과 (Framing)
같은 정보도 표현 방식에 따라 인식이 달라진다.
- 할인: "20% 할인" < "연 120,000원 절약" (구체적 금액이 효과적)
- 기능: "50GB 저장공간" < "사진 25,000장 저장 가능" (체감 단위)
- 무료 체험: "무료 체험 시작" < "14일 동안 모든 기능을 무료로" (구체적 기간+범위)

### 5. 적시 넛지 (Timely Nudge)
의사결정 시점에 정보를 제공해야 효과적이다.
- 장바구니: "무료 배송까지 ₩12,000 남았습니다"
- 해지 시: "지난 3개월간 이 기능을 47회 사용하셨습니다"
- 업그레이드: 무료 용량 80% 도달 시 "저장 공간이 부족해지고 있습니다"

## Connections

### CO_CREATES (6)

- → [[marketing.persuasion.anchoring]] `w=0.6`
- → [[marketing.persuasion.authority]] `w=0.6`
- ← [[marketing.persuasion.hook-model]] `w=0.6`
- → [[marketing.persuasion.reciprocity]] `w=0.6`
- ← [[marketing.persuasion.role]] `w=0.6`
- → [[marketing.persuasion.social-proof]] `w=0.6`
