---
id: "design.wireframe.layout"
domain: "design"
type: "pattern"
region: LIMBIC
token_estimate: 420
theory: "#49 Grid Systems (Müller-Brockmann, 1961)"
tags: [design, wireframe, layout, grid, responsive]
---

# design.wireframe.layout

> **Region**: 💜 [[LIMBIC]]  
> **Domain**: `design`  
> **Type**: `pattern`  
> **Theory**: #49 Grid Systems (Müller-Brockmann, 1961)  
> **Tokens**: 420

## Content

레이아웃 패턴 (페이지 구조를 결정하는 검증된 패턴):

### 1. Sidebar + Main (대시보드, 관리자)
```tsx
<div className="flex min-h-screen">
  <aside className="hidden w-64 border-r lg:block">
    {/* 사이드바 네비게이션 */}
  </aside>
  <main className="flex-1 p-6">{children}</main>
</div>
```

### 2. Top Nav + Content (일반 웹앱)
```tsx
<div className="flex min-h-screen flex-col">
  <header className="sticky top-0 z-50 border-b bg-background/80 backdrop-blur">
    <nav className="mx-auto flex h-14 max-w-7xl items-center px-4">
      {/* 로고 + 메뉴 + CTA */}
    </nav>
  </header>
  <main className="flex-1">{children}</main>
  <footer className="border-t py-8">{/* 푸터 */}</footer>
</div>
```

### 3. 12-Column Grid (반응형 콘텐츠)
```tsx
<div className="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
  <Card /><Card /><Card />
</div>
```

### 반응형 전환 규칙
| 화면 | 레이아웃 | Tailwind |
|------|---------|---------|
| 모바일 (< 768px) | 세로 스택, 풀 너비 | 기본 |
| 태블릿 (768px+) | 2열 그리드 | md: |
| 데스크톱 (1024px+) | 사이드바 + 메인 | lg: |

### 콘텐츠 너비 제한
- 텍스트: max-w-prose (65ch)
- 페이지: max-w-7xl (1280px) mx-auto
- 폼: max-w-md (448px)

## Connections

### CO_CREATES (2)

- ← [[design.wireframe.role]] `w=0.6`
- → [[design.wireframe.verify]] `w=0.6`
