---
id: "dev.frontend.component.animation"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "animation", "framer-motion", "css-transition", "reduced-motion", "performance", "accessibility"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.frontend.component.animation

> #35 Doherty Threshold (Doherty & Kelisky, 1979) — 400ms 이내 응답

애니메이션 패턴 (사용자 인지 흐름을 돕고 인터랙션 품질을 높인다):

### 애니메이션 시간 기준
- 즉각 반응 (hover, press): 100-150ms
- 상태 전환 (토글, 탭 전환): 200-300ms
- 진입/퇴장 (모달, 드로어): 300-400ms
- 복잡한 전환 (페이지, 레이아웃): 400-500ms (Doherty 상한)
- 500ms 초과: 사용자가 "느리다"고 인지 → 절대 금지

### 1. Framer Motion — 선언적 애니메이션

DO:
```tsx
// ✅ 기본 진입 애니메이션
import { motion, AnimatePresence } from "framer-motion";

function FadeIn({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3, ease: "easeOut" }}
    >
      {children}
    </motion.div>
  );
}

// ✅ AnimatePresence — 퇴장 애니메이션 (unmount 시)
function Modal({ isOpen, onClose }: ModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            className="fixed inset-0 bg-black/50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
          />
          <motion.div
            className="fixed inset-x-4 top-1/2 -translate-y-1/2 bg-white rounded-xl p-6"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2 }}
          >
            {/* 모달 내용 */}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

// ✅ layout 애니메이션 — 리스트 순서 변경, 필터링
function FilterableList({ items }: { items: Item[] }) {
  return (
    <motion.ul layout className="space-y-2">
      <AnimatePresence>
        {items.map((item) => (
          <motion.li
            key={item.id}
            layout                    // 위치 변경 시 부드럽게
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ layout: { duration: 0.3 } }}
          >
            {item.name}
          </motion.li>
        ))}
      </AnimatePresence>
    </motion.ul>
  );
}
```

### 2. CSS Transition — 단순 상태 전환

```tsx
// ✅ CSS만으로 충분한 경우 (hover, focus, 색상 변화)
function Button({ children }: { children: React.ReactNode }) {
  return (
    <button className="
      transform transition-all duration-200 ease-out
      hover:scale-105 hover:shadow-md
      active:scale-95
      focus-visible:ring-2 focus-visible:ring-primary
    ">
      {children}
    </button>
  );
}
```

### 3. Reduced Motion 존중 (접근성 필수)

DO:
```tsx
// ✅ prefers-reduced-motion 미디어 쿼리 체크
import { useReducedMotion } from "framer-motion";

function AnimatedCard({ children }: { children: React.ReactNode }) {
  const shouldReduceMotion = useReducedMotion();

  return (
    <motion.div
      initial={shouldReduceMotion ? false : { opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: shouldReduceMotion ? 0 : 0.3 }}
    >
      {children}
    </motion.div>
  );
}

// ✅ Tailwind — motion-safe / motion-reduce 유틸리티
// <div className="motion-safe:animate-bounce motion-reduce:animate-none">
```

### 성능 규칙: GPU 가속 속성만 애니메이션

DO: `transform` (translate, scale, rotate), `opacity` — GPU 가속, 리페인트 없음
DON'T: `width`, `height`, `top`, `left`, `margin`, `padding` — 레이아웃 재계산 발생

DON'T:
```tsx
// ❌ 레이아웃 속성 애니메이션 — 매 프레임 레이아웃 재계산 (jank)
<motion.div
  animate={{ width: isOpen ? 300 : 0 }}  // ❌ width 변경
  // 대신: scaleX 또는 translateX 사용
/>

// ❌ reduced-motion 무시 — 전정 장애 사용자에게 어지러움 유발
// ❌ will-change 남발 — GPU 메모리 과다 사용
// will-change는 실제 성능 문제가 측정된 요소에만 적용
```
