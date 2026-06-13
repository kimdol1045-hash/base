---
id: "dev.performance.budget"
domain: "development.performance"
type: "rule"
region: CORTEX
token_estimate: 480
theory: "#139 Performance Budget (Grigorik, 2013)"
tags: [performance, budget, optimization, next.js]
---

# dev.performance.budget

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.performance`  
> **Type**: `rule`  
> **Theory**: #139 Performance Budget (Grigorik, 2013)  
> **Tokens**: 480

## Content

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

### REQUIRES (1)

- ← [[dev.performance.role]] `w=0.9`

### FEEDS (4)

- → [[dev.frontend.component.performance]] `w=0.5`
- → [[dev.performance.amdahl]] `w=0.7`
- ← [[dev.performance.caching]] `w=0.7`
- → [[dev.performance.verify]] `w=0.8`

### CO_CREATES (5)

- → [[dev.performance.amdahl]] `w=0.6`
- ← [[dev.performance.caching]] `w=0.6`
- → [[dev.performance.littles-law]] `w=0.6`
- ← [[dev.performance.role]] `w=0.6`
- ← [[dev.performance.web-vitals]] `w=0.6`
