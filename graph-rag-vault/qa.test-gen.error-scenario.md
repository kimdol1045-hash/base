---
id: "qa.test-gen.error-scenario"
domain: "qa.testing"
type: "pattern"
bloom_level: "에러 시나리오 테스트 — 경계값, 예외, 장애 상황 검증"
tags: ["error-testing", "boundary", "edge-case", "negative-testing"]
brain_region: "CEREBELLUM"
token_estimate: 380
---

# qa.test-gen.error-scenario

> 에러 시나리오 테스트 — 경계값, 예외, 장애 상황 검증

# 에러 시나리오 테스트 가이드

## 핵심 원칙
- Happy path뿐 아니라 실패 경로 체계적 검증
- 경계값 분석: 최소/최대/제로/음수/오버플로
- 네트워크 장애, 타임아웃, 동시성 문제 시뮬레이션

## DO
- 모든 입력 필드에 경계값 테스트 적용
- 외부 서비스 장애 시나리오 Mock
- 에러 메시지와 HTTP 상태 코드 검증

## DON'T
- 성공 케이스만 테스트하지 않기
- 에러 핸들링 코드를 테스트하지 않고 방치하지 않기
- 비현실적 에러 시나리오에 과투자하지 않기
