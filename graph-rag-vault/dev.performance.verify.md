---
id: "dev.performance.verify"
domain: "development.performance"
type: "verify"
bloom_level: ""
tags: ["performance", "verify", "checklist"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.performance.verify

성능 자기 검증 체크리스트:

### A. Core Web Vitals
- [ ] LCP < 2.5초인가? (히어로 이미지에 priority 설정?)
- [ ] INP < 200ms인가? (무거운 연산이 메인 스레드를 블로킹하지 않는가?)
- [ ] CLS < 0.1인가? (이미지/영상에 width/height 명시? 동적 삽입 시 공간 확보?)

### B. 번들 최적화
- [ ] JS 번들이 200KB(gzipped) 이하인가?
- [ ] 동적 임포트(code splitting)로 초기 로딩 줄였는가?
- [ ] barrel export(index.ts)로 불필요한 코드가 포함되지 않았는가?
- [ ] next/image, next/font 사용하여 에셋 최적화했는가?

### C. API / 서버
- [ ] API 응답 시간이 400ms 이하인가? (도허티 임계값)
- [ ] N+1 쿼리가 없는가?
- [ ] 독립적인 쿼리/API 호출은 Promise.all로 병렬화했는가?
- [ ] 적절한 Cache-Control 헤더가 설정되어 있는가?

### D. 데이터베이스
- [ ] SELECT *를 사용하지 않았는가?
- [ ] 자주 조회하는 컬럼에 인덱스가 있는가?
- [ ] 커넥션 풀 크기가 적절한가? (리틀의 법칙 기반)

### E. 사용자 경험
- [ ] 로딩 시 스켈레톤 UI 또는 스피너가 표시되는가?
- [ ] 낙관적 업데이트가 적용되어 즉각 반응하는가?
- [ ] 에러 시 재시도 가능한가?

## Connections

- [[dev.performance.role]] — REQUIRES (weight: 0.85)
- [[dev.performance.web-vitals]] — FEEDS (weight: 0.8)
- [[dev.performance.caching]] — FEEDS (weight: 0.8)
- [[dev.performance.budget]] — FEEDS (weight: 0.8)
- [[dev.performance.amdahl]] — FEEDS (weight: 0.8)
