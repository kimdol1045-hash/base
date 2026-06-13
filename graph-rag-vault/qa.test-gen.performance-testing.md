---
id: "qa.test-gen.performance-testing"
domain: "qa.testing"
type: "pattern"
bloom_level: "성능 테스트 — 응답시간, 처리량, 리소스 사용량 검증"
tags: ["performance", "testing", "latency", "throughput"]
brain_region: "CEREBELLUM"
token_estimate: 380
---

# qa.test-gen.performance-testing

> 성능 테스트 — 응답시간, 처리량, 리소스 사용량 검증

# 성능 테스트 가이드

## 핵심 원칙
- 응답시간(P50/P95/P99), 처리량(TPS), 에러율 측정
- 부하 프로파일: 점진적 증가(ramp-up) → 유지 → 종료
- 병목 지점 식별 및 용량 계획 수립

## DO
- 실 사용 패턴 기반 시나리오 설계
- 베이스라인 측정 후 변경사항 비교
- 모니터링과 병행하여 리소스 상관관계 분석

## DON'T
- 프로덕션 환경에서 사전 고지 없이 실행하지 않기
- 단일 요청 유형만 테스트하지 않기
- 네트워크 지연 무시하지 않기
