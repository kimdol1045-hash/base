---
id: "dev.backend.database.multi-tenancy"
domain: "development.database"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#115 Saltzer 최소 권한 원칙 (Saltzer & Schroeder, 1975)"
tags: [database, multi-tenancy, rls, postgres, saas, isolation, security]
---

# dev.backend.database.multi-tenancy

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.database`  
> **Type**: `pattern`  
> **Theory**: #115 Saltzer 최소 권한 원칙 (Saltzer & Schroeder, 1975)  
> **Tokens**: 500

## Content

멀티테넌시 패턴 (한 시스템에서 여러 테넌트의 데이터를 안전하게 격리한다):

### 3가지 전략 비교

| 기준 | Shared DB + RLS | Schema per Tenant | DB per Tenant |
|------|----------------|-------------------|---------------|
| 격리 수준 | 논리적 (행 수준) | 논리적 (스키마 수준) | 물리적 (완전 격리) |
| 비용 | 최저 | 중간 | 최고 |
| 구현 복잡도 | 낮음 | 중간 | 높음 |
| 확장성 | 수천 테넌트 | 수백 테넌트 | 수십 테넌트 |
| 백업/복구 | 전체 단위 | 스키마 단위 | 테넌트 단위 |
| 마이그레이션 | 1회 | N회 (자동화 필수) | N회 (자동화 필수) |
| 적합 사례 | SaaS MVP, B2C | B2B 중규모 | 금융, 의료 (규정 준수) |

추천: **Shared DB + RLS** (90% 사례). 규정 요구 시에만 DB 분리.

### RLS 구현 (Postgres + Supabase)

DO:
```typescript
// ✅ Step 1: 테넌트 컨텍스트 설정 미들웨어
async function tenantMiddleware(req: Request, next: Next) {
  const tenantId = req.headers.get("X-Tenant-ID");
  if (!tenantId) throw new ForbiddenError("Tenant ID required");

  // SET LOCAL은 현재 트랜잭션 내에서만 유효 (안전)
  await db.$executeRaw`SELECT set_config('app.tenant_id', ${tenantId}, true)`;
  return next(req);
}

// ✅ Step 2: RLS 정책 (SQL)
// -- 모든 테넌트 테이블에 tenant_id 컬럼 추가
// ALTER TABLE projects ADD COLUMN tenant_id UUID NOT NULL;
// ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
//
// CREATE POLICY tenant_isolation ON projects
//   USING (tenant_id = current_setting('app.tenant_id')::UUID)
//   WITH CHECK (tenant_id = current_setting('app.tenant_id')::UUID);

// ✅ Step 3: 인덱스 (tenant_id 첫 번째)
// CREATE INDEX idx_projects_tenant ON projects (tenant_id, created_at DESC);
```

```typescript
// ✅ 트랜잭션 내에서 SET LOCAL 사용 (트랜잭션 종료 시 자동 해제)
await db.$transaction(async (tx) => {
  await tx.$executeRaw`SELECT set_config('app.tenant_id', ${tenantId}, true)`;
  const projects = await tx.project.findMany();  // RLS 자동 적용
  return projects;
});
```

### Schema per Tenant 패턴
```typescript
// ✅ 테넌트별 스키마 전환
async function withTenantSchema<T>(
  tenantId: string,
  callback: (tx: PrismaClient) => Promise<T>
): Promise<T> {
  const schema = `tenant_${tenantId}`;
  await db.$executeRawUnsafe(`SET search_path TO "${schema}", public`);
  return callback(db);
}
```

DON'T:
```typescript
// ❌ WHERE 절에 tenant_id 필터만 의존 — 누락 시 전체 데이터 노출
async function getProjects(tenantId: string) {
  return db.project.findMany({
    where: { tenantId }, // 개발자가 빠뜨리면 전체 노출
  });
}

// ❌ SET 대신 SET LOCAL — 커넥션 풀에서 다른 요청에 영향
await db.$executeRaw`SET app.tenant_id = ${tenantId}`; // 커넥션 반환 후 잔류

// ❌ RLS 없이 API에서만 필터링 — 직접 DB 접근 시 격리 불가
```

### 체크리스트
- [ ] 모든 테넌트 테이블에 `tenant_id` 컬럼 + NOT NULL
- [ ] RLS 정책이 SELECT, INSERT, UPDATE, DELETE 모두 적용
- [ ] `SET LOCAL` 사용 (SET 아님)
- [ ] tenant_id 포함 복합 인덱스
- [ ] 슈퍼관리자용 BYPASSRLS 역할 분리
