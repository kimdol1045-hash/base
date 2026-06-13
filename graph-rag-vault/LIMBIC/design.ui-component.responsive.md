---
id: "design.ui-component.responsive"
domain: "design"
type: "rule"
region: LIMBIC
token_estimate: 500
theory: "#47 Responsive Web Design (Marcotte, 2010)"
tags: [design, ui, responsive, mobile-first, breakpoints, tailwind, layout]
---

# design.ui-component.responsive

> **Region**: 💜 [[LIMBIC]]  
> **Domain**: `design`  
> **Type**: `rule`  
> **Theory**: #47 Responsive Web Design (Marcotte, 2010)  
> **Tokens**: 500

## Content

반응형 설계 — 모바일 퍼스트로 설계하고, 더 큰 화면으로 점진적 확장한다.

### 1. 브레이크포인트 전략 (Tailwind CSS)
| 접두사 | 최소 너비 | 대상 디바이스 |
|--------|----------|-------------|
| (기본) | 0px | 모바일 (320px~) |
| sm: | 640px | 큰 모바일 / 작은 태블릿 |
| md: | 768px | 태블릿 |
| lg: | 1024px | 작은 데스크톱 |
| xl: | 1280px | 데스크톱 |
| 2xl: | 1536px | 큰 데스크톱 |

핵심 원칙: 모바일 스타일을 기본으로 작성하고, 큰 화면에서만 접두사 추가.

DO:
```tsx
{/* 모바일: 1열, 태블릿: 2열, 데스크톱: 3열 */}
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
  <Card />
  <Card />
  <Card />
</div>
```

DON'T:
```tsx
{/* 데스크톱 먼저 -> 모바일에서 깨짐 */}
<div className="grid grid-cols-3 sm:grid-cols-1">
  <Card />
</div>
```

### 2. 컨테이너 너비 제한
- 최대 너비: max-w-7xl (1280px) — 일반 콘텐츠
- 좁은 콘텐츠: max-w-2xl (672px) — 블로그, 폼
- 전폭 레이아웃: max-w-full + 좌우 패딩 px-4 sm:px-6 lg:px-8
- 항상 mx-auto로 중앙 정렬

```tsx
<div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
  {/* 콘텐츠 */}
</div>
```

### 3. 텍스트 반응형
- 제목: text-2xl sm:text-3xl lg:text-4xl (단계적 확대)
- 본문: text-sm sm:text-base (기본은 14px, 태블릿 이상 16px)
- 최대 줄 길이: max-w-prose (65ch) — 가독성 한계
- clamp() 대안: text-[clamp(1.25rem,3vw,2rem)]

DO:
```tsx
<h1 className="text-2xl font-bold sm:text-3xl lg:text-4xl">
  반응형 제목
</h1>
<p className="text-sm sm:text-base max-w-prose text-muted-foreground">
  본문 텍스트는 최대 65자 너비로 제한하여 가독성을 확보합니다.
</p>
```

### 4. 레이아웃 패턴 전환
- 네비게이션: 모바일=햄버거 메뉴, md+=수평 네비게이션
- 사이드바: 모바일=시트(Sheet), lg+=고정 사이드바
- 테이블: 모바일=카드 리스트, md+=테이블
- 그리드: 모바일=1열 스택, 점진적으로 열 추가

```tsx
{/* 네비게이션 반응형 전환 */}
<nav className="flex items-center justify-between">
  <Logo />
  {/* 모바일: 햄버거 */}
  <Sheet>
    <SheetTrigger asChild className="md:hidden">
      <Button variant="ghost" size="icon">
        <Menu className="h-5 w-5" />
      </Button>
    </SheetTrigger>
    <SheetContent>
      <NavLinks className="flex flex-col gap-4" />
    </SheetContent>
  </Sheet>
  {/* 데스크톱: 수평 네비 */}
  <NavLinks className="hidden md:flex md:gap-6" />
</nav>
```

### 5. 이미지 반응형
- next/image 사용, sizes 속성 필수
- 모바일: 100vw, 태블릿: 50vw, 데스크톱: 33vw
- aspect-ratio로 비율 유지 (CLS 방지)
- 장식 이미지: hidden sm:block으로 모바일에서 숨기기

```tsx
<Image
  src="/hero.jpg"
  alt="히어로 이미지"
  width={1200}
  height={600}
  className="w-full h-auto rounded-lg object-cover aspect-[2/1]"
  sizes="(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw"
  priority
/>
```

### 6. 숨기기 vs 재배치
- 콘텐츠를 숨기지 말고 레이아웃을 변경한다
- 부가 정보만 hidden sm:block 허용 (핵심 콘텐츠 숨김 금지)
- order 클래스로 시각 순서 조정: order-first sm:order-none

## Connections

### REQUIRES (1)

- ← [[design.ui-component.role]] `w=0.9`

### FEEDS (3)

- → [[design.ui-component.accessibility]] `w=0.7`
- ← [[design.ui-component.spacing]] `w=0.7`
- → [[design.ui-component.verify]] `w=0.8`
