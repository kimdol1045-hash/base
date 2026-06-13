---
id: "dev.backend.patterns.timeout-patterns"
domain: "development.backend"
type: "rule"
bloom_level: ""
tags: ["backend", "patterns", "timeout", "resilience", "database"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.patterns.timeout-patterns

> #125 Release It! Stability Patterns

타임아웃 설계 (모든 외부 호출에는 반드시 타임아웃을 설정한다):

### 계층별 타임아웃 기준
| 계층 | 타임아웃 | 근거 |
|------|----------|------|
| Client (브라우저) | 30s | 사용자 체감 한계 |
| API Gateway/LB | 25s | Client보다 짧아야 함 |
| Application Service | 20s | Gateway보다 짧아야 함 |
| External API 호출 | 10s | 제어 불가 구간, 짧게 |
| DB Query | 5s | 5초 넘는 쿼리는 최적화 필요 |
| Redis/Cache | 1s | 캐시는 빨라야 의미 있음 |
| DNS Lookup | 2s | 네트워크 기본 |

핵심 원칙: **upstream(호출자) > downstream(피호출자)** — 역전되면 upstream이 먼저 타임아웃

### AbortController 기반 구현
```typescript
// DO: AbortSignal.timeout()으로 fetch 타임아웃, 계층별 차등 적용
async function callExternalApi(endpoint: string, data: unknown) {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
    signal: AbortSignal.timeout(10_000), // 10초 타임아웃
  });
  if (!response.ok) throw new HttpError(response.status);
  return response.json();
}

// DB 쿼리 타임아웃 (statement_timeout)
async function queryWithTimeout<T>(sql: string, params: unknown[]): Promise<T> {
  const client = await pool.connect();
  try {
    await client.query('SET statement_timeout = 5000'); // 5초
    const result = await client.query(sql, params);
    return result.rows as T;
  } finally {
    await client.query('RESET statement_timeout');
    client.release();
  }
}

// 커넥션 풀 타임아웃 설정
import { Pool } from 'pg';
const pool = new Pool({
  connectionTimeoutMillis: 3000,   // 커넥션 획득 대기 3초
  idleTimeoutMillis: 30000,        // 유휴 커넥션 30초 후 반환
  query_timeout: 5000,             // 쿼리 실행 5초
  max: 20,                         // 최대 커넥션 수
});
```

### 복합 호출 타임아웃
```typescript
// DO: 전체 요청에 대한 상위 타임아웃 + 개별 호출 타임아웃
async function processOrder(orderId: string) {
  // 전체 처리 20초 제한
  return Promise.race([
    (async () => {
      const inventory = await callService('/inventory/check', { orderId }); // 10s
      const payment = await callExternalApi('/payment/charge', { orderId }); // 10s
      return { inventory, payment };
    })(),
    sleep(20_000).then(() => { throw new TimeoutError('Order processing timeout'); }),
  ]);
}
```

DON'T:
```typescript
// ❌ 타임아웃 없는 외부 호출 — 상대 서버 무응답 시 무한 대기
const res = await fetch('https://external-api.com/data'); // 타임아웃 없음!

// ❌ 하위 서비스 타임아웃 > 상위 서비스 타임아웃
// Gateway: 10s, Service: 20s → Service가 처리 중인데 Gateway가 먼저 503 반환
// 클라이언트는 에러, 서비스는 계속 실행 (좀비 요청)

// ❌ DB 커넥션 풀 타임아웃 미설정 — 커넥션 고갈 시 전체 서비스 마비
const pool = new Pool({ max: 20 }); // connectionTimeoutMillis 기본값 0 = 무한 대기
```

### 타임아웃 모니터링
- 타임아웃 발생률 메트릭: `timeout_total{service, target}`
- P99 응답시간이 타임아웃의 80%에 근접하면 알림
- 타임아웃 로그에 호출 대상, 소요시간 포함

### 흔한 실수
- 개발 환경에서 타임아웃 비활성화 후 프로덕션에서도 적용 안 됨
- 타임아웃 후 리소스(DB 커넥션, 파일 핸들) 미정리
- Promise.race 사용 시 패배한 Promise의 에러 미처리 (unhandled rejection)

## Connections

- [[dev.backend.patterns.circuit-breaker]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.retry-patterns]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.health-check]] — CO_CREATES (weight: 0.6)
