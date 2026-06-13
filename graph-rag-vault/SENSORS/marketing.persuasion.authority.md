---
id: "marketing.persuasion.authority"
domain: "marketing"
type: "pattern"
region: SENSORS
token_estimate: 480
theory: "#64 권위 (Cialdini, 1984 Ch.6)"
tags: [marketing, persuasion, authority, trust, certification, credibility]
---

# marketing.persuasion.authority

> **Region**: 📡 [[SENSORS]]  
> **Domain**: `marketing`  
> **Type**: `pattern`  
> **Theory**: #64 권위 (Cialdini, 1984 Ch.6)  
> **Tokens**: 480

## Content

권위의 원칙 — 전문가, 기관, 인증이 신뢰를 만들고 설득력을 높인다:

### 권위 신호 5가지 유형

**1. 전문가 추천 (Expert Endorsement)**
- "서울대 경영학과 김OO 교수 추천"
- "10년차 시니어 개발자가 설계한 커리큘럼"
- "전 구글 엔지니어가 만든 개발 도구"
- 핵심: 해당 분야의 전문가여야 한다 (관련성 필수)

**2. 인증 및 배지 (Certifications & Badges)**
- 보안: SOC 2, ISO 27001, ISMS-P
- 결제: PCI DSS 인증
- 리뷰: G2 Leader, Product Hunt #1
- 수상: 레드닷 디자인 어워드, IF 디자인 어워드
- 배치: 푸터 또는 가격표 근처

**3. 미디어 노출 (Media Mentions)**
- "조선일보, 매일경제, 한국경제에 소개"
- "Forbes, TechCrunch가 주목한 스타트업"
- 미디어 로고 + 기사 발췌문 조합
```
┌─────────────────────────────────────┐
│  "국내 최초 AI 기반 마케팅 자동화"     │
│   — 매일경제, 2025.03                │
│                                      │
│  조선일보 | 한경 | 매경 | Forbes      │
└─────────────────────────────────────┘
```

**4. 데이터 기반 권위 (Data Authority)**
- "10만 건의 A/B 테스트 데이터로 검증"
- "3년간 축적한 업종별 벤치마크"
- "자체 연구 보고서: 이커머스 전환율 트렌드 2025"
- 원본 데이터/연구를 생산하는 것이 최강의 권위

**5. 이력 및 실적 (Track Record)**
- "2019년 창업, 5년간 서비스 운영"
- "누적 처리 건수 500만 건, 무장애 운영 99.99%"
- "국내 1위 시장 점유율 (카테고리 한정 가능)"

### Trust Signals 배치 전략

**랜딩 페이지 배치 맵**:
```
[히어로] ← 미디어 언급 배지
[로고월] ← 고객사 브랜드
[기능 소개]
[실적 수치] ← "10만 팀 | 500만 건 | 99.99%"
[인증 배지] ← SOC2, ISO 등
[전문가 추천] ← 사진 + 직함 + 인용문
[가격표] ← 인증 배지 반복
[CTA] ← "안전한 결제" 아이콘
```

**전환율에 미치는 영향**:
| Trust Signal | 전환율 영향 |
|-------------|-----------|
| 보안 인증 배지 (결제 페이지) | +15~30% |
| 고객사 로고월 | +10~20% |
| 전문가 추천 (사진+실명) | +10~15% |
| 미디어 로고 | +5~15% |
| 리뷰 평점 표시 | +15~25% |

### 한국어 카피 예시
- "정보보호 관리체계(ISMS-P) 인증 완료"
- "금융위원회 등록 핀테크 기업"
- "대한민국 소프트웨어 대상 수상"
- "삼성, 현대, SK 등 Fortune 500 기업이 신뢰합니다"

## Connections

### REQUIRES (1)

- ← [[marketing.persuasion.role]] `w=0.9`

### FEEDS (3)

- ← [[marketing.persuasion.reciprocity]] `w=0.7`
- → [[marketing.persuasion.scarcity]] `w=0.7`
- → [[marketing.persuasion.verify]] `w=0.8`

### CO_CREATES (6)

- → [[marketing.persuasion.anchoring]] `w=0.6`
- ← [[marketing.persuasion.hook-model]] `w=0.6`
- ← [[marketing.persuasion.nudge]] `w=0.6`
- ← [[marketing.persuasion.reciprocity]] `w=0.6`
- ← [[marketing.persuasion.role]] `w=0.6`
- ← [[marketing.persuasion.social-proof]] `w=0.6`
