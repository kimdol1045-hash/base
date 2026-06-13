---
id: "dev.backend.patterns.cqrs"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "architecture", "cqrs"]
brain_region: "BRAINSTEM"
token_estimate: 480
---

# dev.backend.patterns.cqrs

> #105 CQRS (Young, 2010)

CQRS (읽기와 쓰기 모델을 분리하여 각각 최적화한다):

### 핵심 개념
- Command: 상태를 변경 (Create, Update, Delete). 반환값 없거나 ID만.
- Query: 상태를 조회. 부수 효과 없음.
- 두 모델의 스키마/DB가 다를 수 있다.

### Command 구현
```typescript
// Command 정의
interface CreateOrderCommand {
  userId: string;
  items: { productId: string; quantity: number }[];
}

// Command Handler
async function handleCreateOrder(cmd: CreateOrderCommand): Promise<string> {
  const order = Order.create(cmd.userId, cmd.items);
  await orderRepository.save(order);
  await eventBus.publish(new OrderCreatedEvent(order.id));
  return order.id;  // ID만 반환
}
```

### Query 구현
```typescript
// Query는 읽기 최적화된 별도 모델
interface OrderSummaryQuery {
  userId: string;
  status?: string;
  page: number;
}

async function getOrderSummaries(query: OrderSummaryQuery) {
  // 읽기 전용 뷰/테이블에서 직접 조회 (JOIN 최소화)
  return db.query(`
    SELECT id, total_amount, status, created_at
    FROM order_summaries
    WHERE user_id = $1 AND ($2::text IS NULL OR status = $2)
    ORDER BY created_at DESC
    LIMIT 20 OFFSET $3
  `, [query.userId, query.status, (query.page - 1) * 20]);
}
```

### 적용 판단 기준
- ✅ 적용: 읽기/쓰기 비율 불균형(10:1+), 복잡한 조회, 높은 확장성 필요
- ❌ 부적합: 단순 CRUD, 실시간 일관성 필수, 소규모 프로젝트

### 흔한 실수
- 모든 엔드포인트에 CQRS 적용 (과도한 복잡성)
- Command에서 조회 결과 반환 (분리 원칙 위반)
- 읽기/쓰기 모델 동기화 지연 미고려

## Connections

- [[dev.backend.patterns.role]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.ddd]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.clean-architecture]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.verify]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.event-driven]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.cap-theorem]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.twelve-factor]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.saga-pattern]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.circuit-breaker]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.conways-law]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.strangler-fig]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.event-sourcing]] — CO_CREATES (weight: 0.6)
