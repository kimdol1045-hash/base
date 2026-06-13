---
id: "dev.backend.patterns.cap-theorem"
domain: "development.backend"
type: "rule"
bloom_level: ""
tags: ["backend", "database", "cap-theorem", "distributed-systems"]
brain_region: "BRAINSTEM"
token_estimate: 450
---

# dev.backend.patterns.cap-theorem

> #99 CAP Theorem (Brewer, 2000)

CAP 정리 (분산 시스템에서 C, A, P 중 2개만 선택 가능):

### 세 가지 속성
- **Consistency**: 모든 노드가 동일 데이터를 보여줌
- **Availability**: 모든 요청에 응답 (에러 아닌 데이터)
- **Partition Tolerance**: 네트워크 분할 시에도 동작

### 현실적 선택 (P는 필수이므로 CP vs AP)
| 선택 | 특성 | DB 예시 | 적합한 경우 |
|------|------|---------|------------|
| CP | 일관성 우선, 파티션 시 일부 불가용 | PostgreSQL, MongoDB (default) | 결제, 재고, 금융 |
| AP | 가용성 우선, 일시적 불일치 허용 | Cassandra, DynamoDB | SNS 피드, 좋아요 수, 캐시 |

### PACELC 확장 (Abadi, 2012)
파티션 없을 때도 Latency vs Consistency 트레이드오프:
- PA/EL: 가용성+낮은 지연 (DynamoDB) — 대부분의 웹앱
- PC/EC: 일관성 우선 (전통 RDBMS) — 금융, 결제

### 실무 가이드
- 대부분의 웹앱: PostgreSQL (CP) 하나면 충분
- 글로벌 서비스: 읽기는 AP (리플리카), 쓰기는 CP (프라이머리)
- 결제/재고: 강한 일관성 필수 → PostgreSQL + SERIALIZABLE
- 피드/알림: 최종 일관성 허용 → 캐시/큐 활용

### 흔한 오해
- "NoSQL이 무조건 빠르다" → 스키마와 쿼리 패턴에 따라 다름
- "CAP에서 3개 다 가능" → 네트워크 파티션은 반드시 발생

## Connections

- [[dev.backend.patterns.event-driven]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.cqrs]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.twelve-factor]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.saga-pattern]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.circuit-breaker]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.conways-law]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.strangler-fig]] — CO_CREATES (weight: 0.6)
