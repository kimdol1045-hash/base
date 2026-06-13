---
id: "dev.backend.patterns.idempotency"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "api", "idempotency", "payment"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.patterns.idempotency

> #106 Idempotency (RFC 7231, 2014)

멱등성 (같은 요청을 N번 보내도 결과가 동일해야 한다):

### HTTP 메서드별 멱등성
| 메서드 | 멱등? | 설명 |
|--------|-------|------|
| GET | ✅ | 항상 멱등 |
| PUT | ✅ | 전체 교체이므로 멱등 |
| DELETE | ✅ | 이미 삭제된 것 삭제 = 동일 결과 |
| POST | ❌ | 기본적으로 비멱등 → Idempotency Key 필요 |
| PATCH | ❌ | 상대적 변경 가능 → 주의 필요 |

### Idempotency Key 패턴
```typescript
// 클라이언트: 요청마다 고유 키 생성
// POST /api/payments
// Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000

async function handlePayment(req: Request) {
  const idempotencyKey = req.headers.get('Idempotency-Key');
  if (!idempotencyKey) return error(400, 'Idempotency-Key 헤더 필수');

  // 1. 이미 처리된 요청인지 확인
  const existing = await db.query(
    'SELECT response_body, status_code FROM idempotency_keys WHERE key = $1',
    [idempotencyKey]
  );
  if (existing) return new Response(existing.response_body, { status: existing.status_code });

  // 2. 락 획득 (동시 중복 요청 방지)
  const locked = await db.query(
    'INSERT INTO idempotency_keys (key, status) VALUES ($1, $2) ON CONFLICT DO NOTHING RETURNING key',
    [idempotencyKey, 'processing']
  );
  if (!locked) return error(409, '동일 요청 처리 중');

  // 3. 실제 처리
  try {
    const result = await processPayment(req.body);
    await db.query(
      'UPDATE idempotency_keys SET status = $1, response_body = $2, status_code = $3 WHERE key = $4',
      ['completed', JSON.stringify(result), 200, idempotencyKey]
    );
    return json(result);
  } catch (e) {
    await db.query('DELETE FROM idempotency_keys WHERE key = $1', [idempotencyKey]);
    throw e;
  }
}
```

### 적용 대상
- 결제/송금 API (필수)
- 주문 생성 (필수)
- 이메일/알림 발송 (권장)
- 일반 CRUD POST (선택)

### 키 만료: 24시간 후 자동 삭제 (TTL)

## Connections

- [[dev.backend.api.payment]] — CO_CREATES (weight: 0.6)
- [[dev.backend.auth.jwt-auth]] — CO_CREATES (weight: 0.6)
- [[dev.backend.api.webhook]] — CO_CREATES (weight: 0.6)
