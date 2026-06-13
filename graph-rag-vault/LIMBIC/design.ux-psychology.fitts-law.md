---
id: "design.ux-psychology.fitts-law"
domain: "design"
type: "rule"
region: LIMBIC
token_estimate: 500
theory: "#42 피츠 법칙 (Fitts, 1954)"
tags: [design, ux, fitts-law, touch-target, mobile, thumb-zone, cta]
---

# design.ux-psychology.fitts-law

> **Region**: 💜 [[LIMBIC]]  
> **Domain**: `design`  
> **Type**: `rule`  
> **Theory**: #42 피츠 법칙 (Fitts, 1954)  
> **Tokens**: 500

## Content

피츠 법칙 — 타겟까지 이동 시간 = f(거리/크기).
MT = a + b * log2(D/W + 1) — 거리 D ↓, 크기 W ↑ → 더 빠른 접근.

### 핵심 수치 기준
- CTA 버튼 최소: **44x44px** (WCAG 터치 타겟)
- 주요 버튼 권장: **48px** 높이, 좌우 패딩 **px-6** (24px)
- 터치 타겟 간 최소 간격: **8px** (오탭 방지)
- 모바일 핵심 액션: **thumb zone** (화면 하단 1/3) 배치
- 화면 모서리/가장자리: 무한 타겟 효과 활용

### 1. 모바일 CTA — Thumb Zone 배치

DO:
```tsx
{/* 핵심 CTA를 하단 고정 → thumb zone 최적 위치 */}
<div className="fixed bottom-0 inset-x-0 p-4 bg-background/80 backdrop-blur-sm border-t">
  <Button className="w-full h-12 text-base font-semibold">
    구매하기
  </Button>
</div>
{/* 본문 콘텐츠에 하단 패딩 추가 */}
<main className="pb-24">
  {/* ... */}
</main>
```

DON'T:
```tsx
{/* CTA가 스크롤 중간에 작은 크기로 배치 → 찾기 어렵고 탭 어려움 */}
<Button className="h-8 px-3 text-xs mt-2">구매하기</Button>
```

### 2. 터치 타겟 간격

```tsx
{/* 아이콘 버튼 그룹: 44px 타겟 + 8px 간격 */}
<div className="flex items-center gap-2">
  <Button variant="ghost" size="icon" className="h-11 w-11">
    <Heart className="h-5 w-5" />
    <span className="sr-only">좋아요</span>
  </Button>
  <Button variant="ghost" size="icon" className="h-11 w-11">
    <Share className="h-5 w-5" />
    <span className="sr-only">공유</span>
  </Button>
  <Button variant="ghost" size="icon" className="h-11 w-11">
    <Bookmark className="h-5 w-5" />
    <span className="sr-only">저장</span>
  </Button>
</div>
```

### 3. 모바일 Bottom Navigation — 가장자리 활용

```tsx
{/* 하단 네비: 화면 가장자리 → 무한 타겟 효과 */}
<nav className="fixed bottom-0 inset-x-0 bg-background border-t
                flex justify-around items-center h-16 pb-safe">
  {[
    { icon: Home, label: "홈", href: "/" },
    { icon: Search, label: "검색", href: "/search" },
    { icon: PlusCircle, label: "작성", href: "/new" },
    { icon: Bell, label: "알림", href: "/notifications" },
    { icon: User, label: "내 정보", href: "/profile" },
  ].map(({ icon: Icon, label, href }) => (
    <Link key={href} href={href}
      className="flex flex-col items-center gap-1 min-w-[48px] min-h-[48px]
                 justify-center text-muted-foreground hover:text-primary">
      <Icon className="h-5 w-5" />
      <span className="text-[10px]">{label}</span>
    </Link>
  ))}
</nav>
```

### 4. 데스크톱 — 주요 액션 크기 차별화

```tsx
{/* 주요 CTA > 보조 액션 크기로 계층 표현 */}
<div className="flex items-center gap-3">
  <Button size="lg" className="h-12 px-8 text-base">프로젝트 생성</Button>
  <Button variant="outline" size="sm" className="h-9">가져오기</Button>
</div>
```

### 측정 기준
- 터치 성공률: 44px → 95%+, 32px → 85%, 24px → 70%
- 모바일 CTA 클릭률: 하단 고정 vs 스크롤 내 → 약 30% 향상

## Connections

### REQUIRES (1)

- ← [[design.ux-psychology.role]] `w=0.9`

### FEEDS (2)

- → [[design.ux-psychology.hicks-law]] `w=0.7`
- → [[design.ux-psychology.verify]] `w=0.8`
