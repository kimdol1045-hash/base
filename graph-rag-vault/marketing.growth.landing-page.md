---
id: "marketing.growth.landing-page"
domain: "marketing"
type: "pattern"
bloom_level: ""
tags: ["marketing", "growth", "landing-page", "cro", "conversion", "aida", "fogg"]
brain_region: "SENSORS"
token_estimate: 500
---

# marketing.growth.landing-page

> #56 AIDA (Strong, 1925), #63 Fogg Behavior Model (Fogg, 2009)

랜딩 페이지 설계 — AIDA 구조와 Fogg 행동 모델을 결합하여 전환율을 극대화하는 패턴:

### Above-the-Fold 구조 (스크롤 없이 보이는 영역)
```
┌─────────────────────────────────────────────────┐
│ [로고]                    [로그인] [무료 시작하기] │  ← 네비게이션 최소화
│                                                  │
│   팀 생산성을 34% 높이는                          │  ← 헤드라인 (이점 + 수치)
│   프로젝트 관리의 새로운 방법                       │
│                                                  │
│   칸반 보드, 자동화, 실시간 협업으로                │  ← 서브헤드 (HOW)
│   매주 5시간을 절약하세요.                         │
│                                                  │
│        [무료로 시작하기]                           │  ← Primary CTA (1개만)
│   카드 등록 없이 14일 체험 | 2분 만에 설정          │  ← 리스크 제거
│                                                  │
│   ⭐ 4.8/5 (2,341개 리뷰) | 12,000+ 팀 사용      │  ← 소셜 프루프
│   [삼성] [카카오] [토스] [배민] [당근]              │  ← 로고월
└─────────────────────────────────────────────────┘
```

### Fogg 행동 모델 적용
```
행동 = 동기(Motivation) x 능력(Ability) x 촉발(Prompt)

동기 ↑: 이점 중심 헤드라인, 사회적 증거, 손실 회피 카피
능력 ↑: 폼 필드 최소화 (이름 + 이메일만), 원클릭 가입
촉발 ✓: 명확한 CTA 1개, 스크롤 시 CTA 반복, 긴급성 요소
```

### F-패턴 레이아웃 (시선 흐름)
```
시선 흐름:
████████████████████  ← 헤드라인 (가로 스캔)
████████████████      ← 서브헤드 (가로 스캔)
████                  ← CTA 버튼 (시선 정지)
████████████          ← 소셜 프루프 (가로 스캔)
██                    ← 세로 스캔 시작
██
██
핵심 요소는 F 패턴의 '가로선' 위치에 배치
```

### DO: 전환율 높이는 패턴
```html
<!-- 이점 중심 헤드라인 (Feature X → Benefit O) -->
<h1>매주 금요일 야근을 없애는 리포트 자동화</h1>
<p>AI가 데이터를 분석하고, 리포트를 자동 생성합니다.
   매주 5시간을 전략 기획에 쓰세요.</p>

<!-- CTA: 행동 동사 + 구체적 결과 -->
<button>무료로 리포트 자동화 시작하기</button>
<p class="subtext">30초 가입 | 카드 등록 불필요 | 언제든 취소</p>

<!-- 소셜 프루프를 CTA 근처에 배치 -->
<div class="social-proof">
  <img src="/stars.svg" /> 4.8/5 (2,341개 리뷰)
  <span>| 이번 주 89명 가입</span>
</div>
```

DON'T:
```html
<!-- ❌ 복수 CTA가 경쟁 — 선택 마비 유발 -->
<button>무료 시작</button>
<button>데모 예약</button>
<button>가격 보기</button>
<a href="/docs">문서 보기</a>
<!-- Hick's Law: 선택지가 많을수록 결정 시간 증가 → 이탈 -->

<!-- ❌ 기능 중심 헤드라인 (사용자 이점 없음) -->
<h1>AI 기반 실시간 데이터 파이프라인 솔루션</h1>
<!-- "그래서 나한테 뭐가 좋은데?"에 답하지 못함 -->

<!-- ❌ 소셜 프루프 없음 -->
<!-- 신뢰 요소 0 → "이거 믿을 만해?" 의구심 → 이탈 -->
```

### A/B 테스트 우선순위 (영향도 순)
| 요소 | 테스트 예시 | 기대 전환율 변화 |
|------|-----------|---------------|
| 헤드라인 | 이점형 vs 고통형 | +10~30% |
| CTA 문구 | "무료로 시작" vs "지금 체험" | +5~15% |
| 소셜 프루프 위치 | CTA 위 vs 아래 | +3~10% |
| 폼 필드 수 | 4개 → 2개 | +10~25% |
| 페이지 로딩 속도 | 4초 → 2초 | +7~12% |

### 필수 기준
- 로딩 시간: 3초 이내 (1초 지연 → 전환율 7% 하락)
- 모바일 최적화: 트래픽 60%+ 모바일, 반드시 우선
- CTA 버튼: 대비 높은 색상, 최소 44x44px 터치 영역

## Connections

- [[marketing.growth.role]] — REQUIRES (weight: 0.9)
- [[marketing.growth.verify]] — FEEDS (weight: 0.8)
- [[marketing.growth.growth-hack]] — FEEDS (weight: 0.7)
- [[marketing.growth.social-media]] — FEEDS (weight: 0.7)
- [[marketing.copy.cta]] — FEEDS (weight: 0.5)
- [[marketing.growth.role]] — CO_CREATES (weight: 0.6)
- [[marketing.growth.growth-hack]] — CO_CREATES (weight: 0.6)
- [[marketing.growth.social-media]] — CO_CREATES (weight: 0.6)
- [[marketing.growth.verify]] — CO_CREATES (weight: 0.6)
