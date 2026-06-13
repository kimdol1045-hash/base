---
id: "qa.code-review.performance"
domain: "qa"
type: "rule"
bloom_level: ""
tags: ["qa", "code-review", "performance"]
brain_region: "CEREBELLUM"
token_estimate: 380
---

# qa.code-review.performance

성능 관점 코드 리뷰 (비효율적인 코드를 식별한다):

### 시간복잡도 확인
- O(n²) 이상 루프 경고 (데이터 1000건+ 시 문제)
- 중첩 루프 내 DB/API 호출 = N+1 (무조건 수정)
- 대안: Map/Set으로 O(1) 조회, Promise.all 병렬화

### 메모리 누수 패턴
- 이벤트 리스너 미해제 (useEffect cleanup 누락)
- setInterval 미정리
- 클로저에서 큰 객체 참조 유지
- 무한 배열 축적 (로그, 히스토리)

### React 리렌더링
- 불필요한 리렌더링: React DevTools Profiler로 확인
- 객체/배열 props 인라인 생성 금지 (매번 새 참조)
- 컨텍스트 분리: 자주 변하는 값과 안 변하는 값 분리

### 체크리스트
- [ ] O(n²) 이상 루프가 있는가?
- [ ] 루프 내 비동기 호출이 있는가?
- [ ] useEffect에 cleanup이 있는가?
- [ ] 불필요한 리렌더링이 발생하는가?
- [ ] 큰 리스트에 가상화(virtualization)가 적용되었는가?

## Connections

- [[qa.code-review.role]] — REQUIRES (weight: 0.9)
- [[qa.code-review.verify]] — FEEDS (weight: 0.8)
- [[qa.code-review.bug-analysis]] — FEEDS (weight: 0.7)
- [[qa.code-review.role]] — CO_CREATES (weight: 0.6)
- [[qa.code-review.priority]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.role]] — FEEDS (weight: 0.5)
- [[qa.test-gen.unit]] — FEEDS (weight: 0.5)
- [[qa.test-gen.integration]] — FEEDS (weight: 0.5)
- [[qa.test-gen.component-test]] — FEEDS (weight: 0.5)
- [[qa.test-gen.testing-trophy]] — FEEDS (weight: 0.5)
- [[qa.test-gen.verify]] — FEEDS (weight: 0.5)
