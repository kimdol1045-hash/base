---
id: "dev.frontend.page.ssr"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "ssr", "nextjs", "rendering"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.page.ssr

> #241 Server-Side Rendering (Next.js App Router Documentation, Vercel 2023)

# SSR (Server-Side Rendering) 가이드

## 핵심 원칙
- 매 요청마다 서버에서 HTML을 생성하여 클라이언트에 전달한다
- SEO가 중요하고, 데이터가 자주 변경되는 페이지에 적합하다
- Next.js App Router에서는 Server Components가 기본 SSR이다
- TTFB(Time to First Byte)와 데이터 신선도 사이의 균형을 고려한다

## DO
- 사용자별 맞춤 콘텐츠(대시보드, 프로필)에 SSR을 사용한다
- `cache: 'no-store'` 또는 `dynamic = 'force-dynamic'`으로 동적 렌더링을 명시한다
- Streaming SSR로 긴 데이터 로딩의 체감 속도를 개선한다
- 에러 페이지(error.tsx)를 준비한다

## DON'T
- 변경이 드문 정적 콘텐츠에 SSR을 사용하지 않는다 (SSG/ISR 사용)
- 서버 컴포넌트에서 브라우저 전용 API(window, localStorage)를 호출하지 않는다
- 무거운 연산을 매 요청마다 서버에서 수행하지 않는다 (캐시 활용)
- 모든 페이지를 SSR로 구현하지 않는다 (렌더링 전략 혼합)

## 코드 예시
```tsx
// app/dashboard/page.tsx (SSR - 매 요청마다 데이터 페칭)
export const dynamic = "force-dynamic";

async function getDashboardData(userId: string) {
  const res = await fetch(`${API_URL}/dashboard/${userId}`, {
    cache: "no-store",
    headers: { Authorization: `Bearer ${getToken()}` },
  });
  if (!res.ok) throw new Error("대시보드 데이터 로딩 실패");
  return res.json();
}

export default async function DashboardPage() {
  const session = await getServerSession();
  if (!session) redirect("/login");

  const data = await getDashboardData(session.user.id);

  return (
    <div className="grid grid-cols-12 gap-6 p-6">
      <div className="col-span-8">
        <Suspense fallback={<ChartSkeleton />}>
          <AnalyticsSection data={data.analytics} />
        </Suspense>
      </div>
      <div className="col-span-4">
        <Suspense fallback={<ListSkeleton />}>
          <RecentActivity items={data.activities} />
        </Suspense>
      </div>
    </div>
  );
}

// app/dashboard/error.tsx
"use client";
export default function Error({ error, reset }: { error: Error; reset: () => void }) {
  return (
    <div className="flex flex-col items-center gap-4 p-8">
      <p>데이터를 불러오지 못했습니다.</p>
      <button onClick={reset} className="btn-primary">다시 시도</button>
    </div>
  );
}
```
