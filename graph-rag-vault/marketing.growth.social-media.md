---
id: "marketing.growth.social-media"
domain: "marketing"
type: "rule"
bloom_level: ""
tags: ["marketing", "growth", "social-media", "og-tags", "viral", "community", "content"]
brain_region: "SENSORS"
token_estimate: 500
---

# marketing.growth.social-media

> #64 Social Proof (Cialdini, 1984)

소셜 미디어 마케팅 — 플랫폼 특성에 맞는 네이티브 콘텐츠로 도달, 참여, 전환을 최적화:

### 플랫폼별 콘텐츠 전략
| 플랫폼 | 최적 포맷 | 길이 | 게시 빈도 | 핵심 전략 |
|--------|----------|------|----------|----------|
| Twitter/X | 스레드, 짧은 인사이트 | 280자 x 5~10개 | 일 1~3회 | 스레드 첫 트윗이 Hook |
| LinkedIn | 롱폼 텍스트, 캐러셀 | 1,300자 | 주 3~5회 | 전문성 + 개인 경험 |
| Instagram | 릴스, 캐러셀 | 릴스 30~60초 | 주 4~5회 | 비주얼 + 짧은 교육 |
| YouTube | 롱폼 영상, Shorts | 8~15분 / 60초 | 주 1~2회 | 썸네일 CTR > 10% |
| TikTok | 숏폼 영상 | 15~60초 | 일 1~2회 | 처음 3초에 Hook |

### Twitter/X 스레드 패턴
```
DO: Hook → Value → CTA 구조

1/ [Hook] 매출 0원에서 MRR 5,000만원까지 12개월.
아무도 안 알려주는 SaaS 성장 전략 7가지:
🧵👇

2/ 전략 1: 무료 도구로 리드 확보
가격 계산기, ROI 시뮬레이터 등 무료 도구를 만들어
자연 유입 트래픽을 확보했습니다.
→ 월 3,000명 유입 (유료 광고 0원)

...

10/ 요약:
1. 무료 도구 → 자연 유입
2. 온보딩 이메일 → 활성화
3. 고객 성공 사례 → 신뢰
...

11/ 이 전략을 더 자세히 알고 싶다면
[링크] 에서 전체 가이드를 받아보세요.

이 스레드가 도움이 됐다면 RT 부탁드려요 🙏
```

### Open Graph 최적화 (링크 공유 시 미리보기)
```typescript
// DO: 플랫폼별 OG 태그 최적화
export const metadata: Metadata = {
  openGraph: {
    title: "SaaS 성장 전략 7가지 — 0 → MRR 5천만원",  // 60자 이내
    description: "12개월간 검증된 실전 그로스 해킹 전략",   // 155자 이내
    images: [{
      url: "/og/growth-strategy.png",
      width: 1200,                    // Facebook/LinkedIn 권장
      height: 630,
      alt: "SaaS 성장 전략 인포그래픽",
    }],
    type: "article",
    siteName: "AppName Blog",
  },
  twitter: {
    card: "summary_large_image",      // 큰 이미지 카드
    title: "SaaS 성장 전략 7가지",
    description: "0 → MRR 5천만원, 12개월 실전 가이드",
    images: ["/og/growth-strategy-twitter.png"],  // 2:1 비율
  },
};
```

### 바이럴 메커닉스 (공유 트리거)
```
사람들이 공유하는 5가지 이유 (Jonah Berger, Contagious):

1. Social Currency (사회적 화폐)
   → "이걸 공유하면 내가 똑똑해 보여"
   → 데이터, 인사이트, 독점 정보 콘텐츠

2. Triggers (연상 촉발)
   → 일상에서 자연스럽게 떠오르는 연결고리
   → "매주 월요일" "매일 아침" 루틴 연결

3. Emotion (감정 자극)
   → 경외감, 놀라움, 분노 (고각성 감정이 공유율 높음)
   → 저각성 감정(슬픔, 만족)은 공유율 낮음

4. Public (가시성)
   → 사용하는 모습이 다른 사람에게 보임
   → "Powered by AppName" 배지, 공유 가능한 대시보드

5. Practical Value (실용적 가치)
   → "이거 유용하니까 알려줘야지"
   → How-to 가이드, 체크리스트, 템플릿
```

### 커뮤니티 빌딩 전략
```
Level 1: 일방향 콘텐츠 발행 (팔로워 확보)
Level 2: 댓글/DM 적극 응답 (관계 형성)
Level 3: UGC 유도 — 해시태그 챌린지, 사례 공유
Level 4: 전용 커뮤니티 — Slack, Discord, 카카오 오픈채팅
Level 5: 앰배서더 프로그램 — 핵심 팬 10~30명 관리
```

DON'T:
```
❌ 모든 플랫폼에 동일 콘텐츠 복사:
LinkedIn 글을 그대로 Twitter에 → 300자 잘림, 포맷 깨짐
→ 각 플랫폼 네이티브 포맷에 맞게 재가공

❌ OG 태그 미설정:
링크 공유 시 제목/이미지 없이 URL만 표시
→ CTR 50% 이상 하락

❌ Engagement bait:
"좋아요 누르면 행운이!" "이거 공유 안 하면 불행이!"
→ 알고리즘 패널티 + 브랜드 신뢰 하락

❌ 불규칙한 게시:
한 달에 10개 → 2개월 공백 → 다시 폭발 게시
→ 일관된 스케줄이 알고리즘 + 팔로워 기대 형성
```

## Connections

- [[marketing.growth.role]] — REQUIRES (weight: 0.9)
- [[marketing.growth.verify]] — FEEDS (weight: 0.8)
- [[marketing.growth.landing-page]] — FEEDS (weight: 0.7)
- [[marketing.growth.email-sequence]] — FEEDS (weight: 0.7)
- [[marketing.copy.cta]] — FEEDS (weight: 0.5)
- [[marketing.growth.role]] — CO_CREATES (weight: 0.6)
- [[marketing.growth.growth-hack]] — CO_CREATES (weight: 0.6)
- [[marketing.growth.landing-page]] — CO_CREATES (weight: 0.6)
- [[marketing.growth.verify]] — CO_CREATES (weight: 0.6)
