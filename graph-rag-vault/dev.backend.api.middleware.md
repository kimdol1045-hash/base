---
id: "dev.backend.api.middleware"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "api", "middleware", "pattern", "hono", "express"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.api.middleware

> #103 Chain of Responsibility (GoF, 1994)

미들웨어/파이프라인 패턴 (횡단 관심사를 비즈니스 로직에서 분리하여 재사용성과 가독성을 높인다):

### 미들웨어란?
요청(Request)과 응답(Response) 사이에서 실행되는 함수 체인이다.
각 미들웨어는 요청을 가로채어 처리하거나, 다음 미들웨어로 넘긴다.
GoF의 Chain of Responsibility 패턴을 HTTP 서버에 적용한 것이다.

### 미들웨어 실행 순서 (순서가 핵심이다)
```
요청 → [CORS] → [보안헤더] → [Rate Limit] → [로깅] → [인증] → [인가] → [핸들러]
                                                                          ↓
응답 ← [에러핸들러] ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← ← [결과]
```

### Hono 미들웨어 등록
```typescript
import { Hono } from "hono";
import { cors } from "hono/cors";
import { secureHeaders } from "hono/secure-headers";
import { logger } from "hono/logger";

const app = new Hono();

// 1. 보안 헤더 (가장 먼저 -- 모든 응답에 적용)
app.use("*", secureHeaders());

// 2. CORS (preflight 요청을 가장 빨리 처리)
app.use("*", cors({
  origin: ["https://myapp.com"],
  credentials: true,
}));

// 3. 요청 로깅
app.use("*", logger());

// 4. Rate limiting (인증 전에 -- 비인증 요청도 제한)
app.use("/api/auth/*", loginRateLimiter);

// 5. 인증 (보호 라우트에만 적용)
app.use("/api/v1/*", authMiddleware);

// 6. 라우트 핸들러
app.get("/api/v1/users", listUsersHandler);

// 7. 에러 핸들러 (가장 마지막 -- 모든 에러를 잡음)
app.onError(globalErrorHandler);

// 8. 404 핸들러
app.notFound((c) => c.json({
  error: { code: "NOT_FOUND", message: "요청한 리소스를 찾을 수 없습니다" }
}, 404));
```

### 커스텀 미들웨어 작성
DO:
```typescript
// 요청 처리 시간 측정 미들웨어
async function timing(c: Context, next: Next) {
  const start = performance.now();
  await next();  // 반드시 await -- 다음 미들웨어 실행
  const ms = Math.round(performance.now() - start);
  c.header("X-Response-Time", `${ms}ms`);
}

// 요청 ID 부여 미들웨어 (로그 추적용)
async function requestId(c: Context, next: Next) {
  const id = c.req.header("X-Request-Id") ?? crypto.randomUUID();
  c.set("requestId", id);
  c.header("X-Request-Id", id);
  await next();
}
```

DON'T:
```typescript
// ❌ next()를 await하지 않음 -- 응답 헤더 설정이 안 됨
function badMiddleware(c: Context, next: Next) {
  next();  // await 누락!
  c.header("X-Custom", "value");  // next 완료 전에 실행됨
}

// ❌ 미들웨어에서 비즈니스 로직 처리
app.use("*", async (c, next) => {
  const user = await db.query.users.findFirst({ ... });  // DB 호출은 핸들러에서!
  await next();
});

// ❌ 에러 핸들러를 라우트 핸들러보다 먼저 등록
app.onError(errorHandler);  // 이 위치에선 라우트 에러를 잡지 못함
app.get("/users", handler);
```

### 라우트 그룹별 미들웨어
```typescript
// 공개 라우트 그룹
const publicApi = new Hono();
publicApi.post("/auth/login", loginHandler);
publicApi.post("/auth/register", registerHandler);

// 인증 필수 라우트 그룹
const protectedApi = new Hono();
protectedApi.use("*", authMiddleware);
protectedApi.get("/users", listUsersHandler);
protectedApi.get("/users/:id", getUserHandler);

// 관리자 전용 라우트 그룹
const adminApi = new Hono();
adminApi.use("*", authMiddleware);
adminApi.use("*", requireRole("admin"));
adminApi.delete("/users/:id", deleteUserHandler);

// 조합
app.route("/api/v1", publicApi);
app.route("/api/v1", protectedApi);
app.route("/api/v1/admin", adminApi);
```

### Express 에러 미들웨어 (참고)
Express에서는 에러 미들웨어의 시그니처가 다르다 (4개 파라미터).
```typescript
// Express 에러 미들웨어 -- 반드시 4개 파라미터
app.use((err: Error, req: Request, res: Response, next: NextFunction) => {
  // 에러 처리
});
```

### 흔한 실수
- 미들웨어 등록 순서 실수: CORS를 인증 뒤에 놓으면 preflight 요청이 401 반환
- `next()` 호출 누락: 요청이 멈추고 timeout 발생
- 에러 미들웨어를 라우트 정의 전에 등록: 에러를 잡지 못함
- 모든 라우트에 인증 미들웨어 적용 후 공개 라우트 예외 처리 누락
- 미들웨어에서 response body를 읽으면 스트림이 소진되어 후속 처리 불가

## Connections

- [[dev.backend.api.role]] — REQUIRES (weight: 0.9)
- [[dev.backend.api.verify]] — FEEDS (weight: 0.8)
- [[dev.backend.api.error]] — FEEDS (weight: 0.7)
- [[dev.backend.api.auth]] — CO_CREATES (weight: 0.6)
- [[dev.backend.auth.rbac]] — CO_CREATES (weight: 0.6)
