---
id: "marketing.seo.technical-seo"
domain: "marketing"
type: "rule"
region: SENSORS
token_estimate: 500
theory: "#60 ELM (Petty & Cacioppo, 1986) — 정보 접근 경로"
tags: [marketing, seo, technical, metadata, json-ld, sitemap, next-js]
---

# marketing.seo.technical-seo

> **Region**: 📡 [[SENSORS]]  
> **Domain**: `marketing`  
> **Type**: `rule`  
> **Theory**: #60 ELM (Petty & Cacioppo, 1986) — 정보 접근 경로  
> **Tokens**: 500

## Content

Technical SEO — 검색 엔진이 사이트를 올바르게 크롤링, 인덱싱, 렌더링하도록 기술적 기반을 최적화:

### 1. 메타태그 (Next.js Metadata API)
```typescript
// DO: 페이지별 동적 메타데이터 생성
import { Metadata } from "next";

// 정적 페이지
export const metadata: Metadata = {
  title: "SaaS 프로젝트 관리 도구 | AppName",        // 30~60자
  description: "팀 협업을 위한 프로젝트 관리. 칸반 보드, 타임라인, 자동화 기능으로 생산성 34% 향상.",  // 80~160자
  alternates: {
    canonical: "https://app.example.com/features",   // canonical URL
  },
  openGraph: {
    title: "프로젝트 관리, 더 스마트하게",
    description: "12,000+ 팀이 선택한 협업 도구",
    images: [{ url: "/og-features.png", width: 1200, height: 630 }],
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "프로젝트 관리, 더 스마트하게",
  },
};

// 동적 페이지 (블로그 포스트)
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getPost(params.slug);
  return {
    title: `${post.title} | AppName Blog`,
    description: post.excerpt.slice(0, 155) + "...",
    alternates: { canonical: `https://app.example.com/blog/${params.slug}` },
  };
}
```

### 2. 구조화 데이터 (JSON-LD)
```typescript
// DO: 페이지 유형에 맞는 JSON-LD 삽입
// Article (블로그)
const articleJsonLd = {
  "@context": "https://schema.org",
  "@type": "Article",
  headline: post.title,
  author: { "@type": "Person", name: post.author },
  datePublished: post.publishedAt,
  dateModified: post.updatedAt,
  image: post.coverImage,
  publisher: {
    "@type": "Organization",
    name: "AppName",
    logo: { "@type": "ImageObject", url: "https://app.example.com/logo.png" },
  },
};

// Product (SaaS 가격 페이지)
const productJsonLd = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "AppName Pro",
  applicationCategory: "ProjectManagement",
  offers: {
    "@type": "Offer",
    price: "29",
    priceCurrency: "USD",
    priceValidUntil: "2025-12-31",
  },
  aggregateRating: {
    "@type": "AggregateRating",
    ratingValue: "4.8",
    reviewCount: "2341",
  },
};

// 컴포넌트에 삽입
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(articleJsonLd) }} />
```

### 3. 사이트맵 + robots.txt
```typescript
// DO: Next.js App Router sitemap.ts
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getAllPosts();
  const postUrls = posts.map((post) => ({
    url: `https://app.example.com/blog/${post.slug}`,
    lastModified: post.updatedAt,
    changeFrequency: "weekly" as const,
    priority: 0.7,
  }));

  return [
    { url: "https://app.example.com", lastModified: new Date(), priority: 1.0 },
    { url: "https://app.example.com/pricing", priority: 0.9 },
    { url: "https://app.example.com/features", priority: 0.8 },
    ...postUrls,
  ];
}

// robots.ts
export default function robots(): MetadataRoute.Robots {
  return {
    rules: { userAgent: "*", allow: "/", disallow: ["/api/", "/admin/", "/dashboard/"] },
    sitemap: "https://app.example.com/sitemap.xml",
  };
}
```

DON'T:
```typescript
// ❌ 메타 설명 누락 — Google이 자동 생성 (제어 불가)
export const metadata = { title: "Features" };
// description 없음, OG tags 없음

// ❌ 크롤러 실수로 차단
// robots.txt에서 Disallow: / 설정 → 전체 사이트 인덱스 제외

// ❌ canonical 없는 중복 콘텐츠
// /products?sort=price 와 /products?sort=name 이 별도 페이지로 인덱싱
// → 동일 콘텐츠가 여러 URL로 분산 → 순위 하락
```

### 성능과 SEO의 관계
| Core Web Vitals | 기준 | SEO 영향 |
|-----------------|------|---------|
| LCP (Largest Contentful Paint) | < 2.5초 | 직접 순위 요소 |
| INP (Interaction to Next Paint) | < 200ms | 직접 순위 요소 |
| CLS (Cumulative Layout Shift) | < 0.1 | 직접 순위 요소 |

## Connections

### FEEDS (2)

- → [[dev.frontend.page.seo]] `w=0.5`
- → [[marketing.copy.seo]] `w=0.5`

### CO_CREATES (3)

- → [[marketing.seo.content-seo]] `w=0.6`
- ← [[marketing.seo.role]] `w=0.6`
- → [[marketing.seo.verify]] `w=0.6`
