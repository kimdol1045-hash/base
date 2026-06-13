---
id: "dev.backend.patterns.health-check"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#130 Observability"
tags: [backend, patterns, health-check, k8s, observability]
---

# dev.backend.patterns.health-check

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #130 Observability  
> **Tokens**: 500

## Content

헬스체크 패턴 (서비스 상태를 정확히 보고하여 트래픽 라우팅을 제어한다):

### 프로브 종류
| 프로브 | 경로 | 목적 | 검사 항목 |
|--------|------|------|-----------|
| Liveness | /health/live | 프로세스 생존 확인 | 단순 응답 (200 OK) |
| Readiness | /health/ready | 트래픽 수신 가능 여부 | DB, Redis, 외부 의존성 |
| Startup | /health/startup | 초기화 완료 여부 | 마이그레이션, 캐시 워밍 |

### 구현
```typescript
// DO: liveness는 단순, readiness는 의존성 체크
import { Router } from 'express';

const health = Router();

// Liveness: 프로세스가 살아있으면 200 (DB 체크 금지!)
health.get('/health/live', (req, res) => {
  res.status(200).json({ status: 'ok', timestamp: Date.now() });
});

// Readiness: 모든 의존성 정상이면 200
health.get('/health/ready', async (req, res) => {
  const checks = await Promise.allSettled([
    checkDatabase(),
    checkRedis(),
    checkExternalApi(),
  ]);

  const results = {
    database: checks[0].status === 'fulfilled' ? 'up' : 'down',
    redis: checks[1].status === 'fulfilled' ? 'up' : 'down',
    externalApi: checks[2].status === 'fulfilled' ? 'up' : 'down',
  };

  const allHealthy = Object.values(results).every(s => s === 'up');
  res.status(allHealthy ? 200 : 503).json({
    status: allHealthy ? 'ready' : 'not_ready',
    checks: results,
    timestamp: Date.now(),
  });
});

// 의존성 체크 함수 (타임아웃 포함)
async function checkDatabase(): Promise<void> {
  const controller = new AbortController();
  setTimeout(() => controller.abort(), 3000); // 3초 타임아웃
  await db.query('SELECT 1');
}

async function checkRedis(): Promise<void> {
  const pong = await redis.ping();
  if (pong !== 'PONG') throw new Error('Redis not responding');
}
```

### Graceful Shutdown
```typescript
// DO: SIGTERM 수신 시 graceful shutdown
let isShuttingDown = false;

process.on('SIGTERM', async () => {
  isShuttingDown = true;
  logger.info('SIGTERM received, starting graceful shutdown');

  // 1. readiness를 503으로 변경 (새 트래픽 차단)
  // 2. 진행 중인 요청 완료 대기 (최대 30초)
  server.close(async () => {
    await db.end();
    await redis.quit();
    process.exit(0);
  });

  setTimeout(() => process.exit(1), 30000); // 30초 후 강제 종료
});

// readiness에 shutdown 상태 반영
health.get('/health/ready', async (req, res) => {
  if (isShuttingDown) return res.status(503).json({ status: 'shutting_down' });
  // ... 기존 체크
});
```

DON'T:
```typescript
// ❌ Liveness에서 DB 체크 — DB 장애 시 컨테이너 무한 재시작
health.get('/health/live', async (req, res) => {
  await db.query('SELECT 1'); // DB 다운 → liveness 실패 → 재시작 → 반복!
  res.json({ status: 'ok' });
});

// ❌ Readiness에서 의존성 체크 없음 — DB 다운인데 트래픽 수신
health.get('/health/ready', (req, res) => {
  res.json({ status: 'ok' }); // 항상 200 → 의미 없는 체크
});

// ❌ 체크에 타임아웃 없음 — 느린 DB 응답이 프로브 실패 유발
```

### K8s Probe 설정 예시
```yaml
livenessProbe:
  httpGet: { path: /health/live, port: 3000 }
  initialDelaySeconds: 5
  periodSeconds: 10
  failureThreshold: 3
readinessProbe:
  httpGet: { path: /health/ready, port: 3000 }
  initialDelaySeconds: 10
  periodSeconds: 5
  failureThreshold: 2
```

### 흔한 실수
- liveness와 readiness를 하나의 엔드포인트로 합침
- graceful shutdown 미구현으로 진행 중인 요청 강제 종료
- 헬스체크 엔드포인트에 인증 미들웨어 적용 (프로브 실패)

## Connections

### CO_CREATES (3)

- ← [[dev.backend.patterns.circuit-breaker]] `w=0.6`
- ← [[dev.backend.patterns.retry-patterns]] `w=0.6`
- ← [[dev.backend.patterns.timeout-patterns]] `w=0.6`
