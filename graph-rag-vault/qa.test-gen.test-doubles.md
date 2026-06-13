---
id: "qa.test-gen.test-doubles"
domain: "qa.testing"
type: "pattern"
bloom_level: "테스트 더블 — Mock, Stub, Spy, Fake 패턴"
tags: ["mock", "stub", "spy", "fake", "test-double"]
brain_region: "CEREBELLUM"
token_estimate: 380
---

# qa.test-gen.test-doubles

> 테스트 더블 — Mock, Stub, Spy, Fake 패턴

# 테스트 더블 가이드

## 핵심 원칙
- Stub: 고정 응답 반환, Spy: 호출 기록, Mock: 기대 검증
- Fake: 간소화된 실제 구현 (in-memory DB 등)
- 외부 의존성 격리로 테스트 속도와 안정성 확보

## DO
- 외부 API, DB, 파일시스템은 더블로 격리
- Spy로 부수효과(이메일, 로그) 검증
- Fake는 통합 테스트에서 활용

## DON'T
- 내부 구현 세부사항을 과도하게 Mock하지 않기
- Mock이 실제 동작과 괴리되지 않게 관리
- 모든 것을 Mock하여 테스트 의미 상실하지 않기
