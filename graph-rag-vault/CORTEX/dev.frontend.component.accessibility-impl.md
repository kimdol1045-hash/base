---
id: "dev.frontend.component.accessibility-impl"
domain: "development.frontend"
type: "rule"
region: CORTEX
token_estimate: 500
theory: "#32 접근성 — WCAG 2.1 AA 기준 (W3C, 2018)"
tags: [frontend, accessibility, a11y, wcag, aria, keyboard, focus-trap, screen-reader]
---

# dev.frontend.component.accessibility-impl

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.frontend`  
> **Type**: `rule`  
> **Theory**: #32 접근성 — WCAG 2.1 AA 기준 (W3C, 2018)  
> **Tokens**: 500

## Content

접근성 구현 규칙 (장애 유무와 관계없이 모든 사용자가 이용 가능한 UI를 만든다):

### WCAG 2.1 AA 핵심 기준
- 색상 대비: 일반 텍스트 4.5:1, 대형 텍스트(18pt+) 3:1
- 터치 타겟: 최소 44×44px (모바일), 24×24px (데스크톱)
- 포커스 표시: 모든 인터랙티브 요소에 visible focus indicator
- 키보드 접근: 모든 기능을 키보드만으로 사용 가능

### 1. Semantic HTML First

DO:
```tsx
// ✅ 시맨틱 HTML — 스크린 리더가 구조를 이해
<header>
  <nav aria-label="메인 네비게이션">
    <ul role="list">
      <li><Link href="/dashboard">대시보드</Link></li>
      <li><Link href="/settings">설정</Link></li>
    </ul>
  </nav>
</header>
<main>
  <h1>대시보드</h1>
  <section aria-labelledby="recent-projects">
    <h2 id="recent-projects">최근 프로젝트</h2>
    {/* ... */}
  </section>
</main>

// ✅ 아이콘 버튼 — aria-label 필수
<button aria-label="검색" onClick={toggleSearch}>
  <SearchIcon aria-hidden="true" />
</button>

// ✅ 이미지 — 의미 있는 alt 텍스트
<img src="/hero.jpg" alt="팀원들이 화이트보드 앞에서 회의하는 모습" />
// 장식 이미지: alt="" (빈 문자열, 생략 아님)
```

### 2. 키보드 네비게이션

```tsx
// ✅ 커스텀 드롭다운 — 키보드 완전 지원
function Dropdown({ items, onSelect }: DropdownProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);

  const handleKeyDown = (e: KeyboardEvent) => {
    switch (e.key) {
      case "ArrowDown":
        e.preventDefault();
        setActiveIndex((i) => Math.min(i + 1, items.length - 1));
        break;
      case "ArrowUp":
        e.preventDefault();
        setActiveIndex((i) => Math.max(i - 1, 0));
        break;
      case "Enter":
      case " ":
        e.preventDefault();
        if (activeIndex >= 0) onSelect(items[activeIndex]);
        setIsOpen(false);
        break;
      case "Escape":
        setIsOpen(false);
        triggerRef.current?.focus(); // 트리거로 포커스 복귀
        break;
    }
  };

  return (
    <div role="combobox" aria-expanded={isOpen} aria-haspopup="listbox">
      <button ref={triggerRef} onClick={() => setIsOpen(!isOpen)}>
        선택하세요
      </button>
      {isOpen && (
        <ul role="listbox" onKeyDown={handleKeyDown}>
          {items.map((item, i) => (
            <li key={item.id} role="option" aria-selected={i === activeIndex}>
              {item.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### 3. Focus Trap — 모달/다이얼로그

```tsx
// ✅ 모달 내부에 포커스 가두기
import { FocusTrap } from "focus-trap-react";

function Dialog({ isOpen, onClose, children }: DialogProps) {
  return isOpen ? (
    <FocusTrap focusTrapOptions={{
      initialFocus: false,
      escapeDeactivates: true,
      onDeactivate: onClose,
    }}>
      <div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
        <h2 id="dialog-title">확인</h2>
        {children}
        <button onClick={onClose}>닫기</button>
      </div>
    </FocusTrap>
  ) : null;
}
```

### 4. Live Region — 동적 콘텐츠 알림

```tsx
// ✅ 토스트/알림 — 스크린 리더에 실시간 전달
<div role="status" aria-live="polite" aria-atomic="true">
  {message && <p>{message}</p>}  {/* "저장되었습니다" 등 */}
</div>

// ✅ 에러 메시지 — 즉시 전달
<div role="alert" aria-live="assertive">
  {error && <p className="text-destructive">{error}</p>}
</div>
```

DON'T:
```tsx
// ❌ div를 버튼으로 사용 — 키보드/스크린리더 미지원
<div onClick={handleClick} className="cursor-pointer">클릭</div>
// → <button> 사용. focus, Enter, Space 자동 지원

// ❌ alt 텍스트 누락 — 스크린 리더가 파일명 읽음
<img src="/photo-123.jpg" />
// → alt="설명" 또는 alt="" (장식) 필수

// ❌ 보이는 텍스트에 aria-label — 이중 읽기
<button aria-label="저장">저장</button>  // "저장 저장" 읽힘
// → 보이는 텍스트가 있으면 aria-label 불필요
```

### 테스트 도구
- 자동: axe-core (`@axe-core/react`), eslint-plugin-jsx-a11y
- 수동: Tab 키로 전체 페이지 순회, VoiceOver/NVDA 테스트
- 대비 검사: Chrome DevTools > Rendering > CSS Contrast

## Connections

### FEEDS (2)

- ← [[design.ui-component.accessibility]] `w=0.5`
- ← [[design.ui-component.color]] `w=0.5`
