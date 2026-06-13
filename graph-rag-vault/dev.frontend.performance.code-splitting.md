---
id: "dev.frontend.performance.code-splitting"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "performance", "code-splitting", "lazy-loading"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.performance.code-splitting

> #252 Code Splitting (Webpack, Dynamic Imports TC39 Proposal 2017)

# 코드 스플리팅 가이드

## 핵심 원칙
- 초기 로드에 필요하지 않은 코드를 별도 청크로 분리한다
- 라우트 기반 스플리팅을 기본으로 적용한다
- 컴포넌트 레벨 lazy loading으로 세밀하게 최적화한다
- 프리로딩(Preloading)으로 사용자 경험을 개선한다

## DO
- `React.lazy()`와 `Suspense`로 컴포넌트를 지연 로드한다
- `next/dynamic`으로 SSR이 불필요한 컴포넌트를 클라이언트에서만 로드한다
- 모달, 탭, 드로어 같은 초기에 보이지 않는 UI를 지연 로드한다
- 마우스 오버 시 프리로드하여 클릭 시 지연을 줄인다

## DON'T
- 모든 컴포넌트를 lazy loading하지 않는다 (임계 경로는 즉시 로드)
- 크기가 작은 컴포넌트(5KB 미만)를 별도 청크로 분리하지 않는다
- Suspense fallback 없이 lazy 컴포넌트를 사용하지 않는다
- 순환 의존성으로 청크가 비대해지도록 하지 않는다

## 코드 예시
```tsx
import dynamic from "next/dynamic";
import { lazy, Suspense } from "react";

// Next.js dynamic import (SSR 비활성화)
const RichTextEditor = dynamic(
  () => import("@/components/RichTextEditor"),
  { ssr: false, loading: () => <EditorSkeleton /> },
);

// React.lazy
const SettingsModal = lazy(() => import("@/components/SettingsModal"));

// 프리로딩 패턴
const ChartModule = () => import("@/components/Chart");
const LazyChart = lazy(ChartModule);

function Dashboard() {
  const [showChart, setShowChart] = useState(false);

  return (
    <div>
      <button
        onMouseEnter={() => ChartModule()} // 호버 시 프리로드
        onClick={() => setShowChart(true)}
      >
        차트 보기
      </button>
      {showChart && (
        <Suspense fallback={<ChartSkeleton />}>
          <LazyChart />
        </Suspense>
      )}
    </div>
  );
}
```
