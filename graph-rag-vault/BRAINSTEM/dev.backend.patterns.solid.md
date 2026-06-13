---
id: "dev.backend.patterns.solid"
domain: "development.backend"
type: "rule"
region: BRAINSTEM
token_estimate: 430
theory: "#174 SOLID Principles (Robert C. Martin)"
tags: [backend, solid, principles, clean-code]
---

# dev.backend.patterns.solid

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `rule`  
> **Theory**: #174 SOLID Principles (Robert C. Martin)  
> **Tokens**: 430

## Content

SOLID 원칙 (백엔드 코드의 유지보수성을 높인다):

### S — Single Responsibility
클래스/모듈은 하나의 변경 이유만 가져야 한다.
```typescript
// ❌ 나쁨: 주문 + 이메일 + 로깅을 한 클래스에
// ✅ 좋음:
class OrderService { /* 주문 생성/수정 */ }
class OrderNotifier { /* 이메일 알림 */ }
class OrderLogger { /* 로깅 */ }
```

### O — Open/Closed
확장에 열려있고, 수정에 닫혀있어야 한다.
- Strategy 패턴으로 새 로직 추가 시 기존 코드 수정 불필요

### L — Liskov Substitution
하위 타입은 상위 타입을 대체할 수 있어야 한다.
- `ReadOnlyRepository`가 `save()` 호출 시 에러 던지면 위반

### I — Interface Segregation
클라이언트가 사용하지 않는 메서드에 의존하면 안 된다.
```typescript
// ❌ 거대 인터페이스
interface UserService { create(); update(); delete(); sendEmail(); generateReport(); }
// ✅ 분리
interface UserWriter { create(); update(); delete(); }
interface UserNotifier { sendEmail(); }
```

### D — Dependency Inversion
고수준 모듈이 저수준 모듈에 의존하면 안 된다. 둘 다 추상화에 의존.
```typescript
// ❌ class OrderService { private db = new PrismaClient(); }
// ✅ class OrderService { constructor(private repo: OrderRepository) {} }
```

### 적용 기준
- 모든 코드에 SOLID를 적용하면 과잉 설계
- 변경 가능성이 높은 코드, 복잡한 비즈니스 로직에 집중
- 단순 CRUD는 실용적 접근이 낫다

## Connections

*Connections will be populated by Graph RAG ingest.*
