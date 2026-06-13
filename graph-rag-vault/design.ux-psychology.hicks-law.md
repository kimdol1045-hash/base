---
id: "design.ux-psychology.hicks-law"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ux", "hicks-law", "decision-time", "navigation", "form", "progressive-disclosure"]
brain_region: "CORTEX"
token_estimate: 500
---

# design.ux-psychology.hicks-law

> #41 힉스 법칙 (Hick, 1952)

힉스 법칙 — 선택지 수가 증가하면 결정 시간이 로그 비례로 증가한다.
RT = a + b * log2(n+1) — 선택지 n개일 때 반응 시간 RT.

### 핵심 원칙
- 한 화면의 선택지: **3-5개** 이하로 제한
- 7개 이상 → 카테고리 그룹핑 또는 프로그레시브 디스클로저
- 10개 이상 → 검색/필터 UI 필수 제공

### 1. 네비게이션 메뉴 — 5개 이하 유지

DO:
```tsx
{/* 최상위 메뉴 5개, 하위는 드롭다운으로 숨김 */}
<nav className="flex items-center gap-6">
  <NavLink href="/dashboard">대시보드</NavLink>
  <NavLink href="/projects">프로젝트</NavLink>
  <NavLink href="/analytics">분석</NavLink>
  <NavLink href="/team">팀</NavLink>
  <DropdownMenu>
    <DropdownMenuTrigger className="text-sm text-muted-foreground">
      더보기 <ChevronDown className="ml-1 h-4 w-4" />
    </DropdownMenuTrigger>
    <DropdownMenuContent>
      <DropdownMenuItem>설정</DropdownMenuItem>
      <DropdownMenuItem>도움말</DropdownMenuItem>
      <DropdownMenuItem>API 문서</DropdownMenuItem>
    </DropdownMenuContent>
  </DropdownMenu>
</nav>
```

DON'T:
```tsx
{/* 8개 메뉴가 한 줄에 나열 → 결정 시간 증가, 시각 과부하 */}
<nav className="flex gap-4">
  <NavLink>대시보드</NavLink><NavLink>프로젝트</NavLink>
  <NavLink>분석</NavLink><NavLink>팀</NavLink>
  <NavLink>설정</NavLink><NavLink>도움말</NavLink>
  <NavLink>API</NavLink><NavLink>요금</NavLink>
</nav>
```

### 2. 폼 설계 — 프로그레시브 디스클로저

```tsx
{/* 복잡한 폼을 단계별로 분리 → 각 단계 선택지 3-4개 */}
<div className="space-y-6">
  <div className="flex items-center gap-2 text-sm text-muted-foreground">
    <span className="font-medium text-primary">1. 기본 정보</span>
    <ChevronRight className="h-4 w-4" />
    <span>2. 상세 설정</span>
    <ChevronRight className="h-4 w-4" />
    <span>3. 확인</span>
  </div>
  {/* 현재 단계의 3개 필드만 표시 */}
  <div className="space-y-4">
    <Input placeholder="프로젝트 이름" />
    <Select><SelectTrigger>카테고리 선택</SelectTrigger></Select>
    <Textarea placeholder="간단한 설명" rows={3} />
  </div>
  <Button className="w-full">다음 단계</Button>
</div>
```

### 3. 카테고리 그룹핑 — 설정 화면

```tsx
{/* 20개 설정을 4개 그룹으로 분류 → 각 그룹 5개 이하 */}
<div className="space-y-8">
  {["일반", "알림", "보안", "결제"].map((group) => (
    <section key={group} className="rounded-lg border p-6 space-y-4">
      <h3 className="text-lg font-semibold">{group}</h3>
      {/* 그룹당 3-5개 설정 항목 */}
    </section>
  ))}
</div>
```

### 측정 지표
- 메뉴 클릭 결정 시간: 5개 이하 → 평균 1.5초, 10개 이상 → 평균 4초+
- 폼 완료율: 한 화면 10개 필드 → 약 20% 이탈, 3-4개 단계 분리 → 이탈 60% 감소

## Connections

- [[design.ux-psychology.role]] — REQUIRES (weight: 0.9)
- [[design.ux-psychology.verify]] — FEEDS (weight: 0.8)
- [[design.ux-psychology.fitts-law]] — FEEDS (weight: 0.7)
- [[design.ux-psychology.jakobs-law]] — FEEDS (weight: 0.7)
