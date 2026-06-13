---
id: "dev.infra.ci.verify"
domain: "development.infra"
type: "verify"
region: BRAINSTEM
token_estimate: 90
tags: [infra, ci, verification]
---

# dev.infra.ci.verify

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `verify`  
> **Tokens**: 90

## Content

자기 검증 체크리스트:
- [ ] 시크릿이 YAML에 하드코딩되지 않았는가? (GitHub Secrets 사용)
- [ ] 테스트 실패 시 배포가 차단되는가?
- [ ] 캐싱이 적용되었는가? (node_modules, .next)
- [ ] main 브랜치 직접 push가 차단되는가?

## Connections

### CO_CREATES (2)

- ← [[dev.infra.ci.pipeline]] `w=0.6`
- ← [[dev.infra.ci.role]] `w=0.6`
