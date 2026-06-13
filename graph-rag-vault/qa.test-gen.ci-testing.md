---
id: "qa.test-gen.ci-testing"
domain: "qa.testing"
type: "pattern"
bloom_level: "CI 테스트 통합 — 지속적 품질 게이트 자동화"
tags: ["ci", "continuous-integration", "pipeline", "automation"]
brain_region: "CEREBELLUM"
token_estimate: 350
---

# qa.test-gen.ci-testing

> CI 테스트 통합 — 지속적 품질 게이트 자동화

# CI 테스트 통합 가이드

## 핵심 원칙
- PR마다 자동 테스트 실행으로 품질 게이트 역할
- 빠른 피드백: 단위 → 통합 → E2E 순차 실행
- 실패 시 명확한 에러 리포트와 재현 방법 제공

## DO
- 테스트 병렬 실행으로 파이프라인 시간 단축
- Flaky 테스트 격리 및 별도 관리
- 커버리지 리포트 자동 생성 및 추적

## DON'T
- 실패한 테스트를 skip으로 무시하지 않기
- CI에서만 실행되는 테스트 작성하지 않기
- 테스트 실행 시간 15분 초과 방치하지 않기
