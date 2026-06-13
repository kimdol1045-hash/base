---
id: "dev.backend.patterns.event-sourcing"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "event-sourcing", "cqrs", "architecture"]
brain_region: "BRAINSTEM"
token_estimate: 450
---

# dev.backend.patterns.event-sourcing

> #163 Event Sourcing (Martin Fowler, Greg Young)

이벤트 소싱 (상태 대신 이벤트의 시퀀스를 저장한다):

### 핵심 개념
전통적: `UPDATE orders SET status='shipped' WHERE id=1`
이벤트 소싱: `[OrderCreated, PaymentReceived, OrderShipped]` → 현재 상태 재구성

### 이벤트 저장소
```typescript
interface DomainEvent {
  eventId: string;
  aggregateId: string;
  eventType: string;
  payload: Record<string, unknown>;
  occurredAt: Date;
  version: number;  // 낙관적 동시성 제어
}

// 이벤트 append-only 저장
await eventStore.append('order-123', [
  { eventType: 'OrderCreated', payload: { items, userId } },
]);
```

### 상태 재구성
```typescript
function rebuildOrder(events: DomainEvent[]): Order {
  return events.reduce((state, event) => {
    switch (event.eventType) {
      case 'OrderCreated':
        return { ...state, status: 'created', items: event.payload.items };
      case 'PaymentReceived':
        return { ...state, status: 'paid' };
      case 'OrderShipped':
        return { ...state, status: 'shipped' };
      default:
        return state;
    }
  }, {} as Order);
}
```

### Snapshot (성능 최적화)
이벤트가 많으면 매번 재구성이 비쌈 → N번째 이벤트마다 스냅샷 저장

### CQRS와 조합
- Command: 이벤트 발행 (쓰기)
- Query: Projection/Read Model에서 조회 (읽기)
- Projection: 이벤트를 구독하여 읽기 전용 뷰 업데이트

### 주의사항
- 이벤트 스키마 진화: 버전 관리 + upcaster 필수
- 이벤트는 불변 — 삭제/수정 금지 (보상 이벤트로 처리)
- 복잡성 매우 높음 — 정말 필요한 경우에만 도입

## Connections

- [[dev.backend.patterns.event-driven]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.cqrs]] — CO_CREATES (weight: 0.6)
