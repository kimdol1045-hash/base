---
id: "dev.frontend.page.isr"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "isr", "nextjs", "caching"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.page.isr

> #243 Incremental Static Regeneration (Vercel, Next.js 9.5 2020)

# ISR (Incremental Static Regeneration) 가이드

## 핵심 원칙
- SSG의 성능 이점을 유지하면서 데이터를 주기적으로 갱신한다
- `revalidate` 시간을 설정하여 캐시된 페이지를 백그라운드에서 재생성한다
- On-demand Revalidation으로 CMS 업데이트를 즉시 반영할 수 있다
- 정적 생성과 동적 데이터의 균형점을 제공한다

## DO
- 상품 목록, 뉴스 피드 등 주기적 갱신이 필요한 페이지에 사용한다
- `revalidate` 값을 데이터 특성에 맞게 설정한다 (60초~3600초)
- CMS Webhook과 On-demand Revalidation을 연결한다
- `revalidateTag`로 관련 페이지를 태그 기반 갱신한다

## DON'T
- 실시간 데이터가 필요한 페이지에 ISR을 사용하지 않는다
- revalidate 값을 너무 짧게 설정하지 않는다 (SSR과 동일해짐)
- 빌드 시 모든 페이지를 생성하지 않는다 (첫 요청 시 생성)
- On-demand Revalidation API를 인증 없이 노출하지 않는다

## 코드 예시
```tsx
// app/products/[id]/page.tsx (ISR - 60초마다 재생성)
export const revalidate = 60;

export default async function ProductPage({ params }: Props) {
  const product = await fetch(`${API_URL}/products/${params.id}`, {
    next: { revalidate: 60, tags: [`product-${params.id}`] },
  }).then(r => r.json());

  return <ProductDetail product={product} />;
}

// On-demand Revalidation API (CMS Webhook에서 호출)
// app/api/revalidate/route.ts
import { revalidateTag } from "next/cache";
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  const secret = req.headers.get("x-revalidation-secret");
  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const { tag } = await req.json();
  revalidateTag(tag);
  return NextResponse.json({ revalidated: true });
}

// CMS에서 상품 업데이트 시:
// POST /api/revalidate { "tag": "product-123" }
```
