---
id: "dev.frontend.hook.debounce"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "hooks", "debounce", "throttle", "performance"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.hook.debounce

> #239 Debounce & Throttle (Lodash, Underscore.js)

# Debounce/Throttle 훅 가이드

## 핵심 원칙
- Debounce: 마지막 호출 후 지정 시간이 지나면 실행 (검색 입력)
- Throttle: 지정 시간 동안 최대 1회만 실행 (스크롤, 리사이즈)
- 불필요한 API 호출과 렌더링을 줄여 성능을 개선한다
- cleanup 함수에서 타이머를 정리하여 메모리 누수를 방지한다

## DO
- 검색 입력에 300-500ms debounce를 적용한다
- 스크롤 이벤트에 100-200ms throttle을 적용한다
- debounced 값과 원본 값을 모두 제공한다
- 컴포넌트 언마운트 시 대기 중인 콜백을 취소한다

## DON'T
- debounce 간격을 너무 길게 설정하지 않는다 (UX 저하)
- 매 렌더링마다 새로운 debounce 함수를 생성하지 않는다
- submit 같은 즉시 실행이 필요한 액션에 debounce를 적용하지 않는다
- throttle과 debounce를 혼동하지 않는다

## 코드 예시
```tsx
import { useState, useEffect, useRef, useCallback } from "react";

// useDebounce: 값 디바운싱
function useDebounce<T>(value: T, delayMs: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delayMs);
    return () => clearTimeout(timer);
  }, [value, delayMs]);

  return debouncedValue;
}

// useDebouncedCallback: 함수 디바운싱
function useDebouncedCallback<T extends (...args: any[]) => void>(
  callback: T,
  delayMs: number,
): T {
  const timerRef = useRef<ReturnType<typeof setTimeout>>();

  useEffect(() => {
    return () => { if (timerRef.current) clearTimeout(timerRef.current); };
  }, []);

  return useCallback(
    ((...args) => {
      if (timerRef.current) clearTimeout(timerRef.current);
      timerRef.current = setTimeout(() => callback(...args), delayMs);
    }) as T,
    [callback, delayMs],
  );
}

// 사용: 검색 입력
function SearchInput() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebounce(query, 300);
  const { data: results } = useSearch(debouncedQuery);

  return (
    <div>
      <input
        value={query}
        onChange={e => setQuery(e.target.value)}
        placeholder="검색..."
      />
      {/* debouncedQuery가 변경될 때만 API 호출 */}
      <SearchResults results={results} />
    </div>
  );
}
```
