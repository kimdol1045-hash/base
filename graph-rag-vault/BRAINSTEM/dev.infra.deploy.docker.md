---
id: "dev.infra.deploy.docker"
domain: "development.infra"
type: "pattern"
region: BRAINSTEM
token_estimate: 150
tags: [infra, docker, container]
---

# dev.infra.deploy.docker

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `pattern`  
> **Tokens**: 150

## Content

Docker 컨테이너화 규칙:
- 멀티스테이지 빌드: build → production (이미지 크기 최소화)
- .dockerignore: node_modules, .git, .env, .next 제외
- non-root 유저로 실행 (보안)
- HEALTHCHECK 명시
- 환경변수는 빌드 타임(ARG)과 런타임(ENV) 구분
- 레이어 캐싱 활용: package.json 먼저 COPY → install → 소스 COPY

## Connections

### REQUIRES (1)

- ← [[dev.infra.deploy.role]] `w=0.9`

### FEEDS (2)

- ← [[dev.infra.deploy.env]] `w=0.7`
- → [[dev.infra.deploy.verify]] `w=0.8`
