---
id: "dev.frontend.page.parallel-routes"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "parallel-routes", "nextjs", "layout"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.page.parallel-routes

> #245 Parallel Routes (Next.js 13.3+ App Router Documentation, Vercel 2023)

# Parallel Routes 가이드

## 핵심 원칙
- 하나의 레이아웃에서 여러 페이지를 동시에 렌더링한다
- 슬롯(@folder)으로 독립적인 라우팅 영역을 정의한다
- 각 슬롯은 독립적으로 로딩/에러 상태를 가질 수 있다
- 조건부 렌더링(인증 상태별 다른 콘텐츠)에 유용하다

## DO
- 대시보드의 독립적인 패널에 Parallel Routes를 사용한다
- 모달을 Parallel Routes로 구현하여 URL과 동기화한다
- 각 슬롯에 `loading.tsx`와 `default.tsx`를 제공한다
- 인증 여부에 따라 다른 슬롯을 렌더링한다

## DON'T
- 단순한 레이아웃에 불필요하게 Parallel Routes를 사용하지 않는다
- `default.tsx`를 누락하여 404 에러를 유발하지 않는다
- 슬롯 간 상태 공유를 직접 props로 하지 않는다 (URL params 또는 Context)
- 너무 많은 슬롯을 한 레이아웃에 배치하지 않는다

## 코드 예시
```
app/dashboard/
├── layout.tsx          # 메인 레이아웃
├── page.tsx            # 기본 콘텐츠
├── @analytics/         # 분석 슬롯
│   ├── page.tsx
│   ├── loading.tsx
│   └── default.tsx
├── @notifications/     # 알림 슬롯
│   ├── page.tsx
│   ├── loading.tsx
│   └── default.tsx
└── @modal/             # 모달 슬롯
    ├── (.)detail/[id]/page.tsx
    └── default.tsx
```

```tsx
// app/dashboard/layout.tsx
export default function DashboardLayout({
  children,
  analytics,
  notifications,
  modal,
}: {
  children: React.ReactNode;
  analytics: React.ReactNode;
  notifications: React.ReactNode;
  modal: React.ReactNode;
}) {
  return (
    <div className="grid grid-cols-12 gap-4">
      <main className="col-span-8">{children}</main>
      <aside className="col-span-4 space-y-4">
        {analytics}
        {notifications}
      </aside>
      {modal}
    </div>
  );
}

// app/dashboard/@analytics/default.tsx (필수)
export default function Default() {
  return null;
}
```
