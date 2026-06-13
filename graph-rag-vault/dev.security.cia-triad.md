---
id: "dev.security.cia-triad"
domain: "development.security"
type: "pattern"
bloom_level: ""
tags: ["security", "cia-triad", "confidentiality", "integrity", "availability", "iso27001"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.security.cia-triad

> #114 CIA 삼각형 (ISO 27001)

CIA Triad -- 정보 보안의 3대 목표 (ISO 27001 기반):

모든 보안 결정은 Confidentiality, Integrity, Availability 중 어떤 속성을 보호하는지 명확히 해야 한다.

### C: Confidentiality (기밀성)
허가되지 않은 주체가 정보에 접근할 수 없도록 보장한다.

```typescript
// DO: 전송 중 암호화 + 저장 시 암호화
import { createCipheriv, randomBytes } from "node:crypto";

const ALGORITHM = "aes-256-gcm";
function encrypt(plaintext: string, key: Buffer): EncryptedData {
  const iv = randomBytes(16);
  const cipher = createCipheriv(ALGORITHM, key, iv);
  const encrypted = Buffer.concat([cipher.update(plaintext, "utf8"), cipher.final()]);
  const tag = cipher.getAuthTag();
  return { encrypted: encrypted.toString("base64"), iv: iv.toString("base64"), tag: tag.toString("base64") };
}

// DO: 접근 제어 -- 필드 레벨 필터링
function toPublicUser(user: InternalUser): PublicUser {
  const { passwordHash, ssn, internalNotes, ...publicFields } = user;
  return publicFields;
}

// DON'T: 민감 정보 평문 저장
await db.insert(users).values({ password: body.password }); // 평문 저장 금지
```

**구현 체크리스트:**
- 비밀번호: bcrypt cost=12 또는 argon2id (memoryCost=65536, timeCost=3)
- API 키/토큰: AES-256-GCM 암호화 후 DB 저장
- 전송: TLS 1.3 강제, HSTS 헤더 적용
- 로그: PII(이메일, 전화, IP) 마스킹 처리

### I: Integrity (무결성)
데이터가 비인가 변경 없이 정확하고 완전함을 보장한다.

```typescript
// DO: 해시 기반 무결성 검증 + 감사 로그
import { createHash } from "node:crypto";

function computeChecksum(data: string): string {
  return createHash("sha256").update(data).digest("hex");
}

// 감사 로그 -- 누가, 언제, 무엇을 변경했는지 기록
async function auditLog(action: string, userId: string, details: Record<string, unknown>) {
  await db.insert(auditLogs).values({
    action,
    userId,
    details: JSON.stringify(details),
    timestamp: new Date().toISOString(),
    checksum: computeChecksum(JSON.stringify(details)),
  });
}

// DON'T: 감사 추적 없이 직접 수정
await db.update(accounts).set({ balance: newBalance }).where(eq(accounts.id, id));
// 누가 왜 변경했는지 기록 없음
```

**구현 체크리스트:**
- DB: 핵심 테이블에 `updated_by`, `updated_at` 컬럼 필수
- 파일 업로드: SHA-256 체크섬 검증
- API 요청: HMAC 서명으로 요청 변조 탐지
- 감사 로그: append-only 스토리지, 삭제 불가 정책

### A: Availability (가용성)
인가된 사용자가 필요할 때 정보와 시스템에 접근할 수 있도록 보장한다.

```typescript
// DO: Rate Limiting으로 DoS 방어
import { rateLimiter } from "hono-rate-limiter";
app.use(rateLimiter({
  windowMs: 60_000,            // 1분
  limit: 100,                  // 일반 API: 100 req/min
  keyGenerator: (c) => c.req.header("x-forwarded-for") ?? "unknown",
}));

// 인증 엔드포인트는 더 엄격하게: 5 req/min
app.use("/auth/*", rateLimiter({ windowMs: 60_000, limit: 5 }));

// DON'T: Rate limiting 없음, 무제한 payload 허용
app.post("/upload", async (c) => {
  const file = await c.req.blob(); // 크기 제한 없음 = OOM 공격 가능
});
```

**구현 체크리스트:**
- Rate Limiting: 인증 5 req/min, 일반 API 100 req/min
- 파일 업로드: 최대 10MB 제한
- DB: 커넥션 풀링 (max 20), 쿼리 타임아웃 30초
- 배포: 헬스체크 + 자동 재시작 + 이중화(최소 2 인스턴스)

## Connections

- [[dev.security.role]] — REQUIRES (weight: 0.9)
- [[dev.security.verify]] — FEEDS (weight: 0.8)
- [[dev.security.owasp]] — FEEDS (weight: 0.7)
- [[dev.security.stride]] — FEEDS (weight: 0.7)
- [[dev.security.role]] — CO_CREATES (weight: 0.6)
- [[dev.security.owasp]] — CO_CREATES (weight: 0.6)
- [[dev.security.stride]] — CO_CREATES (weight: 0.6)
- [[dev.security.swiss-cheese]] — CO_CREATES (weight: 0.6)
- [[dev.security.saltzer]] — CO_CREATES (weight: 0.6)
- [[dev.security.secure-by-design]] — CO_CREATES (weight: 0.6)
- [[dev.security.defense-in-depth]] — CO_CREATES (weight: 0.6)
- [[dev.security.zero-trust]] — CO_CREATES (weight: 0.6)
- [[dev.security.verify]] — CO_CREATES (weight: 0.6)
