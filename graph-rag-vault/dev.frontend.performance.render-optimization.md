---
id: "dev.frontend.performance.render-optimization"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "performance", "rendering", "react", "memo"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.performance.render-optimization

> #255 React Rendering Optimization (React Documentation, Reconciliation Algorithm)

# React 렌더링 최적화 가이드

## 핵심 원칙
- 불필요한 리렌더링을 방지하여 UI 응답성을 유지한다
- 측정 먼저, 최적화는 나중에 (React DevTools Profiler 활용)
- React Compiler(React 19)를 우선 도입하고, 수동 최적화는 보조적으로 사용한다
- 상태를 가능한 아래쪽(지역적)에 위치시킨다

## DO
- `React.memo()`로 props가 변하지 않으면 리렌더링을 방지한다
- `useMemo()`로 비용이 큰 계산을 캐시한다
- `useCallback()`으로 이벤트 핸들러 참조를 안정화한다
- 상태를 필요한 컴포넌트에 가장 가까이 위치시킨다
- React DevTools Profiler로 병목을 먼저 확인한다

## DON'T
- 모든 컴포넌트에 memo를 적용하지 않는다 (오버헤드 발생)
- 프로파일링 없이 최적화하지 않는다 (추측 금지)
- 객체/배열 리터럴을 JSX props에 인라인으로 전달하지 않는다
- key에 index를 사용하지 않는다 (목록이 변경되는 경우)
- Context의 값이 너무 자주 변경되도록 하지 않는다

## 코드 예시
```tsx
import { memo, useMemo, useCallback } from "react";

// memo: props가 같으면 리렌더링 방지
const ExpensiveList = memo(function ExpensiveList({ items }: { items: Item[] }) {
  return (
    <ul>
      {items.map(item => <ListItem key={item.id} item={item} />)}
    </ul>
  );
});

// 부모 컴포넌트 최적화
function Dashboard() {
  const [filter, setFilter] = useState("");
  const [count, setCount] = useState(0);

  // useMemo: 비싼 필터링 결과 캐시
  const filteredItems = useMemo(
    () => items.filter(item => item.name.includes(filter)),
    [items, filter], // count 변경 시 재계산하지 않음
  );

  // useCallback: 핸들러 참조 안정화
  const handleSelect = useCallback((id: string) => {
    setSelectedId(id);
  }, []);

  return (
    <>
      <Counter count={count} onIncrement={() => setCount(c => c + 1)} />
      <ExpensiveList items={filteredItems} onSelect={handleSelect} />
    </>
  );
}

// ❌ 안티패턴: 매 렌더링마다 새 객체 생성
<Component style={{ color: "red" }} />  // 매번 새 참조
<Component data={items.filter(x => x.active)} />  // 매번 새 배열

// ✅ 개선
const style = useMemo(() => ({ color: "red" }), []);
const activeItems = useMemo(() => items.filter(x => x.active), [items]);
```
