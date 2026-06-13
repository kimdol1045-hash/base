---
id: "marketing.growth.growth-hack"
domain: "marketing"
type: "pattern"
region: SENSORS
token_estimate: 500
theory: "#65 Scarcity (Cialdini, 1984), #61 Hook Model (Eyal, 2014)"
tags: [marketing, growth, aarrr, viral-loop, referral, plg, north-star]
---

# marketing.growth.growth-hack

> **Region**: 📡 [[SENSORS]]  
> **Domain**: `marketing`  
> **Type**: `pattern`  
> **Theory**: #65 Scarcity (Cialdini, 1984), #61 Hook Model (Eyal, 2014)  
> **Tokens**: 500

## Content

그로스 해킹 전략 — 제품 자체에 성장 엔진을 내장하여 사용자가 더 많은 사용자를 데려오게 하는 전략:

### AARRR Pirate Metrics 프레임워크
```
Acquisition   → "사용자가 어떻게 우리를 발견하는가?"
┃               측정: 방문자 수, 채널별 CAC, 유입 경로
▼
Activation    → "사용자가 첫 가치를 경험했는가?" (Aha Moment)
┃               측정: 가입→핵심행동 전환율 (목표: > 40%)
▼
Retention     → "사용자가 다시 돌아오는가?"
┃               측정: D1 리텐션 > 40%, W1 > 35%, M1 > 25%
▼
Revenue       → "사용자가 비용을 지불하는가?"
┃               측정: 전환율, ARPU, LTV, LTV/CAC > 3x
▼
Referral      → "사용자가 다른 사용자를 데려오는가?"
                측정: 바이럴 계수(K), 초대 전환율, NPS > 40
```

### 바이럴 루프 설계 (Dropbox Model)
```
┌──────────────┐    초대     ┌──────────────┐
│  기존 사용자  │ ─────────→ │  신규 사용자  │
│  (인센티브)   │           │  (가치 인식)   │
└──────┬───────┘           └──────┬───────┘
       │                          │
       │    ← 보상 ←─────────────┘
       │    (양쪽 모두 혜택)        가입 완료
       ▼
  더 많은 초대
```

```typescript
// DO: 양면 인센티브 레퍼럴 시스템
const referralProgram = {
  // 추천인: 친구가 가입하면 Pro 1개월 무료
  referrer: {
    reward: "pro_1_month",
    maxRewards: 12,              // 연간 최대 12개월 무료
    triggerEvent: "friend_signup_completed",
  },
  // 피추천인: 가입 시 Pro 14일 무료 체험
  referee: {
    reward: "pro_14_days",
    triggerEvent: "signup",
  },
  // 바이럴 루프: 피추천인도 추천 가능
  viralLoop: true,
  // 링크 생성
  generateLink: (userId: string) =>
    `https://app.example.com/invite/${userId}`,
  // 공유 채널: 이메일, 카카오톡, 링크 복사
  shareChannels: ["email", "kakao", "link"],
};
```

### Product-Led Growth (PLG) 패턴
```
핵심: 제품 사용 자체가 마케팅 + 영업 역할

1. 무료 플랜 / Freemium
   - 핵심 가치는 무료 제공 (사용자 확보)
   - 고급 기능으로 업셀 (수익화)
   - 예: Slack 무료 (10K 메시지) → Pro (무제한)

2. 제품 내 바이럴
   - "Powered by AppName" 워터마크 (무료 플랜)
   - 공유 가능한 산출물 (보고서, 대시보드 공개 링크)
   - 협업 초대 (팀원 추가 = 자연스러운 확산)

3. Self-serve 온보딩
   - 영업 없이 가입→결제 가능
   - 인터랙티브 튜토리얼, 템플릿
   - Time to Value < 5분
```

### North Star Metric 설정
```
North Star Metric = 고객 가치를 대표하는 단일 지표

예시:
- Slack: "주간 활성 팀 수" (팀 단위 사용이 핵심 가치)
- Airbnb: "예약된 숙박 일수" (호스트+게스트 양면 가치)
- Spotify: "주당 청취 시간" (콘텐츠 소비가 핵심 가치)

하위 지표 분해:
North Star = 신규 사용자 x 활성화율 x 핵심행동 빈도
각 하위 지표별로 담당 팀 배정 → OKR 연결
```

### DO: 건강한 성장 전략
```
✓ AARRR 각 단계에 측정 이벤트 설정 (GA4/Mixpanel/Amplitude)
✓ Activation → Retention → Revenue 순서로 최적화 (깔때기 아래부터)
✓ 바이럴 계수(K) = 초대 수 x 전환율 → K > 0.5 목표
✓ 양면 인센티브: 추천인 + 피추천인 모두 혜택
✓ 주 2~3개 소규모 실험, ICE 스코어(Impact x Confidence x Ease)로 우선순위
```

DON'T:
```
❌ Retention 없이 Acquisition만 최적화:
새 사용자 1,000명/주 유입 + 주간 리텐션 5%
= 매주 950명 유출, 새로운 물을 채우는 구멍난 양동이
→ 반드시 Retention 먼저 개선 후 Acquisition 스케일

❌ 허영 지표(Vanity Metrics)에 의존:
"가입자 100만명!" → 활성 사용자는 2만명
"페이지뷰 500만!" → 전환은 100건
→ 의사결정은 활성 사용자, 전환율, 리텐션 기준

❌ 강제 바이럴:
"초대 3명 안 하면 기능 제한" → 사용자 반발 + 리뷰 테러
→ 자연스러운 가치 기반 공유만 유도
```

## Connections

### CO_CREATES (4)

- → [[marketing.growth.landing-page]] `w=0.6`
- ← [[marketing.growth.role]] `w=0.6`
- → [[marketing.growth.social-media]] `w=0.6`
- → [[marketing.growth.verify]] `w=0.6`
