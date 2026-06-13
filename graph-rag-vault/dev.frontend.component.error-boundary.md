---
id: "dev.frontend.component.error-boundary"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "component", "error-boundary", "error-handling", "defensive"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.frontend.component.error-boundary

> #74 Defensive Programming

React 에러 처리 패턴 (예상치 못한 에러로부터 사용자 경험을 보호한다):

### 1. Next.js error.tsx — 페이지 레벨 에러 바운더리
App Router에서 자동으로 에러 바운더리 역할을 한다. 반드시 `'use client'`.

DO:
```tsx
// ✅ app/dashboard/error.tsx
"use client";

import { useEffect } from "react";
import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function DashboardError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // 에러 리포팅 서비스에 전송
    console.error("Dashboard error:", error);
    // Sentry.captureException(error);
  }, [error]);

  return (
    <div className="flex flex-col items-center justify-center gap-4 py-16">
      <AlertCircle className="h-12 w-12 text-destructive" />
      <h2 className="text-xl font-semibold">대시보드 로딩에 실패했습니다</h2>
      <p className="text-muted-foreground max-w-md text-center">
        일시적인 오류가 발생했습니다. 잠시 후 다시 시도해주세요.
      </p>
      {process.env.NODE_ENV === "development" && (
        <pre className="mt-2 max-w-lg overflow-auto rounded bg-muted p-4 text-sm">
          {error.message}
        </pre>
      )}
      <Button onClick={reset}>다시 시도</Button>
    </div>
  );
}
```

### 2. 커스텀 ErrorBoundary — 컴포넌트 레벨 격리
특정 섹션만 보호하고 나머지 UI는 정상 동작하게 할 때 사용.

DO:
```tsx
// ✅ 재사용 가능한 ErrorBoundary
"use client";

import { Component, type ErrorInfo, type ReactNode } from "react";

interface Props {
  children: ReactNode;
  fallback: ReactNode | ((error: Error, reset: () => void) => ReactNode);
  onError?: (error: Error, info: ErrorInfo) => void;
}

interface State {
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { error: null };

  static getDerivedStateFromError(error: Error): State {
    return { error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    this.props.onError?.(error, info);
  }

  reset = () => this.setState({ error: null });

  render() {
    if (this.state.error) {
      const { fallback } = this.props;
      if (typeof fallback === "function") {
        return fallback(this.state.error, this.reset);
      }
      return fallback;
    }
    return this.props.children;
  }
}
```

```tsx
// ✅ 사용 예시 — 차트 섹션만 보호
<ErrorBoundary
  fallback={(error, reset) => (
    <div className="rounded border border-destructive p-4">
      <p>차트를 불러올 수 없습니다: {error.message}</p>
      <button onClick={reset}>다시 시도</button>
    </div>
  )}
  onError={(error) => Sentry.captureException(error)}
>
  <DashboardChart data={chartData} />
</ErrorBoundary>
```

### 3. Suspense + ErrorBoundary 조합
비동기 데이터 로딩과 에러를 함께 처리한다.

DO:
```tsx
// ✅ 로딩 + 에러 동시 처리
import { Suspense } from "react";

export default function DashboardPage() {
  return (
    <div className="grid grid-cols-2 gap-4">
      {/* 각 섹션이 독립적으로 로딩/에러 처리 */}
      <ErrorBoundary fallback={<ChartErrorFallback />}>
        <Suspense fallback={<ChartSkeleton />}>
          <RevenueChart />
        </Suspense>
      </ErrorBoundary>

      <ErrorBoundary fallback={<TableErrorFallback />}>
        <Suspense fallback={<TableSkeleton />}>
          <RecentOrders />
        </Suspense>
      </ErrorBoundary>
    </div>
  );
}
```

### 4. 비동기 에러 처리 (훅 내부)
ErrorBoundary는 이벤트 핸들러, 비동기 코드의 에러를 잡지 못한다.
이벤트 핸들러 내 에러는 직접 try-catch로 처리한다.

DO:
```tsx
// ✅ 이벤트 핸들러 에러 처리
function useDeleteUser() {
  const [error, setError] = useState<Error | null>(null);

  const deleteUser = useCallback(async (userId: string) => {
    try {
      setError(null);
      const res = await fetch(`/api/users/${userId}`, { method: "DELETE" });
      if (!res.ok) throw new Error(`삭제 실패: ${res.status}`);
      toast.success("사용자가 삭제되었습니다");
    } catch (err) {
      const error = err instanceof Error ? err : new Error("Unknown");
      setError(error);
      toast.error(error.message);
    }
  }, []);

  return { deleteUser, error };
}
```

DON'T:
```tsx
// ❌ 에러 무시
const handleDelete = async () => {
  await fetch(`/api/users/${id}`, { method: "DELETE" }); // 실패 시 무시됨
};

// ❌ 사용자에게 기술적 에러 메시지 노출
<p>{error.stack}</p>  // stack trace를 그대로 보여주기
```

### Edge Cases
- ErrorBoundary는 **렌더링 중** 에러만 잡는다 (이벤트 핸들러 X, 비동기 X).
- Server Component의 에러는 가장 가까운 `error.tsx`에서 처리된다.
- `global-error.tsx`는 루트 layout 에러를 처리한다 (반드시 `<html>`, `<body>` 포함).
- 개발 환경에서만 에러 상세를 보여주고, 프로덕션에서는 사용자 친화적 메시지를 보여준다.

## Connections

- [[dev.backend.api.error]] — FEEDS (weight: 0.5)
