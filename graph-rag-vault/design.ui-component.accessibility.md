---
id: "design.ui-component.accessibility"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ui", "accessibility", "wcag", "fitts", "aria", "keyboard", "contrast"]
brain_region: "CORTEX"
token_estimate: 500
---

# design.ui-component.accessibility

> #46 WCAG 2.1 AA (W3C, 2018), #44 Fitts's Law (Fitts, 1954)

접근성 규칙 — 모든 사용자가 동등하게 인터랙션할 수 있는 UI를 만든다.

### 1. 색상 대비 (WCAG 1.4.3 / 1.4.11)
- 일반 텍스트 (< 18px): 최소 4.5:1 대비
- 큰 텍스트 (>= 18px bold 또는 >= 24px): 최소 3:1 대비
- UI 컴포넌트 경계 (버튼, 입력 필드): 최소 3:1 대비
- 포커스 인디케이터: 최소 3:1 대비
- 비활성(disabled) 요소: 대비 요구 없음 (단, 시각적으로 비활성 표시 필수)

DO:
```tsx
{/* text-foreground는 bg-background 대비 4.5:1 이상 보장 */}
<p className="text-foreground">본문 텍스트</p>
<p className="text-muted-foreground">보조 텍스트 (4.5:1 확인 필수)</p>
```

DON'T:
```tsx
{/* 회색 배경에 회색 텍스트 -> 대비 부족 */}
<p className="bg-gray-200 text-gray-400">읽기 어려운 텍스트</p>
```

### 2. 터치/클릭 타겟 (Fitts's Law)
- 최소 터치 타겟: 44x44px (모바일), 24x24px (데스크톱 마우스)
- 인접 타겟 간 최소 간격: 8px
- 작은 아이콘도 클릭 영역은 44px 확보 (padding 활용)

DO:
```tsx
{/* 아이콘은 작지만 클릭 영역은 44px */}
<button className="inline-flex items-center justify-center h-11 w-11 rounded-md hover:bg-accent">
  <XIcon className="h-4 w-4" />
  <span className="sr-only">닫기</span>
</button>
```

DON'T:
```tsx
{/* 아이콘 크기 = 클릭 영역 -> 탭 불가 */}
<button className="h-4 w-4">
  <XIcon className="h-4 w-4" />
</button>
```

### 3. 키보드 내비게이션 (WCAG 2.1.1)
- 모든 인터랙티브 요소: Tab으로 접근 가능
- 논리적 탭 순서: DOM 순서 = 시각 순서 (tabIndex 조작 최소화)
- 모달/드롭다운: 포커스 트랩 필수 (Escape로 닫기)
- 커스텀 위젯: WAI-ARIA 패턴 준수 (방향키, Enter, Space)

```tsx
{/* 드롭다운 키보드 지원 */}
<DropdownMenu>
  <DropdownMenuTrigger asChild>
    <Button variant="ghost" aria-haspopup="true">
      메뉴 <ChevronDown className="ml-1 h-4 w-4" />
    </Button>
  </DropdownMenuTrigger>
  <DropdownMenuContent>
    {/* 방향키로 탐색, Enter로 선택, Escape로 닫기 */}
    <DropdownMenuItem>프로필</DropdownMenuItem>
    <DropdownMenuItem>설정</DropdownMenuItem>
    <DropdownMenuSeparator />
    <DropdownMenuItem className="text-destructive">로그아웃</DropdownMenuItem>
  </DropdownMenuContent>
</DropdownMenu>
```

### 4. 포커스 관리
- outline 제거 금지 (outline-none 단독 사용 금지)
- 커스텀 포커스 링: focus-visible:ring-2 ring-ring ring-offset-2
- 포커스 이동 시 스크롤 위치 자동 조정

DO:
```tsx
<button className="rounded-md px-4 py-2 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
  버튼
</button>
```

DON'T:
```tsx
{/* outline: none만 적용 -> 키보드 사용자 포커스 위치 파악 불가 */}
<button className="outline-none">버튼</button>
```

### 5. ARIA 레이블링
- 텍스트 없는 버튼: aria-label 필수
- 장식 이미지: aria-hidden="true" 또는 alt=""
- 의미 있는 이미지: alt 텍스트 필수 (기능 설명, 내용 설명)
- 라이브 영역: aria-live="polite" (토스트, 알림)
- 폼 에러: aria-invalid="true" + aria-describedby={errorId}

```tsx
{/* 폼 에러 접근성 */}
<div>
  <Label htmlFor="email">이메일</Label>
  <Input
    id="email"
    aria-invalid={!!error}
    aria-describedby={error ? "email-error" : undefined}
  />
  {error && (
    <p id="email-error" className="text-sm text-destructive mt-1" role="alert">
      {error}
    </p>
  )}
</div>
```

### 6. 색상 외 정보 전달 (WCAG 1.4.1)
- 상태 표시: 색상 + 아이콘 + 텍스트 병행
- 그래프: 색상 + 패턴 + 라벨 병행

```tsx
{/* 색상 + 아이콘 + 텍스트로 상태 전달 */}
<Badge variant="destructive">
  <AlertCircle className="mr-1 h-3 w-3" />
  오류 발생
</Badge>
```

## Connections

- [[design.ui-component.role]] — REQUIRES (weight: 0.9)
- [[design.ui-component.verify]] — FEEDS (weight: 0.8)
- [[design.ui-component.responsive]] — FEEDS (weight: 0.7)
- [[design.ui-component.color]] — CO_CREATES (weight: 0.6)
- [[dev.frontend.component.accessibility-impl]] — FEEDS (weight: 0.5)
