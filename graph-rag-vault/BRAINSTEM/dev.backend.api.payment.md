---
id: "dev.backend.api.payment"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#104 Idempotency, #115 Least Privilege"
tags: [backend, api, payment, stripe, webhook, idempotency, pci]
---

# dev.backend.api.payment

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #104 Idempotency, #115 Least Privilege  
> **Tokens**: 500

## Content

결제 연동 패턴 (카드 번호를 절대 직접 다루지 않는다 -- PCI DSS 준수는 선택이 아니라 법적 의무다):

### Stripe Checkout 흐름
```
클라이언트 → 서버(세션 생성) → Stripe(결제 UI) → Webhook(결제 완료) → 서버(주문 확정)
```

DO:
```typescript
import Stripe from "stripe";

const stripe = new Stripe(env.STRIPE_SECRET_KEY, { apiVersion: "2024-06-20" });

// 1. Checkout Session 생성
app.post("/api/v1/checkout", authMiddleware, async (c) => {
  const { items } = CheckoutSchema.parse(await c.req.json());
  const userId = c.get("userId");

  // 주문 생성 (pending 상태)
  const order = await db.insert(orders).values({
    userId,
    status: "pending",
    items: JSON.stringify(items),
    total: calculateTotal(items),
  }).returning();

  // Stripe Checkout Session
  const session = await stripe.checkout.sessions.create({
    mode: "payment",
    customer_email: c.get("userEmail"),
    client_reference_id: order[0].id,
    line_items: items.map((item) => ({
      price_data: {
        currency: "krw",
        product_data: { name: item.name, description: item.description },
        unit_amount: item.price,  // KRW는 소수점 없음
      },
      quantity: item.quantity,
    })),
    success_url: `${env.FRONTEND_URL}/orders/${order[0].id}?status=success`,
    cancel_url: `${env.FRONTEND_URL}/orders/${order[0].id}?status=cancelled`,
    metadata: { orderId: order[0].id },
    // 멱등성 키 (동일 주문 중복 세션 방지)
    idempotency_key: `checkout-${order[0].id}`,
  } as Stripe.Checkout.SessionCreateParams);

  return c.json({ data: { sessionId: session.id, url: session.url } });
});

// 2. Webhook 수신 (결제 완료 처리)
app.post("/webhooks/stripe", async (c) => {
  const sig = c.req.header("stripe-signature");
  if (!sig) return c.json({ error: "Missing signature" }, 400);

  let event: Stripe.Event;
  try {
    const body = await c.req.text();
    event = stripe.webhooks.constructEvent(body, sig, env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    logger.error("Stripe webhook signature verification failed", { error: err });
    return c.json({ error: "Invalid signature" }, 400);
  }

  // 멱등성: 이벤트 중복 처리 방지
  const existing = await db.query.stripeEvents.findFirst({
    where: eq(stripeEvents.eventId, event.id),
  });
  if (existing) return c.json({ received: true, duplicate: true });

  // 이벤트 기록
  await db.insert(stripeEvents).values({
    eventId: event.id,
    type: event.type,
    processedAt: new Date(),
  });

  switch (event.type) {
    case "checkout.session.completed": {
      const session = event.data.object as Stripe.Checkout.Session;
      const orderId = session.metadata?.orderId;
      if (!orderId) break;

      await db.update(orders)
        .set({
          status: "paid",
          stripeSessionId: session.id,
          paidAt: new Date(),
        })
        .where(eq(orders.id, orderId));

      // 후처리 큐 (이메일, 재고 차감 등)
      await orderQueue.add("post-payment", { orderId });
      break;
    }

    case "charge.refunded": {
      const charge = event.data.object as Stripe.Charge;
      await handleRefund(charge);
      break;
    }

    default:
      logger.info(`Unhandled Stripe event: ${event.type}`);
  }

  return c.json({ received: true });
});

// 3. 환불 처리
app.post("/api/v1/orders/:id/refund", authMiddleware, async (c) => {
  const orderId = c.req.param("id");
  const { reason } = RefundSchema.parse(await c.req.json());

  const order = await db.query.orders.findFirst({
    where: and(eq(orders.id, orderId), eq(orders.userId, c.get("userId"))),
  });
  if (!order) throw Errors.notFound("주문");
  if (order.status !== "paid") throw Errors.badRequest("환불 가능한 상태가 아닙니다");

  // Stripe 환불 요청 (멱등성 키 포함)
  const refund = await stripe.refunds.create({
    payment_intent: order.stripePaymentIntentId,
    reason: "requested_by_customer",
    metadata: { orderId, reason },
  }, {
    idempotencyKey: `refund-${orderId}`,
  });

  await db.update(orders).set({
    status: "refund_pending",
    refundId: refund.id,
  }).where(eq(orders.id, orderId));

  return c.json({ data: { refundId: refund.id, status: "pending" } });
});
```

### 결제 상태 머신
| 상태 | 전이 조건 | 다음 상태 |
|------|-----------|-----------|
| pending | checkout.session.completed | paid |
| pending | 세션 만료 (30분) | expired |
| paid | 환불 요청 | refund_pending |
| refund_pending | charge.refunded | refunded |
| paid | 부분 환불 | partially_refunded |

DON'T:
```typescript
// ❌ 카드 번호 직접 처리 -- PCI DSS 위반, 법적 처벌 대상
app.post("/api/v1/pay", async (c) => {
  const { cardNumber, cvv, expiry } = await c.req.json();
  await stripe.charges.create({ source: cardNumber });  // 절대 금지
});

// ❌ Webhook 없이 클라이언트 콜백만 신뢰
// success_url 도달 = 결제 완료로 간주 -> 결제 없이 URL 직접 접근 가능
app.get("/orders/:id/success", async (c) => {
  await db.update(orders).set({ status: "paid" });  // webhook 확인 없이 완료 처리
});

// ❌ 멱등성 키 없이 결제 요청 -- 네트워크 재시도 시 이중 과금
await stripe.charges.create({ amount: 10000, currency: "krw" });

// ❌ Stripe Secret Key를 클라이언트에 노출
// STRIPE_SECRET_KEY는 서버에서만, STRIPE_PUBLISHABLE_KEY만 클라이언트
```

### 흔한 실수
- success_url 도달을 결제 완료로 간주 -> 반드시 webhook으로 확인
- 환불 시 Stripe 응답만 확인하고 DB 업데이트 누락 -> webhook(charge.refunded)으로 최종 확인
- KRW 통화에서 소수점 처리 -> KRW는 zero-decimal currency (100 = 100원)
- 테스트 환경에서 실제 키 사용 -> STRIPE_SECRET_KEY의 sk_test_ 접두어 확인
- Webhook endpoint에 Rate Limiting 미적용 -> DDoS 공격 벡터

## Connections

### CO_CREATES (2)

- → [[dev.backend.auth.jwt-auth]] `w=0.6`
- → [[dev.backend.patterns.idempotency]] `w=0.6`
