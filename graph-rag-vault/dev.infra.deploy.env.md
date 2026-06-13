---
id: "dev.infra.deploy.env"
domain: "development.infra"
type: "rule"
bloom_level: ""
tags: ["infra", "env", "12factor", "config"]
brain_region: "CEREBELLUM"
token_estimate: 180
---

# dev.infra.deploy.env

> #103 12-Factor (Wiggins, 2011)

환경변수 관리 규칙 (12-Factor: Config):
- 모든 설정은 환경변수로 분리. 코드에 하드코딩 절대 금지
- .env.example: 모든 키를 빈 값으로 커밋 (실제 값 커밋 금지)
- .env.local: 로컬 개발용 (gitignore 필수)
- 환경별 분리: development / staging / production
- 시크릿(API 키, DB 비밀번호): 플랫폼 시크릿 매니저 사용
- 네이밍: SCREAMING_SNAKE_CASE (DATABASE_URL, NEXT_PUBLIC_API_URL)
- Next.js: 클라이언트 노출은 NEXT_PUBLIC_ 접두사만

## Connections

- [[dev.infra.deploy.role]] — REQUIRES (weight: 0.9)
- [[dev.infra.deploy.verify]] — FEEDS (weight: 0.8)
- [[dev.infra.deploy.docker]] — FEEDS (weight: 0.7)
