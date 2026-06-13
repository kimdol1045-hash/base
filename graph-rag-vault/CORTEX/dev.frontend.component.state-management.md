---
id: "dev.frontend.component.state-management"
domain: "development.frontend"
type: "pattern"
region: CORTEX
token_estimate: 500
theory: "#21 Miller's Law — 정보 청킹 (Miller, 1956)"
tags: [frontend, state-management, zustand, react-query, tanstack, context, url-state]
---

# dev.frontend.component.state-management

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.frontend`  
> **Type**: `pattern`  
> **Theory**: #21 Miller's Law — 정보 청킹 (Miller, 1956)  
> **Tokens**: 500

## Content

상태 관리 패턴 (상태를 유형별로 분류하고 적합한 도구를 선택한다):

### 상태 유형 분류표

| 상태 유형 | 예시 | 권장 도구 | 갱신 빈도 |
|-----------|------|-----------|-----------|
| Server State | API 데이터, 목록, 상세 | TanStack Query / SWR | 서버 변경 시 |
| Client Global | 테마, 사이드바 열림, 토스트 | Zustand | 사용자 액션 |
| Client Local | 폼 입력, 모달 열림, 토글 | useState | 즉시 |
| URL State | 필터, 페이지, 정렬, 탭 | nuqs / searchParams | 네비게이션 |
| Form State | 폼 값, 유효성, 제출 상태 | React Hook Form | 입력 시 |

핵심 원칙: **Server State와 Client State를 절대 섞지 않는다.**

### 1. Server State — TanStack Query
DO:
```typescript
// ✅ TanStack Query — 캐싱, 리페칭, 로딩/에러 자동 관리
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";

function useProjects() {
  return useQuery({
    queryKey: ["projects"],
    queryFn: () => api.get<Project[]>("/projects"),
    staleTime: 5 * 60 * 1000,   // 5분간 fresh (불필요한 리페칭 방지)
    gcTime: 30 * 60 * 1000,     // 30분간 캐시 유지
  });
}

function useCreateProject() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: CreateProjectDto) => api.post("/projects", data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["projects"] }); // 목록 갱신
    },
  });
}
```

### 2. Client Global State — Zustand
```typescript
// ✅ Zustand — 보일러플레이트 최소, 선택적 구독
import { create } from "zustand";

interface UIStore {
  sidebarOpen: boolean;
  toggleSidebar: () => void;
  theme: "light" | "dark";
  setTheme: (theme: "light" | "dark") => void;
}

const useUIStore = create<UIStore>((set) => ({
  sidebarOpen: true,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  theme: "light",
  setTheme: (theme) => set({ theme }),
}));

// ✅ 선택적 구독 — 필요한 값만 구독 (불필요한 리렌더 방지)
function Sidebar() {
  const isOpen = useUIStore((s) => s.sidebarOpen); // sidebarOpen만 구독
  return isOpen ? <SidebarContent /> : null;
}
```

### 3. URL State — 필터/검색/페이지
```typescript
// ✅ nuqs — type-safe URL state (Next.js App Router)
import { useQueryState, parseAsInteger } from "nuqs";

function ProductList() {
  const [search, setSearch] = useQueryState("q", { defaultValue: "" });
  const [page, setPage] = useQueryState("page", parseAsInteger.withDefault(1));
  const [sort, setSort] = useQueryState("sort", { defaultValue: "newest" });

  const { data } = useQuery({
    queryKey: ["products", { search, page, sort }],
    queryFn: () => api.get("/products", { params: { q: search, page, sort } }),
  });
}
```

### 4. Context — 소규모 주입 (테마, 인증)
```typescript
// ✅ Context는 자주 변경되지 않는 값에만 사용
const AuthContext = createContext<AuthState | null>(null);

function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
```

DON'T:
```typescript
// ❌ Redux for everything — 과도한 보일러플레이트
// action type 정의 → action creator → reducer → selector → dispatch
// 단순한 UI 토글에 4개 파일 필요

// ❌ useEffect로 데이터 페칭 — 캐싱/로딩/에러 수동 관리
const [users, setUsers] = useState<User[]>([]);
const [loading, setLoading] = useState(true);
useEffect(() => {
  fetch("/api/users").then(r => r.json()).then(setUsers).finally(() => setLoading(false));
}, []); // 캐싱 없음, 경쟁 조건, 메모리 누수 위험

// ❌ 로컬 상태를 글로벌로 올림 — 불필요한 리렌더 전파
// 모달 열림 상태를 Zustand에 저장? → useState로 충분
```
