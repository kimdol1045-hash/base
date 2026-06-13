---
id: "dev.backend.testing.test-containers"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["testing", "testcontainers", "docker", "integration"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.testing.test-containers

> #230 Testcontainers (AtomicJar, 2015)

# Testcontainers 통합 테스트 가이드

## 핵심 원칙
- 실제 데이터베이스, Redis, 메시지 브로커를 Docker 컨테이너로 실행하여 테스트한다
- Mock 대신 실제 인프라를 사용하므로 프로덕션에 가까운 테스트가 가능하다
- 테스트 종료 시 컨테이너가 자동으로 정리된다
- CI/CD 환경에서도 Docker만 있으면 실행 가능하다

## DO
- 데이터베이스 마이그레이션과 쿼리를 실제 DB에서 테스트한다
- 테스트 간 데이터 격리를 보장한다 (트랜잭션 롤백 또는 DB 초기화)
- 컨테이너 시작 시간을 최소화하기 위해 재사용(Reusable) 옵션을 활용한다
- 글로벌 설정(beforeAll)에서 컨테이너를 시작한다

## DON'T
- 각 테스트마다 컨테이너를 새로 시작하지 않는다 (느림)
- 테스트에서 외부 공유 DB에 의존하지 않는다
- 컨테이너 포트를 하드코딩하지 않는다 (동적 포트 매핑 사용)
- 단위 테스트에 Testcontainers를 사용하지 않는다 (통합 테스트용)

## 코드 예시
```typescript
import { PostgreSqlContainer } from "@testcontainers/postgresql";
import { RedisContainer } from "@testcontainers/redis";
import { describe, beforeAll, afterAll, it, expect } from "vitest";

let pgContainer: StartedPostgreSqlContainer;
let redisContainer: StartedRedisContainer;
let db: Database;

beforeAll(async () => {
  pgContainer = await new PostgreSqlContainer("postgres:16")
    .withReuse()
    .start();

  redisContainer = await new RedisContainer("redis:7")
    .withReuse()
    .start();

  db = createDatabase({
    connectionString: pgContainer.getConnectionUri(),
  });

  // 마이그레이션 실행
  await runMigrations(db);
}, 60_000); // 컨테이너 시작 대기

afterAll(async () => {
  await db.close();
  await pgContainer?.stop();
  await redisContainer?.stop();
});

describe("UserRepository", () => {
  it("사용자를 생성하고 조회할 수 있다", async () => {
    const repo = new UserRepository(db);
    const user = await repo.create({
      email: "test@example.com",
      displayName: "테스트",
    });

    const found = await repo.findById(user.id);
    expect(found?.email).toBe("test@example.com");
  });
});
```
