---
id: "dev.backend.api.validation"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#72 SOLID.D -- 방어적 프로그래밍"
tags: [backend, api, validation, zod, security]
---

# dev.backend.api.validation

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #72 SOLID.D -- 방어적 프로그래밍  
> **Tokens**: 500

## Content

입력 검증 패턴 (모든 외부 입력은 신뢰하지 않는다 -- 클라이언트는 항상 거짓말할 수 있다):

### Zod 스키마 우선 원칙
모든 API 엔드포인트의 request body, query params, path params를 Zod로 검증한다.

DO:
```typescript
// schemas/user.ts
export const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).trim(),
  age: z.number().int().min(0).max(150).optional(),
  role: z.enum(["user", "admin"]).default("user"),
});
export type CreateUserInput = z.infer<typeof CreateUserSchema>;

// routes/users.ts
app.post("/users", async (c) => {
  const body = CreateUserSchema.parse(await c.req.json());
  // body는 이제 타입 안전
});
```

DON'T:
```typescript
// ❌ 수동 검증 -- 누락 가능성 높음
app.post("/users", async (c) => {
  const body = await c.req.json();
  if (!body.email || !body.email.includes("@")) {
    return c.json({ error: "Invalid email" }, 400);
  }
  // name 검증 깜빡함... 보안 구멍
});

// ❌ any 타입으로 DB에 직접 전달
const data = req.body as any;
await db.insert(users).values(data);
```

### Query Params 검증
```typescript
const ListQuerySchema = z.object({
  cursor: z.string().uuid().optional(),
  limit: z.coerce.number().int().min(1).max(100).default(20),
  sort: z.enum(["created_at", "updated_at"]).default("created_at"),
  order: z.enum(["asc", "desc"]).default("desc"),
});

app.get("/users", async (c) => {
  const query = ListQuerySchema.parse(c.req.query());
});
```

### Path Params 검증
```typescript
const IdParamSchema = z.object({
  id: z.string().uuid("유효한 UUID 형식이 아닙니다"),
});

app.get("/users/:id", async (c) => {
  const { id } = IdParamSchema.parse(c.req.param());
});
```

### 검증 실패 응답 표준
```typescript
// Zod 에러를 일관된 형식으로 변환
function formatZodError(error: ZodError) {
  return {
    error: {
      code: "VALIDATION_ERROR",
      message: "입력값 검증에 실패했습니다",
      details: error.issues.map((i) => ({
        field: i.path.join("."),
        message: i.message,
      })),
    },
  };
}
```

### 검증 위치
- Controller 진입 직후 (미들웨어 또는 핸들러 첫 줄)
- DB 저장 직전 이중 검증은 불필요 (Zod 통과 = 타입 안전)
- 단, 비즈니스 규칙 검증(중복 체크 등)은 서비스 레이어에서 수행

### 흔한 실수
- `.optional()`과 `.nullable()` 혼동: optional은 필드 생략 가능, nullable은 null 값 허용
- 배열 입력 시 `.array().max(100)`으로 크기 제한 누락 -> DoS 가능
- `.coerce.number()`를 안 쓰고 query param이 string으로 들어와서 타입 에러
- 파일 업로드 시 mimetype/크기 검증 누락
- `.transform()`으로 데이터 변환 시 원본 타입과 변환 타입 혼동

## Connections

### REQUIRES (1)

- ← [[dev.backend.api.role]] `w=0.9`

### FEEDS (4)

- → [[dev.backend.api.error]] `w=0.7`
- ← [[dev.backend.api.rest]] `w=0.7`
- → [[dev.backend.api.verify]] `w=0.8`
- ← [[dev.frontend.component.form]] `w=0.5`

### CO_CREATES (1)

- ← [[dev.backend.api.rest]] `w=0.6`
