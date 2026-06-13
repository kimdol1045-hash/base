---
id: "dev.infra.deploy.env"
domain: "development.infra"
type: "rule"
region: BRAINSTEM
token_estimate: 180
theory: "#103 12-Factor (Wiggins, 2011)"
tags: [infra, env, 12factor, config]
---

# dev.infra.deploy.env

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `rule`  
> **Theory**: #103 12-Factor (Wiggins, 2011)  
> **Tokens**: 180

## Content

환경변수 관리 규칙 (12-Factor: Config):
- 모든 설정은 환경변수로 분리. 코드에 하드코딩 절대 금지
- .env.example: 모든 키를 빈 값으로 커밋 (실제 값 커밋 금지)
- .env.local: 로컬 개발용 (gitignore 필수)
- 환경별 분리: development / staging / production
- 시크릿(API 키, DB 비밀번호): 플랫폼 시크릿 매니저 사용
- 네이밍: SCREAMING_SNAKE_CASE (DATABASE_URL, NEXT_PUBLIC_API_URL)
- Next.js: 클라이언트 노출은 NEXT_PUBLIC_ 접두사만

## Connections

### REQUIRES (1)

- ← [[dev.infra.deploy.role]] `w=0.9`

### FEEDS (2)

- → [[dev.infra.deploy.docker]] `w=0.7`
- → [[dev.infra.deploy.verify]] `w=0.8`
