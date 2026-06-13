---
id: "design.ui-component.verify"
domain: "design"
type: "verify"
bloom_level: ""
tags: ["design", "ui", "verification", "checklist", "qa"]
brain_region: "CORTEX"
token_estimate: 450
---

# design.ui-component.verify

UI 컴포넌트 자기 검증 체크리스트 — 모든 항목을 통과해야 출력한다.

### A. 반응형 (Responsive)
- [ ] 320px 뷰포트에서 가로 스크롤 없이 표시되는가?
- [ ] 모바일 퍼스트로 작성했는가? (기본=모바일, sm:/md:/lg: 확장)
- [ ] 텍스트가 잘리거나 넘치지 않는가? (truncate 또는 line-clamp 적용)
- [ ] 이미지에 aspect-ratio와 sizes 속성이 있는가?
- [ ] 네비게이션이 모바일에서 햄버거/시트로 전환되는가?

### B. 접근성 (Accessibility)
- [ ] 모든 텍스트 색상 대비 4.5:1 이상인가?
- [ ] CTA 버튼 터치 타겟이 44x44px 이상인가?
- [ ] 키보드 Tab으로 모든 인터랙티브 요소 접근 가능한가?
- [ ] 포커스 링이 보이는가? (focus-visible:ring-2)
- [ ] 아이콘 버튼에 aria-label 또는 sr-only 텍스트가 있는가?
- [ ] 폼 에러에 aria-invalid + aria-describedby가 있는가?
- [ ] 색상만으로 정보를 전달하지 않는가? (아이콘/텍스트 병행)

### C. 다크모드 (Dark Mode)
- [ ] dark: 접두사 또는 CSS 변수로 다크모드 지원하는가?
- [ ] 하드코딩 색상(bg-white, text-black) 없이 시맨틱 색상 사용하는가?
- [ ] 그림자가 다크모드에서 과하지 않은가? (dark:shadow-none 또는 감소)
- [ ] 이미지/아이콘이 다크 배경에서 잘 보이는가?

### D. 코드 품질 (Code Quality)
- [ ] Tailwind 클래스만 사용했는가? (인라인 스타일 금지)
- [ ] cn() 유틸리티로 조건부 클래스 병합하는가?
- [ ] TypeScript Props interface가 정의되어 있는가?
- [ ] forwardRef로 ref 전달을 지원하는가?
- [ ] 컴포넌트가 150줄 이하인가?
- [ ] any 타입이 없는가?

### E. 게슈탈트 / 시각 (Visual)
- [ ] 관련 요소 간 간격(8px) < 그룹 간 간격(32px+) 인가?
- [ ] 버튼 계층이 일관적인가? (Primary 1개, Secondary/Ghost 보조)
- [ ] 시각적 계층: 제목 > 부제 > 본문 > 캡션 크기 순서인가?
- [ ] 카드/섹션이 padding, border, 배경으로 그룹핑 되어 있는가?

### F. 인터랙션 (Interaction)
- [ ] 로딩 상태가 있는가? (스피너, 스켈레톤)
- [ ] 호버/포커스/액티브 상태가 구분되는가?
- [ ] 트랜지션이 150ms~300ms 범위인가?
- [ ] 에러/성공 피드백이 있는가? (토스트, 인라인 메시지)

## Connections

- [[design.ui-component.role]] — REQUIRES (weight: 0.85)
- [[design.ui-component.gestalt]] — FEEDS (weight: 0.8)
- [[design.ui-component.typography]] — FEEDS (weight: 0.8)
- [[design.ui-component.spacing]] — FEEDS (weight: 0.8)
- [[design.ui-component.responsive]] — FEEDS (weight: 0.8)
- [[design.ui-component.accessibility]] — FEEDS (weight: 0.8)
