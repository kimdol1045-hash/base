---
id: "dev.backend.patterns.hexagonal"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 430
theory: "#162 Hexagonal Architecture / Ports & Adapters (Alistair Cockburn, 2005)"
tags: [backend, hexagonal, ports-adapters, architecture]
---

# dev.backend.patterns.hexagonal

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #162 Hexagonal Architecture / Ports & Adapters (Alistair Cockburn, 2005)  
> **Tokens**: 430

## Content

헥사고날 아키텍처 (외부 의존성과 비즈니스 로직을 완전히 분리한다):

### 핵심 구조
```
[Driving Adapter]  →  [Port]  →  [Application Core]  →  [Port]  →  [Driven Adapter]
(Controller)       (Input)    (Use Case + Domain)     (Output)    (DB, API, MQ)
```

### Port (인터페이스)
```typescript
// Input Port (Driving) — 애플리케이션이 외부에 제공
interface CreateOrderUseCase {
  execute(command: CreateOrderCommand): Promise<OrderId>;
}

// Output Port (Driven) — 애플리케이션이 외부에 요청
interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(id: OrderId): Promise<Order | null>;
}
```

### Adapter (구현체)
```typescript
// Driving Adapter — HTTP Controller
class OrderController {
  constructor(private createOrder: CreateOrderUseCase) {}
  async handlePost(req: Request) {
    const orderId = await this.createOrder.execute(req.body);
    return { status: 201, body: { orderId } };
  }
}

// Driven Adapter — Prisma Repository
class PrismaOrderRepository implements OrderRepository {
  async save(order: Order) { /* Prisma 호출 */ }
  async findById(id: OrderId) { /* Prisma 호출 */ }
}
```

### vs Clean Architecture
- 동일 원칙 (의존성 역전), 표현 방식이 다름
- Hexagonal: Port/Adapter 중심 사고
- Clean Architecture: 동심원 계층 중심 사고
- 실무에서는 혼용이 일반적

### 적용 판단
- ✅: 외부 시스템 교체 가능성, 비즈니스 로직 복잡, 테스트 격리 필요
- ❌: 단순 CRUD, 프로토타입, 학습 비용 대비 이점 없을 때

## Connections

*Connections will be populated by Graph RAG ingest.*
