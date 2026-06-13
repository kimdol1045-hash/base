---
id: "dev.frontend.page.ssg"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "ssg", "nextjs", "static"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.page.ssg

> #242 Static Site Generation (Jamstack, Mathias Biilmann 2015)

# SSG (Static Site Generation) 가이드

## 핵심 원칙
- 빌드 시점에 HTML을 미리 생성하여 CDN에서 서빙한다
- 가장 빠른 응답 속도와 최고의 SEO 성능을 제공한다
- 콘텐츠가 자주 변경되지 않는 페이지에 적합하다
- Next.js App Router에서는 기본 동작이 정적 렌더링이다

## DO
- 마케팅 페이지, 블로그, 문서 등에 SSG를 사용한다
- `generateStaticParams`로 동적 경로의 정적 페이지를 미리 생성한다
- `fetch`의 기본 캐싱(`force-cache`)을 활용한다
- 빌드 시간이 긴 경우 중요 페이지만 미리 생성하고 나머지는 on-demand로 처리한다

## DON'T
- 사용자별 데이터가 필요한 페이지에 SSG를 사용하지 않는다
- 수천 개의 페이지를 모두 빌드 시점에 생성하지 않는다 (ISR 활용)
- 빌드 시 외부 API 장애로 전체 배포가 실패하도록 두지 않는다
- 인증이 필요한 페이지를 정적으로 생성하지 않는다

## 코드 예시
```tsx
// app/blog/[slug]/page.tsx (SSG)
import { notFound } from "next/navigation";

// 빌드 시 생성할 경로 목록
export async function generateStaticParams() {
  const posts = await fetch(`${CMS_URL}/posts`).then(r => r.json());
  return posts.map((post: Post) => ({ slug: post.slug }));
}

// 메타데이터 생성
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getPost(params.slug);
  if (!post) return {};
  return {
    title: post.title,
    description: post.excerpt,
    openGraph: { images: [post.coverImage] },
  };
}

async function getPost(slug: string) {
  const res = await fetch(`${CMS_URL}/posts/${slug}`, {
    next: { tags: [`post-${slug}`] },
  });
  if (!res.ok) return null;
  return res.json();
}

export default async function BlogPost({ params }: Props) {
  const post = await getPost(params.slug);
  if (!post) notFound();

  return (
    <article className="prose mx-auto max-w-3xl">
      <h1>{post.title}</h1>
      <time>{formatDate(post.publishedAt)}</time>
      <div dangerouslySetInnerHTML={{ __html: post.contentHtml }} />
    </article>
  );
}
```
