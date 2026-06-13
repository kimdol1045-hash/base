---
id: "qa.code-review.readability"
domain: "qa"
type: "rule"
bloom_level: ""
tags: ["qa", "code-review", "readability", "clean-code"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# qa.code-review.readability

> #122 Clean Code (Martin, 2008)

코드 가독성 (읽기 쉬운 코드가 유지보수 가능한 코드):

### 네이밍 규칙
- 변수: 의미를 담은 명사. `data` ❌ → `activeUsers` ✅
- 함수: 동사로 시작. `process` ❌ → `calculateTotalPrice` ✅
- 불리언: is/has/should 접두사. `active` ❌ → `isActive` ✅
- 상수: UPPER_SNAKE_CASE. `MAX_RETRY_COUNT = 3`
- 약어 지양: `usr` ❌ → `user` ✅ (반복 사용되는 관용어 제외: id, url, api)

### 함수 크기
- 한 함수 = 한 가지 일 (SRP)
- 20줄 이하 권장. 40줄 초과 시 분리 고려.
- 인자 3개 이하. 초과 시 객체로 묶기.
- 중첩 if/for 2단계 이하. 초과 시 early return 또는 함수 추출.

### 주석
- 코드가 "왜"인지 설명할 때만. "무엇"은 코드 자체로.
- DO: `// 브라우저 호환성을 위해 setTimeout 사용 (Safari 버그)`
- DON'T: `// 유저를 가져온다` (코드만 봐도 알 수 있음)
- TODO 주석: 이슈 번호 포함 `// TODO(#123): 캐시 무효화 추가`

### Cyclomatic Complexity
- 10 이하 권장. 20 초과 시 반드시 리팩토링.
- 측정: ESLint complexity 규칙

## Connections

- [[qa.code-review.role]] — REQUIRES (weight: 0.9)
- [[qa.test-gen.role]] — REQUIRES (weight: 0.9)
- [[qa.code-review.verify]] — FEEDS (weight: 0.8)
- [[qa.test-gen.verify]] — FEEDS (weight: 0.8)
- [[qa.code-review.priority]] — FEEDS (weight: 0.7)
- [[qa.code-review.security]] — FEEDS (weight: 0.7)
