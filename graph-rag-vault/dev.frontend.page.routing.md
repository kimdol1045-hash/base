---
id: "dev.frontend.page.routing"
domain: "development.frontend"
type: "rule"
bloom_level: ""
tags: ["frontend", "page", "routing", "nextjs", "app-router", "navigation"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.frontend.page.routing

Next.js App Router 라우팅 규칙 (예측 가능한 URL 구조와 최적화된 네비게이션):

### 1. 파일 기반 라우팅
디렉토리 구조가 곧 URL이다. 명확한 RESTful 패턴을 따른다.

```
app/
  page.tsx                    → /
  about/page.tsx              → /about
  users/
    page.tsx                  → /users          (목록)
    [id]/
      page.tsx                → /users/123      (상세)
      edit/page.tsx           → /users/123/edit (수정)
  dashboard/
    layout.tsx                → 대시보드 공유 레이아웃
    page.tsx                  → /dashboard
    settings/page.tsx         → /dashboard/settings
  (auth)/
    login/page.tsx            → /login          (Route Group)
    register/page.tsx         → /register
  api/
    users/route.ts            → /api/users      (API Route)
```

### 2. 동적 라우트 패턴

DO:
```tsx
// ✅ 동적 세그먼트 — app/posts/[slug]/page.tsx
export default async function PostPage({
  params,
}: {
  params: { slug: string };
}) {
  const post = await getPostBySlug(params.slug);
  if (!post) notFound();
  return <PostContent post={post} />;
}

// ✅ 정적 경로 생성 (빌드 타임)
export async function generateStaticParams() {
  const posts = await getAllPosts();
  return posts.map((post) => ({ slug: post.slug }));
}

// ✅ Catch-all 세그먼트 — app/docs/[...slug]/page.tsx
// /docs/intro, /docs/guide/setup 등 모두 매칭
export default function DocsPage({
  params,
}: {
  params: { slug: string[] };
}) {
  const path = params.slug.join("/");
  return <DocContent path={path} />;
}
```

DON'T:
```tsx
// ❌ query string으로 ID 전달 (App Router에서 비권장)
// /users?id=123 대신 /users/123 사용
export default function UserPage() {
  const searchParams = useSearchParams();
  const id = searchParams.get("id"); // ❌
}
```

### 3. Route Group — 레이아웃 분리
괄호 `(group)`은 URL에 영향 없이 레이아웃을 공유한다.

```
app/
  (marketing)/              → URL에 포함되지 않음
    layout.tsx              → 마케팅 레이아웃 (헤더, 푸터)
    page.tsx                → /
    pricing/page.tsx        → /pricing
  (dashboard)/
    layout.tsx              → 대시보드 레이아웃 (사이드바)
    dashboard/page.tsx      → /dashboard
    settings/page.tsx       → /settings
```

### 4. Parallel Routes & Intercepting Routes

```
// Parallel Routes — 동시에 여러 슬롯 렌더링
app/
  layout.tsx                → children + @modal 슬롯 모두 렌더링
  @modal/
    (.)photo/[id]/page.tsx  → 모달로 인터셉트
  photo/[id]/page.tsx       → 직접 접근 시 전체 페이지
```

### 5. 네비게이션
DO:
```tsx
// ✅ Link 컴포넌트 (프리페칭 자동)
import Link from "next/link";
<Link href="/users/123" className="text-primary hover:underline">
  사용자 프로필
</Link>

// ✅ 프로그래매틱 네비게이션
"use client";
import { useRouter } from "next/navigation";
const router = useRouter();
router.push("/dashboard");
router.replace("/login");  // 히스토리 대체
router.back();
```

DON'T:
```tsx
// ❌ a 태그 직접 사용 (프리페칭 없음, full reload)
<a href="/users">Users</a>

// ❌ next/router (pages/ 전용, App Router에서 사용 불가)
import { useRouter } from "next/router";
```

### Edge Cases
- `loading.tsx`는 해당 경로 이하 모든 하위 페이지에 적용된다.
- `layout.tsx`는 리렌더링되지 않는다 (상태 유지). 페이지 전환 시 초기화 필요하면 `template.tsx` 사용.
- `searchParams`는 Server Component에서 `page.tsx`의 props로 받는다.
- Middleware는 `middleware.ts` (루트)에서 인증, 리다이렉트 등 처리.

## Connections

- [[dev.frontend.component.role]] — REQUIRES (weight: 0.9)
- [[dev.frontend.page.role]] — REQUIRES (weight: 0.9)
- [[dev.frontend.component.verify]] — FEEDS (weight: 0.8)
- [[dev.frontend.page.verify]] — FEEDS (weight: 0.8)
- [[dev.frontend.component.stack]] — FEEDS (weight: 0.7)
- [[dev.frontend.page.role]] — CO_CREATES (weight: 0.6)
- [[dev.frontend.page.nextjs-patterns]] — CO_CREATES (weight: 0.6)
