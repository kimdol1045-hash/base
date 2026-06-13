---
id: "design.ux-psychology.jakobs-law"
domain: "design"
type: "rule"
region: LIMBIC
token_estimate: 500
theory: "#44 제이콥 법칙 (Nielsen, 2000)"
tags: [design, ux, jakobs-law, mental-model, convention, shadcn, standard-pattern]
---

# design.ux-psychology.jakobs-law

> **Region**: 💜 [[LIMBIC]]  
> **Domain**: `design`  
> **Type**: `rule`  
> **Theory**: #44 제이콥 법칙 (Nielsen, 2000)  
> **Tokens**: 500

## Content

제이콥 법칙 — 사용자는 대부분의 시간을 *다른* 사이트에서 보낸다.
따라서 당신의 사이트도 이미 알고 있는 방식으로 동작하길 기대한다.

### 핵심 원칙
- 검증된 UI 패턴을 **우선** 사용 (재발명 금지)
- 커스텀 UI는 명확한 사용성 이득이 있을 때만 허용
- shadcn/ui 등 **표준 컴포넌트 라이브러리** 기반 설계
- 사용자 멘탈 모델과 일치하는 정보 구조

### 1. 검증된 패턴 — E-commerce 레이아웃

DO:
```tsx
{/* 사용자가 이미 아는 표준 패턴: 좌 필터, 우 그리드, 상단 정렬 */}
<div className="flex gap-6">
  <aside className="w-64 shrink-0 space-y-6">
    <FilterSection title="카테고리" options={categories} />
    <FilterSection title="가격대" options={priceRanges} />
    <FilterSection title="브랜드" options={brands} />
  </aside>
  <main className="flex-1 space-y-4">
    <div className="flex items-center justify-between">
      <p className="text-sm text-muted-foreground">1,234개 상품</p>
      <Select defaultValue="popular">
        <SelectTrigger className="w-40">
          <SelectValue placeholder="정렬 기준" />
        </SelectTrigger>
        <SelectContent>
          <SelectItem value="popular">인기순</SelectItem>
          <SelectItem value="price-asc">낮은 가격순</SelectItem>
          <SelectItem value="price-desc">높은 가격순</SelectItem>
          <SelectItem value="newest">최신순</SelectItem>
        </SelectContent>
      </Select>
    </div>
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {products.map((p) => <ProductCard key={p.id} {...p} />)}
    </div>
  </main>
</div>
```

DON'T:
```tsx
{/* 비표준: 필터가 하단에, 정렬이 좌측 사이드바에 → 멘탈 모델 불일치 */}
<div className="flex flex-col">
  <div className="grid grid-cols-4 gap-4">{products.map(...)}</div>
  <aside className="mt-8 border-t pt-4">필터...</aside>
</div>
```

### 2. 표준 컴포넌트 활용 — shadcn/ui 우선

```tsx
{/* 표준 Dialog: 제목→설명→내용→액션 패턴 준수 */}
<Dialog>
  <DialogTrigger asChild>
    <Button variant="destructive">계정 삭제</Button>
  </DialogTrigger>
  <DialogContent>
    <DialogHeader>
      <DialogTitle>정말 삭제하시겠습니까?</DialogTitle>
      <DialogDescription>
        이 작업은 되돌릴 수 없습니다. 모든 데이터가 영구 삭제됩니다.
      </DialogDescription>
    </DialogHeader>
    <DialogFooter className="gap-2">
      <DialogClose asChild><Button variant="ghost">취소</Button></DialogClose>
      <Button variant="destructive" onClick={handleDelete}>삭제</Button>
    </DialogFooter>
  </DialogContent>
</Dialog>
```

### 3. 관습적 위치 — 사용자 기대 매핑

| 요소 | 기대 위치 | 근거 |
|------|----------|------|
| 로고 | 좌상단 | 홈 링크 기대 (96% 사이트) |
| 검색 | 상단 중앙/우측 | 글로벌 검색 기대 |
| 장바구니 | 우상단 | E-commerce 표준 |
| 로그인/프로필 | 우상단 | 98% 사이트 관습 |
| 푸터 링크 | 하단 | 약관, 연락처, 사이트맵 |
| 뒤로가기 | 좌상단 | 모바일 네이티브 관습 |

### 언제 관습을 깨도 되는가?
- 사용자 테스트에서 기존 패턴보다 **측정 가능하게** 나은 경우만
- 학습 비용 < 장기 효율 이득일 때
- 반드시 온보딩/툴팁으로 새 패턴을 안내할 것

## Connections

### REQUIRES (1)

- ← [[design.ux-psychology.role]] `w=0.9`

### FEEDS (3)

- ← [[design.ux-psychology.hicks-law]] `w=0.7`
- → [[design.ux-psychology.peak-end]] `w=0.7`
- → [[design.ux-psychology.verify]] `w=0.8`
