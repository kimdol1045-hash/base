---
id: "dev.performance.web-vitals"
domain: "development.performance"
type: "rule"
region: CORTEX
token_estimate: 500
theory: "#139 Core Web Vitals (Google, 2020)"
tags: [performance, web-vitals, frontend, lcp, cls]
---

# dev.performance.web-vitals

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.performance`  
> **Type**: `rule`  
> **Theory**: #139 Core Web Vitals (Google, 2020)  
> **Tokens**: 500

## Content

Core Web Vitals (사용자 체감 성능의 핵심 3대 지표):

### 목표치
| 지표 | Good | Needs Improvement | Poor |
|------|------|-------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5-4s | > 4s |
| INP (Interaction to Next Paint) | < 200ms | 200-500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1-0.25 | > 0.25 |

### LCP 최적화
```tsx
// DO: 히어로 이미지 우선 로딩
import Image from 'next/image';
<Image src="/hero.webp" alt="hero" width={1200} height={600}
  priority  // LCP 요소에 priority 필수
  sizes="100vw"
/>

// DON'T: lazy loading on LCP element
<Image src="/hero.webp" loading="lazy" />  // ❌ LCP 지연
```

### INP 최적화
```tsx
// DO: 무거운 작업은 비동기 또는 Web Worker
const handleSearch = useDeferredValue(searchTerm);
// 또는
startTransition(() => setSearchResults(heavyFilter(data)));

// DON'T: 메인 스레드 블로킹
const results = data.filter(item => expensiveMatch(item)); // ❌ 동기 처리
```

### CLS 방지
```tsx
// DO: 이미지/영상에 크기 명시
<Image width={640} height={360} />
// DO: 스켈레톤 UI로 공간 확보
{isLoading ? <Skeleton className="h-[360px] w-full" /> : <Content />}

// DON'T: 동적 콘텐츠 삽입으로 레이아웃 밀림
{ad && <Banner />}  // ❌ 갑자기 나타나면 CLS 발생
```

### 측정 도구
- Chrome DevTools → Performance 탭
- Lighthouse (lab data)
- PageSpeed Insights (field data)
- web-vitals 라이브러리 (RUM)

## Connections

### REQUIRES (1)

- ← [[dev.performance.role]] `w=0.9`

### FEEDS (3)

- → [[dev.frontend.component.performance]] `w=0.5`
- → [[dev.performance.caching]] `w=0.7`
- → [[dev.performance.verify]] `w=0.8`

### CO_CREATES (5)

- → [[dev.performance.amdahl]] `w=0.6`
- → [[dev.performance.budget]] `w=0.6`
- → [[dev.performance.caching]] `w=0.6`
- → [[dev.performance.littles-law]] `w=0.6`
- ← [[dev.performance.role]] `w=0.6`
