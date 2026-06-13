---
id: "marketing.copy.cta"
domain: "marketing"
type: "pattern"
bloom_level: ""
tags: ["marketing", "copy", "cta", "conversion", "nudge", "button", "action"]
brain_region: "SENSORS"
token_estimate: 500
---

# marketing.copy.cta

> #59 Nudge Theory (Thaler & Sunstein, 2008)

CTA (Call to Action) 설계 — 사용자의 행동 마찰을 최소화하고 즉시 행동을 유도한다.
CTA는 카피의 최종 목적지다. 여기서 실패하면 모든 설득이 무의미해진다.

### 1. CTA 문구 공식
**공식: [행동 동사] + [구체적 결과/혜택]**

효과적인 CTA 문구 (DO):
| 유형 | CTA 문구 | 이유 |
|------|---------|------|
| SaaS | "무료로 자동화 시작하기" | 행동+혜택+리스크 제거 |
| 커머스 | "30% 할인가로 주문하기" | 행동+구체적 혜택 |
| 뉴스레터 | "매주 인사이트 받아보기" | 행동+기대 가치 |
| 다운로드 | "무료 가이드북 받기" | 행동+무료+결과물 |
| 상담 | "15분 무료 상담 예약하기" | 행동+시간 구체화+무료 |
| 데모 | "나에게 맞는 플랜 찾기" | 행동+개인화 |

비효과적인 CTA 문구 (DON'T):
| CTA 문구 | 문제점 |
|---------|--------|
| "클릭하세요" | 결과 불명확 |
| "자세히 보기" | 행동이 아닌 탐색 |
| "제출" | 비인간적, 결과 없음 |
| "여기를 눌러주세요" | 모호, 가치 없음 |
| "가입" | 사용자에게 비용만 암시 |

### 2. CTA 시각 설계 규칙
- 색상: 페이지에서 가장 높은 대비 색상 (Primary 색상)
- 크기: 최소 높이 44px, 너비 최소 120px (모바일에서 전폭 권장)
- 여백: CTA 주변 최소 24px 빈 공간 (시각적 고립)
- 위치: Above the Fold에 1개, 페이지 하단에 1개 (긴 페이지)
- 개수: 주요 CTA 1개 + 보조 CTA 최대 1개 (Hick's Law)

```tsx
{/* Primary CTA + 보조 텍스트 */}
<div className="flex flex-col items-center gap-3">
  <Button size="lg" className="w-full sm:w-auto min-w-[200px]">
    무료로 시작하기
  </Button>
  <p className="text-sm text-muted-foreground">
    카드 등록 불필요 · 14일 무료 체험 · 언제든 취소
  </p>
</div>
```

### 3. 리스크 제거 패턴 (Friction Reducers)
CTA 바로 아래에 불안 요소를 해소하는 텍스트를 배치한다.

효과적인 리스크 제거 문구:
- "카드 등록 없이 시작" — 결제 불안 해소
- "14일 무료 체험" — 비용 불안 해소
- "2분이면 설정 완료" — 시간 부담 해소
- "언제든 취소 가능" — 구속 불안 해소
- "100% 환불 보장" — 손실 불안 해소
- "10,000개 팀이 사용 중" — 선택 불안 해소

### 4. 긴급성/희소성 (Scarcity & Urgency)
남용하면 신뢰가 파괴된다. 진실한 경우에만 사용한다.

DO (진실한 긴급성):
```
"얼리버드 할인: 6월 30일까지 (잔여 23석)"
"이번 분기 도입 시 온보딩 무료 지원"
```

DON'T (거짓 긴급성):
```
"지금 안 사면 영원히 못 삽니다!!!"
"딱 1시간 남았습니다!" (매일 반복되는 타이머)
"마지막 기회!!!" (매주 반복)
```

### 5. CTA 배치 전략 (페이지 유형별)
- 랜딩 페이지: Hero CTA + 중간 CTA + 하단 CTA (3회 반복)
- 블로그 포스트: 하단 CTA + 사이드바 CTA
- 가격 페이지: 각 플랜별 CTA + 추천 플랜 강조
- 이메일: 상단 1개 CTA (스크롤 없이 보이는 위치)

### 6. A/B 테스트 우선순위
CTA 최적화 시 테스트 순서:
1. CTA 문구 (가장 큰 영향)
2. CTA 색상/크기
3. 리스크 제거 문구
4. CTA 위치
5. 보조 CTA 유무

## Connections

- [[marketing.copy.role]] — REQUIRES (weight: 0.9)
- [[marketing.copy.verify]] — FEEDS (weight: 0.8)
- [[marketing.copy.storytelling]] — FEEDS (weight: 0.7)
- [[marketing.persuasion.fogg-model]] — FEEDS (weight: 0.5)
- [[marketing.persuasion.scarcity]] — FEEDS (weight: 0.5)
- [[marketing.persuasion.anchoring]] — FEEDS (weight: 0.5)
- [[marketing.persuasion.endowment]] — FEEDS (weight: 0.5)
- [[marketing.persuasion.prospect-theory]] — FEEDS (weight: 0.5)
- [[marketing.growth.landing-page]] — FEEDS (weight: 0.5)
- [[marketing.growth.social-media]] — FEEDS (weight: 0.5)
