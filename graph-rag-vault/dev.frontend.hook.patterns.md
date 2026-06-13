---
id: "dev.frontend.hook.patterns"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "hook", "patterns", "debounce", "intersection-observer", "custom-hook"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.frontend.hook.patterns

자주 사용되는 커스텀 훅 패턴 (반복 로직을 재사용 가능한 훅으로 추출한다):

### 1. useDebounce — 입력 디바운싱
사용자 입력(검색, 필터)의 연속 호출을 제어하여 API 요청을 줄인다.

```tsx
import { useState, useEffect } from "react";

export function useDebounce<T>(value: T, delay: number = 300): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer); // cleanup 필수
  }, [value, delay]);

  return debouncedValue;
}

// 사용 예시
function SearchInput() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebounce(query, 300);

  useEffect(() => {
    if (debouncedQuery) {
      searchAPI(debouncedQuery); // 300ms 동안 입력 없을 때만 호출
    }
  }, [debouncedQuery]);

  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

### 2. useLocalStorage — localStorage 동기화
상태와 localStorage를 자동으로 동기화한다. SSR 환경(Server Component)에서 안전하게 동작한다.

```tsx
import { useState, useEffect, useCallback } from "react";

export function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((prev: T) => T)) => void, () => void] {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === "undefined") return initialValue;
    try {
      const item = localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });

  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(storedValue));
    } catch (error) {
      console.warn(`localStorage 저장 실패 (key: ${key})`, error);
    }
  }, [key, storedValue]);

  const remove = useCallback(() => {
    setStoredValue(initialValue);
    localStorage.removeItem(key);
  }, [key, initialValue]);

  return [storedValue, setStoredValue, remove];
}

// 사용 예시
const [theme, setTheme] = useLocalStorage("theme", "light");
const [cart, setCart, clearCart] = useLocalStorage<CartItem[]>("cart", []);
```

### 3. useMediaQuery — 반응형 브레이크포인트 감지
CSS 미디어 쿼리를 JavaScript에서 감지하여 조건부 렌더링에 사용한다.

```tsx
import { useState, useEffect } from "react";

export function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);

  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);

    const handler = (e: MediaQueryListEvent) => setMatches(e.matches);
    media.addEventListener("change", handler);
    return () => media.removeEventListener("change", handler);
  }, [query]);

  return matches;
}

// Tailwind 브레이크포인트에 맞춘 편의 훅
export function useIsMobile() {
  return useMediaQuery("(max-width: 767px)");
}
export function useIsDesktop() {
  return useMediaQuery("(min-width: 1024px)");
}

// 사용 예시
function Navigation() {
  const isMobile = useIsMobile();
  return isMobile ? <MobileNav /> : <DesktopNav />;
}
```

### 4. useIntersectionObserver — 뷰포트 진입 감지
무한 스크롤, lazy loading, 애니메이션 트리거에 사용한다.

```tsx
import { useState, useEffect, useRef, type RefObject } from "react";

interface UseIntersectionOptions {
  threshold?: number;
  rootMargin?: string;
  enabled?: boolean;
}

export function useIntersectionObserver<T extends HTMLElement>(
  options: UseIntersectionOptions = {}
): { ref: RefObject<T>; isIntersecting: boolean } {
  const { threshold = 0, rootMargin = "0px", enabled = true } = options;
  const ref = useRef<T>(null);
  const [isIntersecting, setIsIntersecting] = useState(false);

  useEffect(() => {
    if (!enabled || !ref.current) return;

    const observer = new IntersectionObserver(
      ([entry]) => setIsIntersecting(entry.isIntersecting),
      { threshold, rootMargin }
    );
    observer.observe(ref.current);
    return () => observer.disconnect();
  }, [threshold, rootMargin, enabled]);

  return { ref, isIntersecting };
}

// ✅ 무한 스크롤 사용 예시
function InfiniteList() {
  const { ref, isIntersecting } = useIntersectionObserver<HTMLDivElement>({
    rootMargin: "100px", // 100px 전에 미리 로드
  });

  useEffect(() => {
    if (isIntersecting) loadMore();
  }, [isIntersecting]);

  return (
    <div>
      {items.map(item => <ItemCard key={item.id} item={item} />)}
      <div ref={ref} className="h-4" /> {/* 센티넬 요소 */}
    </div>
  );
}
```

### 5. useClickOutside — 외부 클릭 감지
드롭다운, 모달, 팝오버를 외부 클릭으로 닫을 때 사용한다.

```tsx
import { useEffect, useRef, type RefObject } from "react";

export function useClickOutside<T extends HTMLElement>(
  handler: () => void
): RefObject<T> {
  const ref = useRef<T>(null);

  useEffect(() => {
    const listener = (event: MouseEvent | TouchEvent) => {
      if (!ref.current || ref.current.contains(event.target as Node)) return;
      handler();
    };
    document.addEventListener("mousedown", listener);
    document.addEventListener("touchstart", listener);
    return () => {
      document.removeEventListener("mousedown", listener);
      document.removeEventListener("touchstart", listener);
    };
  }, [handler]);

  return ref;
}

// 사용 예시
function Dropdown() {
  const [isOpen, setIsOpen] = useState(false);
  const ref = useClickOutside<HTMLDivElement>(() => setIsOpen(false));

  return (
    <div ref={ref}>
      <button onClick={() => setIsOpen(!isOpen)}>메뉴</button>
      {isOpen && <DropdownMenu />}
    </div>
  );
}
```

### 6. useCopyToClipboard — 클립보드 복사

```tsx
import { useState, useCallback } from "react";

export function useCopyToClipboard(resetDelay: number = 2000) {
  const [copied, setCopied] = useState(false);

  const copy = useCallback(async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      setTimeout(() => setCopied(false), resetDelay);
      return true;
    } catch {
      console.warn("클립보드 복사 실패");
      return false;
    }
  }, [resetDelay]);

  return { copied, copy };
}

// 사용 예시
const { copied, copy } = useCopyToClipboard();
<button onClick={() => copy(code)}>
  {copied ? "복사됨!" : "코드 복사"}
</button>
```

### 훅 설계 원칙 요약
- **cleanup을 반드시** 구현한다 (타이머, 이벤트 리스너, Observer).
- **SSR 안전성**: `typeof window === "undefined"` 체크로 서버 환경 대응.
- **Generic 타입**으로 재사용성을 높인다.
- **옵션 객체 패턴**: 파라미터가 3개 이상이면 옵션 객체로 전달한다.

## Connections

- [[dev.frontend.hook.role]] — CO_CREATES (weight: 0.6)
- [[dev.frontend.hook.verify]] — CO_CREATES (weight: 0.6)
