---
id: "dev.frontend.component.suspense"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "suspense", "react", "async"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.component.suspense

> #234 React Suspense (React 18 Documentation, Meta 2022)

# React Suspense 활용 가이드

## 핵심 원칙
- Suspense는 비동기 작업(데이터 로딩, 코드 분할)의 로딩 상태를 선언적으로 처리한다
- 컴포넌트 트리의 일부분만 폴백(fallback)을 보여줄 수 있다
- 중첩된 Suspense 경계로 세밀한 로딩 상태를 제어한다
- Server Components와 함께 사용하면 스트리밍 SSR이 가능하다

## DO
- 페이지 레이아웃의 독립된 섹션마다 Suspense 경계를 설정한다
- `loading.tsx` 파일로 Next.js App Router의 자동 Suspense를 활용한다
- Skeleton UI를 fallback으로 사용하여 레이아웃 시프트를 방지한다
- `React.lazy()`와 함께 코드 분할에 활용한다

## DON'T
- 전체 페이지를 하나의 Suspense로 감싸지 않는다 (부분 로딩 활용)
- Suspense 안에서 useEffect로 데이터를 페칭하지 않는다 (서버 컴포넌트 활용)
- fallback에 무거운 컴포넌트를 렌더링하지 않는다
- 오류 처리를 Suspense에 의존하지 않는다 (ErrorBoundary 병행)

## 코드 예시
```tsx
import { Suspense } from "react";
import { ErrorBoundary } from "react-error-boundary";

// 페이지 레벨 Suspense 구성
export default function DashboardPage() {
  return (
    <div className="grid grid-cols-12 gap-4">
      <div className="col-span-8">
        <ErrorBoundary fallback={<ErrorCard />}>
          <Suspense fallback={<ChartSkeleton />}>
            <AnalyticsChart />
          </Suspense>
        </ErrorBoundary>
      </div>
      <div className="col-span-4">
        <Suspense fallback={<ListSkeleton count={5} />}>
          <RecentActivities />
        </Suspense>
      </div>
    </div>
  );
}

// Server Component에서 데이터 페칭
async function AnalyticsChart() {
  const data = await fetchAnalytics(); // 서버에서 실행
  return <Chart data={data} />;
}

// Skeleton 컴포넌트
function ChartSkeleton() {
  return (
    <div className="animate-pulse rounded-lg bg-muted h-[400px]" />
  );
}

function ListSkeleton({ count }: { count: number }) {
  return (
    <div className="space-y-3">
      {Array.from({ length: count }, (_, i) => (
        <div key={i} className="h-12 animate-pulse rounded bg-muted" />
      ))}
    </div>
  );
}
```
