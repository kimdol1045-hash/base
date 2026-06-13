---
id: "dev.backend.database.transaction"
domain: "development.database"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#109 ACID Properties (Haerder & Reuter, 1983)"
tags: [database, transaction, acid, locking, deadlock, isolation]
---

# dev.backend.database.transaction

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.database`  
> **Type**: `pattern`  
> **Theory**: #109 ACID Properties (Haerder & Reuter, 1983)  
> **Tokens**: 500

## Content

트랜잭션 패턴 (데이터 일관성과 동시성 안전을 보장한다):

### ACID 원칙
- **Atomicity**: 전부 성공 또는 전부 실패. 부분 반영 없음
- **Consistency**: 트랜잭션 전후 모든 제약조건 충족
- **Isolation**: 동시 트랜잭션 간 간섭 없음
- **Durability**: 커밋된 데이터는 영구 보존

### 트랜잭션 사용 기준
2개 이상의 쓰기 작업이 하나의 논리적 단위일 때 반드시 트랜잭션으로 묶는다.

DO:
```sql
-- ✅ 주문 생성: 주문 + 재고 차감 + 결제 기록을 원자적으로 처리
BEGIN;
  INSERT INTO orders (id, user_id, total_amount, status)
  VALUES (gen_random_uuid(), $1, $2, 'confirmed');

  UPDATE products
  SET stock = stock - $3
  WHERE id = $4 AND stock >= $3;  -- 재고 부족 시 0행 업데이트

  INSERT INTO payments (id, order_id, amount, method)
  VALUES (gen_random_uuid(), $5, $2, $6);
COMMIT;
```

DON'T:
```typescript
// ❌ 트랜잭션 없이 개별 실행 → 중간 실패 시 데이터 불일치
await db.query('INSERT INTO orders ...');
await db.query('UPDATE products SET stock = stock - $1 ...'); // 여기서 실패하면?
await db.query('INSERT INTO payments ...'); // 실행 안 됨 → 주문은 있고 결제는 없는 상태
```

### 트랜잭션 격리 수준 (PostgreSQL)
| 격리 수준 | Dirty Read | Non-repeatable Read | Phantom Read | 사용 시나리오 |
|-----------|-----------|-------------------|-------------|-------------|
| READ COMMITTED (기본) | 방지 | 허용 | 허용 | 일반적인 CRUD |
| REPEATABLE READ | 방지 | 방지 | 허용 | 보고서/집계 |
| SERIALIZABLE | 방지 | 방지 | 방지 | 금융/재고 (성능 비용 큼) |

```sql
-- 금융 거래: SERIALIZABLE로 완전한 격리
BEGIN ISOLATION LEVEL SERIALIZABLE;
  UPDATE accounts SET balance = balance - 1000 WHERE id = $1;
  UPDATE accounts SET balance = balance + 1000 WHERE id = $2;
COMMIT;
```

### Optimistic vs Pessimistic Locking

**Optimistic Locking** (충돌이 적은 경우 권장):
```sql
-- version 컬럼으로 동시 수정 감지
UPDATE products
SET name = $1, price = $2, version = version + 1
WHERE id = $3 AND version = $4;
-- affected rows = 0이면 다른 트랜잭션이 먼저 수정 → 재시도
```

```typescript
const result = await db.query(
  'UPDATE products SET name=$1, version=version+1 WHERE id=$2 AND version=$3',
  [newName, productId, currentVersion]
);
if (result.rowCount === 0) {
  throw new ConflictError('다른 사용자가 이미 수정했습니다. 새로고침 후 재시도하세요.');
}
```

**Pessimistic Locking** (충돌이 잦은 경우):
```sql
-- SELECT FOR UPDATE로 행 잠금
BEGIN;
  SELECT stock FROM products WHERE id = $1 FOR UPDATE;
  -- 다른 트랜잭션은 이 행에 대해 대기
  UPDATE products SET stock = stock - 1 WHERE id = $1;
COMMIT;
```

### 데드락 방지 규칙
1. **테이블 접근 순서 고정**: 모든 트랜잭션에서 동일한 순서로 테이블 접근
2. **트랜잭션 최소화**: 트랜잭션 내에서 외부 API 호출 절대 금지
3. **타임아웃 설정**: `SET lock_timeout = '5s';` (5초 이상 대기 시 실패)
4. **NOWAIT 옵션**: 즉시 실패가 나은 경우 `SELECT ... FOR UPDATE NOWAIT`

### 흔한 실수
- 트랜잭션 안에서 HTTP 요청 → 커넥션 장시간 점유
- 큰 트랜잭션(1000행+ UPDATE) → 다른 쿼리 대기, 메모리 과다 사용
- COMMIT/ROLLBACK 누락 → 커넥션 풀 고갈
- Optimistic Locking에서 재시도 로직 누락 → 사용자 데이터 유실

## Connections

### REQUIRES (1)

- ← [[dev.backend.database.role]] `w=0.9`

### FEEDS (2)

- ← [[dev.backend.database.query]] `w=0.7`
- → [[dev.backend.database.verify]] `w=0.8`

### CO_CREATES (3)

- ← [[dev.backend.database.index]] `w=0.6`
- ← [[dev.backend.database.query]] `w=0.6`
- ← [[dev.backend.database.schema]] `w=0.6`
