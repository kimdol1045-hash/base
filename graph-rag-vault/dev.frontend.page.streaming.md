---
id: "dev.frontend.page.streaming"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "streaming", "ssr", "suspense"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.page.streaming

> #244 Streaming SSR (React 18 Selective Hydration, Meta 2022)

# Streaming SSR 가이드

## 핵심 원칙
- HTML을 한 번에 보내지 않고, 준비된 부분부터 점진적으로 스트리밍한다
- TTFB를 크게 개선하여 사용자가 빠르게 콘텐츠를 볼 수 있다
- Suspense 경계 단위로 스트리밍이 동작한다
- Selective Hydration으로 인터랙티브 부분을 우선 활성화한다

## DO
- 느린 데이터 소스를 포함하는 컴포넌트를 Suspense로 감싼다
- 레이아웃 쉘(header, sidebar)은 즉시 전송하고 콘텐츠는 스트리밍한다
- `loading.tsx` 파일로 자동 스트리밍을 구성한다
- 독립적인 데이터 요청은 병렬로 실행한다

## DON'T
- 전체 페이지를 하나의 await로 블로킹하지 않는다
- 스트리밍이 필요 없는 단순 페이지에 불필요한 Suspense를 추가하지 않는다
- 데이터 의존성 체인을 길게 만들지 않는다 (워터폴 방지)
- fallback UI의 높이를 실제 콘텐츠와 크게 다르게 만들지 않는다

## 코드 예시
```tsx
// app/dashboard/page.tsx - 스트리밍 SSR
import { Suspense } from "react";

export default function DashboardPage() {
  return (
    <div className="grid grid-cols-12 gap-6">
      {/* 레이아웃 쉘은 즉시 전송 */}
      <header className="col-span-12">
        <DashboardHeader />
      </header>

      {/* 각 섹션이 독립적으로 스트리밍 */}
      <div className="col-span-4">
        <Suspense fallback={<StatsSkeleton />}>
          <StatsSection />     {/* DB 조회 500ms */}
        </Suspense>
      </div>

      <div className="col-span-8">
        <Suspense fallback={<ChartSkeleton />}>
          <ChartSection />     {/* 외부 API 2초 */}
        </Suspense>
      </div>

      <div className="col-span-12">
        <Suspense fallback={<TableSkeleton rows={10} />}>
          <DataTable />        {/* 무거운 쿼리 3초 */}
        </Suspense>
      </div>
    </div>
  );
}

// 병렬 데이터 페칭
async function StatsSection() {
  const [users, revenue, orders] = await Promise.all([
    fetchUserCount(),
    fetchRevenue(),
    fetchOrderCount(),
  ]);
  return <StatsGrid users={users} revenue={revenue} orders={orders} />;
}
```
