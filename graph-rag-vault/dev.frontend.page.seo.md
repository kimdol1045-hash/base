---
id: "dev.frontend.page.seo"
domain: "development.frontend"
type: "rule"
bloom_level: ""
tags: ["frontend", "page", "seo", "metadata", "structured-data", "nextjs"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.frontend.page.seo

> #131 SEO (Google Webmaster Guidelines)

Next.js SEO 최적화 규칙 (검색 엔진이 콘텐츠를 정확히 이해하고 노출하도록 한다):

### 1. Metadata API — 정적 & 동적 메타데이터

DO:
```tsx
// ✅ 정적 메타데이터 (layout.tsx 또는 page.tsx)
import { type Metadata } from "next";

export const metadata: Metadata = {
  title: {
    default: "MyApp — 설명",
    template: "%s | MyApp",  // 하위 페이지: "대시보드 | MyApp"
  },
  description: "서비스 설명 (120~160자). 핵심 키워드 포함.",
  keywords: ["SaaS", "프로젝트 관리", "협업 도구"],
  authors: [{ name: "MyApp Team" }],
  openGraph: {
    type: "website",
    locale: "ko_KR",
    url: "https://myapp.com",
    siteName: "MyApp",
    images: [
      {
        url: "https://myapp.com/og-image.png",
        width: 1200,
        height: 630,
        alt: "MyApp 소개 이미지",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    creator: "@myapp",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
};
```

```tsx
// ✅ 동적 메타데이터 (상세 페이지)
export async function generateMetadata({
  params,
}: {
  params: { slug: string };
}): Promise<Metadata> {
  const post = await getPost(params.slug);
  if (!post) return { title: "Not Found" };

  return {
    title: post.title,
    description: post.excerpt.slice(0, 160),
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [{ url: post.coverImage, width: 1200, height: 630 }],
      type: "article",
      publishedTime: post.publishedAt,
      authors: [post.author.name],
    },
    alternates: {
      canonical: `https://myapp.com/blog/${params.slug}`,
    },
  };
}
```

DON'T:
```tsx
// ❌ 메타데이터 누락
export default function Page() {
  return <div>콘텐츠</div>; // title, description 없음
}

// ❌ 하드코딩된 title (동적 페이지에서)
export const metadata = { title: "상세 페이지" }; // 모든 상세 페이지가 같은 제목
```

### 2. 구조화된 데이터 (JSON-LD)
검색 엔진이 콘텐츠 의미를 이해하도록 Schema.org 마크업을 추가한다.

DO:
```tsx
// ✅ JSON-LD 구조화 데이터
export default async function BlogPost({ params }: { params: { slug: string } }) {
  const post = await getPost(params.slug);

  const jsonLd = {
    "@context": "https://schema.org",
    "@type": "BlogPosting",
    headline: post.title,
    description: post.excerpt,
    image: post.coverImage,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      "@type": "Person",
      name: post.author.name,
      url: post.author.url,
    },
  };

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <article>
        <h1>{post.title}</h1>
        {/* ... */}
      </article>
    </>
  );
}
```

### 3. sitemap.xml & robots.txt

```tsx
// ✅ app/sitemap.ts — 동적 사이트맵
import { type MetadataRoute } from "next";

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const posts = await getAllPosts();

  const postUrls = posts.map((post) => ({
    url: `https://myapp.com/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: "weekly" as const,
    priority: 0.8,
  }));

  return [
    { url: "https://myapp.com", lastModified: new Date(), priority: 1.0 },
    { url: "https://myapp.com/about", lastModified: new Date(), priority: 0.5 },
    ...postUrls,
  ];
}
```

```tsx
// ✅ app/robots.ts
import { type MetadataRoute } from "next";

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/api/", "/dashboard/", "/admin/"],
      },
    ],
    sitemap: "https://myapp.com/sitemap.xml",
  };
}
```

### 4. 시맨틱 HTML 규칙
- `h1`은 페이지당 **1개만** 사용한다.
- 제목은 `h1 → h2 → h3` 순서로 건너뛰지 않는다 (h1 다음 h3 금지).
- 메인 콘텐츠는 `<main>`, 내비게이션은 `<nav>`, 보조는 `<aside>` 사용.
- 이미지에 의미 있는 `alt` 텍스트 필수 (장식 이미지: `alt=""`).
- 링크 텍스트는 설명적으로 ("여기 클릭" 금지, "사용자 가이드 보기" 사용).

### 5. 성능 & Core Web Vitals
- LCP (Largest Contentful Paint): 히어로 이미지에 `priority` 속성 추가.
- CLS (Cumulative Layout Shift): 이미지/비디오에 width, height 명시.
- FID (First Input Delay): 무거운 JS를 dynamic import로 지연.

```tsx
// ✅ 히어로 이미지 최적화
import Image from "next/image";
<Image
  src="/hero.webp"
  alt="서비스 소개 히어로 이미지"
  width={1200}
  height={630}
  priority  // LCP 최적화: 프리로드
  className="w-full h-auto"
/>
```

### Edge Cases
- SPA 모달 내 콘텐츠는 검색 엔진이 크롤링하기 어렵다. 중요한 콘텐츠는 별도 페이지로.
- `noindex` 페이지에도 `canonical` URL을 설정하면 중복 콘텐츠 문제를 방지한다.
- 다국어 사이트는 `alternates.languages`로 hreflang을 설정한다.

## Connections

- [[marketing.seo.role]] — FEEDS (weight: 0.5)
- [[marketing.seo.technical-seo]] — FEEDS (weight: 0.5)
- [[marketing.seo.content-seo]] — FEEDS (weight: 0.5)
- [[marketing.seo.verify]] — FEEDS (weight: 0.5)
- [[marketing.copy.seo]] — FEEDS (weight: 0.5)
