---
id: "dev.frontend.performance.web-vitals"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "performance", "web-vitals", "lighthouse"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.performance.web-vitals

> #254 Core Web Vitals (Google, Web Vitals Initiative 2020)

# Core Web Vitals 최적화 가이드

## 핵심 원칙
- LCP, INP, CLS 세 가지 핵심 지표를 모니터링하고 최적화한다
- 실제 사용자 데이터(RUM)와 실험실 데이터(Lighthouse)를 모두 활용한다
- 성능 예산을 설정하고 CI에서 자동 검증한다
- 75번째 백분위수(p75)를 기준으로 평가한다

## 핵심 지표
| 지표 | 좋음 | 보통 | 나쁨 | 의미 |
|------|------|------|------|------|
| LCP | < 2.5s | < 4.0s | > 4.0s | 가장 큰 콘텐츠 요소 로드 시간 |
| INP | < 200ms | < 500ms | > 500ms | 상호작용 응답 시간 |
| CLS | < 0.1 | < 0.25 | > 0.25 | 레이아웃 이동 정도 |

## DO
- LCP: 히어로 이미지에 priority 설정, 서버 응답 시간 최적화
- INP: 무거운 이벤트 핸들러를 비동기로 처리, `startTransition` 활용
- CLS: 이미지/광고에 명시적 크기 설정, 폰트 swap 설정
- 실제 사용자 데이터를 수집하여 대시보드로 모니터링한다

## DON'T
- Lighthouse 점수만 보고 실제 사용자 경험을 무시하지 않는다
- layout shift를 유발하는 동적 콘텐츠 삽입을 하지 않는다
- 메인 스레드를 50ms 이상 블로킹하는 작업을 하지 않는다
- 폰트 로딩으로 인한 FOIT/FOUT를 방치하지 않는다

## 코드 예시
```tsx
// Web Vitals 측정 및 리포팅
import { onLCP, onINP, onCLS } from "web-vitals";

function reportWebVitals() {
  onLCP((metric) => sendToAnalytics("LCP", metric));
  onINP((metric) => sendToAnalytics("INP", metric));
  onCLS((metric) => sendToAnalytics("CLS", metric));
}

function sendToAnalytics(name: string, metric: Metric) {
  fetch("/api/analytics/vitals", {
    method: "POST",
    body: JSON.stringify({
      name,
      value: metric.value,
      rating: metric.rating, // "good" | "needs-improvement" | "poor"
      navigationType: metric.navigationType,
      url: window.location.href,
    }),
    keepalive: true,
  });
}

// CLS 방지: 이미지 크기 명시
<Image src={url} width={800} height={600} alt="..." />

// INP 최적화: startTransition
import { startTransition } from "react";

function handleFilterChange(filter: string) {
  startTransition(() => {
    setFilter(filter); // 무거운 리렌더링을 비긴급으로 처리
  });
}

// 폰트 최적화
// app/layout.tsx
import { Inter } from "next/font/google";
const inter = Inter({ subsets: ["latin"], display: "swap" });
```
