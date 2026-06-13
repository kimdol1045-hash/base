---
id: "dev.infra.ci.verify"
domain: "development.infra"
type: "verify"
bloom_level: ""
tags: ["infra", "ci", "verification"]
brain_region: "CEREBELLUM"
token_estimate: 90
---

# dev.infra.ci.verify

자기 검증 체크리스트:
- [ ] 시크릿이 YAML에 하드코딩되지 않았는가? (GitHub Secrets 사용)
- [ ] 테스트 실패 시 배포가 차단되는가?
- [ ] 캐싱이 적용되었는가? (node_modules, .next)
- [ ] main 브랜치 직접 push가 차단되는가?

## Connections

- [[dev.infra.ci.role]] — CO_CREATES (weight: 0.6)
- [[dev.infra.ci.pipeline]] — CO_CREATES (weight: 0.6)
