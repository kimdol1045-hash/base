---
id: "dev.frontend.page.nextjs-patterns"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "nextjs", "app-router", "server-components"]
brain_region: "CORTEX"
token_estimate: 450
---

# dev.frontend.page.nextjs-patterns

> #161 Next.js App Router Patterns (Vercel, 2023+)

Next.js App Router 패턴 (서버/클라이언트 경계를 올바르게 설계한다):

### Server vs Client Components
| 구분 | Server Component (기본) | Client Component ('use client') |
|------|------------------------|-------------------------------|
| 용도 | 데이터 페칭, 정적 콘텐츠 | 인터랙션, 상태, 브라우저 API |
| 번들 | 포함 안 됨 (제로 JS) | 클라이언트 번들에 포함 |
| 예시 | 페이지 레이아웃, DB 조회 | 폼, 모달, 드롭다운 |

### 데이터 페칭 패턴
```tsx
// Server Component에서 직접 async
async function ProductPage({ params }: { params: { id: string } }) {
  const product = await db.product.findUnique({
    where: { id: params.id }
  });
  return <ProductDetail product={product} />;
}
```

### 레이아웃 중첩
```
app/
  layout.tsx          ← 루트 레이아웃 (html, body)
  (marketing)/
    layout.tsx        ← 마케팅 전용 레이아웃
    page.tsx
  (app)/
    layout.tsx        ← 앱 전용 레이아웃 (사이드바)
    dashboard/
      page.tsx
```

### Server Actions
```tsx
async function createPost(formData: FormData) {
  'use server';
  const title = formData.get('title') as string;
  await db.post.create({ data: { title } });
  revalidatePath('/posts');
}
```

### 캐싱/재검증
- `revalidatePath()`: 특정 경로 캐시 무효화
- `revalidateTag()`: 태그 기반 무효화
- `unstable_cache()`: 함수 레벨 캐싱

### 주의사항
- 'use client' 경계를 최대한 아래로 (leaf에 가깝게)
- Server Component에서 클라이언트 훅(useState 등) 사용 불가
- 민감 데이터는 Server Component/Action에서만 접근

## Connections

- [[dev.frontend.page.role]] — CO_CREATES (weight: 0.6)
- [[dev.frontend.page.routing]] — CO_CREATES (weight: 0.6)
