---
id: "dev.backend.patterns.strangler-fig"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "migration", "legacy", "strangler-fig"]
brain_region: "BRAINSTEM"
token_estimate: 380
---

# dev.backend.patterns.strangler-fig

> #147 Strangler Fig Pattern (Martin Fowler, 2004)

Strangler Fig 패턴 (레거시를 점진적으로 교체한다):

### 핵심 원리
새 시스템이 레거시를 감싸면서 점진적으로 기능을 대체.
빅뱅 마이그레이션의 위험 없이 안전하게 전환.

### 구현 단계
1. **Intercept**: 프록시/게이트웨이를 앞에 배치
2. **Route**: 요청을 신/구 시스템으로 분기
3. **Replace**: 기능 하나씩 새 시스템으로 이전
4. **Remove**: 모든 트래픽 이전 후 레거시 제거

### 라우팅 전략
```
API Gateway
  /api/users/*    → New Service (이전 완료)
  /api/orders/*   → New Service (이전 중)
  /api/reports/*  → Legacy System (아직)
```

### 데이터 동기화
- 이중 쓰기: 양쪽 모두 기록 (일시적)
- Change Data Capture: 레거시 DB 변경을 이벤트로 전파
- 읽기는 새 시스템, 쓰기는 레거시에서 시작 → 점진 전환

### 주의사항
- 프록시 레이어가 SPOF가 되지 않도록
- 양쪽 시스템 동시 운영 기간 최소화
- 기능 단위로 전환 (테이블 단위 X)
- 전환 완료 후 반드시 레거시 코드 제거

## Connections

- [[dev.backend.patterns.event-driven]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.cqrs]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.cap-theorem]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.twelve-factor]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.saga-pattern]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.circuit-breaker]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.conways-law]] — CO_CREATES (weight: 0.6)
