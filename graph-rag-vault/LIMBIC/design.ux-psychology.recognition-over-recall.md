---
id: "design.ux-psychology.recognition-over-recall"
domain: "design"
type: "rule"
region: LIMBIC
token_estimate: 500
theory: "#45 재인 vs 회상 (Nielsen, 1993)"
tags: [design, ux, recognition, recall, autocomplete, search, form, navigation]
---

# design.ux-psychology.recognition-over-recall

> **Region**: 💜 [[LIMBIC]]  
> **Domain**: `design`  
> **Type**: `rule`  
> **Theory**: #45 재인 vs 회상 (Nielsen, 1993)  
> **Tokens**: 500

## Content

재인 > 회상 — 사용자에게 기억에서 꺼내라고 요구하지 말고, 보여주고 선택하게 하라.
회상(recall)은 인지 부하가 높고, 재인(recognition)은 단서만 있으면 즉시 작동한다.

### 우선순위: 빈칸 입력 < 선택지 제시 < 자동완성/추천

### 1. 검색 — 자동완성 + 최근 검색

```tsx
{/* 빈 검색창 대신: 최근 검색어 + 자동완성으로 재인 지원 */}
<Command className="rounded-lg border shadow-md">
  <CommandInput placeholder="검색어를 입력하세요..." />
  <CommandList>
    <CommandEmpty>결과가 없습니다.</CommandEmpty>
    <CommandGroup heading="최근 검색">
      {recentSearches.map((term) => (
        <CommandItem key={term}>
          <Clock className="mr-2 h-4 w-4 text-muted-foreground" />
          {term}
        </CommandItem>
      ))}
    </CommandGroup>
    <CommandSeparator />
    <CommandGroup heading="추천 검색어">
      {suggestions.map((s) => (
        <CommandItem key={s.id}>
          <TrendingUp className="mr-2 h-4 w-4 text-muted-foreground" />
          {s.label}
        </CommandItem>
      ))}
    </CommandGroup>
  </CommandList>
</Command>
```

### 2. 폼 입력 — 선택지 > 빈칸

DO:
```tsx
{/* 드롭다운으로 선택지 제시 → 회상 불필요 */}
<div className="space-y-4">
  <div className="space-y-1.5">
    <Label>직종</Label>
    <Select>
      <SelectTrigger><SelectValue placeholder="직종을 선택하세요" /></SelectTrigger>
      <SelectContent>
        <SelectItem value="frontend">프론트엔드 개발자</SelectItem>
        <SelectItem value="backend">백엔드 개발자</SelectItem>
        <SelectItem value="design">UI/UX 디자이너</SelectItem>
        <SelectItem value="pm">프로덕트 매니저</SelectItem>
      </SelectContent>
    </Select>
  </div>
  <div className="space-y-1.5">
    <Label>경력</Label>
    <RadioGroup defaultValue="mid" className="flex gap-4">
      <RadioGroupItem value="junior" label="1-3년" />
      <RadioGroupItem value="mid" label="4-7년" />
      <RadioGroupItem value="senior" label="8년+" />
    </RadioGroup>
  </div>
</div>
```

DON'T:
```tsx
{/* 빈칸에 직접 입력 요구 → 높은 인지 부하, 입력 오류 */}
<Input placeholder="직종을 입력하세요" />
<Input placeholder="경력 연차를 입력하세요" />
```

### 3. 네비게이션 — 현재 위치 표시

```tsx
{/* 브레드크럼 + 활성 메뉴 강조 → "내가 어디 있지?" 회상 불필요 */}
<Breadcrumb>
  <BreadcrumbItem><BreadcrumbLink href="/">홈</BreadcrumbLink></BreadcrumbItem>
  <BreadcrumbSeparator />
  <BreadcrumbItem><BreadcrumbLink href="/settings">설정</BreadcrumbLink></BreadcrumbItem>
  <BreadcrumbSeparator />
  <BreadcrumbItem><BreadcrumbPage>알림</BreadcrumbPage></BreadcrumbItem>
</Breadcrumb>
```

### 4. 최근 항목 / 즐겨찾기

```tsx
{/* 대시보드 상단에 최근 접근 항목 → 재방문 시 즉시 재인 */}
<section className="space-y-3">
  <h3 className="text-sm font-medium text-muted-foreground">최근 작업</h3>
  <div className="flex gap-3 overflow-x-auto pb-2">
    {recentItems.map((item) => (
      <Link key={item.id} href={item.href}
        className="flex items-center gap-2 rounded-lg border p-3
                   min-w-[200px] hover:bg-accent transition-colors">
        <item.icon className="h-4 w-4 text-muted-foreground shrink-0" />
        <div className="min-w-0">
          <p className="text-sm font-medium truncate">{item.name}</p>
          <p className="text-xs text-muted-foreground">{item.updatedAt}</p>
        </div>
      </Link>
    ))}
  </div>
</section>
```

### 적용 체크리스트
- 텍스트 입력 → 드롭다운/라디오/체크박스로 대체 가능한가?
- 현재 위치/상태가 시각적으로 표시되는가?
- 최근 사용/즐겨찾기 기능이 있는가?
- 검색에 자동완성/추천이 제공되는가?

## Connections

### REQUIRES (1)

- ← [[design.ux-psychology.role]] `w=0.9`

### FEEDS (3)

- ← [[design.ux-psychology.doherty-threshold]] `w=0.7`
- → [[design.ux-psychology.teslers-law]] `w=0.7`
- → [[design.ux-psychology.verify]] `w=0.8`
