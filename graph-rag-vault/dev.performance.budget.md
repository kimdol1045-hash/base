---
id: "dev.performance.budget"
domain: "development.performance"
type: "rule"
bloom_level: ""
tags: ["performance", "budget", "optimization", "next.js"]
brain_region: "CORTEX"
token_estimate: 480
---

# dev.performance.budget

> #139 Performance Budget (Grigorik, 2013)

성능 예산 (로딩 성능의 상한선을 설정하고 초과를 방지한다):

### 권장 예산
| 항목 | 예산 | 측정 |
|------|------|------|
| JS 번들 (gzipped) | < 200KB | `next build` 출력 |
| 이미지 (페이지당) | < 500KB | DevTools Network |
| 웹폰트 | < 100KB (2개 이내) | |
| 전체 페이지 무게 | < 1MB | |
| LCP | < 2.5s | Lighthouse |
| TTI (Time to Interactive) | < 3.5s | |

### Next.js 번들 최적화
```typescript
// DO: 동적 임포트로 코드 스플릿
const HeavyChart = dynamic(() => import('@/components/Chart'), {
  loading: () => <Skeleton className="h-[400px]" />,
  ssr: false,  // 서버에서 불필요한 경우
});

// DO: barrel export 지양
// ❌ import { Button } from '@/components';  // 전체 번들 포함
// ✅ import { Button } from '@/components/ui/button';  // 개별 임포트
```

### 이미지 최적화
```tsx
// next/image 필수 사용 (자동 WebP/AVIF, 리사이징, lazy)
<Image
  src="/product.jpg"
  alt="상품"
  width={640} height={480}
  sizes="(max-width: 768px) 100vw, 50vw"
  quality={80}  // 기본 75, 80이면 화질 유지하면서 크기 절약
/>
```

### 폰트 최적화
```typescript
// next/font로 자동 최적화
import { Inter } from 'next/font/google';
const inter = Inter({
  subsets: ['latin'],
  display: 'swap',  // FOUT > FOIT (텍스트 먼저 보이기)
  preload: true,
});
```

### CI에서 예산 강제
```yaml
# GitHub Actions
- name: Check bundle size
  run: |
    npx next build
    # .next/analyze 또는 @next/bundle-analyzer로 확인
```

## Connections

- [[dev.performance.role]] — REQUIRES (weight: 0.9)
- [[dev.performance.verify]] — FEEDS (weight: 0.8)
- [[dev.performance.caching]] — FEEDS (weight: 0.7)
- [[dev.performance.amdahl]] — FEEDS (weight: 0.7)
- [[dev.performance.role]] — CO_CREATES (weight: 0.6)
- [[dev.performance.web-vitals]] — CO_CREATES (weight: 0.6)
- [[dev.performance.caching]] — CO_CREATES (weight: 0.6)
- [[dev.performance.amdahl]] — CO_CREATES (weight: 0.6)
- [[dev.performance.littles-law]] — CO_CREATES (weight: 0.6)
- [[dev.frontend.component.performance]] — FEEDS (weight: 0.5)
