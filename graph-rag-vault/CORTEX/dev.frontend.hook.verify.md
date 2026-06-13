---
id: "dev.frontend.hook.verify"
domain: "development.frontend"
type: "verify"
region: CORTEX
token_estimate: 500
theory: "#8 Flavell MGV"
tags: [frontend, hook, verification, checklist, react]
---

# dev.frontend.hook.verify

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.frontend`  
> **Type**: `verify`  
> **Theory**: #8 Flavell MGV  
> **Tokens**: 500

## Content

커스텀 훅 자기 검증 체크리스트 (출력 전 반드시 모든 항목을 점검한다):

### A. 네이밍 & 구조 (FAIL 시 수정 필수)
- [ ] 훅 이름이 `use`로 시작하는가?
- [ ] 반환 타입 인터페이스가 명시적으로 선언되었는가?
- [ ] 한 훅이 한 가지 관심사만 다루는가?
- [ ] 파일명이 `use[Feature].ts` 패턴인가?

PASS: `use` 접두사 + 명시적 반환 타입 + 단일 책임
FAIL: 네이밍 규칙 위반 또는 반환 타입 미선언

### B. 상태 & 에러 처리 (FAIL 시 수정 필수)
- [ ] 비동기 훅이 `isLoading` 상태를 반환하는가?
- [ ] 비동기 훅이 `error` 상태를 반환하는가?
- [ ] error 타입이 `Error | null`로 정확하게 선언되었는가?
- [ ] try-catch-finally 패턴을 사용하는가?

DO:
```tsx
// ✅ 완전한 비동기 훅 반환
interface UseDataReturn<T> {
  data: T | null;
  isLoading: boolean;
  error: Error | null;
  refetch: () => Promise<void>;
}

export function useData<T>(url: string): UseDataReturn<T> {
  const [data, setData] = useState<T | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const refetch = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      setData(await res.json());
    } catch (err) {
      setError(err instanceof Error ? err : new Error("Unknown"));
    } finally {
      setIsLoading(false);
    }
  }, [url]);

  useEffect(() => { refetch(); }, [refetch]);
  return { data, isLoading, error, refetch };
}
```

DON'T:
```tsx
// ❌ error/loading 누락, any 타입
function useData(url: string) {
  const [data, setData] = useState<any>(null);
  useEffect(() => {
    fetch(url).then(r => r.json()).then(setData);
  }, [url]);
  return data; // loading, error 상태 없음
}
```

PASS: isLoading + error + 타입 안전한 반환
FAIL: 상태 누락 또는 any 타입 사용

### C. useEffect 안전성 (FAIL 시 수정 필수)
- [ ] cleanup 함수가 필요한 경우 구현되었는가?
  - 타이머(setInterval/setTimeout) → `clearInterval/clearTimeout`
  - 이벤트 리스너 → `removeEventListener`
  - 구독(WebSocket, subscription) → `unsubscribe/close`
  - fetch 요청 → `AbortController`
- [ ] 의존성 배열이 정확한가? (빠진 의존성 없음)
- [ ] 빈 의존성 배열 `[]`이 의도적인가?

DO:
```tsx
// ✅ AbortController로 fetch cleanup
useEffect(() => {
  const controller = new AbortController();
  fetch(url, { signal: controller.signal })
    .then(r => r.json())
    .then(setData)
    .catch(err => {
      if (err.name !== "AbortError") setError(err);
    });
  return () => controller.abort();
}, [url]);
```

PASS: 모든 사이드 이펙트에 cleanup 구현
FAIL: cleanup 누락 (메모리 누수 위험)

### D. React 규칙 준수 (FAIL 시 수정 필수)
- [ ] 조건부 훅 호출이 없는가? (if/for 안에서 useState/useEffect 금지)
- [ ] 훅 내부에서 다른 훅 호출 순서가 일정한가?
- [ ] 일반 함수 안에서 훅을 호출하지 않았는가? (컴포넌트/훅 내에서만)

PASS: React Hooks 규칙 100% 준수
FAIL: 규칙 위반 1건 이상

### E. 재사용성 & 유연성 (FAIL 시 수정 권장)
- [ ] Generic 타입을 활용하여 다양한 데이터 타입에 대응하는가?
- [ ] 설정값을 파라미터로 주입받아 유연하게 사용할 수 있는가?
- [ ] 외부 의존성(fetch, localStorage 등)을 주입 가능한 구조인가?

PASS: 제네릭 활용 + 설정 주입 가능
FAIL: 특정 타입/설정에 하드코딩

## Connections

### CO_CREATES (2)

- ← [[dev.frontend.hook.patterns]] `w=0.6`
- ← [[dev.frontend.hook.role]] `w=0.6`
