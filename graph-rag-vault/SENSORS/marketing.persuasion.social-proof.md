---
id: "marketing.persuasion.social-proof"
domain: "marketing"
type: "pattern"
region: SENSORS
token_estimate: 500
theory: "#62 사회적 증거 (Cialdini, 1984 Ch.4)"
tags: [marketing, persuasion, social-proof, testimonial, trust, conversion]
---

# marketing.persuasion.social-proof

> **Region**: 📡 [[SENSORS]]  
> **Domain**: `marketing`  
> **Type**: `pattern`  
> **Theory**: #62 사회적 증거 (Cialdini, 1984 Ch.4)  
> **Tokens**: 500

## Content

사회적 증거 — 불확실한 상황에서 사람은 다른 사람의 행동을 따른다:

### 사회적 증거 6가지 유형

**1. 숫자 증거 (Numbers)**
- "12,847개 팀이 사용 중입니다"
- "누적 거래액 1조 2천억원"
- "월 평균 350만 건 처리"
- 배치: 히어로 섹션 바로 아래, CTA 근처

**2. 고객 로고월 (Logo Wall)**
- 인지도 높은 브랜드 6~12개 로고 가로 배치
- "신뢰하는 기업들" 또는 문구 없이 로고만
- 배치: 히어로 바로 아래 또는 가격표 위
```
┌─────────────────────────────────────┐
│  삼성  |  카카오  |  네이버  |  토스   │
│  쿠팡  |  배민   |  당근    |  라인   │
└─────────────────────────────────────┘
```

**3. 고객 후기 (Testimonials)**
- 실명 + 직함 + 회사명 + 얼굴 사진 (신뢰도 순)
- 구체적 수치 포함: "도입 후 CS 응대 시간이 40% 줄었습니다"
- 스토리 구조: 문제 → 도입 → 결과
- 예시: "매일 3시간씩 수동으로 리포트를 만들었는데, 이제 버튼 하나로 끝납니다" — 김지영, 마케팅 팀장, ABC Corp

**4. 사례 연구 (Case Studies)**
- 구조: 기업 소개 → 과제 → 솔루션 → 정량적 결과
- 핵심 지표 3개 이내로 강조
- "전환율 2.1% → 5.8% (176% 향상)"
- "온보딩 완료율 34% → 72%"

**5. 실시간 활동 (Real-time Activity)**
- "방금 서울에서 김OO님이 구매했습니다"
- "현재 247명이 이 페이지를 보고 있습니다"
- "오늘 89명이 가입했습니다"
- 토스트 알림으로 실시간 표시 (좌측 하단)

**6. 평점 및 리뷰 (Ratings & Reviews)**
- 별점 4.5 이상 + 리뷰 수 표시: "4.8/5 (2,341개 리뷰)"
- 외부 플랫폼 연동: G2, Product Hunt, 앱스토어 평점
- 배치: CTA 버튼 바로 아래

### 배치 전략 (랜딩 페이지)
```
[히어로 섹션 — 헤드라인 + CTA]
[로고월 — 6~12개 브랜드]
[기능 소개 — 핵심 가치 3가지]
[숫자 증거 — "12,000+ 팀 | 99.9% 가동률 | 4.8/5 평점"]
[고객 후기 — 3개 카드 (실명+사진+수치)]
[가격표]
[사례 연구 — 상세 1개]
[CTA 반복 + 숫자 증거 반복]
```

### 효과 극대화 원칙
- 유사성: 타겟과 비슷한 사람/기업의 증거가 가장 효과적
- 구체성: "많은 기업" < "12,847개 팀" < "같은 업종 347개 기업"
- 최신성: 날짜가 있는 후기가 없는 것보다 효과적
- 다양성: 한 종류가 아닌 2~3종류 조합이 효과적

## Connections

### REQUIRES (1)

- ← [[marketing.persuasion.role]] `w=0.9`

### FEEDS (3)

- ← [[marketing.persuasion.hook-model]] `w=0.7`
- → [[marketing.persuasion.reciprocity]] `w=0.7`
- → [[marketing.persuasion.verify]] `w=0.8`

### CO_CREATES (6)

- → [[marketing.persuasion.anchoring]] `w=0.6`
- → [[marketing.persuasion.authority]] `w=0.6`
- ← [[marketing.persuasion.hook-model]] `w=0.6`
- ← [[marketing.persuasion.nudge]] `w=0.6`
- → [[marketing.persuasion.reciprocity]] `w=0.6`
- ← [[marketing.persuasion.role]] `w=0.6`
