---
id: "dev.backend.patterns.ddd"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "architecture", "ddd", "domain-driven"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.patterns.ddd

> #102 Domain-Driven Design (Evans, 2003)

DDD (복잡한 비즈니스 로직을 도메인 중심으로 구조화한다):

### Bounded Context
하나의 모델이 유효한 경계. 같은 단어도 컨텍스트마다 의미가 다르다.
- 예: "Order"는 주문 컨텍스트에서는 결제 포함, 배송 컨텍스트에서는 배송지 포함
- 컨텍스트 간 통신: Domain Event 또는 Anti-Corruption Layer

### 전술적 패턴

Entity (식별자로 구분, 생명주기 있음):
```typescript
class Order {
  constructor(
    readonly id: string,
    private items: OrderItem[],
    private status: OrderStatus,
  ) {}

  addItem(item: OrderItem): void {
    if (this.status !== 'draft') throw new Error('확정된 주문 수정 불가');
    if (this.items.length >= 50) throw new Error('항목 50개 초과');
    this.items.push(item);
  }

  get totalAmount(): number {
    return this.items.reduce((sum, i) => sum + i.price * i.quantity, 0);
  }
}
```

Value Object (값으로 비교, 불변):
```typescript
class Money {
  constructor(readonly amount: number, readonly currency: string) {
    if (amount < 0) throw new Error('음수 금액 불가');
  }
  add(other: Money): Money {
    if (this.currency !== other.currency) throw new Error('통화 불일치');
    return new Money(this.amount + other.amount, this.currency);
  }
  equals(other: Money): boolean {
    return this.amount === other.amount && this.currency === other.currency;
  }
}
```

Aggregate (일관성 경계):
- Aggregate Root를 통해서만 내부 Entity 접근
- 하나의 트랜잭션 = 하나의 Aggregate 수정
- Aggregate 간 참조는 ID로만 (객체 참조 금지)

Repository (Aggregate 영속성):
```typescript
interface OrderRepository {
  findById(id: string): Promise<Order | null>;
  save(order: Order): Promise<void>;
  // findAll이 아닌, 비즈니스 의미 있는 메서드만
  findPendingByUserId(userId: string): Promise<Order[]>;
}
```

### 적용 판단 기준
- ✅ 적용: 비즈니스 규칙 복잡, 도메인 전문가 있음, 장기 유지보수
- ❌ 부적합: CRUD 위주, 단순 데이터 파이프라인, 프로토타입

## Connections

- [[dev.backend.patterns.role]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.cqrs]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.clean-architecture]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.verify]] — CO_CREATES (weight: 0.6)
