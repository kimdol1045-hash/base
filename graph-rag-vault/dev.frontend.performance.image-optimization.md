---
id: "dev.frontend.performance.image-optimization"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "performance", "image", "next-image"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.performance.image-optimization

> #253 Image Optimization (web.dev, Google 2020)

# 이미지 최적화 가이드

## 핵심 원칙
- 이미지는 웹 페이지에서 가장 큰 페이로드를 차지한다
- 자동 포맷 변환(WebP/AVIF), 리사이즈, 지연 로딩을 적용한다
- Next.js의 `next/image`를 필수로 사용한다
- LCP(Largest Contentful Paint) 이미지는 우선 로드한다

## DO
- 모든 이미지에 `next/image`를 사용한다 (img 태그 금지)
- LCP 이미지에 `priority` 속성을 설정한다
- `sizes` 속성으로 반응형 이미지 크기를 정확히 지정한다
- placeholder="blur"로 로딩 중 레이아웃 시프트를 방지한다

## DON'T
- 원본 이미지를 리사이즈 없이 서빙하지 않는다
- 뷰포트 밖 이미지에 `priority`를 설정하지 않는다
- `width`와 `height`를 누락하여 CLS를 유발하지 않는다
- Base64 인코딩된 큰 이미지를 인라인하지 않는다

## 코드 예시
```tsx
import Image from "next/image";

// 히어로 이미지 (LCP - 우선 로드)
function HeroSection() {
  return (
    <Image
      src="/images/hero.jpg"
      alt="메인 배너"
      width={1200}
      height={600}
      priority  // LCP 이미지는 반드시 priority
      sizes="100vw"
      className="w-full h-auto object-cover"
    />
  );
}

// 상품 이미지 (지연 로드 + blur placeholder)
function ProductImage({ product }: { product: Product }) {
  return (
    <Image
      src={product.imageUrl}
      alt={product.name}
      width={400}
      height={400}
      placeholder="blur"
      blurDataURL={product.blurHash}
      sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
      className="rounded-lg"
    />
  );
}

// next.config.js 이미지 설정
const nextConfig = {
  images: {
    formats: ["image/avif", "image/webp"],
    deviceSizes: [640, 750, 828, 1080, 1200, 1920],
    imageSizes: [16, 32, 48, 64, 96, 128, 256],
    remotePatterns: [
      { protocol: "https", hostname: "cdn.example.com" },
    ],
  },
};
```
