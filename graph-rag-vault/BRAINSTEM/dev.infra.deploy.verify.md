---
id: "dev.infra.deploy.verify"
domain: "development.infra"
type: "verify"
region: BRAINSTEM
token_estimate: 110
tags: [infra, deploy, verification]
---

# dev.infra.deploy.verify

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `verify`  
> **Tokens**: 110

## Content

자기 검증 체크리스트:
- [ ] 환경변수가 하드코딩되지 않았는가?
- [ ] .env 파일이 .gitignore에 포함되었는가?
- [ ] .env.example이 모든 필요 키를 포함하는가?
- [ ] 프로덕션 빌드가 정상 동작하는가?
- [ ] HTTPS가 강제되는가?
- [ ] 헬스체크 엔드포인트가 있는가?

## Connections

### REQUIRES (1)

- ← [[dev.infra.deploy.role]] `w=0.85`

### FEEDS (2)

- ← [[dev.infra.deploy.docker]] `w=0.8`
- ← [[dev.infra.deploy.env]] `w=0.8`
