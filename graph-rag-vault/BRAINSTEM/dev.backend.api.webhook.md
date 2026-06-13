---
id: "dev.backend.api.webhook"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#104 Idempotency"
tags: [backend, api, webhook, idempotency, hmac, event-driven]
---

# dev.backend.api.webhook

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #104 Idempotency  
> **Tokens**: 500

## Content

Webhook 패턴 (수신과 발신 모두 멱등성과 서명 검증이 필수다 -- 한 번의 이벤트가 여러 번 도착할 수 있다):

### 수신 Webhook (Receiving)
외부 서비스(Stripe, GitHub 등)에서 이벤트를 수신할 때의 패턴.

DO:
```typescript
import { createHmac, timingSafeEqual } from "crypto";

// 1. 서명 검증 미들웨어
function webhookSignatureMiddleware(secret: string) {
  return async (c: Context, next: Next) => {
    const signature = c.req.header("x-webhook-signature");
    const timestamp = c.req.header("x-webhook-timestamp");
    if (!signature || !timestamp) {
      return c.json({ error: "Missing signature headers" }, 401);
    }

    // 타임스탬프 검증 (5분 이내만 허용 -- replay attack 방지)
    const age = Date.now() - parseInt(timestamp) * 1000;
    if (age > 300_000) {
      return c.json({ error: "Webhook timestamp expired" }, 401);
    }

    const body = await c.req.text();
    const expected = createHmac("sha256", secret)
      .update(`${timestamp}.${body}`)
      .digest("hex");

    const signatureBuffer = Buffer.from(signature, "hex");
    const expectedBuffer = Buffer.from(expected, "hex");

    // timing-safe 비교 (타이밍 공격 방지)
    if (!timingSafeEqual(signatureBuffer, expectedBuffer)) {
      return c.json({ error: "Invalid signature" }, 401);
    }

    c.set("webhookBody", JSON.parse(body));
    await next();
  };
}

// 2. 멱등성 보장 핸들러
app.post("/webhooks/payment", webhookSignatureMiddleware(env.PAYMENT_WEBHOOK_SECRET), async (c) => {
  const event = c.get("webhookBody") as WebhookEvent;

  // 멱등성 키로 중복 처리 방지
  const existing = await db.query.webhookEvents.findFirst({
    where: eq(webhookEvents.eventId, event.id),
  });
  if (existing) {
    return c.json({ received: true, duplicate: true }); // 200 반환하여 재전송 중단
  }

  // 이벤트 저장 (처리 전에 기록)
  await db.insert(webhookEvents).values({
    eventId: event.id,
    type: event.type,
    payload: event,
    status: "processing",
  });

  // 비동기 처리 (빠른 응답을 위해 큐에 위임)
  await webhookQueue.add("process", { eventId: event.id, type: event.type });

  return c.json({ received: true }, 200); // 즉시 200 반환 (3초 이내)
});

// 3. Worker에서 이벤트 타입별 처리
const webhookWorker = new Worker("webhook", async (job) => {
  const { eventId, type } = job.data;
  const event = await db.query.webhookEvents.findFirst({
    where: eq(webhookEvents.eventId, eventId),
  });

  switch (type) {
    case "payment.completed":
      await handlePaymentCompleted(event!.payload);
      break;
    case "subscription.cancelled":
      await handleSubscriptionCancelled(event!.payload);
      break;
    default:
      logger.warn(`Unknown webhook type: ${type}`);
  }

  await db.update(webhookEvents)
    .set({ status: "processed", processedAt: new Date() })
    .where(eq(webhookEvents.eventId, eventId));
}, { connection });
```

### 발신 Webhook (Sending)
우리 서비스에서 외부로 이벤트를 전송할 때의 패턴.

```typescript
// 발신 Webhook 시스템
async function sendWebhook(subscription: WebhookSubscription, event: AppEvent): Promise<void> {
  const payload = JSON.stringify({
    id: randomUUID(),
    type: event.type,
    data: event.data,
    createdAt: new Date().toISOString(),
  });

  const timestamp = Math.floor(Date.now() / 1000);
  const signature = createHmac("sha256", subscription.secret)
    .update(`${timestamp}.${payload}`)
    .digest("hex");

  // 재시도 로직 (exponential backoff)
  const MAX_RETRIES = 5;
  const retryDelays = [0, 1_000, 5_000, 30_000, 120_000]; // 즉시, 1초, 5초, 30초, 2분

  for (let attempt = 0; attempt < MAX_RETRIES; attempt++) {
    if (attempt > 0) await sleep(retryDelays[attempt]);

    try {
      const response = await fetch(subscription.url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Webhook-Signature": signature,
          "X-Webhook-Timestamp": String(timestamp),
          "X-Webhook-Id": event.id,
        },
        body: payload,
        signal: AbortSignal.timeout(10_000), // 10초 타임아웃
      });

      // 200-299만 성공으로 간주
      if (response.ok) {
        await recordDelivery(subscription.id, event.id, "delivered", attempt + 1);
        return;
      }

      // 4xx는 재시도하지 않음 (클라이언트 오류)
      if (response.status >= 400 && response.status < 500) {
        await recordDelivery(subscription.id, event.id, "rejected", attempt + 1);
        return;
      }
    } catch (err) {
      logger.warn(`Webhook delivery attempt ${attempt + 1} failed`, { error: err });
    }
  }

  await recordDelivery(subscription.id, event.id, "failed", MAX_RETRIES);
  // 연속 실패 시 구독 비활성화 검토
  await checkAndDisableSubscription(subscription.id);
}
```

DON'T:
```typescript
// ❌ 서명 검증 없이 webhook 수신 -- 누구나 위조 가능
app.post("/webhooks/payment", async (c) => {
  const body = await c.req.json();  // 서명 확인 없이 바로 처리
  await processPayment(body);
});

// ❌ 동기적으로 처리 후 응답 -- 타임아웃으로 재전송 폭탄
app.post("/webhooks/order", async (c) => {
  const event = await c.req.json();
  await processOrder(event);       // 30초 걸리는 작업
  await sendNotification(event);   // 추가 10초
  return c.json({ ok: true });     // 외부 서비스는 이미 타임아웃
});

// ❌ 멱등성 키 없이 처리 -- 재전송 시 이중 결제
await chargeUser(event.data.userId, event.data.amount);  // 매번 과금
```

### 발신 재시도 전략
| 시도 | 대기 시간 | 누적 대기 | 비고 |
|------|-----------|-----------|------|
| 1차 | 즉시 | 0초 | 초기 시도 |
| 2차 | 1초 | 1초 | 일시 오류 대응 |
| 3차 | 5초 | 6초 | 서버 복구 대기 |
| 4차 | 30초 | 36초 | 장기 복구 대기 |
| 5차 | 2분 | 156초 | 최종 시도 후 실패 기록 |

### 흔한 실수
- timingSafeEqual 대신 === 로 서명 비교 -> 타이밍 공격 취약
- Webhook 응답을 3초 이내에 반환하지 않음 -> 발신자가 타임아웃으로 재전송
- eventId 기반 멱등성 체크 없이 처리 -> 재전송 시 이중 처리
- 수신 webhook 엔드포인트에 Rate Limiting 미적용 -> 악의적 대량 요청 가능
- 발신 시 4xx 에러에도 재시도 -> 불필요한 트래픽 발생

## Connections

### CO_CREATES (1)

- → [[dev.backend.patterns.idempotency]] `w=0.6`
