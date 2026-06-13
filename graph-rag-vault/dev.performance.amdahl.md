---
id: "dev.performance.amdahl"
domain: "development.performance"
type: "rule"
bloom_level: ""
tags: ["performance", "parallel", "optimization"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.performance.amdahl

> #135 Amdahl's Law (Amdahl, 1967)

암달의 법칙 (병렬화해도 직렬 구간이 전체 성능 한계를 결정한다):

### 공식
Speedup = 1 / (S + P/N)
- S = 직렬 비율, P = 병렬화 가능 비율 (S + P = 1), N = 코어/워커 수

### 실무 적용: 직렬 병목을 먼저 찾아라
```typescript
// ❌ BAD: 순차 실행 (직렬 100%)
const user = await getUser(userId);
const orders = await getOrders(userId);
const reviews = await getReviews(userId);
// 총 시간: 100ms + 200ms + 150ms = 450ms

// ✅ GOOD: 독립적 작업 병렬 실행
const [user, orders, reviews] = await Promise.all([
  getUser(userId),
  getOrders(userId),
  getReviews(userId),
]);
// 총 시간: max(100, 200, 150) = 200ms
```

### 병렬화 판단 기준
- ✅ 병렬 가능: 서로 의존 없는 API 호출, 독립 DB 쿼리, 파일 처리
- ❌ 병렬 불가: A의 결과가 B의 입력인 경우, 트랜잭션 내 순차 작업

### 주의사항
- Promise.all: 하나 실패 시 전부 실패 → Promise.allSettled 고려
- DB 커넥션 풀: 병렬 쿼리 수 > 풀 크기면 오히려 느려짐
- 외부 API Rate Limit: 병렬 요청이 limit에 걸릴 수 있음

## Connections

- [[dev.performance.role]] — REQUIRES (weight: 0.9)
- [[dev.performance.verify]] — FEEDS (weight: 0.8)
- [[dev.performance.budget]] — FEEDS (weight: 0.7)
- [[dev.performance.role]] — CO_CREATES (weight: 0.6)
- [[dev.performance.web-vitals]] — CO_CREATES (weight: 0.6)
- [[dev.performance.caching]] — CO_CREATES (weight: 0.6)
- [[dev.performance.budget]] — CO_CREATES (weight: 0.6)
- [[dev.performance.littles-law]] — CO_CREATES (weight: 0.6)
- [[dev.frontend.component.performance]] — FEEDS (weight: 0.5)
