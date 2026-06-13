---
id: "dev.frontend.component.react-patterns"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "react", "patterns", "component"]
brain_region: "CORTEX"
token_estimate: 450
---

# dev.frontend.component.react-patterns

> #160 React Component Patterns (Compound, HOC, Render Props)

React 컴포넌트 패턴 (재사용성과 유연성을 높인다):

### Compound Components
```tsx
// 부모가 상태를 관리, 자식이 소비
<Select value={selected} onChange={setSelected}>
  <Select.Trigger>{selected || "선택하세요"}</Select.Trigger>
  <Select.Options>
    <Select.Option value="a">옵션 A</Select.Option>
    <Select.Option value="b">옵션 B</Select.Option>
  </Select.Options>
</Select>
```
- Context로 암묵적 상태 공유
- 사용처: Accordion, Tabs, Menu, Dialog

### Custom Hook 패턴 (권장)
```tsx
function useToggle(initial = false) {
  const [on, setOn] = useState(initial);
  const toggle = useCallback(() => setOn(prev => !prev), []);
  return { on, toggle, setOn };
}
```
- 로직 재사용의 기본 방법
- 테스트 용이 (renderHook)

### Container/Presentational 분리
```tsx
// Container: 데이터 + 로직
function UserListContainer() {
  const { data, isLoading } = useUsers();
  return <UserList users={data} loading={isLoading} />;
}
// Presentational: UI만
function UserList({ users, loading }: Props) {
  if (loading) return <Skeleton />;
  return <ul>{users.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

### 패턴 선택 가이드
| 상황 | 패턴 |
|------|------|
| 로직 재사용 | Custom Hook |
| 유연한 UI 조합 | Compound Components |
| 데이터/UI 분리 | Container/Presentational |
| 횡단 관심사 | Custom Hook (HOC보다 권장) |

### 안티패턴
- Prop Drilling 5단계 이상 → Context 또는 상태관리 도입
- God Component (300줄+) → 분리
- useEffect 내 비즈니스 로직 → Custom Hook으로 추출

## Connections

- [[dev.frontend.component.role]] — CO_CREATES (weight: 0.6)
- [[dev.frontend.component.solid]] — CO_CREATES (weight: 0.6)
