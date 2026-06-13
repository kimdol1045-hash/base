---
id: "dev.backend.api.auth"
domain: "development.backend"
type: "rule"
region: BRAINSTEM
token_estimate: 500
theory: "#115 Saltzer 최소권한, #116 OWASP A07"
tags: [backend, api, auth, jwt, security, rbac]
---

# dev.backend.api.auth

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `rule`  
> **Theory**: #115 Saltzer 최소권한, #116 OWASP A07  
> **Tokens**: 500

## Content

인증/인가 규칙 (모든 비공개 리소스 접근에는 신원 확인과 권한 검증이 필수다):

### JWT 인증 흐름
```typescript
// middleware/auth.ts
import { verify } from "hono/jwt";

export async function authMiddleware(c: Context, next: Next) {
  const header = c.req.header("Authorization");
  if (!header?.startsWith("Bearer ")) {
    return c.json({
      error: { code: "AUTH_REQUIRED", message: "인증 토큰이 필요합니다" }
    }, 401);
  }

  try {
    const token = header.slice(7);
    const payload = await verify(token, c.env.JWT_SECRET);
    c.set("userId", payload.sub);
    c.set("userRole", payload.role);
    await next();
  } catch {
    return c.json({
      error: { code: "AUTH_INVALID", message: "유효하지 않은 토큰입니다" }
    }, 401);
  }
}
```

### 토큰 설정 기준
| 항목 | 값 | 이유 |
|------|-----|------|
| Access Token 만료 | 15분 | 탈취 시 피해 최소화 |
| Refresh Token 만료 | 7일 | UX와 보안의 균형 |
| 저장 위치 (웹) | httpOnly Cookie | XSS로부터 보호 |
| Cookie 옵션 | `secure; sameSite=strict; path=/` | CSRF 방지 |

DON'T:
```typescript
// ❌ localStorage에 토큰 저장 (XSS 취약)
localStorage.setItem("token", jwt);

// ❌ 토큰 만료 검증 건너뛰기
const payload = jwt.decode(token); // decode만 하면 서명 검증 안 됨!

// ❌ 하드코딩된 시크릿
const secret = "my-super-secret-key";
```

### 역할 기반 인가 (RBAC)
```typescript
// middleware/authorize.ts
export function requireRole(...roles: string[]) {
  return async (c: Context, next: Next) => {
    const userRole = c.get("userRole");
    if (!roles.includes(userRole)) {
      return c.json({
        error: { code: "FORBIDDEN", message: "접근 권한이 없습니다" }
      }, 403);
    }
    await next();
  };
}

// 사용
app.delete("/users/:id", authMiddleware, requireRole("admin"), handler);
```

### 리소스 소유권 검증
```typescript
// 자신의 리소스만 수정 가능
app.patch("/posts/:id", authMiddleware, async (c) => {
  const userId = c.get("userId");
  const post = await db.query.posts.findFirst({
    where: eq(posts.id, c.req.param("id")),
  });

  if (!post) return c.json({ error: { code: "NOT_FOUND", message: "게시글을 찾을 수 없습니다" } }, 404);
  if (post.authorId !== userId) return c.json({ error: { code: "FORBIDDEN", message: "본인의 게시글만 수정 가능합니다" } }, 403);

  // ... 수정 로직
});
```

### 비밀번호 처리
- 해싱: bcrypt (cost 12+) 또는 argon2id
- 비밀번호 정책: 최소 8자, 최대 72자 (bcrypt 제한)
- 비교: `await bcrypt.compare(input, hash)` (타이밍 공격 방지 내장)
- 평문 전송/저장/로깅 절대 금지

### 공개 엔드포인트 명시
```typescript
// 공개 라우트는 명시적으로 분리
const publicRoutes = new Hono();
publicRoutes.post("/auth/login", loginHandler);    // PUBLIC
publicRoutes.post("/auth/register", registerHandler); // PUBLIC

// 인증 필요 라우트
const protectedRoutes = new Hono();
protectedRoutes.use("*", authMiddleware);
protectedRoutes.get("/me", getMeHandler);
```

### 흔한 실수
- 401(인증 실패)과 403(인가 실패) 혼동
- Refresh Token을 access token과 같은 곳에 저장
- 토큰 해독(decode)과 검증(verify)을 혼동
- 로그아웃 시 서버 측 토큰 무효화 미처리 (블랙리스트 필요)
