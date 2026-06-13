---
id: "dev.backend.patterns.verify"
domain: "development.backend"
type: "verify"
bloom_level: ""
tags: ["backend", "architecture", "patterns", "verify"]
brain_region: "BRAINSTEM"
token_estimate: 450
---

# dev.backend.patterns.verify

아키텍처 패턴 자기 검증 체크리스트:

### A. 도메인 모델링
- [ ] Bounded Context 경계가 명확한가? (한 Context에 하나의 유비쿼터스 언어)
- [ ] Aggregate 크기가 적절한가? (너무 크면 분리, 트랜잭션 경계 = Aggregate 경계)
- [ ] Entity vs Value Object 구분이 올바른가? (식별자 필요 여부)
- [ ] Aggregate 간 참조가 ID로만 되어 있는가? (객체 참조 금지)

### B. 패턴 적합성
- [ ] 현재 복잡도에 맞는 패턴인가? (CRUD에 DDD/CQRS는 과도)
- [ ] 패턴 선택 근거가 명시되어 있는가?
- [ ] 팀이 이해하고 유지보수할 수 있는 수준인가?

### C. 이벤트 설계 (이벤트 주도 사용 시)
- [ ] 이벤트명이 과거형인가? (OrderCreated, not CreateOrder)
- [ ] 소비자가 추가 조회 없이 처리할 수 있는 충분한 데이터가 포함되어 있는가?
- [ ] 이벤트 스키마 버전 관리 전략이 있는가?
- [ ] 실패 이벤트 처리 방안이 있는가? (Dead Letter Queue)

### D. 멱등성/안정성
- [ ] 결제/주문 API에 Idempotency Key가 적용되어 있는가?
- [ ] 동시 요청 시 Race Condition이 발생하지 않는가?
- [ ] 재시도 시 부작용이 없는가?

### E. 12-Factor 준수
- [ ] 환경변수로만 설정 가능한가?
- [ ] 프로세스가 stateless인가?
- [ ] 로그가 stdout으로 출력되는가?

## Connections

- [[dev.backend.patterns.role]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.ddd]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.cqrs]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.clean-architecture]] — CO_CREATES (weight: 0.6)
