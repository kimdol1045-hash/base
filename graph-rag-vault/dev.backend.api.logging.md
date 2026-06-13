---
id: "dev.backend.api.logging"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "api", "logging", "observability", "security"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.api.logging

> #130 Observability (Sridharan, 2018)

구조화 로깅과 관측성 패턴 (문제가 발생했을 때 원인을 추적할 수 없다면, 로깅이 없는 것과 같다):

### 로그 레벨 기준
| 레벨 | 사용 시점 | 프로덕션 기본 출력 | 예시 |
|------|-----------|-------------------|------|
| `error` | 즉시 조치가 필요한 오류 | O | DB 연결 실패, 결제 처리 실패 |
| `warn` | 잠재적 문제, 당장은 아님 | O | Rate limit 근접, deprecated API 호출 |
| `info` | 정상 비즈니스 이벤트 | O | 사용자 가입, 주문 생성, 배포 완료 |
| `debug` | 개발/디버깅용 상세 정보 | X | SQL 쿼리, 캐시 hit/miss, 함수 인자 |

### 구조화 로깅 (Structured Logging)
JSON 형태로 로그를 남겨 검색과 분석을 용이하게 한다.

DO:
```typescript
// 구조화된 로그 -- 파싱/검색 가능
const logger = {
  info: (message: string, context: Record<string, unknown> = {}) => {
    console.log(JSON.stringify({
      level: "info",
      message,
      timestamp: new Date().toISOString(),
      ...context,
    }));
  },
  error: (message: string, error: unknown, context: Record<string, unknown> = {}) => {
    console.error(JSON.stringify({
      level: "error",
      message,
      timestamp: new Date().toISOString(),
      error: error instanceof Error ? {
        name: error.name,
        message: error.message,
        stack: error.stack,
      } : String(error),
      ...context,
    }));
  },
};

// 사용
logger.info("사용자 생성 완료", { userId: user.id, email: user.email });
logger.error("결제 처리 실패", err, { orderId, amount });
```

DON'T:
```typescript
// ❌ 비구조화 로그 -- 검색/분석 불가능
console.log("User created: " + user.id);
console.log(`Error: ${err}`);

// ❌ 객체를 그대로 출력 -- 형식이 일관되지 않음
console.log("user:", user);  // [object Object]가 출력될 수 있음
```

### 요청 로깅 미들웨어
```typescript
async function requestLogger(c: Context, next: Next) {
  const requestId = c.get("requestId") ?? crypto.randomUUID();
  const start = performance.now();

  logger.info("요청 수신", {
    requestId,
    method: c.req.method,
    path: c.req.path,
    userAgent: c.req.header("User-Agent"),
    ip: c.req.header("x-forwarded-for"),
  });

  await next();

  const duration = Math.round(performance.now() - start);
  const status = c.res.status;

  const logFn = status >= 500 ? logger.error : logger.info;
  logFn("요청 완료", null as any, {
    requestId,
    method: c.req.method,
    path: c.req.path,
    status,
    duration,
  });
}
```

### 민감 정보 마스킹
로그에 절대 평문으로 남기면 안 되는 데이터를 마스킹한다.

```typescript
const SENSITIVE_FIELDS = new Set([
  "password", "token", "secret", "authorization",
  "creditCard", "ssn", "accessToken", "refreshToken",
]);

function maskSensitive(obj: Record<string, unknown>): Record<string, unknown> {
  const masked: Record<string, unknown> = {};
  for (const [key, value] of Object.entries(obj)) {
    if (SENSITIVE_FIELDS.has(key.toLowerCase())) {
      masked[key] = "***MASKED***";
    } else if (typeof value === "object" && value !== null) {
      masked[key] = maskSensitive(value as Record<string, unknown>);
    } else {
      masked[key] = value;
    }
  }
  return masked;
}

// 사용
logger.info("로그인 시도", maskSensitive({ email, password, ip }));
// 출력: { email: "user@test.com", password: "***MASKED***", ip: "1.2.3.4" }
```

### Request ID를 통한 추적
하나의 요청이 여러 서비스/함수를 거칠 때 Request ID로 전체 흐름을 추적한다.

```typescript
// 미들웨어에서 Request ID 설정
app.use("*", async (c, next) => {
  const requestId = c.req.header("X-Request-Id") ?? crypto.randomUUID();
  c.set("requestId", requestId);
  c.header("X-Request-Id", requestId);
  await next();
});

// 서비스 레이어에서도 requestId를 전달
async function createOrder(input: CreateOrderInput, requestId: string) {
  logger.info("주문 생성 시작", { requestId, userId: input.userId });
  // ... 로직
  logger.info("주문 생성 완료", { requestId, orderId: order.id });
}
```

### 흔한 실수
- 비밀번호, JWT 토큰을 로그에 평문으로 남김
- `console.log(err)` -- Error 객체는 JSON.stringify하면 빈 객체 `{}`가 됨
- 로그 레벨 없이 모두 `console.log` 사용 -> 프로덕션에서 노이즈 과다
- 요청 ID 없이 로깅 -> 동시 요청 시 어떤 요청의 로그인지 구분 불가
- 과도한 debug 로그를 프로덕션에서 켜놓음 -> 성능 저하 + 스토리지 낭비
