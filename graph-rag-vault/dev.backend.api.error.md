---
id: "dev.backend.api.error"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "api", "error-handling", "pattern"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.api.error

> #72 방어적 프로그래밍 (Defensive Programming)

에러 핸들링 패턴 (에러는 숨기는 것이 아니라 제어하는 것이다):

### 커스텀 에러 클래스 정의
비즈니스 로직에서 발생하는 에러를 HTTP 에러와 분리한다.

```typescript
// errors/app-error.ts
export class AppError extends Error {
  constructor(
    public readonly code: string,
    public readonly statusCode: number,
    message: string,
    public readonly details?: unknown,
  ) {
    super(message);
    this.name = "AppError";
  }
}

// 자주 쓰는 에러 팩토리
export const Errors = {
  notFound: (resource: string) =>
    new AppError("NOT_FOUND", 404, `${resource}을(를) 찾을 수 없습니다`),
  conflict: (message: string) =>
    new AppError("CONFLICT", 409, message),
  forbidden: (message = "접근 권한이 없습니다") =>
    new AppError("FORBIDDEN", 403, message),
  validation: (details: unknown) =>
    new AppError("VALIDATION_ERROR", 422, "입력값 검증에 실패했습니다", details),
} as const;
```

### 글로벌 에러 핸들러
```typescript
// middleware/error-handler.ts (Hono)
app.onError((err, c) => {
  // Zod 검증 에러
  if (err instanceof ZodError) {
    return c.json({
      error: {
        code: "VALIDATION_ERROR",
        message: "입력값 검증에 실패했습니다",
        details: err.issues.map((i) => ({
          field: i.path.join("."),
          message: i.message,
        })),
      },
    }, 422);
  }

  // 비즈니스 에러
  if (err instanceof AppError) {
    return c.json({
      error: { code: err.code, message: err.message, details: err.details },
    }, err.statusCode);
  }

  // 예상치 못한 에러 -- 내부 정보 노출 금지
  console.error("[UNHANDLED]", err);
  return c.json({
    error: { code: "INTERNAL", message: "서버 오류가 발생했습니다" },
  }, 500);
});
```

### 핸들러에서의 사용
DO:
```typescript
app.get("/users/:id", async (c) => {
  const { id } = IdParamSchema.parse(c.req.param());
  const user = await userService.findById(id);
  if (!user) throw Errors.notFound("사용자");
  return c.json({ data: user });
});
```

DON'T:
```typescript
// ❌ 모든 핸들러에 try-catch 중복
app.get("/users/:id", async (c) => {
  try {
    const user = await getUser(id);
    return c.json(user);
  } catch (e) {
    return c.json({ error: e.message }, 500); // 내부 에러 메시지 노출!
  }
});

// ❌ 에러 삼키기
try { await riskyOperation(); } catch {} // 빈 catch = 디버깅 지옥

// ❌ 일관성 없는 에러 형식
return c.json({ msg: "not found" }, 404);      // msg? error? message?
return c.json({ error: "not found" }, 404);     // string? object?
```

### 에러 코드 표준
| 코드 | HTTP | 설명 |
|------|------|------|
| AUTH_REQUIRED | 401 | 인증 토큰 없음/만료 |
| AUTH_INVALID | 401 | 토큰 서명 검증 실패 |
| FORBIDDEN | 403 | 권한 부족 |
| NOT_FOUND | 404 | 리소스 없음 |
| VALIDATION_ERROR | 422 | 입력 검증 실패 |
| CONFLICT | 409 | 중복/충돌 |
| RATE_LIMITED | 429 | 요청 한도 초과 |
| INTERNAL | 500 | 예상치 못한 서버 오류 |

### 비동기 에러 처리
```typescript
// 프로세스 레벨 안전장치 (서버 시작 시)
process.on("unhandledRejection", (reason) => {
  console.error("[UnhandledRejection]", reason);
  // 프로덕션에서는 graceful shutdown 고려
});
```

### 흔한 실수
- 스택 트레이스를 클라이언트에 노출: `c.json({ error: err.stack })` -- 절대 금지
- 404와 403 혼동: 존재하지만 권한 없을 때 404를 반환하는 것이 보안상 나을 수 있음 (정보 유출 방지)
- Zod 에러를 그대로 던지면 글로벌 핸들러에서 잡히지만, `safeParse` 사용 시 수동 처리 필요

## Connections

- [[dev.backend.api.role]] — REQUIRES (weight: 0.9)
- [[dev.backend.api.verify]] — FEEDS (weight: 0.8)
- [[dev.backend.api.validation]] — FEEDS (weight: 0.7)
- [[dev.backend.api.middleware]] — FEEDS (weight: 0.7)
- [[dev.backend.api.caching]] — FEEDS (weight: 0.7)
- [[dev.frontend.component.error-boundary]] — FEEDS (weight: 0.5)
