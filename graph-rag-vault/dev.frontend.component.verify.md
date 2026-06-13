---
id: "dev.frontend.component.verify"
domain: "development.frontend"
type: "verify"
bloom_level: ""
tags: ["frontend", "component", "verification", "checklist", "quality"]
brain_region: "CORTEX"
token_estimate: 480
---

# dev.frontend.component.verify

> #8 Flavell MGV

컴포넌트 자기 검증 체크리스트 (출력 전 반드시 모든 항목을 점검한다):

### A. 타입 안전성 (FAIL 시 수정 필수)
- [ ] TypeScript strict 에러가 없는가?
- [ ] `any` 타입을 사용하지 않았는가? (`unknown` + type guard로 대체)
- [ ] Props 인터페이스가 명시적으로 선언되었는가?
- [ ] 이벤트 핸들러의 event 타입이 정확한가? (`React.MouseEvent<HTMLButtonElement>`)

PASS: 모든 타입이 명시적이고 `any`가 0개
FAIL: `any` 1개 이상 또는 타입 에러 존재

### B. 렌더링 최적화 (FAIL 시 수정 권장)
- [ ] 불필요한 리렌더링이 없는가?
- [ ] 객체/배열/함수를 props로 넘길 때 매 렌더마다 새로 생성하지 않는가?
- [ ] 리스트 렌더링에서 `key`가 고유하고 안정적인가? (index 사용 금지)

DO:
```tsx
// ✅ 안정적인 key
{users.map(user => <UserCard key={user.id} user={user} />)}
```

DON'T:
```tsx
// ❌ index를 key로 사용 (순서 변경 시 버그)
{users.map((user, i) => <UserCard key={i} user={user} />)}
// ❌ 렌더마다 새 객체 생성
<Chart options={{ color: "blue" }} />
```

### C. UI 상태 완전성 (FAIL 시 수정 필수)
- [ ] **로딩 상태**를 처리하는가? (Skeleton 또는 Spinner)
- [ ] **에러 상태**를 처리하는가? (사용자에게 의미 있는 메시지)
- [ ] **빈 상태**를 처리하는가? (데이터 0건일 때 안내 UI)
- [ ] **성공 상태**가 정상 렌더링되는가?

PASS: 로딩/에러/빈/성공 4가지 상태 모두 처리
FAIL: 하나라도 누락

### D. 반응형 & 접근성 (FAIL 시 수정 권장)
- [ ] 모바일 320px에서 레이아웃이 깨지지 않는가?
- [ ] 클릭 가능한 요소에 `button` 또는 `a` 태그를 사용하는가? (`div onClick` 금지)
- [ ] 이미지에 `alt` 텍스트가 있는가?
- [ ] 폼 input에 `label`이 연결되어 있는가?

DON'T:
```tsx
// ❌ div를 버튼처럼 사용 (접근성 위반)
<div onClick={handleClick} className="cursor-pointer">삭제</div>
```

DO:
```tsx
// ✅ 시맨틱 태그 사용
<button onClick={handleClick} className="cursor-pointer">삭제</button>
```

### E. 코드 규칙 (FAIL 시 수정 필수)
- [ ] `'use client'`가 꼭 필요한 곳에만 있는가?
- [ ] 환경변수를 하드코딩하지 않았는가?
- [ ] `next/image`를 사용하는가? (`<img>` 태그 금지)
- [ ] named export를 사용하는가? (page.tsx 제외)
- [ ] 컴포넌트 파일이 200줄을 초과하지 않는가?

PASS: 모든 규칙 준수
FAIL: 하나라도 위반

## Connections

- [[dev.frontend.component.role]] — REQUIRES (weight: 0.85)
- [[dev.frontend.page.role]] — REQUIRES (weight: 0.85)
- [[dev.frontend.component.solid]] — FEEDS (weight: 0.8)
- [[dev.frontend.component.stack]] — FEEDS (weight: 0.8)
- [[dev.frontend.page.routing]] — FEEDS (weight: 0.8)
