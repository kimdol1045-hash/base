---
id: "dev.backend.auth.api-key"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["auth", "api-key", "security", "backend"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.auth.api-key

> #225 API Key Authentication (OWASP API Security Top 10, 2023)

# API Key 인증 가이드

## 핵심 원칙
- API Key는 서비스 간 통신(M2M) 인증에 적합하다
- 키 값은 해시하여 저장하고, 평문으로 보관하지 않는다
- 키별 권한 범위(Scope)를 제한한다
- 키 순환(Rotation) 메커니즘을 구현한다

## DO
- API Key를 `Authorization` 헤더 또는 `X-API-Key` 헤더로 전달한다
- 키 생성 시 충분한 엔트로피를 확보한다 (최소 32바이트)
- 키에 접두사를 붙여 식별 가능하게 한다 (예: `secret_live_`, `public_test_`)
- 키별 Rate Limit과 사용량 추적을 구현한다
- 만료 일자를 설정하고 주기적으로 순환한다

## DON'T
- API Key를 URL 쿼리 파라미터로 전달하지 않는다 (로그에 기록됨)
- API Key를 평문으로 데이터베이스에 저장하지 않는다
- 하나의 키에 모든 권한을 부여하지 않는다
- 사용자 인증(로그인)에 API Key를 사용하지 않는다 (JWT/세션 사용)

## 코드 예시
```typescript
import { randomBytes, createHash } from "crypto";

// API Key 생성
function generateApiKey(prefix: string): { key: string; hash: string } {
  const raw = randomBytes(32).toString("base64url");
  const key = `${prefix}_${raw}`;
  const hash = createHash("sha256").update(key).digest("hex");
  return { key, hash }; // key는 사용자에게 한 번만 보여주고, hash만 DB에 저장
}

// API Key 검증 미들웨어
async function apiKeyAuth(req: Request, res: Response, next: NextFunction) {
  const apiKey = req.headers["x-api-key"] as string;
  if (!apiKey) {
    return res.status(401).json({ error: { code: "API_KEY_REQUIRED" } });
  }

  const hash = createHash("sha256").update(apiKey).digest("hex");
  const keyRecord = await db.apiKeys.findOne({
    where: { hash, revokedAt: null },
  });

  if (!keyRecord) {
    return res.status(401).json({ error: { code: "INVALID_API_KEY" } });
  }

  if (keyRecord.expiresAt && keyRecord.expiresAt < new Date()) {
    return res.status(401).json({ error: { code: "API_KEY_EXPIRED" } });
  }

  // 사용량 기록
  await db.apiKeyUsage.increment(keyRecord.id);

  req.apiKey = keyRecord;
  next();
}
```
