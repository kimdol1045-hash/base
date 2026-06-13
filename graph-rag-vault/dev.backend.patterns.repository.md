---
id: "dev.backend.patterns.repository"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "repository", "data-access", "clean-architecture"]
brain_region: "BRAINSTEM"
token_estimate: 400
---

# dev.backend.patterns.repository

> #173 Repository Pattern (Martin Fowler, PoEAA)

Repository 패턴 (데이터 접근을 비즈니스 로직에서 분리한다):

### 인터페이스 정의
```typescript
interface UserRepository {
  findById(id: string): Promise<User | null>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<void>;
  delete(id: string): Promise<void>;
  findActive(page: number, limit: number): Promise<User[]>;
}
```

### 구현체
```typescript
class PrismaUserRepository implements UserRepository {
  constructor(private prisma: PrismaClient) {}

  async findById(id: string) {
    const data = await this.prisma.user.findUnique({ where: { id } });
    return data ? UserMapper.toDomain(data) : null;
  }

  async save(user: User) {
    await this.prisma.user.upsert({
      where: { id: user.id },
      create: UserMapper.toPersistence(user),
      update: UserMapper.toPersistence(user),
    });
  }
}
```

### 핵심 규칙
- Repository는 Aggregate Root 단위 (User, 하위 Entity 포함)
- 비즈니스 의미 있는 메서드만 (`findAll` 지양, `findActiveByRole` 등)
- Mapper로 도메인 모델 ↔ 영속성 모델 변환
- 테스트 시 InMemoryRepository로 교체 가능

### vs DAO
| Repository | DAO |
|-----------|-----|
| 도메인 중심 | 데이터 중심 |
| Aggregate 단위 | 테이블 단위 |
| 비즈니스 메서드 | CRUD 메서드 |
