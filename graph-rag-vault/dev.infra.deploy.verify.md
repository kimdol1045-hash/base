---
id: "dev.infra.deploy.verify"
domain: "development.infra"
type: "verify"
bloom_level: ""
tags: ["infra", "deploy", "verification"]
brain_region: "CEREBELLUM"
token_estimate: 110
---

# dev.infra.deploy.verify

자기 검증 체크리스트:
- [ ] 환경변수가 하드코딩되지 않았는가?
- [ ] .env 파일이 .gitignore에 포함되었는가?
- [ ] .env.example이 모든 필요 키를 포함하는가?
- [ ] 프로덕션 빌드가 정상 동작하는가?
- [ ] HTTPS가 강제되는가?
- [ ] 헬스체크 엔드포인트가 있는가?

## Connections

- [[dev.infra.deploy.role]] — REQUIRES (weight: 0.85)
- [[dev.infra.deploy.env]] — FEEDS (weight: 0.8)
- [[dev.infra.deploy.docker]] — FEEDS (weight: 0.8)
