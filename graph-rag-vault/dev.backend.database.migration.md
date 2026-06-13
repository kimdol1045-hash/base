---
id: "dev.backend.database.migration"
domain: "development.database"
type: "pattern"
bloom_level: ""
tags: ["database", "migration", "zero-downtime", "rollback", "evolutionary"]
brain_region: "BRAINSTEM"
token_estimate: 480
---

# dev.backend.database.migration

> #108 Evolutionary Database Design (Ambler, 2003)

마이그레이션 패턴 (프로덕션 안전성과 롤백 가능성을 보장한다):

### up/down 패턴 필수
모든 마이그레이션은 반드시 롤백(down)을 포함한다. 롤백 불가능한 변경은 별도로 표시한다.

DO:
```sql
-- up: 컬럼 추가
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
CREATE INDEX idx_users_phone ON users(phone);

-- down: 컬럼 제거 (롤백)
DROP INDEX IF EXISTS idx_users_phone;
ALTER TABLE users DROP COLUMN IF EXISTS phone;
```

DON'T:
```sql
-- ❌ down 없이 up만 작성 → 롤백 불가
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
-- down: ??? (없음)
```

### 스키마 마이그레이션 vs 데이터 마이그레이션
두 종류를 하나의 파일에 섞지 않는다. 분리하여 순서대로 실행한다.

```sql
-- 1단계: 스키마 마이그레이션 (구조 변경)
ALTER TABLE users ADD COLUMN full_name VARCHAR(200);

-- 2단계: 데이터 마이그레이션 (별도 파일)
UPDATE users SET full_name = first_name || ' ' || last_name
WHERE full_name IS NULL;

-- 3단계: 스키마 정리 (별도 파일, 다음 배포 사이클)
ALTER TABLE users DROP COLUMN first_name;
ALTER TABLE users DROP COLUMN last_name;
```

### Zero-Downtime Migration 패턴
프로덕션에서 서비스 중단 없이 스키마를 변경하는 전략:

**컬럼 추가** (안전):
```sql
-- ✅ 새 컬럼 + DEFAULT = 즉시 완료 (PostgreSQL 11+)
ALTER TABLE orders ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'pending';
```

**컬럼 이름 변경** (위험 → 3단계 전략):
```sql
-- Step 1: 새 컬럼 추가 + 데이터 복사
ALTER TABLE users ADD COLUMN display_name VARCHAR(100);
UPDATE users SET display_name = username;

-- Step 2: 애플리케이션 코드에서 양쪽 컬럼 모두 지원 (배포)

-- Step 3: 이전 컬럼 제거 (다음 배포 사이클)
ALTER TABLE users DROP COLUMN username;
```

**테이블 락 방지**:
```sql
-- ✅ CREATE INDEX CONCURRENTLY (락 없이 인덱스 생성)
CREATE INDEX CONCURRENTLY idx_orders_status ON orders(status);

-- ❌ 일반 CREATE INDEX → 테이블 쓰기 락 발생
CREATE INDEX idx_orders_status ON orders(status);
```

### Prisma 마이그레이션 예시
```typescript
// prisma/migrations/20240101_add_user_phone/migration.sql
-- CreateIndex
ALTER TABLE "users" ADD COLUMN "phone" VARCHAR(20);
CREATE INDEX "idx_users_phone" ON "users"("phone");
```

### 흔한 실수
- NOT NULL 컬럼 추가 시 DEFAULT 없음 → 기존 행 에러
- 대량 테이블에 ALTER TABLE → 장시간 테이블 락
- 데이터 마이그레이션과 스키마 변경 혼합 → 롤백 복잡성 증가
- 마이그레이션 순서 의존성 미관리 → 배포 환경마다 결과 다름
- DROP COLUMN을 코드 변경 없이 실행 → 런타임 에러

## Connections

- [[dev.backend.database.schema]] — CO_CREATES (weight: 0.6)
