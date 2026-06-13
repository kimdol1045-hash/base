---
id: "dev.frontend.component.performance"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "component", "performance", "react", "memo", "virtualization"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.frontend.component.performance

> #73 React Reconciliation (Facebook, 2013)

React 성능 최적화 패턴 (불필요한 리렌더링을 방지하고 런타임 비용을 줄인다):

### 1. React.memo — 리렌더링 방지
부모가 리렌더링되어도 props가 변하지 않으면 자식은 건너뛴다.
**사용 기준**: props가 자주 같은 값으로 전달되는 중간~무거운 컴포넌트에 적용.

DO:
```tsx
// ✅ 비용이 큰 리스트 아이템에 memo 적용
const UserCard = memo(function UserCard({ user }: { user: User }) {
  return (
    <div className="rounded-lg border p-4">
      <h3 className="text-lg font-semibold">{user.name}</h3>
      <p className="text-muted-foreground">{user.email}</p>
    </div>
  );
});

// ✅ 커스텀 비교 함수 (깊은 비교 필요 시)
const Chart = memo(
  function Chart({ data }: { data: ChartData }) {
    return <canvas>{/* ... */}</canvas>;
  },
  (prev, next) => prev.data.id === next.data.id && prev.data.version === next.data.version
);
```

DON'T:
```tsx
// ❌ 모든 컴포넌트에 무분별하게 memo 적용 (오버헤드만 추가)
const Label = memo(({ text }: { text: string }) => <span>{text}</span>);
// ❌ children을 받는 컴포넌트에 memo (children은 매번 새 참조)
const Card = memo(({ children }: { children: React.ReactNode }) => <div>{children}</div>);
```

### 2. useMemo — 비싼 계산 캐싱
**사용 기준**: 계산 비용이 O(n) 이상이거나 1ms 이상 걸리는 연산에만 적용.

DO:
```tsx
// ✅ 정렬 + 필터 (O(n log n))
const filteredUsers = useMemo(
  () => users
    .filter(u => u.name.toLowerCase().includes(query.toLowerCase()))
    .sort((a, b) => a.name.localeCompare(b.name)),
  [users, query]
);

// ✅ 파생 객체 (하위 memo 컴포넌트에 전달 시)
const chartConfig = useMemo(
  () => ({ labels: data.map(d => d.label), values: data.map(d => d.value) }),
  [data]
);
```

DON'T:
```tsx
// ❌ 단순 계산에 useMemo (오버헤드 > 이득)
const fullName = useMemo(() => `${first} ${last}`, [first, last]);
// ❌ 의존성 배열 부정확 (stale data 버그)
const result = useMemo(() => compute(a, b), [a]); // b 누락!
```

### 3. useCallback — 함수 참조 안정화
**사용 기준**: memo된 자식에게 함수를 props로 넘길 때만 사용.

DO:
```tsx
// ✅ memo된 자식에게 전달하는 핸들러
const handleDelete = useCallback(
  (userId: string) => {
    deleteUser(userId);
    toast.success("삭제 완료");
  },
  [deleteUser]
);

return <UserList users={users} onDelete={handleDelete} />;
// UserList는 memo 적용됨
```

DON'T:
```tsx
// ❌ memo 안 된 자식에게 useCallback (효과 없음)
const handleClick = useCallback(() => setCount(c => c + 1), []);
return <button onClick={handleClick}>+1</button>; // button은 memo 아님
```

### 4. 리스트 가상화 (Virtualization)
**사용 기준**: 리스트 아이템이 100개 이상일 때 적용.

DO:
```tsx
// ✅ @tanstack/react-virtual 사용
import { useVirtualizer } from "@tanstack/react-virtual";

function VirtualList({ items }: { items: Item[] }) {
  const parentRef = useRef<HTMLDivElement>(null);
  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 64, // 아이템 예상 높이(px)
    overscan: 5, // 화면 밖 미리 렌더링 수
  });

  return (
    <div ref={parentRef} className="h-[600px] overflow-auto">
      <div style={{ height: virtualizer.getTotalSize(), position: "relative" }}>
        {virtualizer.getVirtualItems().map(virtualRow => (
          <div
            key={virtualRow.key}
            style={{
              position: "absolute",
              top: virtualRow.start,
              height: virtualRow.size,
              width: "100%",
            }}
          >
            <ItemCard item={items[virtualRow.index]} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 5. 리렌더링 디버깅
```tsx
// 개발 환경에서 리렌더링 원인 추적
import { useRef, useEffect } from "react";

function useWhyDidYouRender(name: string, props: Record<string, unknown>) {
  const prevProps = useRef(props);
  useEffect(() => {
    const changes = Object.entries(props).filter(
      ([key, val]) => prevProps.current[key] !== val
    );
    if (changes.length > 0) {
      console.log(`[${name}] rerender:`, changes.map(([k]) => k));
    }
    prevProps.current = props;
  });
}
```

### 판단 기준 요약
| 도구 | 언제 사용 | 언제 불필요 |
|------|----------|------------|
| React.memo | props 자주 같은 중~무거운 컴포넌트 | 가벼운 컴포넌트, children 받는 경우 |
| useMemo | O(n) 이상 계산, memo 자식에 전달 | 단순 문자열 연산, 원시 값 |
| useCallback | memo 자식에 함수 전달 | memo 안 된 요소에 전달 |
| 가상화 | 아이템 100개 이상 리스트 | 아이템 50개 미만 |

## Connections

- [[dev.performance.role]] — FEEDS (weight: 0.5)
- [[dev.performance.web-vitals]] — FEEDS (weight: 0.5)
- [[dev.performance.caching]] — FEEDS (weight: 0.5)
- [[dev.performance.budget]] — FEEDS (weight: 0.5)
- [[dev.performance.amdahl]] — FEEDS (weight: 0.5)
- [[dev.performance.littles-law]] — FEEDS (weight: 0.5)
