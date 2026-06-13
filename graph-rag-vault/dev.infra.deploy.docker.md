---
id: "dev.infra.deploy.docker"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "docker", "container"]
brain_region: "CEREBELLUM"
token_estimate: 150
---

# dev.infra.deploy.docker

Docker 컨테이너화 규칙:
- 멀티스테이지 빌드: build → production (이미지 크기 최소화)
- .dockerignore: node_modules, .git, .env, .next 제외
- non-root 유저로 실행 (보안)
- HEALTHCHECK 명시
- 환경변수는 빌드 타임(ARG)과 런타임(ENV) 구분
- 레이어 캐싱 활용: package.json 먼저 COPY → install → 소스 COPY

## Connections

- [[dev.infra.deploy.role]] — REQUIRES (weight: 0.9)
- [[dev.infra.deploy.verify]] — FEEDS (weight: 0.8)
- [[dev.infra.deploy.env]] — FEEDS (weight: 0.7)
