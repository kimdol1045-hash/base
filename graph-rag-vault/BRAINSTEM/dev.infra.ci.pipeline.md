---
id: "dev.infra.ci.pipeline"
domain: "development.infra"
type: "pattern"
region: BRAINSTEM
token_estimate: 420
theory: "#133 Continuous Integration (Fowler, 2006)"
tags: [infra, ci, github-actions, pipeline]
---

# dev.infra.ci.pipeline

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `pattern`  
> **Theory**: #133 Continuous Integration (Fowler, 2006)  
> **Tokens**: 420

## Content

CI 파이프라인 (코드 변경마다 자동으로 품질을 보증한다):

### 파이프라인 단계
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'  # 의존성 캐시로 속도 향상

      - name: Install
        run: npm ci  # npm install 대신 ci (lock 파일 기반)

      - name: Lint
        run: npm run lint  # ESLint + Prettier

      - name: Type Check
        run: npm run type-check  # tsc --noEmit

      - name: Test
        run: npm run test  # vitest

      - name: Build
        run: npm run build
```

### 규칙
- 순서: lint → type-check → test → build (빠른 것부터)
- 실패 시 즉시 중단 (느린 단계까지 기다리지 않음)
- PR에서만 전체 실행, push는 lint+type-check만 (속도)
- 테스트 병렬화: vitest --pool=threads

### 캐시 전략
- node_modules: package-lock.json 해시 기반 캐시
- Next.js: .next/cache 캐시
- Docker: 레이어 캐시

### 목표 시간
- lint + type-check: < 1분
- 테스트: < 3분
- 빌드: < 3분
- 전체 파이프라인: < 5분

## Connections

### CO_CREATES (2)

- ← [[dev.infra.ci.role]] `w=0.6`
- → [[dev.infra.ci.verify]] `w=0.6`
