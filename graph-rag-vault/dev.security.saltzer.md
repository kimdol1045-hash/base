---
id: "dev.security.saltzer"
domain: "development.security"
type: "pattern"
bloom_level: ""
tags: ["security", "saltzer-schroeder", "design-principles", "least-privilege", "pattern"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.security.saltzer

> #115 Saltzer-Schroeder 8원칙 (1975)

보안 설계의 근본 원칙 (Saltzer & Schroeder, 1975):

50년이 지난 지금도 유효한 보안 설계의 8대 원칙. 모든 보안 아키텍처 결정은 이 원칙으로 검증한다.

### 1. 최소 권한 (Least Privilege)
모든 주체는 작업 수행에 필요한 최소한의 권한만 가진다.
```typescript
// DO: 역할별 최소 권한 정의
const PERMISSIONS = {
  viewer: ["read:posts"],
  editor: ["read:posts", "write:posts"],
  admin:  ["read:posts", "write:posts", "delete:posts", "manage:users"],
} as const;

function authorize(user: User, required: Permission) {
  const userPerms = PERMISSIONS[user.role];
  if (!userPerms.includes(required)) throw Errors.forbidden();
}

// DON'T: 모든 사용자에게 admin 권한
if (user.isLoggedIn) { /* 전체 기능 허용 */ }
```

### 2. 실패 안전 기본값 (Fail-Safe Defaults)
기본 상태는 "거부"이며, 명시적으로 허용된 경우만 접근을 승인한다.
```typescript
// DO: 기본 거부, 명시적 허용
function hasAccess(user: User, resource: Resource): boolean {
  if (!user.permissions) return false; // 기본: 거부
  return user.permissions.includes(resource.requiredPermission);
}

// DON'T: 기본 허용, 명시적 거부
function hasAccess(user: User): boolean {
  if (user.isBanned) return false;
  return true; // 기본: 허용 = 위험
}
```

### 3. 완전 중재 (Complete Mediation)
모든 접근 요청은 매번 권한을 검증한다. 캐시된 인가 결과를 신뢰하지 않는다.
```typescript
// DO: 매 요청마다 권한 확인
app.use("*", async (c, next) => {
  const token = c.req.header("Authorization")?.replace("Bearer ", "");
  if (!token) throw Errors.authRequired();
  const payload = await verifyJWT(token); // 매번 서명 검증 + 만료 확인
  const user = await userService.findById(payload.sub); // 최신 권한 조회
  if (user.status === "suspended") throw Errors.forbidden("계정 정지됨");
  c.set("user", user);
  await next();
});
```

### 4. 개방 설계 (Open Design)
보안은 알고리즘의 비밀이 아닌 키의 비밀에 의존한다 (Kerckhoffs' Principle).
```typescript
// DO: 표준 알고리즘 + 안전한 키
import bcrypt from "bcrypt";
const hash = await bcrypt.hash(password, 12); // 검증된 알고리즘, cost=12

// DON'T: 자작 암호화
function myEncrypt(text: string): string {
  return text.split("").reverse().join(""); // 보안 아님
}
```

### 5. 권한 분리 (Separation of Privilege)
중요 작업은 단일 조건이 아닌 복수 조건으로 승인한다.
```typescript
// DO: 관리자 작업에 2단계 인증 필수
app.delete("/users/:id", authMiddleware, async (c) => {
  const admin = c.get("user");
  if (admin.role !== "admin") throw Errors.forbidden();
  const mfaCode = c.req.header("X-MFA-Code");
  if (!mfaCode || !(await verifyMFA(admin.id, mfaCode))) {
    throw Errors.authRequired("MFA 인증이 필요합니다");
  }
  await userService.delete(c.req.param("id"));
  return c.json({ success: true });
});
```

### 6. 최소 공통 메커니즘 (Least Common Mechanism)
사용자 간 공유 자원을 최소화하여 한 사용자의 침해가 다른 사용자에게 전파되지 않도록 한다.
- 테넌트별 DB 스키마 분리 또는 Row-Level Security 적용
- 공유 캐시에 테넌트 ID prefix 적용: `cache:${tenantId}:${key}`

### 7. 심리적 수용성 (Psychological Acceptability)
보안 메커니즘은 사용자 경험을 심각하게 방해하지 않아야 한다.
- 비밀번호 규칙: 최소 12자 + 강도 미터(실시간 피드백)
- MFA: TOTP 앱 기반 (SMS보다 안전하고 편리)
- 세션: 7일 유지 + sliding window refresh

### 8. 경제적 메커니즘 (Economy of Mechanism)
보안 코드는 가능한 단순하게 유지한다. 복잡한 코드는 감사가 어렵고 취약점이 숨기 쉽다.
- 인증 로직은 하나의 미들웨어로 통일
- 인가 로직은 하나의 정책 엔진으로 중앙화
- 커스텀 보안 코드보다 검증된 라이브러리 우선 사용

## Connections

- [[dev.security.role]] — CO_CREATES (weight: 0.6)
- [[dev.security.owasp]] — CO_CREATES (weight: 0.6)
- [[dev.security.cia-triad]] — CO_CREATES (weight: 0.6)
- [[dev.security.stride]] — CO_CREATES (weight: 0.6)
- [[dev.security.swiss-cheese]] — CO_CREATES (weight: 0.6)
- [[dev.security.secure-by-design]] — CO_CREATES (weight: 0.6)
- [[dev.security.defense-in-depth]] — CO_CREATES (weight: 0.6)
- [[dev.security.zero-trust]] — CO_CREATES (weight: 0.6)
- [[dev.security.verify]] — CO_CREATES (weight: 0.6)
