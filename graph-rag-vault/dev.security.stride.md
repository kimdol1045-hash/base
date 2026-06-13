---
id: "dev.security.stride"
domain: "development.security"
type: "pattern"
bloom_level: ""
tags: ["security", "stride", "threat-modeling", "pattern"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.security.stride

> #117 STRIDE (Shostack, 2014)

STRIDE 위협 모델링 -- 체계적 위협 식별과 대응 (Adam Shostack, 2014):

모든 신규 기능/API 설계 시 STRIDE 6가지 위협 유형을 점검한다.
각 위협에 대해 "이 시스템에서 이 공격이 가능한가?" 질문을 던진다.

### S: Spoofing (위장)
공격자가 다른 사용자/시스템으로 위장한다.
**대응:**
```typescript
// DO: JWT 서명 검증 + 발급자 확인
const payload = jwt.verify(token, secret, {
  algorithms: ["HS256"],
  issuer: "myapp.com",       // 발급자 검증
  audience: "myapp-api",     // 대상 검증
});

// DON'T: 토큰 디코딩만 하고 서명 미검증
const payload = JSON.parse(atob(token.split(".")[1])); // 서명 검증 없음!
```
**탐지:** 만료된 토큰, 조작된 토큰으로 API 호출 시 401 반환 여부.

### T: Tampering (변조)
전송 중 또는 저장된 데이터를 무단 변경한다.
**대응:**
```typescript
// DO: 요청 무결성 검증 (Webhook 수신 시)
function verifyWebhookSignature(body: string, signature: string, secret: string): boolean {
  const expected = crypto.createHmac("sha256", secret).update(body).digest("hex");
  return crypto.timingsSafeEqual(Buffer.from(signature), Buffer.from(expected));
}

app.post("/webhook", async (c) => {
  const rawBody = await c.req.text();
  const signature = c.req.header("X-Signature-256") ?? "";
  if (!verifyWebhookSignature(rawBody, signature, WEBHOOK_SECRET)) {
    throw Errors.forbidden("서명 검증 실패");
  }
  // 안전하게 처리
});
```
**탐지:** 변조된 payload로 요청 시 거부 여부.

### R: Repudiation (부인)
사용자가 수행한 행위를 부인한다 ("나는 그 작업을 하지 않았다").
**대응:**
```typescript
// DO: 변경 불가 감사 로그 + 타임스탬프
const auditEntry = {
  actor: user.id,
  action: "DELETE_USER",
  target: targetUserId,
  ip: c.req.header("x-forwarded-for"),
  userAgent: c.req.header("user-agent"),
  timestamp: new Date().toISOString(),
};
await auditLogService.append(auditEntry); // append-only 스토리지
```
**핵심:** 로그는 별도 권한으로 보호, 삭제/수정 불가 정책.

### I: Information Disclosure (정보 노출)
민감 정보가 비인가 주체에게 노출된다.
**대응:**
```typescript
// DO: 에러 응답에서 내부 정보 제거
app.onError((err, c) => {
  console.error("[ERROR]", err); // 서버 로그에만 상세 기록
  return c.json({ error: { code: "INTERNAL", message: "서버 오류" } }, 500);
  // DON'T: c.json({ error: err.message, stack: err.stack })
});
```
**탐지:** 5xx 응답 body에 스택 트레이스, DB 쿼리, 파일 경로 포함 여부.

### D: Denial of Service (서비스 거부)
정상 사용자의 서비스 접근을 방해한다.
**대응:**
- Rate Limiting: IP별 100 req/min, 인증 엔드포인트 5 req/min
- 요청 크기 제한: body 1MB, 파일 업로드 10MB
- 쿼리 복잡도 제한: GraphQL depth limit 5, pagination max 100
- 타임아웃: DB 쿼리 30초, API 응답 60초

### E: Elevation of Privilege (권한 상승)
일반 사용자가 관리자 권한을 획득한다.
**대응:**
```typescript
// DO: 서버 측 역할 검증 (클라이언트 전송 역할 무시)
app.post("/admin/users", authMiddleware, async (c) => {
  const user = c.get("user"); // DB에서 조회한 서버 측 역할
  if (user.role !== "admin") throw Errors.forbidden();
  // DON'T: body에서 role을 받아 신뢰
  // const { role } = await c.req.json(); if (role === "admin") ...
});
```
**탐지:** 일반 사용자 토큰으로 관리자 API 호출 시 403 반환 여부.

### STRIDE 위협 분석 템플릿
| 위협 유형 | 해당 여부 | 공격 시나리오 | 대응 수단 | 잔여 리스크 |
|----------|----------|-------------|----------|-----------|
| Spoofing | Y/N | ... | ... | ... |
| Tampering | Y/N | ... | ... | ... |
| Repudiation | Y/N | ... | ... | ... |
| Info Disclosure | Y/N | ... | ... | ... |
| DoS | Y/N | ... | ... | ... |
| EoP | Y/N | ... | ... | ... |

## Connections

- [[dev.security.role]] — REQUIRES (weight: 0.9)
- [[dev.security.verify]] — FEEDS (weight: 0.8)
- [[dev.security.cia-triad]] — FEEDS (weight: 0.7)
- [[dev.security.nist-framework]] — FEEDS (weight: 0.7)
- [[dev.security.role]] — CO_CREATES (weight: 0.6)
- [[dev.security.owasp]] — CO_CREATES (weight: 0.6)
- [[dev.security.cia-triad]] — CO_CREATES (weight: 0.6)
- [[dev.security.swiss-cheese]] — CO_CREATES (weight: 0.6)
- [[dev.security.saltzer]] — CO_CREATES (weight: 0.6)
- [[dev.security.secure-by-design]] — CO_CREATES (weight: 0.6)
- [[dev.security.defense-in-depth]] — CO_CREATES (weight: 0.6)
- [[dev.security.zero-trust]] — CO_CREATES (weight: 0.6)
- [[dev.security.verify]] — CO_CREATES (weight: 0.6)
