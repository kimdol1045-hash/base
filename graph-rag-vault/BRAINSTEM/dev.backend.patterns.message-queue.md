---
id: "dev.backend.patterns.message-queue"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#109 Event-Driven Architecture"
tags: [backend, patterns, message-queue, bullmq, async]
---

# dev.backend.patterns.message-queue

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #109 Event-Driven Architecture  
> **Tokens**: 500

## Content

메시지 큐 패턴 (비동기 처리로 서비스 간 결합도를 낮추고 부하를 평탄화한다):

### 큐 기술 비교
| 기술 | 프로토콜 | 장점 | 적합 사례 |
|------|----------|------|-----------|
| BullMQ | Redis | 간편, 지연/반복 작업 | Node.js 모노리스 |
| RabbitMQ | AMQP | 라우팅, 교환기, 신뢰성 | MSA 간 통신 |
| SQS | HTTP | 관리형, 무한 확장 | AWS 서버리스 |
| Kafka | TCP | 순서 보장, 재처리 | 이벤트 스트리밍, 로그 |

### BullMQ 구현
```typescript
// DO: 도메인별 큐 분리, 멱등 컨슈머, DLQ 처리
import { Queue, Worker, QueueEvents } from 'bullmq';
import Redis from 'ioredis';

const connection = new Redis({ host: 'localhost', port: 6379, maxRetriesPerRequest: null });

// 도메인별 큐 분리
const emailQueue = new Queue('email', { connection });
const paymentQueue = new Queue('payment', { connection });

// Producer: 작업 추가
async function sendWelcomeEmail(userId: string) {
  await emailQueue.add('welcome', { userId }, {
    attempts: 3,                    // 최대 3회 재시도
    backoff: { type: 'exponential', delay: 2000 }, // 2s, 4s, 8s
    removeOnComplete: { count: 1000 },  // 완료된 작업 1000개만 유지
    removeOnFail: { count: 5000 },
  });
}

// 지연 작업: 결제 후 30분 뒤 리뷰 요청
await emailQueue.add('review-request', { orderId }, {
  delay: 30 * 60 * 1000, // 30분 후 실행
});

// 반복 작업: 매일 오전 9시 일일 보고서
await emailQueue.add('daily-report', {}, {
  repeat: { pattern: '0 9 * * *' }, // cron 표현식
});

// Consumer: 멱등 처리
const emailWorker = new Worker('email', async (job) => {
  // 멱등성: 이미 보낸 이메일인지 확인
  const sent = await db.findEmail({ jobId: job.id, type: job.name });
  if (sent) return { skipped: true };

  switch (job.name) {
    case 'welcome':
      await mailer.send({ to: job.data.userId, template: 'welcome' });
      break;
    case 'review-request':
      await mailer.send({ to: job.data.orderId, template: 'review' });
      break;
  }
  // 처리 기록 저장
  await db.saveEmailLog({ jobId: job.id, type: job.name, sentAt: new Date() });
}, {
  connection,
  concurrency: 5,       // 동시 처리 5개
  limiter: { max: 10, duration: 1000 }, // 초당 최대 10건 (rate limit)
});
```

### DLQ (Dead Letter Queue) 처리
```typescript
// 실패 작업 모니터링 및 재처리
emailWorker.on('failed', async (job, err) => {
  if (job && job.attemptsMade >= job.opts.attempts!) {
    logger.error(`Job ${job.id} moved to DLQ`, { error: err.message, data: job.data });
    await alerting.notify(`Email job failed permanently: ${job.id}`);
    // DLQ 큐에 명시적 이동
    await dlqQueue.add('email-failed', { originalJob: job.data, error: err.message });
  }
});
```

DON'T:
```typescript
// ❌ 단일 큐에 모든 작업 — 이메일 폭주가 결제 처리를 블로킹
const queue = new Queue('everything', { connection });
await queue.add('email', emailData);
await queue.add('payment', paymentData); // 이메일 작업에 밀려 지연

// ❌ DLQ 없음 — 실패 작업이 영구 유실
// ❌ 멱등하지 않은 컨슈머 — 재시도 시 이메일 중복 발송
// ❌ concurrency 무제한 — 외부 서비스 rate limit 초과
```

### 흔한 실수
- Redis 연결 끊김 시 작업 유실 (persistence 설정 필요: appendonly yes)
- 작업 데이터에 거대한 payload 포함 (ID만 전달 후 조회 권장)
- 완료된 작업을 삭제하지 않아 Redis 메모리 폭증

## Connections

### CO_CREATES (2)

- → [[dev.backend.api.background-jobs]] `w=0.6`
- ← [[dev.backend.patterns.event-driven]] `w=0.6`
