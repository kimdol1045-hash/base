---
id: "design.ux-psychology.von-restorff"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ux", "von-restorff", "isolation-effect", "pricing", "cta", "badge", "emphasis"]
brain_region: "CORTEX"
token_estimate: 500
---

# design.ux-psychology.von-restorff

> #46 폰 레스토프 효과 (Von Restorff, 1933)

폰 레스토프 효과 (격리 효과) — 시각적으로 구별되는 요소가 기억에 더 잘 남는다.
동질적 항목 그룹에서 하나만 다르면, 그것이 가장 먼저 인지되고 기억된다.

### 핵심 원칙
- 페이지당 **1개의 시각적 차별 요소**만 사용 (남용 시 효과 소멸)
- CTA 버튼: 색상/크기로 주변과 명확히 구분
- 가격표: 추천 플랜만 강조 (배경, 크기, 뱃지)
- 알림/뱃지: 빨간 점 하나가 전체 시선 유도

### 1. 가격표 — 추천 플랜 강조

```tsx
<div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-start">
  {/* 기본 플랜 */}
  <div className="rounded-lg border p-6 space-y-4">
    <h3 className="text-lg font-semibold">Starter</h3>
    <p className="text-3xl font-bold">$9<span className="text-sm font-normal text-muted-foreground">/월</span></p>
    <ul className="space-y-2 text-sm text-muted-foreground">
      <li>프로젝트 3개</li><li>1GB 스토리지</li>
    </ul>
    <Button variant="outline" className="w-full">시작하기</Button>
  </div>

  {/* 추천 플랜 — 폰 레스토프: 유일하게 다른 시각 처리 */}
  <div className="rounded-lg border-2 border-primary bg-primary/5 p-6 space-y-4
                  relative shadow-lg scale-105">
    <Badge className="absolute -top-3 left-1/2 -translate-x-1/2">
      가장 인기
    </Badge>
    <h3 className="text-lg font-semibold">Pro</h3>
    <p className="text-3xl font-bold">$29<span className="text-sm font-normal text-muted-foreground">/월</span></p>
    <ul className="space-y-2 text-sm">
      <li>프로젝트 무제한</li><li>10GB 스토리지</li><li>우선 지원</li>
    </ul>
    <Button className="w-full">시작하기</Button>
  </div>

  {/* 엔터프라이즈 */}
  <div className="rounded-lg border p-6 space-y-4">
    <h3 className="text-lg font-semibold">Enterprise</h3>
    <p className="text-3xl font-bold">$99<span className="text-sm font-normal text-muted-foreground">/월</span></p>
    <ul className="space-y-2 text-sm text-muted-foreground">
      <li>모든 Pro 기능</li><li>SSO/SAML</li><li>전담 매니저</li>
    </ul>
    <Button variant="outline" className="w-full">문의하기</Button>
  </div>
</div>
```

### 2. CTA 버튼 차별화

```tsx
{/* 핵심 CTA만 Primary 색상 → 나머지는 ghost/outline */}
<div className="flex items-center justify-between border-b pb-4">
  <div className="flex gap-2">
    <Button variant="ghost" size="sm">임시저장</Button>
    <Button variant="ghost" size="sm">미리보기</Button>
  </div>
  {/* 유일한 Primary → 폰 레스토프 */}
  <Button size="sm" className="bg-primary text-primary-foreground px-6">
    게시하기
  </Button>
</div>
```

### 3. 알림 뱃지 — 최소 시각 요소로 주의 유도

```tsx
{/* 작은 빨간 점 하나로 전체 시선 유도 */}
<Button variant="ghost" size="icon" className="relative">
  <Bell className="h-5 w-5" />
  {unreadCount > 0 && (
    <span className="absolute -top-1 -right-1 flex h-5 w-5 items-center
                     justify-center rounded-full bg-destructive text-[10px]
                     font-bold text-destructive-foreground">
      {unreadCount > 9 ? "9+" : unreadCount}
    </span>
  )}
</Button>
```

### 주의사항
- 강조가 2개 이상이면 아무것도 강조되지 않는다
- 색상 외에 크기, 위치, 움직임으로도 격리 효과 달성 가능
- 접근성: 색상만으로 구분 금지 → 크기/텍스트/아이콘 병행

## Connections

- [[design.ux-psychology.role]] — REQUIRES (weight: 0.9)
- [[design.ux-psychology.verify]] — FEEDS (weight: 0.8)
- [[design.ux-psychology.peak-end]] — FEEDS (weight: 0.7)
- [[design.ux-psychology.serial-position]] — FEEDS (weight: 0.7)
