---
id: "dev.backend.patterns.outbox"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["patterns", "outbox", "event-driven", "consistency"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.patterns.outbox

> #291 Transactional Outbox Pattern (Chris Richardson, Microservices Patterns 2018)

# Transactional Outbox 패턴 가이드

## 핵심 원칙
- DB 쓰기와 이벤트 발행의 원자성을 보장한다
- 비즈니스 데이터와 이벤트를 같은 트랜잭션에서 저장한다
- 별도의 Relay 프로세스가 Outbox 테이블에서 이벤트를 발행한다
- 최소 한 번(at-least-once) 전달을 보장하므로 컨슈머는 멱등해야 한다

## DO
- 비즈니스 엔티티와 Outbox 이벤트를 같은 DB 트랜잭션에서 저장한다
- CDC(Change Data Capture) 또는 폴링으로 Outbox Relay를 구현한다
- 이벤트에 aggregate_id를 포함하여 순서를 보장한다
- 발행 완료된 이벤트를 주기적으로 정리(아카이브)한다
- 컨슈머 측에서 멱등성을 반드시 구현한다

## DON'T
- DB 커밋 후 별도 트랜잭션에서 이벤트를 발행하지 않는다 (불일치 위험)
- Outbox 테이블을 무한정 쌓이게 방치하지 않는다
- 이벤트 페이로드에 대용량 데이터를 넣지 않는다 (참조만 저장)
- Relay 프로세스 장애 시 이벤트가 영구 누락되도록 하지 않는다

## 코드 예시
```typescript
// 트랜잭션 내 Outbox 저장
async function createOrder(input: CreateOrderInput) {
  return db.transaction(async (tx) => {
    // 1. 비즈니스 데이터 저장
    const order = await tx.insert(orders).values({
      userId: input.userId,
      items: input.items,
      totalAmount: input.totalAmount,
      status: "created",
    }).returning();

    // 2. 같은 트랜잭션에서 Outbox에 이벤트 저장
    await tx.insert(outboxEvents).values({
      id: generateId(),
      aggregateType: "Order",
      aggregateId: order[0].id,
      eventType: "OrderCreated",
      payload: { orderId: order[0].id, userId: input.userId, totalAmount: input.totalAmount },
    });

    return order[0];
  });
}

// Outbox Relay (폴링 방식)
async function relayOutboxEvents() {
  const events = await db.select()
    .from(outboxEvents)
    .where(isNull(outboxEvents.publishedAt))
    .orderBy(outboxEvents.createdAt)
    .limit(100);

  for (const event of events) {
    try {
      await messageBroker.publish(event.eventType, event.payload);
      await db.update(outboxEvents)
        .set({ publishedAt: new Date() })
        .where(eq(outboxEvents.id, event.id));
    } catch (err) {
      logger.error({ eventId: event.id, err }, "Outbox 이벤트 발행 실패");
      break; // 순서 보장을 위해 중단
    }
  }
}

// 30초마다 Relay 실행
setInterval(relayOutboxEvents, 30_000);
```
