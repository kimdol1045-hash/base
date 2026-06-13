---
id: "dev.frontend.page.data-fetching"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "page", "data-fetching", "nextjs", "ssr", "ssg", "isr", "server-components"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.frontend.page.data-fetching

> #75 SSR/SSG/ISR Rendering Strategies (Vercel, 2020)

Next.js 14 데이터 페칭 패턴 (올바른 렌더링 전략을 선택하여 성능과 신선도를 균형 잡는다):

### 1. Server Components — 기본 데이터 페칭
Server Component에서 직접 async/await로 데이터를 가져온다.
fetch API에 캐싱 옵션을 지정하여 렌더링 전략을 결정한다.

DO:
```tsx
// ✅ 정적 생성 (SSG) — 빌드 타임에 생성, CDN 캐싱
// 변경이 드문 데이터: 블로그 글, 문서, 약관 등
async function getPost(slug: string) {
  const res = await fetch(`${API_URL}/posts/${slug}`, {
    cache: "force-cache", // 기본값. 무기한 캐싱
  });
  if (!res.ok) throw new Error("Failed to fetch post");
  return res.json() as Promise<Post>;
}

// ✅ ISR (Incremental Static Regeneration) — 주기적 갱신
// 자주 변하지만 실시간일 필요 없는 데이터: 상품 목록, 가격 등
async function getProducts() {
  const res = await fetch(`${API_URL}/products`, {
    next: { revalidate: 3600 }, // 1시간마다 갱신
  });
  return res.json() as Promise<Product[]>;
}

// ✅ 동적 렌더링 (SSR) — 매 요청마다 새로 가져옴
// 사용자별 데이터, 실시간 데이터
async function getUserProfile(userId: string) {
  const res = await fetch(`${API_URL}/users/${userId}`, {
    cache: "no-store", // 캐싱 없음
  });
  return res.json() as Promise<UserProfile>;
}
```

### 2. 렌더링 전략 판단 기준

| 전략 | 캐싱 설정 | 적합한 데이터 | 예시 |
|------|----------|-------------|------|
| **SSG** | `force-cache` (기본) | 변경 없음 | 블로그, 문서, 약관 |
| **ISR** | `next: { revalidate: N }` | 주기적 변경 | 상품 목록, 가격, 랭킹 |
| **SSR** | `cache: "no-store"` | 매 요청 변경 | 사용자 프로필, 장바구니 |
| **CSR** | SWR/React Query | 실시간 인터랙션 | 댓글, 알림, 채팅 |

### 3. Server vs Client Component 판단 기준

**Server Component 사용** (기본):
- 데이터 페칭이 필요한 경우
- 민감한 정보(API 키, DB 접근)를 사용하는 경우
- 번들 크기를 줄여야 하는 경우
- SEO가 중요한 콘텐츠

**Client Component 사용** (`'use client'`):
- `onClick`, `onChange` 등 이벤트 리스너가 필요한 경우
- `useState`, `useEffect` 등 React 훅이 필요한 경우
- 브라우저 API (localStorage, geolocation) 사용
- 실시간 업데이트 (WebSocket, polling)

DO:
```tsx
// ✅ Server Component에서 데이터 → Client Component에 주입
// app/dashboard/page.tsx (Server)
export default async function DashboardPage() {
  const stats = await getStats();       // 서버에서 페칭
  const recentOrders = await getOrders(); // 서버에서 페칭

  return (
    <div className="grid grid-cols-12 gap-6">
      {/* 정적 표시 → Server Component */}
      <StatsCards stats={stats} />

      {/* 필터/정렬 인터랙션 → Client Component */}
      <OrderTable initialOrders={recentOrders} />
    </div>
  );
}

// components/OrderTable.tsx (Client)
"use client";
export function OrderTable({ initialOrders }: { initialOrders: Order[] }) {
  const [filter, setFilter] = useState("");
  const filtered = initialOrders.filter(o => o.status.includes(filter));
  return (/* 인터랙티브 테이블 */);
}
```

DON'T:
```tsx
// ❌ 페이지 전체를 Client Component로 — 번들 크기 증가 + SEO 불리
"use client";
export default function DashboardPage() {
  const { data } = useSWR("/api/stats", fetcher);
  return <div>{data?.revenue}</div>;
}

// ❌ Server Component에서 이벤트 핸들러 사용 (불가능)
export default async function Page() {
  return <button onClick={() => alert("hi")}>Click</button>; // 에러!
}
```

### 4. 병렬 데이터 페칭
여러 데이터가 필요하면 `Promise.all`로 병렬 처리한다.

DO:
```tsx
// ✅ 병렬 페칭 — 가장 느린 요청 시간만큼만 대기
export default async function DashboardPage() {
  const [stats, orders, notifications] = await Promise.all([
    getStats(),
    getOrders(),
    getNotifications(),
  ]);

  return (
    <>
      <StatsCards stats={stats} />
      <OrderTable orders={orders} />
      <NotificationList notifications={notifications} />
    </>
  );
}
```

DON'T:
```tsx
// ❌ 순차 페칭 — 워터폴 발생 (총 시간 = 각 요청 합산)
export default async function DashboardPage() {
  const stats = await getStats();           // 200ms
  const orders = await getOrders();         // 300ms (200ms 후 시작)
  const notifications = await getNotifications(); // 150ms (500ms 후 시작)
  // 총 650ms (병렬이면 300ms)
}
```

### 5. Streaming & Suspense
독립적인 섹션은 Suspense로 감싸서 점진적 로딩한다.

```tsx
// ✅ 느린 섹션만 Suspense로 격리
export default async function Page() {
  return (
    <main>
      <h1>대시보드</h1>
      {/* 빠른 데이터: 즉시 렌더링 */}
      <QuickStats />

      {/* 느린 데이터: Suspense로 스트리밍 */}
      <Suspense fallback={<ChartSkeleton />}>
        <SlowChart />
      </Suspense>
    </main>
  );
}
```

### Edge Cases
- `cookies()`, `headers()` 호출 시 자동으로 동적 렌더링으로 전환된다.
- `searchParams`를 사용하면 동적 렌더링이 된다.
- Server Action (`'use server'`)은 mutation에만 사용한다 (데이터 변경).
- revalidation: `revalidatePath()`, `revalidateTag()` 으로 on-demand 갱신 가능.

## Connections

- [[dev.frontend.component.role]] — CO_CREATES (weight: 0.6)
- [[dev.frontend.component.stack]] — CO_CREATES (weight: 0.6)
- [[dev.frontend.page.role]] — CO_CREATES (weight: 0.6)
