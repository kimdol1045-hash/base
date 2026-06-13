---
id: "dev.backend.patterns.outbox-pattern"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 430
theory: "#148 Transactional Outbox Pattern (Chris Richardson)"
tags: [backend, event-driven, outbox, consistency]
---

# dev.backend.patterns.outbox-pattern

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #148 Transactional Outbox Pattern (Chris Richardson)  
> **Tokens**: 430

## Content

Outbox 패턴 (DB 쓰기 + 이벤트 발행의 원자성을 보장한다):

### 문제 상황
주문 저장 + 이벤트 발행이 별도 트랜잭션:
- DB 성공 + 이벤트 실패 = 데이터 불일치
- 이벤트 성공 + DB 실패 = 유령 이벤트

### 해결: Outbox 테이블
```sql
CREATE TABLE outbox_events (
  id UUID PRIMARY KEY,
  aggregate_type VARCHAR(255) NOT NULL,
  aggregate_id VARCHAR(255) NOT NULL,
  event_type VARCHAR(255) NOT NULL,
  payload JSONB NOT NULL,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  published_at TIMESTAMPTZ NULL
);
```

### 동작 흐름
```
1. BEGIN TRANSACTION
2.   INSERT INTO orders (...)
3.   INSERT INTO outbox_events (event_type='OrderCreated', ...)
4. COMMIT

5. [별도 프로세스] Outbox Relay
   - published_at IS NULL인 이벤트 조회
   - 메시지 브로커에 발행
   - published_at 업데이트
```

### Relay 구현 방식
| 방식 | 장점 | 단점 |
|------|------|------|
| Polling | 구현 간단 | 지연 발생, DB 부하 |
| CDC (Debezium) | 실시간, DB 부하 적음 | 인프라 복잡 |
| pg_notify | PostgreSQL 네이티브 | DB 종속 |

### 주의사항
- 이벤트 컨슈머는 반드시 멱등 처리 (중복 발행 가능)
- Outbox 테이블 정리: 발행 완료 후 일정 기간 지나면 삭제
- 순서 보장: aggregate_id 기준 파티셔닝

## Connections

*Connections will be populated by Graph RAG ingest.*
