---
id: "qa.test-gen.accessibility-testing"
domain: "qa.testing"
type: "pattern"
bloom_level: "접근성 테스트 — WCAG 2.1 준수 자동화 검증"
tags: ["accessibility", "a11y", "wcag", "testing"]
brain_region: "CEREBELLUM"
token_estimate: 380
---

# qa.test-gen.accessibility-testing

> 접근성 테스트 — WCAG 2.1 준수 자동화 검증

# 접근성 테스트 가이드

## 핵심 원칙
- WCAG 2.1 AA 기준 자동/수동 테스트 병행
- 스크린리더, 키보드 네비게이션, 색상 대비 검증
- axe-core, Lighthouse 등 자동화 도구 활용

## DO
- CI/CD에 axe-core 자동 검사 통합
- 실제 보조 기술 사용자 테스트 수행
- ARIA 역할과 라벨 누락 검사

## DON'T
- 자동 도구 결과만으로 접근성 완료 판단하지 않기
- 마우스 전용 인터랙션 설계하지 않기
- 색상만으로 정보 구분하지 않기
