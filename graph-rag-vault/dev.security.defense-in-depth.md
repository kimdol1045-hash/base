---
id: "dev.security.defense-in-depth"
domain: "development.security"
type: "pattern"
bloom_level: ""
tags: ["security", "defense-in-depth", "layered-security", "network", "pattern"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.security.defense-in-depth

> #119 심층 방어 (Defense in Depth)

심층 방어 -- 네트워크부터 데이터까지 4개 레이어 보안 (Defense in Depth):

단일 방어선이 뚫려도 다음 레이어가 공격을 차단한다.
각 레이어는 독립적으로 작동하며, 이전 레이어의 성공을 가정하지 않는다.

### Layer 1: 네트워크 레이어
공격 트래픽이 서버에 도달하기 전에 차단한다.

**방어 수단:**
- WAF(Web Application Firewall): SQL Injection, XSS 패턴 차단
- DDoS 방어: Cloudflare/AWS Shield (L3/L4 공격 완화)
- IP 허용/차단 목록: 관리자 API는 사무실 IP만 허용
- TLS 1.3 강제: 모든 통신 암호화

```typescript
// DO: 보안 헤더 설정 (Helmet.js 또는 직접 설정)
app.use(async (c, next) => {
  await next();
  c.header("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
  c.header("X-Content-Type-Options", "nosniff");
  c.header("X-Frame-Options", "DENY");
  c.header("Content-Security-Policy", "default-src 'self'; script-src 'self'");
  c.header("Referrer-Policy", "strict-origin-when-cross-origin");
  c.header("Permissions-Policy", "camera=(), microphone=(), geolocation=()");
});
```

### Layer 2: 호스트 레이어
서버/컨테이너 자체의 보안을 강화한다.

**방어 수단:**
- 컨테이너: non-root 사용자, 읽기 전용 파일시스템
- 의존성: `npm audit` 주기적 실행, Snyk/Dependabot 연동
- 환경변수: 시크릿은 Vault/AWS Secrets Manager에 저장
- 프로세스 격리: 컨테이너별 리소스 제한 (CPU 1코어, RAM 512MB)

```dockerfile
# DO: 보안 강화된 Dockerfile
FROM node:20-alpine AS runner
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
COPY --chown=appuser:appgroup ./dist ./dist
EXPOSE 3000
CMD ["node", "dist/index.js"]

# DON'T: root 실행, 전체 소스 포함
FROM node:20
COPY . .
CMD ["npm", "start"]
```

### Layer 3: 애플리케이션 레이어
비즈니스 로직 수준의 보안 제어를 적용한다.

**방어 수단:**
- 입력 검증: Zod 스키마 (허용 목록 기반)
- 인증/인가: JWT + RBAC/ABAC
- Rate Limiting: IP 및 사용자별 제한
- CSRF 방어: SameSite 쿠키 + CSRF 토큰
- 세션 관리: 단기 토큰(15분) + Refresh rotation

```typescript
// DO: 다중 보안 미들웨어 체인
app.use("*", securityHeaders);          // L1 보안 헤더
app.use("*", rateLimiter({ limit: 100 })); // L3 Rate limit
app.use("/api/*", authMiddleware);       // L3 인증
app.use("/api/*", csrfProtection);       // L3 CSRF

// DON'T: 단일 미들웨어에 의존
app.use("/api/*", authMiddleware);       // 인증만 있고 나머지 없음
```

### Layer 4: 데이터 레이어
데이터 자체를 보호하여 DB 유출 시에도 피해를 최소화한다.

**방어 수단:**
- 저장 시 암호화(Encryption at Rest): 민감 컬럼 AES-256-GCM
- 필드 레벨 암호화: PII(이메일, 전화번호) 개별 암호화
- 백업 암호화: 백업 파일도 암호화 필수
- 접근 감사: DB 쿼리 로그 + 이상 접근 탐지

```typescript
// DO: 민감 필드 암호화 저장
await db.insert(users).values({
  email: encrypt(body.email, ENCRYPTION_KEY),     // 암호화 저장
  passwordHash: await bcrypt.hash(body.password, 12), // 해싱
  phone: encrypt(body.phone, ENCRYPTION_KEY),     // 암호화 저장
});

// DON'T: 민감 정보 평문 저장
await db.insert(users).values({
  email: body.email,       // 평문
  password: body.password, // 평문 비밀번호!
});
```

### 레이어별 체크리스트
| 레이어 | 필수 항목 | 확인 |
|--------|---------|------|
| 네트워크 | TLS 1.3 + 보안 헤더 + CORS strict | [ ] |
| 호스트 | non-root 컨테이너 + 의존성 스캔 | [ ] |
| 애플리케이션 | 입력검증 + 인증 + Rate limit | [ ] |
| 데이터 | 민감필드 암호화 + 백업 암호화 | [ ] |

## Connections

- [[dev.security.role]] — REQUIRES (weight: 0.9)
- [[dev.security.verify]] — FEEDS (weight: 0.8)
- [[dev.security.nist-framework]] — FEEDS (weight: 0.7)
- [[dev.security.zero-trust]] — FEEDS (weight: 0.7)
- [[dev.security.role]] — CO_CREATES (weight: 0.6)
- [[dev.security.owasp]] — CO_CREATES (weight: 0.6)
- [[dev.security.cia-triad]] — CO_CREATES (weight: 0.6)
- [[dev.security.stride]] — CO_CREATES (weight: 0.6)
- [[dev.security.swiss-cheese]] — CO_CREATES (weight: 0.6)
- [[dev.security.saltzer]] — CO_CREATES (weight: 0.6)
- [[dev.security.secure-by-design]] — CO_CREATES (weight: 0.6)
- [[dev.security.zero-trust]] — CO_CREATES (weight: 0.6)
- [[dev.security.verify]] — CO_CREATES (weight: 0.6)
