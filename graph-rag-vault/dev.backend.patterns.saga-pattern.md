---
id: "dev.backend.patterns.saga-pattern"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "patterns", "saga", "distributed-transaction", "microservice"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.patterns.saga-pattern

> #107 CQRS, #109 Event-Driven

Saga 패턴 (분산 시스템에서 2PC 없이 트랜잭션 일관성을 보장한다):

### Choreography vs Orchestration
| 방식 | 조정자 | 장점 | 단점 |
|------|--------|------|------|
| Choreography | 없음 (이벤트 기반) | 느슨한 결합, 단순 | 흐름 추적 어려움 |
| Orchestration | Saga Coordinator | 흐름 명확, 디버깅 용이 | 중앙 집중, 단일 장애점 |

### 주문 Saga: Orchestrator 구현
```typescript
// DO: 각 단계에 보상 트랜잭션 정의, Saga 상태 머신
interface SagaStep<T> {
  name: string;
  execute: (context: T) => Promise<void>;
  compensate: (context: T) => Promise<void>;
}

class SagaOrchestrator<T> {
  private steps: SagaStep<T>[] = [];
  private completedSteps: SagaStep<T>[] = [];

  addStep(step: SagaStep<T>) {
    this.steps.push(step);
    return this;
  }

  async execute(context: T & { sagaId: string }): Promise<void> {
    // Saga 로그 시작
    await sagaLog.create({ sagaId: context.sagaId, status: 'started', steps: [] });

    for (const step of this.steps) {
      try {
        await step.execute(context);
        this.completedSteps.push(step);
        await sagaLog.addStep(context.sagaId, { name: step.name, status: 'completed' });
      } catch (error) {
        await sagaLog.addStep(context.sagaId, { name: step.name, status: 'failed', error });
        // 보상 트랜잭션: 역순으로 실행
        await this.compensate(context);
        throw new SagaFailedError(step.name, error);
      }
    }
    await sagaLog.update(context.sagaId, { status: 'completed' });
  }

  private async compensate(context: T & { sagaId: string }) {
    for (const step of [...this.completedSteps].reverse()) {
      try {
        await step.compensate(context);
        await sagaLog.addStep(context.sagaId, { name: `${step.name}_compensate`, status: 'completed' });
      } catch (compError) {
        // 보상 실패: 수동 개입 필요 — 알림 발송
        await sagaLog.addStep(context.sagaId, { name: `${step.name}_compensate`, status: 'failed' });
        await alerting.critical(`Saga compensation failed: ${context.sagaId}/${step.name}`);
      }
    }
    await sagaLog.update(context.sagaId, { status: 'compensated' });
  }
}

// 주문 생성 Saga 정의
interface OrderContext {
  sagaId: string;
  orderId: string;
  userId: string;
  items: { productId: string; quantity: number }[];
  totalAmount: number;
}

const createOrderSaga = new SagaOrchestrator<OrderContext>()
  .addStep({
    name: 'reserve_inventory',
    execute: async (ctx) => { await inventoryService.reserve(ctx.orderId, ctx.items); },
    compensate: async (ctx) => { await inventoryService.release(ctx.orderId, ctx.items); },
  })
  .addStep({
    name: 'process_payment',
    execute: async (ctx) => { await paymentService.charge(ctx.orderId, ctx.totalAmount); },
    compensate: async (ctx) => { await paymentService.refund(ctx.orderId, ctx.totalAmount); },
  })
  .addStep({
    name: 'confirm_order',
    execute: async (ctx) => { await orderService.confirm(ctx.orderId); },
    compensate: async (ctx) => { await orderService.cancel(ctx.orderId); },
  });

// 실행
await createOrderSaga.execute({
  sagaId: crypto.randomUUID(),
  orderId, userId, items, totalAmount,
});
```

DON'T:
```typescript
// ❌ 마이크로서비스 간 2PC (분산 락) — 가용성 저하, 확장 불가
await db.beginTransaction(); // 서비스 A의 DB
await remoteDb.beginTransaction(); // 서비스 B의 DB → 네트워크 파티션 시 교착!

// ❌ 보상 트랜잭션 없음 — 결제 성공 후 재고 부족 시 환불 불가
await paymentService.charge(orderId, amount);
await inventoryService.reserve(orderId, items); // 실패해도 결제 유지!

// ❌ Saga 로그 미기록 — 실패 원인 추적 불가, 수동 복구 불가능
```

### Saga 상태 머신
```
STARTED → INVENTORY_RESERVED → PAYMENT_CHARGED → ORDER_CONFIRMED → COMPLETED
             ↓ (실패)              ↓ (실패)
        INVENTORY_RELEASED    PAYMENT_REFUNDED → INVENTORY_RELEASED → COMPENSATED
```

### 흔한 실수
- 보상 트랜잭션의 멱등성 미보장 (중복 환불 발생)
- 보상 실패 시 처리 방안 없음 (수동 개입 큐 필요)
- 타임아웃으로 인한 불확실 상태 (pending) 미처리
- Saga 로그가 비즈니스 DB와 다른 트랜잭션에 기록 (비정합)

## Connections

- [[dev.backend.patterns.event-driven]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.cqrs]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.cap-theorem]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.twelve-factor]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.circuit-breaker]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.conways-law]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.strangler-fig]] — CO_CREATES (weight: 0.6)
