---
id: "dev.backend.api.security"
domain: "development.backend"
type: "rule"
region: BRAINSTEM
token_estimate: 500
theory: "#116 OWASP Top 10 (2021)"
tags: [backend, api, security, owasp, cors, rate-limiting]
---

# dev.backend.api.security

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `rule`  
> **Theory**: #116 OWASP Top 10 (2021)  
> **Tokens**: 500

## Content

API 보안 규칙 (보안은 기능이 아니라 품질 속성이다 -- 모든 코드에 내재해야 한다):

### 1. SQL Injection 방지
ORM/Query Builder의 parameterized query만 사용한다.

DO:
```typescript
// Drizzle ORM -- 자동 파라미터화
const user = await db.query.users.findFirst({
  where: eq(users.email, email),
});

// 부득이한 raw query
const result = await db.execute(
  sql`SELECT * FROM users WHERE id = ${userId}`  // 템플릿 리터럴 = 자동 파라미터화
);
```

DON'T:
```typescript
// ❌ 문자열 연결 -- SQL Injection 취약
const result = await db.execute(
  `SELECT * FROM users WHERE email = '${email}'`
);

// ❌ 동적 컬럼명도 위험
const result = await db.execute(
  `SELECT * FROM users ORDER BY ${sortColumn}`  // sortColumn 검증 없이 사용
);
```

### 2. XSS 방지
- 모든 응답에 `Content-Type: application/json` 명시
- HTML을 반환할 경우 반드시 이스케이핑
- CSP 헤더 설정: `Content-Security-Policy: default-src 'self'`

### 3. CORS 설정
```typescript
// DO: 명시적 origin 목록
app.use("*", cors({
  origin: ["https://myapp.com", "https://admin.myapp.com"],
  allowMethods: ["GET", "POST", "PATCH", "DELETE"],
  allowHeaders: ["Content-Type", "Authorization"],
  credentials: true,
  maxAge: 86400, // preflight 캐시 24시간
}));

// DON'T: 와일드카드 (개발 환경 외 금지)
app.use("*", cors({ origin: "*" }));  // ❌ credentials와 함께 사용 불가
```

### 4. Rate Limiting
| 엔드포인트 유형 | 제한 | 이유 |
|-----------------|------|------|
| 로그인/회원가입 | 분당 5회 (IP 기준) | 브루트포스 방지 |
| 비밀번호 재설정 | 시간당 3회 | 스팸 방지 |
| 일반 API (인증) | 분당 100회 (유저 기준) | 남용 방지 |
| 일반 API (비인증) | 분당 30회 (IP 기준) | 스크래핑 방지 |
| 파일 업로드 | 분당 5회 | 스토리지 남용 방지 |

```typescript
import { rateLimiter } from "hono-rate-limiter";

const loginLimiter = rateLimiter({
  windowMs: 60 * 1000,
  limit: 5,
  keyGenerator: (c) => c.req.header("x-forwarded-for") ?? "unknown",
  handler: (c) => c.json({
    error: { code: "RATE_LIMITED", message: "요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요." }
  }, 429),
});
```

### 5. 환경변수 관리
```typescript
// DO: Zod로 환경변수 검증 (서버 시작 시)
const EnvSchema = z.object({
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(32),
  REDIS_URL: z.string().url().optional(),
  NODE_ENV: z.enum(["development", "production", "test"]),
});
export const env = EnvSchema.parse(process.env);

// DON'T:
const secret = "hardcoded-secret";              // ❌ 하드코딩
const dbUrl = process.env.DATABASE_URL!;         // ❌ non-null assertion
const port = process.env.PORT as unknown as number; // ❌ 위험한 타입 캐스팅
```

### 6. 파일 업로드 보안
- MIME 타입 검증 (magic bytes 기반, 확장자만 믿지 말것)
- 크기 제한: 이미지 5MB, 문서 20MB, 동영상은 별도 처리
- 원본 파일명 사용 금지 -- UUID로 재명명
- 업로드 경로: 애플리케이션 디렉토리 외부 또는 클라우드 스토리지

### 7. 보안 헤더
```typescript
app.use("*", secureHeaders({
  xFrameOptions: "DENY",
  xContentTypeOptions: "nosniff",
  strictTransportSecurity: "max-age=31536000; includeSubDomains",
  referrerPolicy: "strict-origin-when-cross-origin",
}));
```

### 흔한 실수
- `.env` 파일을 git에 커밋 (`.gitignore` 필수 확인)
- CORS origin에 정규식 사용 시 `\.` 이스케이프 누락 -> 하위 도메인 위조 가능
- Rate limiter를 로드밸런서 뒤에서 IP 기반으로만 설정 -> 모든 요청이 같은 IP로 인식

## Connections

### CO_CREATES (3)

- ← [[dev.backend.api.file-upload]] `w=0.6`
- ← [[dev.backend.auth.jwt-auth]] `w=0.6`
- ← [[dev.backend.auth.password]] `w=0.6`
