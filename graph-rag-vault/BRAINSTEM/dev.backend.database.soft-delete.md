---
id: "dev.backend.database.soft-delete"
domain: "development.database"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#110 Data Integrity (데이터 무결성과 감사 추적)"
tags: [database, soft-delete, data-retention, prisma, audit, gdpr, recovery]
---

# dev.backend.database.soft-delete

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.database`  
> **Type**: `pattern`  
> **Theory**: #110 Data Integrity (데이터 무결성과 감사 추적)  
> **Tokens**: 500

## Content

Soft Delete 패턴 (데이터를 물리 삭제하지 않고 논리 삭제하여 복구와 감사를 보장한다):

### 왜 Soft Delete인가?
- 실수로 삭제한 데이터 복구 가능 (MTTR 감소)
- 법적 데이터 보존 의무 (GDPR 삭제 요청 시에도 감사 로그 필요)
- 관계형 데이터 참조 무결성 유지 (CASCADE DELETE 방지)
- 삭제 이력 분석 가능 (이탈률, 해지 패턴)

### 기본 구현

DO:
```typescript
// ✅ Prisma schema — deletedAt 컬럼
// model User {
//   id        String    @id @default(uuid())
//   email     String    @unique
//   name      String
//   deletedAt DateTime? // null = 활성, 값 있으면 = 삭제됨
//   createdAt DateTime  @default(now())
//   updatedAt DateTime  @updatedAt
// }

// ✅ Prisma Middleware — 전역 soft delete 필터
prisma.$use(async (params, next) => {
  // findMany, findFirst 등에 자동으로 deletedAt: null 조건 추가
  if (params.action === "findMany" || params.action === "findFirst") {
    if (!params.args) params.args = {};
    if (!params.args.where) params.args.where = {};
    if (params.args.where.deletedAt === undefined) {
      params.args.where.deletedAt = null; // 삭제되지 않은 것만
    }
  }

  // delete → update로 변환
  if (params.action === "delete") {
    params.action = "update";
    params.args.data = { deletedAt: new Date() };
  }
  if (params.action === "deleteMany") {
    params.action = "updateMany";
    if (!params.args) params.args = {};
    params.args.data = { deletedAt: new Date() };
  }

  return next(params);
});
```

### Unique 제약조건 + Soft Delete
`email UNIQUE`에서 삭제된 유저의 email이 유니크 충돌 발생.

DO:
```sql
-- ✅ Partial Unique Index — deletedAt IS NULL인 행만 유니크 적용
CREATE UNIQUE INDEX idx_users_email_active
  ON users (email)
  WHERE deleted_at IS NULL;

-- 삭제된 유저의 email은 유니크 제약 없음 → 재가입 가능
```

### 계단식 Soft Delete
```typescript
// ✅ 부모 삭제 시 자식도 soft delete (CASCADE 대체)
async function softDeleteProject(projectId: string) {
  const now = new Date();
  await prisma.$transaction([
    prisma.task.updateMany({
      where: { projectId, deletedAt: null },
      data: { deletedAt: now },
    }),
    prisma.project.update({
      where: { id: projectId },
      data: { deletedAt: now },
    }),
  ]);
}

// ✅ 복구 시 자식도 함께 복구
async function restoreProject(projectId: string) {
  await prisma.$transaction([
    prisma.project.update({
      where: { id: projectId },
      data: { deletedAt: null },
    }),
    prisma.task.updateMany({
      where: { projectId, deletedAt: { not: null } },
      data: { deletedAt: null },
    }),
  ]);
}
```

### 데이터 보존 정책
```typescript
// ✅ 30일 후 물리 삭제 (GDPR 준수) — Cron Job
async function purgeDeletedRecords() {
  const threshold = subDays(new Date(), 30);
  await prisma.user.deleteMany({
    where: {
      deletedAt: { lt: threshold }, // 30일 이전 삭제 건
    },
  });
}
// cron: "0 3 * * *" — 매일 새벽 3시 실행
```

DON'T:
```typescript
// ❌ 모든 쿼리에서 수동 필터링 — 누락 시 삭제 데이터 노출
const users = await prisma.user.findMany({
  where: { deletedAt: null }, // 매번 수동 추가? 반드시 누락됨
});

// ❌ Hard Delete without Audit Log — 복구 불가, 감사 불가
await prisma.user.delete({ where: { id } }); // 영구 삭제, 흔적 없음

// ❌ Boolean isDeleted — 삭제 시점 알 수 없음
// deletedAt: DateTime?이 isDeleted: Boolean보다 우수
```

### 성능 고려
- 삭제 데이터가 쿼리 성능에 영향 → Partial Index 활용
- `WHERE deleted_at IS NULL` 인덱스로 활성 데이터만 빠르게 조회
- 삭제 비율 30% 초과 시 파티셔닝 또는 아카이브 테이블 검토
