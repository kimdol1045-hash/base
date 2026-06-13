---
id: "dev.frontend.component.solid"
domain: "development.frontend"
type: "rule"
region: CORTEX
token_estimate: 480
theory: "#72 SOLID.S (Martin, 2003)"
tags: [frontend, component, solid, architecture, srp]
---

# dev.frontend.component.solid

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.frontend`  
> **Type**: `rule`  
> **Theory**: #72 SOLID.S (Martin, 2003)  
> **Tokens**: 480

## Content

컴포넌트 설계 원칙 (복잡도를 제어하고 재사용성을 확보한다):

### 1. 단일 책임 (SRP)
한 컴포넌트는 한 가지 역할만 수행한다. UI와 로직을 분리한다.

DO:
```tsx
// ✅ UI만 담당하는 Presentational 컴포넌트
function UserCard({ user }: { user: User }) {
  return (
    <div className="rounded-lg border p-4">
      <h3 className="text-lg font-semibold">{user.name}</h3>
      <p className="text-muted-foreground">{user.email}</p>
    </div>
  );
}

// ✅ 로직은 훅으로 분리
function useUser(id: string) {
  return useSWR<User>(`/api/users/${id}`, fetcher);
}
```

DON'T:
```tsx
// ❌ UI + fetch + 상태 + 이벤트가 한 컴포넌트에 혼재
function UserCard({ id }: { id: string }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    fetch(`/api/users/${id}`).then(r => r.json()).then(setUser).finally(() => setLoading(false));
  }, [id]);
  const handleDelete = async () => { await fetch(`/api/users/${id}`, { method: "DELETE" }); };
  if (loading) return <Skeleton />;
  return <div onClick={handleDelete}>{user?.name}</div>;
}
```

### 2. Props 제한 (밀러의 법칙)
- Props는 **5개 이하** 권장. 초과 시 객체로 그룹핑하거나 컴포넌트를 분리한다.
- Boolean props가 **3개 이상**이면 variant 패턴으로 전환한다.

DO:
```tsx
// ✅ variant 패턴으로 통합
interface ButtonProps {
  variant: "primary" | "secondary" | "ghost" | "destructive";
  size: "sm" | "md" | "lg";
  children: React.ReactNode;
}
```

DON'T:
```tsx
// ❌ Boolean props 남발
interface ButtonProps {
  isPrimary?: boolean;
  isGhost?: boolean;
  isLarge?: boolean;
  isSmall?: boolean;
  isDestructive?: boolean;
  isOutline?: boolean;
}
```

### 3. DRY — 2회 반복 시 추출
- 같은 UI 패턴이 **2번 이상** 반복되면 컴포넌트로 추출한다.
- 같은 로직이 **2번 이상** 반복되면 커스텀 훅으로 추출한다.

### 4. 상태 관리 단계
로컬 → 공유 → 글로벌 순서로 복잡도를 올린다:
```
useState (컴포넌트 내부) → props drilling (1~2단계) → Context (테마, 인증)
→ Zustand (복잡한 클라이언트 상태) → Server State (SWR/React Query)
```

### 5. 컴포넌트 크기 기준
- JSX return 문이 **50줄 초과** 시 하위 컴포넌트로 분리한다.
- 훅 호출이 **5개 초과** 시 커스텀 훅으로 합성한다.
- 하나의 파일이 **200줄 초과** 시 파일을 분리한다.

### Edge Cases
- children을 받는 컴포넌트는 반드시 `React.ReactNode` 타입을 사용한다.
- 이벤트 핸들러를 props로 전달할 때는 optional로 선언한다.
- 조건부 훅 호출은 React 규칙 위반이므로 절대 금지한다.

## Connections

### REQUIRES (2)

- ← [[dev.frontend.component.role]] `w=0.9`
- ← [[dev.frontend.page.role]] `w=0.9`

### FEEDS (3)

- → [[dev.frontend.component.stack]] `w=0.7`
- → [[dev.frontend.component.verify]] `w=0.8`
- → [[dev.frontend.page.verify]] `w=0.8`
