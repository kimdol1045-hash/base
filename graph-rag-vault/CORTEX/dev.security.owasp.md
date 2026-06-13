---
id: "dev.security.owasp"
domain: "development.security"
type: "pattern"
region: CORTEX
token_estimate: 500
theory: "#116 OWASP Top 10 (2021)"
tags: [security, owasp, top10, vulnerability, pattern]
---

# dev.security.owasp

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.security`  
> **Type**: `pattern`  
> **Theory**: #116 OWASP Top 10 (2021)  
> **Tokens**: 500

## Content

OWASP Top 10 (2021) -- 웹 애플리케이션 10대 보안 위협과 대응:

### A01: Broken Access Control (접근 제어 실패)
```typescript
// DON'T: IDOR -- 타인의 리소스 접근 가능
app.get("/orders/:id", async (c) => {
  return c.json(await db.select().from(orders).where(eq(orders.id, c.req.param("id"))));
});

// DO: 소유권 검증 필수
app.get("/orders/:id", authMiddleware, async (c) => {
  const order = await orderService.findById(c.req.param("id"));
  if (!order) throw Errors.notFound("주문");
  if (order.userId !== c.get("user").id) throw Errors.forbidden();
  return c.json({ data: order });
});
```
탐지: 다른 사용자의 리소스 ID로 요청 시 403 반환 여부 테스트.

### A02: Cryptographic Failures (암호화 실패)
```typescript
// DON'T: MD5/SHA1 해싱, 평문 전송
const hash = crypto.createHash("md5").update(password).digest("hex");

// DO: bcrypt/argon2id, TLS 강제
const hash = await bcrypt.hash(password, 12);
```
탐지: `grep -r "createHash.*md5\|createHash.*sha1\|password.*=.*body"` 코드 검색.

### A03: Injection (인젝션)
```typescript
// DON'T: SQL 문자열 연결
const query = `SELECT * FROM users WHERE name = '${name}'`;

// DO: Parameterized query
const user = await db.select().from(users).where(eq(users.name, name));
```
탐지: 템플릿 리터럴 안에 사용자 입력이 직접 삽입되는 패턴 검색.

### A04: Insecure Design (불안전한 설계)
- 위협 모델링(STRIDE)을 설계 단계에서 수행
- 비즈니스 로직 제한: 일일 이체 한도, 비밀번호 시도 횟수 제한(5회/15분)
- Abuse case를 user story와 함께 작성

### A05: Security Misconfiguration (보안 설정 오류)
```typescript
// DON'T: 디버그 모드 프로덕션 배포, 기본 계정 유지
app.use(cors({ origin: "*" })); // 모든 origin 허용

// DO: 명시적 설정
app.use(cors({ origin: ["https://myapp.com"], credentials: true }));
app.use(helmet()); // 보안 헤더 일괄 적용
```
탐지: `origin: "*"`, `debug: true`, 기본 포트/계정 사용 여부 점검.

### A06: Vulnerable Components (취약한 컴포넌트)
```bash
# DO: 정기 취약점 스캔
npm audit --audit-level=high
npx better-npm-audit audit
```
- `package-lock.json`에서 known vulnerability 있는 패키지 확인
- Dependabot 또는 Snyk 연동 필수

### A07: Auth Failures (인증 실패)
```typescript
// DO: 안전한 세션 관리
const token = jwt.sign(payload, secret, { expiresIn: "15m", algorithm: "HS256" });
// Refresh Token은 httpOnly + Secure + SameSite=Strict 쿠키에 저장
setCookie(c, "refresh_token", refreshToken, {
  httpOnly: true, secure: true, sameSite: "Strict", maxAge: 60 * 60 * 24 * 7,
});
```
- 비밀번호 최소 12자, brute-force 방어(rate limit 5회/15분)

### A08: Software & Data Integrity Failures (무결성 실패)
- CI/CD 파이프라인에서 의존성 해시 검증 (`npm ci` 사용)
- 서브리소스 무결성(SRI) 적용: `<script integrity="sha384-...">`

### A09: Logging & Monitoring Failures (로깅 실패)
```typescript
// DO: 보안 이벤트 구조화 로깅
logger.warn({ event: "AUTH_FAILURE", ip: req.ip, email: maskEmail(email), reason: "invalid_password" });
// DON'T: 민감 정보 로깅
logger.info({ event: "LOGIN", password: body.password }); // 비밀번호 로그 기록 금지
```

### A10: SSRF (서버 사이드 요청 위조)
```typescript
// DO: URL 허용 목록 기반 검증
const ALLOWED_HOSTS = ["api.example.com", "cdn.example.com"];
function validateUrl(url: string): boolean {
  const parsed = new URL(url);
  return ALLOWED_HOSTS.includes(parsed.hostname) && parsed.protocol === "https:";
}

// DON'T: 사용자 URL을 검증 없이 fetch
const response = await fetch(body.webhookUrl); // SSRF 취약
```

## Connections

### REQUIRES (1)

- ← [[dev.security.role]] `w=0.9`

### FEEDS (2)

- → [[dev.security.cia-triad]] `w=0.7`
- → [[dev.security.verify]] `w=0.8`

### CO_CREATES (9)

- → [[dev.security.cia-triad]] `w=0.6`
- → [[dev.security.defense-in-depth]] `w=0.6`
- ← [[dev.security.role]] `w=0.6`
- → [[dev.security.saltzer]] `w=0.6`
- → [[dev.security.secure-by-design]] `w=0.6`
- → [[dev.security.stride]] `w=0.6`
- → [[dev.security.swiss-cheese]] `w=0.6`
- → [[dev.security.verify]] `w=0.6`
- → [[dev.security.zero-trust]] `w=0.6`
