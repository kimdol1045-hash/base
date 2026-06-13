---
id: "design.ui-component.gestalt"
domain: "design"
type: "rule"
region: LIMBIC
token_estimate: 500
theory: "#41 Gestalt Principles (Wertheimer, 1923)"
tags: [design, ui, gestalt, proximity, similarity, closure, continuity, psychology]
---

# design.ui-component.gestalt

> **Region**: 💜 [[LIMBIC]]  
> **Domain**: `design`  
> **Type**: `rule`  
> **Theory**: #41 Gestalt Principles (Wertheimer, 1923)  
> **Tokens**: 500

## Content

게슈탈트 원리 — 인간의 시각 인지 패턴에 맞는 UI를 설계한다.

### 1. 근접성 (Proximity) — Wertheimer, 1923
관련 요소는 가까이, 비관련 그룹은 간격으로 구분한다.

구체적 간격 기준:
- 같은 그룹 내 요소 간: gap-2 (8px)
- 폼 필드와 라벨: gap-1.5 (6px)
- 그룹 간 구분: gap-8 (32px) 이상
- 섹션 간 구분: gap-12 (48px) 이상
- 카드 내부 패딩: p-4 (16px) ~ p-6 (24px)

DO:
```tsx
{/* 라벨-입력 근접, 필드 간 적당한 간격 */}
<div className="space-y-6">
  <div className="space-y-1.5">
    <Label htmlFor="name">이름</Label>
    <Input id="name" placeholder="홍길동" />
  </div>
  <div className="space-y-1.5">
    <Label htmlFor="email">이메일</Label>
    <Input id="email" type="email" placeholder="hong@example.com" />
  </div>
</div>
```

DON'T:
```tsx
{/* 라벨과 입력 사이 간격 = 필드 간 간격 -> 그룹 구분 불가 */}
<div className="space-y-4">
  <Label>이름</Label>
  <Input />
  <Label>이메일</Label>
  <Input />
</div>
```

### 2. 유사성 (Similarity)
같은 계층/기능의 요소는 동일 시각 스타일을 적용한다.

버튼 계층 체계:
- Primary: bg-primary text-primary-foreground — 페이지당 1개 (핵심 CTA)
- Secondary: bg-secondary text-secondary-foreground — 보조 액션
- Ghost: hover:bg-accent — 취소, 뒤로가기 등
- Destructive: bg-destructive — 삭제, 해지 등 (확인 다이얼로그 필수)

DO:
```tsx
<div className="flex gap-3">
  <Button variant="primary">저장하기</Button>
  <Button variant="ghost">취소</Button>
</div>
```

DON'T:
```tsx
{/* 동일 계층 버튼에 서로 다른 스타일 -> 계층 혼란 */}
<div className="flex gap-3">
  <Button className="bg-blue-500 rounded-full">저장</Button>
  <Button className="bg-green-400 rounded-md border-2">취소</Button>
</div>
```

### 3. 폐쇄 (Closure)
불완전한 형태도 완성된 것으로 인지 — 최소 시각 요소로 그룹을 표현한다.

- 카드: rounded-lg border bg-card 로 영역 구분 (무거운 그림자 불필요)
- 구분선: border-b 하나로 섹션 분리 (전체 박스 불필요)
- 아바타 그룹: -space-x-2로 겹치면 "그룹"으로 인지

```tsx
{/* 최소 테두리로 카드 그룹핑 */}
<div className="rounded-lg border bg-card p-4">
  <h3 className="font-semibold">제목</h3>
  <p className="text-sm text-muted-foreground">설명 텍스트</p>
</div>
```

### 4. 연속성 (Continuity)
시선 흐름이 자연스러운 레이아웃을 설계한다.

- 랜딩 페이지: Z패턴 (로고→네비→히어로→CTA)
- 콘텐츠 페이지: F패턴 (좌측 헤딩→본문 스캔)
- 폼: 단일 컬럼 상→하 흐름 (좌→우 분할 지양)
- 진행 표시: Stepper, Progress bar로 시선 유도

### 5. 공통 영역 (Common Region)
배경색, 테두리, 카드로 논리적 그룹핑을 명시한다.

```tsx
{/* 배경색으로 관련 설정 그룹핑 */}
<div className="space-y-6">
  <section className="rounded-lg bg-muted/50 p-6 space-y-4">
    <h3 className="text-lg font-semibold">알림 설정</h3>
    <SwitchField label="이메일 알림" />
    <SwitchField label="푸시 알림" />
  </section>
  <section className="rounded-lg bg-muted/50 p-6 space-y-4">
    <h3 className="text-lg font-semibold">보안 설정</h3>
    <SwitchField label="2단계 인증" />
  </section>
</div>
```

## Connections

### REQUIRES (1)

- ← [[design.ui-component.role]] `w=0.9`

### FEEDS (2)

- → [[design.ui-component.typography]] `w=0.7`
- → [[design.ui-component.verify]] `w=0.8`
