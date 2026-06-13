---
id: "dev.backend.patterns.clean-architecture"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "architecture", "clean-architecture", "solid"]
brain_region: "BRAINSTEM"
token_estimate: 450
---

# dev.backend.patterns.clean-architecture

> #146 Clean Architecture (Robert C. Martin, 2017)

Clean Architecture (의존성 방향으로 변경 영향 범위를 제어한다):

### 계층 구조 (안쪽이 바깥을 모른다)
```
Entities (도메인 모델)
  ← Use Cases (비즈니스 로직)
    ← Interface Adapters (Controller, Gateway, Presenter)
      ← Frameworks & Drivers (Express, Prisma, React)
```

### 의존성 규칙
- 안쪽 계층은 바깥 계층을 절대 import 하지 않는다
- 바깥에서 안쪽으로만 의존
- 경계를 넘을 때는 인터페이스(Port)를 사용

### 디렉토리 구조 예시
```
src/
  domain/          # Entity, Value Object, Domain Event
    entities/
    value-objects/
  application/     # Use Case, Port (interface)
    use-cases/
    ports/
  infrastructure/  # 외부 구현 (DB, API, 메일)
    repositories/
    services/
  presentation/    # Controller, Route, DTO
    controllers/
    dtos/
```

### Port & Adapter 패턴
```typescript
// Port (application 계층에 위치)
interface UserRepository {
  findById(id: string): Promise<User | null>;
  save(user: User): Promise<void>;
}

// Adapter (infrastructure 계층에 위치)
class PrismaUserRepository implements UserRepository {
  async findById(id: string) {
    return prisma.user.findUnique({ where: { id } });
  }
}
```

### 적용 판단
- ✅ 적용: 비즈니스 로직 복잡, 프레임워크 교체 가능성, 장기 프로젝트
- ❌ 과잉: CRUD 앱, 프로토타입, 마이크로서비스 (서비스 자체가 작음)

## Connections

- [[dev.backend.patterns.role]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.ddd]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.cqrs]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.verify]] — CO_CREATES (weight: 0.6)
