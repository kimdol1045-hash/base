---
id: "dev.backend.api.idempotency"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["api", "idempotency", "reliability", "backend"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.api.idempotency

> #219 Idempotency Patterns (Stripe API Design, 2018)

# API 멱등성(Idempotency) 가이드

## 핵심 원칙
- 동일한 요청을 여러 번 보내도 결과가 동일해야 한다
- POST/PATCH 같은 비멱등 메서드에 Idempotency Key를 적용한다
- 네트워크 장애로 인한 중복 요청을 안전하게 처리한다
- 클라이언트가 안전하게 재시도할 수 있는 API를 설계한다

## DO
- `Idempotency-Key` 요청 헤더를 지원한다
- 키와 응답을 저장하여 동일 키 요청 시 저장된 응답을 반환한다
- 키 저장소에 TTL을 설정한다 (보통 24시간)
- 결제, 주문 생성 등 부작용이 큰 API에 필수 적용한다

## DON'T
- GET, DELETE는 이미 멱등하므로 별도 키를 요구하지 않는다
- Idempotency Key를 영구 저장하지 않는다 (TTL 필수)
- 진행 중인 요청의 동일 키로 중복 실행을 허용하지 않는다
- 요청 본문이 다른데 같은 키를 재사용하는 것을 허용하지 않는다

## 코드 예시
```typescript
async function idempotencyMiddleware(req: Request, res: Response, next: NextFunction) {
  const key = req.headers["idempotency-key"] as string;
  if (!key) return next(); // 키 없으면 통과

  const existing = await redis.get(`idempotency:${key}`);
  if (existing) {
    const cached = JSON.parse(existing);
    // 요청 본문 해시 비교 (같은 키, 다른 요청 방지)
    const bodyHash = createHash("sha256").update(JSON.stringify(req.body)).digest("hex");
    if (cached.bodyHash !== bodyHash) {
      return res.status(422).json({
        error: { code: "IDEMPOTENCY_MISMATCH", message: "동일 키에 다른 요청 본문" }
      });
    }
    return res.status(cached.status).json(cached.body);
  }

  // 진행 중 잠금
  const locked = await redis.set(`idempotency:lock:${key}`, "1", "NX", "EX", 60);
  if (!locked) {
    return res.status(409).json({ error: { code: "REQUEST_IN_PROGRESS" } });
  }

  const originalJson = res.json.bind(res);
  res.json = (body: unknown) => {
    const bodyHash = createHash("sha256").update(JSON.stringify(req.body)).digest("hex");
    redis.set(`idempotency:${key}`, JSON.stringify({
      status: res.statusCode, body, bodyHash,
    }), "EX", 86400);
    redis.del(`idempotency:lock:${key}`);
    return originalJson(body);
  };
  next();
}
```
