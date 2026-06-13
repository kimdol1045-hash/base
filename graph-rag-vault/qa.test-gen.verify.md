---
id: "qa.test-gen.verify"
domain: "qa"
type: "verify"
bloom_level: ""
tags: ["qa", "test", "verification"]
brain_region: "CEREBELLUM"
token_estimate: 90
---

# qa.test-gen.verify

자기 검증 체크리스트:
- [ ] 정상 케이스와 에러 케이스를 모두 커버하는가?
- [ ] 경계값 테스트가 포함되었는가? (min, max, 0, null, empty)
- [ ] 테스트가 독립적으로 실행 가능한가? (다른 테스트에 의존하지 않는가)

## Connections

- [[qa.code-review.role]] — REQUIRES (weight: 0.85)
- [[qa.test-gen.role]] — REQUIRES (weight: 0.85)
- [[qa.code-review.priority]] — FEEDS (weight: 0.8)
- [[qa.code-review.readability]] — FEEDS (weight: 0.8)
- [[qa.code-review.security]] — FEEDS (weight: 0.8)
- [[qa.test-gen.integration]] — FEEDS (weight: 0.8)
- [[qa.test-gen.unit]] — FEEDS (weight: 0.8)
- [[qa.test-gen.testing-trophy]] — FEEDS (weight: 0.8)
- [[qa.code-review.role]] — FEEDS (weight: 0.5)
- [[qa.code-review.performance]] — FEEDS (weight: 0.5)
- [[qa.test-gen.role]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.unit]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.integration]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.component-test]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.testing-trophy]] — CO_CREATES (weight: 0.6)
