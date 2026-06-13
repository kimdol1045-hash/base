---
id: "design.ui-component.motion"
domain: "design"
type: "rule"
region: LIMBIC
token_estimate: 390
theory: "#188 Motion Design (Disney 12 Principles + Material Motion)"
tags: [design, motion, animation, ux]
---

# design.ui-component.motion

> **Region**: 💜 [[LIMBIC]]  
> **Domain**: `design`  
> **Type**: `rule`  
> **Theory**: #188 Motion Design (Disney 12 Principles + Material Motion)  
> **Tokens**: 390

## Content

모션 디자인 (애니메이션으로 사용성과 피드백을 향상한다):

### 목적별 애니메이션
| 목적 | 예시 | 시간 |
|------|------|------|
| 피드백 | 버튼 클릭 반응 | 100~200ms |
| 전환 | 페이지/모달 전환 | 200~300ms |
| 주목 유도 | 배지, 알림 | 300~500ms |
| 설명 | 온보딩 가이드 | 500ms~1s |

### 핵심 원칙
- **Easing**: linear 금지. ease-out(진입), ease-in(퇴장) 사용
- **Duration**: 200~500ms 권장. 300ms 초과 시 느림 인지
- **의미**: 모든 애니메이션은 목적이 있어야 함 (장식 ≠ 애니메이션)
- **성능**: transform/opacity만 사용 (layout 트리거 속성 금지)

### CSS 구현
```css
/* 좋은 예: GPU 가속 속성만 */
.modal-enter {
  opacity: 0;
  transform: translateY(20px);
}
.modal-enter-active {
  opacity: 1;
  transform: translateY(0);
  transition: opacity 200ms ease-out, transform 200ms ease-out;
}
```

### prefers-reduced-motion
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
접근성 필수 — 움직임 민감한 사용자 배려

### 하지 말 것
- 자동 재생 애니메이션 (집중 방해)
- 3초 이상 로딩 애니메이션 (스켈레톤으로 대체)
- layout shift 유발하는 애니메이션

## Connections

*Connections will be populated by Graph RAG ingest.*
