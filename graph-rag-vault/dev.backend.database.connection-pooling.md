---
id: "dev.backend.database.connection-pooling"
domain: "development.database"
type: "rule"
bloom_level: ""
tags: ["database", "connection-pool", "pgbouncer", "serverless", "prisma", "postgres"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.database.connection-pooling

> #110 Little's Law (Little, 1961)

DB 커넥션 풀링 규칙 (제한된 커넥션을 효율적으로 관리한다):

### 왜 커넥션 풀링이 중요한가?
DB 커넥션 생성 비용: TCP 핸드셰이크 + TLS + 인증 = ~50-100ms.
Little's Law: L = λ × W (동시 커넥션 = 요청률 × 평균 처리시간).
풀링 없이 요청당 커넥션 생성 시 Postgres 기본 max_connections(100) 즉시 소진.

### 풀 사이즈 공식
최적 커넥션 수 = (CPU 코어 수 × 2) + 디스크 스핀들 수
예: 4코어 서버 + SSD(1) = (4 × 2) + 1 = **9개**

### 풀 설정 기준표

| 설정 | 값 | 설명 |
|------|------|------|
| min | 2 | 유휴 시에도 유지할 최소 커넥션 |
| max | 20 | CPU 코어 기반 최대값 (Postgres max의 80%) |
| idleTimeoutMs | 10000 | 10초 유휴 시 커넥션 반환 |
| connectionTimeoutMs | 5000 | 5초 내 획득 실패 시 에러 |
| maxLifetimeMs | 1800000 | 30분 후 커넥션 재생성 (stale 방지) |

DO:
```typescript
// ✅ Prisma — 풀 사이즈 명시 (connection_limit)
// DATABASE_URL="postgresql://user:pass@host:5432/db?connection_limit=10&pool_timeout=5"

// ✅ Node.js pg 라이브러리 — 풀 설정
import { Pool } from "pg";
const pool = new Pool({
  max: 10,                   // 최대 커넥션 수
  idleTimeoutMillis: 10000,  // 10초 유휴 시 해제
  connectionTimeoutMillis: 5000, // 5초 내 획득 실패 시 에러
  maxLifetimeMillis: 1800000,    // 30분 후 커넥션 재생성
});

// ✅ 커넥션 사용 후 반드시 반환
const client = await pool.connect();
try {
  const result = await client.query("SELECT * FROM users WHERE id = $1", [id]);
  return result.rows[0];
} finally {
  client.release(); // 반드시 반환
}
```

### Serverless 환경 패턴 (Lambda, Vercel)
콜드 스타트마다 커넥션 생성 → 수백 개 커넥션 폭발 위험.

DO:
```typescript
// ✅ PgBouncer / Supabase Pooler — Transaction Mode
// connection string에 pooler 엔드포인트 사용
// DATABASE_URL="postgresql://user:pass@pooler.supabase.com:6543/db?pgbouncer=true"

// ✅ Prisma + Serverless: connection pooler 사용
// schema.prisma
// datasource db {
//   provider  = "postgresql"
//   url       = env("DATABASE_URL")        // pooler 엔드포인트
//   directUrl = env("DIRECT_URL")           // 마이그레이션용 직접 연결
// }

// ✅ Neon Serverless Driver — HTTP 기반 (커넥션 불필요)
import { neon } from "@neondatabase/serverless";
const sql = neon(process.env.DATABASE_URL!);
const users = await sql`SELECT * FROM users WHERE active = true`;
```

DON'T:
```typescript
// ❌ 요청마다 새 풀 생성 — 커넥션 폭발
export async function handler(req: Request) {
  const pool = new Pool({ max: 10 }); // 매 요청마다 새 풀!
  const result = await pool.query("SELECT 1");
  return Response.json(result.rows);
  // pool.end() 호출 안 함 → 커넥션 누수
}

// ❌ 커넥션 리밋 미설정 — Postgres max_connections 초과
const pool = new Pool(); // max 기본값: 10이지만 인스턴스별 누적
```

### 모니터링 지표
- `pool.totalCount`: 전체 커넥션 수
- `pool.idleCount`: 유휴 커넥션 수
- `pool.waitingCount`: 대기 중인 요청 수 (> 0이면 풀 확장 검토)
- Postgres: `SELECT count(*) FROM pg_stat_activity;` — 현재 연결 수 확인
