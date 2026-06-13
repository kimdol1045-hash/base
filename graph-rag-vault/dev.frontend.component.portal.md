---
id: "dev.frontend.component.portal"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "portal", "modal", "overlay"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.component.portal

> #235 React Portal (React Documentation, Meta 2017)

# React Portal 가이드

## 핵심 원칙
- Portal은 DOM 트리의 다른 위치에 자식을 렌더링한다
- 모달, 토스트, 드롭다운 등 오버레이 UI에 사용한다
- CSS z-index, overflow 문제를 근본적으로 해결한다
- React 이벤트 버블링은 Portal에서도 논리적 트리를 따른다

## DO
- 모달, 다이얼로그, 토스트 알림에 Portal을 사용한다
- document.body에 마운트할 Portal 타겟 요소를 미리 생성한다
- Portal 컨테이너의 접근성(aria 속성)을 설정한다
- 포커스 트랩(Focus Trap)을 모달 Portal에 적용한다

## DON'T
- SSR 환경에서 document 참조를 직접 사용하지 않는다 (useEffect 내에서 처리)
- Portal 내부에서 부모 컴포넌트의 CSS에 의존하지 않는다
- 불필요하게 Portal을 사용하지 않는다 (일반 컴포넌트로 충분한 경우)
- Portal 컨테이너를 매 렌더링마다 새로 생성하지 않는다

## 코드 예시
```tsx
import { createPortal } from "react-dom";
import { useEffect, useRef, useState } from "react";

interface PortalProps {
  children: React.ReactNode;
  containerId?: string;
}

export function Portal({ children, containerId = "portal-root" }: PortalProps) {
  const [mounted, setMounted] = useState(false);
  const containerRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    let container = document.getElementById(containerId);
    if (!container) {
      container = document.createElement("div");
      container.id = containerId;
      document.body.appendChild(container);
    }
    containerRef.current = container;
    setMounted(true);
  }, [containerId]);

  if (!mounted || !containerRef.current) return null;
  return createPortal(children, containerRef.current);
}

// 모달에서 사용
export function Modal({ open, onClose, children }: ModalProps) {
  if (!open) return null;
  return (
    <Portal>
      <div
        className="fixed inset-0 z-50 flex items-center justify-center"
        role="dialog"
        aria-modal="true"
      >
        <div className="fixed inset-0 bg-black/50" onClick={onClose} />
        <div className="relative z-10 rounded-lg bg-white p-6 shadow-xl">
          {children}
        </div>
      </div>
    </Portal>
  );
}
```
