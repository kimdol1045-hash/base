---
id: "dev.backend.patterns.event-driven"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 480
theory: "#104 Event-Driven Architecture (Hohpe & Woolf, 2003)"
tags: [backend, architecture, event-driven, messaging]
---

# dev.backend.patterns.event-driven

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #104 Event-Driven Architecture (Hohpe & Woolf, 2003)  
> **Tokens**: 480

## Content

이벤트 주도 아키텍처 (서비스 간 느슨한 결합을 달성한다):

### Domain Event 설계
이벤트 = 과거에 발생한 사실. 불변. 과거형 명명.

```typescript
interface DomainEvent {
  eventId: string;        // UUID
  eventType: string;      // "OrderCreated"
  aggregateId: string;    // 관련 Aggregate ID
  occurredAt: string;     // ISO 8601
  payload: Record<string, unknown>;
  metadata?: { userId?: string; correlationId?: string };
}

// DO: 충분한 정보 포함 (소비자가 추가 조회 불필요하게)
const event: DomainEvent = {
  eventId: crypto.randomUUID(),
  eventType: "OrderCreated",
  aggregateId: orderId,
  occurredAt: new Date().toISOString(),
  payload: { userId, items, totalAmount, currency },
};
```

### 이벤트 버스 패턴
```typescript
// 인메모리 (단일 서비스)
class EventBus {
  private handlers = new Map<string, Function[]>();

  subscribe(eventType: string, handler: Function) {
    const list = this.handlers.get(eventType) ?? [];
    list.push(handler);
    this.handlers.set(eventType, list);
  }

  async publish(event: DomainEvent) {
    const handlers = this.handlers.get(event.eventType) ?? [];
    await Promise.allSettled(handlers.map(h => h(event)));
  }
}
```

### 주의사항
- 이벤트 순서 보장: 같은 Aggregate의 이벤트는 순서 유지
- 멱등성: 소비자가 같은 이벤트를 2번 받아도 안전하게
- 이벤트 스키마 버전 관리: v1 → v2 마이그레이션 전략
- 실패 처리: Dead Letter Queue로 실패 이벤트 격리

## Connections

### CO_CREATES (6)

- → [[dev.backend.patterns.cap-theorem]] `w=0.6`
- → [[dev.backend.patterns.circuit-breaker]] `w=0.6`
- → [[dev.backend.patterns.cqrs]] `w=0.6`
- → [[dev.backend.patterns.message-queue]] `w=0.6`
- → [[dev.backend.patterns.saga-pattern]] `w=0.6`
- → [[dev.backend.patterns.twelve-factor]] `w=0.6`
