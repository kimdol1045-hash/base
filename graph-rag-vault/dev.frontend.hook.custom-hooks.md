---
id: "dev.frontend.hook.custom-hooks"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "hooks", "react", "abstraction"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.hook.custom-hooks

> #236 React Custom Hooks (React Documentation, Meta 2019)

# 커스텀 훅 설계 가이드

## 핵심 원칙
- 컴포넌트에서 재사용 가능한 상태 로직을 커스텀 훅으로 추출한다
- 훅 이름은 반드시 `use` 접두사로 시작한다
- 하나의 훅은 하나의 관심사만 처리한다 (단일 책임)
- 훅의 반환값은 사용하기 쉬운 인터페이스로 설계한다

## DO
- 상태 + 액션을 객체 또는 튜플로 반환한다
- 훅 내부에서 cleanup 함수를 올바르게 구현한다
- 제네릭을 활용하여 타입 안전한 훅을 작성한다
- 훅의 의존성(deps)을 최소화한다

## DON'T
- 훅 안에서 조건부로 다른 훅을 호출하지 않는다 (Rules of Hooks)
- 비즈니스 로직과 UI 로직을 하나의 훅에 혼합하지 않는다
- 불필요한 상태를 만들지 않는다 (파생 값은 useMemo로)
- 너무 많은 파라미터를 받는 훅을 만들지 않는다 (옵션 객체 사용)

## 코드 예시
```tsx
// 토글 훅
function useToggle(initial = false) {
  const [value, setValue] = useState(initial);
  const toggle = useCallback(() => setValue(v => !v), []);
  const setTrue = useCallback(() => setValue(true), []);
  const setFalse = useCallback(() => setValue(false), []);
  return { value, toggle, setTrue, setFalse } as const;
}

// 로컬 스토리지 동기화 훅
function useLocalStorage<T>(key: string, initialValue: T) {
  const [storedValue, setStoredValue] = useState<T>(() => {
    if (typeof window === "undefined") return initialValue;
    try {
      const item = localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setValue = useCallback((value: T | ((prev: T) => T)) => {
    setStoredValue(prev => {
      const newValue = value instanceof Function ? value(prev) : value;
      localStorage.setItem(key, JSON.stringify(newValue));
      return newValue;
    });
  }, [key]);

  return [storedValue, setValue] as const;
}

// 사용
function Settings() {
  const sidebar = useToggle(true);
  const [theme, setTheme] = useLocalStorage("theme", "light");

  return (
    <div>
      <button onClick={sidebar.toggle}>사이드바 {sidebar.value ? "닫기" : "열기"}</button>
      <select value={theme} onChange={e => setTheme(e.target.value)}>
        <option value="light">라이트</option>
        <option value="dark">다크</option>
      </select>
    </div>
  );
}
```
