---
id: "dev.backend.api.background-jobs"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#109 Event-Driven Architecture"
tags: [backend, api, background-jobs, bullmq, queue, worker, redis]
---

# dev.backend.api.background-jobs

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #109 Event-Driven Architecture  
> **Tokens**: 500

## Content

Background Job 패턴 (요청 핸들러에서 오래 걸리는 작업을 직접 처리하지 않는다 -- 큐에 넣고 즉시 응답한다):

### BullMQ 큐 아키텍처
```
API Server → Queue (Redis) → Worker → Result/DLQ
```

DO:
```typescript
// 1. 큐 정의 (우선순위별 분리)
import { Queue, Worker, QueueEvents } from "bullmq";

const connection = { host: env.REDIS_HOST, port: env.REDIS_PORT };

// 기능별 큐 분리
const emailQueue = new Queue("email", { connection, defaultJobOptions: {
  attempts: 3,
  backoff: { type: "exponential", delay: 1_000 },
  removeOnComplete: { age: 86_400 },  // 완료 후 24시간 보관
  removeOnFail: { age: 604_800 },     // 실패 후 7일 보관
}});

const imageQueue = new Queue("image-processing", { connection, defaultJobOptions: {
  attempts: 2,
  backoff: { type: "exponential", delay: 2_000 },
  timeout: 60_000,  // 1분 타임아웃
}});

// 2. API에서 큐에 작업 추가
app.post("/api/v1/orders", authMiddleware, async (c) => {
  const order = await createOrder(c.get("userId"), body);

  // 이메일 발송은 큐에 위임 (즉시 응답)
  await emailQueue.add("order-confirmation", {
    orderId: order.id,
    email: order.userEmail,
  }, {
    priority: 1,  // 높은 우선순위
    jobId: `order-email-${order.id}`,  // 중복 방지 키
  });

  // 비동기 후처리도 큐에 위임
  await imageQueue.add("generate-receipt", { orderId: order.id });

  return c.json({ data: order }, 201);
});

// 3. Worker 정의 (별도 프로세스)
const emailWorker = new Worker("email", async (job) => {
  const { orderId, email } = job.data;

  // 멱등성 확인: 이미 발송된 이메일인지 체크
  const alreadySent = await db.query.emailLogs.findFirst({
    where: and(eq(emailLogs.orderId, orderId), eq(emailLogs.type, "order-confirmation")),
  });
  if (alreadySent) {
    console.log(`Email already sent for order ${orderId}, skipping`);
    return { skipped: true };
  }

  await sendEmail({ to: email, template: "order-confirmation", data: { orderId } });
  await db.insert(emailLogs).values({ orderId, type: "order-confirmation", sentAt: new Date() });

  return { sent: true };
}, {
  connection,
  concurrency: 5,          // 동시 처리 5개
  limiter: { max: 10, duration: 1_000 },  // 초당 10건 제한
});

// 4. 이벤트 모니터링
const emailEvents = new QueueEvents("email", { connection });
emailEvents.on("failed", ({ jobId, failedReason }) => {
  logger.error(`Job ${jobId} failed: ${failedReason}`);
});
emailEvents.on("completed", ({ jobId }) => {
  logger.info(`Job ${jobId} completed`);
});
```

### Dead Letter Queue (DLQ) 처리
```typescript
// 최대 재시도 후 실패한 작업을 DLQ로 이동
const dlqQueue = new Queue("dead-letter", { connection });

emailWorker.on("failed", async (job, err) => {
  if (job && job.attemptsMade >= job.opts.attempts!) {
    await dlqQueue.add("failed-email", {
      originalQueue: "email",
      originalData: job.data,
      error: err.message,
      failedAt: new Date().toISOString(),
      attempts: job.attemptsMade,
    });
    logger.error(`Job moved to DLQ: ${job.id}`, { error: err.message });
  }
});

// DLQ 수동 재처리 API (관리자용)
app.post("/admin/dlq/:jobId/retry", adminMiddleware, async (c) => {
  const dlqJob = await dlqQueue.getJob(c.req.param("jobId"));
  if (!dlqJob) throw Errors.notFound("DLQ 작업");

  const targetQueue = new Queue(dlqJob.data.originalQueue, { connection });
  await targetQueue.add("retry", dlqJob.data.originalData);
  await dlqJob.remove();

  return c.json({ data: { message: "재처리 요청됨" } });
});
```

### 재시도 전략
| 시도 | 대기 시간 | 누적 시간 | 비고 |
|------|-----------|-----------|------|
| 1차 | 1초 | 1초 | 일시적 오류 대응 |
| 2차 | 4초 | 5초 | 네트워크 복구 대기 |
| 3차 | 16초 | 21초 | 최종 시도 후 DLQ 이동 |

DON'T:
```typescript
// ❌ 요청 핸들러에서 직접 이메일 발송 -- 응답 지연 + 실패 시 재시도 불가
app.post("/api/v1/orders", async (c) => {
  const order = await createOrder(body);
  await sendEmail(order.email, "confirmation");  // 3초 블로킹
  return c.json({ data: order });
});

// ❌ 작업 중복 방지 없음 -- 같은 이메일 여러 번 발송
await emailQueue.add("send", data);  // jobId 없음 → 중복 추가 가능

// ❌ 모든 작업을 하나의 큐에 -- 우선순위 관리 불가
await generalQueue.add("email", emailData);
await generalQueue.add("video-encode", videoData);  // 이메일이 영상 인코딩에 밀림

// ❌ Worker에서 멱등성 미보장 -- 재시도 시 이중 처리
const worker = new Worker("payment", async (job) => {
  await chargeUser(job.data.userId, job.data.amount);  // 재시도 시 이중 과금!
});
```

### 흔한 실수
- Worker 프로세스가 API 서버와 같은 프로세스 -> 크래시 시 모든 작업 중단
- 완료된 작업을 영구 보관 -> Redis 메모리 폭증 (removeOnComplete 설정 필수)
- 작업 타임아웃 미설정 -> 무한 대기 작업이 Worker 슬롯 점유
- concurrency를 너무 높게 설정 -> 외부 서비스 Rate Limit 초과
- 큐 상태 모니터링 미구축 -> Bull Board 또는 Arena로 대시보드 구축 권장

## Connections

### CO_CREATES (2)

- ← [[dev.backend.api.third-party]] `w=0.6`
- ← [[dev.backend.patterns.message-queue]] `w=0.6`
