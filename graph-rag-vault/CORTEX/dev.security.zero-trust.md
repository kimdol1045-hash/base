---
id: "dev.security.zero-trust"
domain: "development.security"
type: "pattern"
region: CORTEX
token_estimate: 480
theory: "#118 제로 트러스트 (NIST SP 800-207)"
tags: [security, zero-trust, nist, authentication, pattern]
---

# dev.security.zero-trust

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.security`  
> **Type**: `pattern`  
> **Theory**: #118 제로 트러스트 (NIST SP 800-207)  
> **Tokens**: 480

## Content

제로 트러스트 아키텍처 -- "절대 신뢰하지 말고, 항상 검증하라" (NIST SP 800-207):

내부 네트워크라도 암묵적으로 신뢰하지 않는다. 모든 요청은 매번 인증/인가/검증을 거친다.

### 핵심 원칙
1. **모든 요청 인증** -- 네트워크 위치와 무관하게 매 요청 신원 확인
2. **최소 권한 접근** -- 필요한 최소한의 리소스에만 접근 허용
3. **마이크로 세그먼테이션** -- 서비스 간 통신도 개별 인증
4. **지속적 검증** -- 세션 유지 중에도 컨텍스트 변화 시 재검증
5. **위반 가정** -- 이미 침해되었다고 가정하고 설계

### 패턴 1: 모든 요청 인증 + 최소 권한
```typescript
// DO: 모든 내부 API 간 호출에도 서비스 토큰 필수
async function callPaymentService(orderId: string, serviceToken: string) {
  const response = await fetch(`${PAYMENT_SERVICE_URL}/process/${orderId}`, {
    headers: {
      "Authorization": `Bearer ${serviceToken}`,
      "X-Service-Name": "order-service",
      "X-Request-Id": crypto.randomUUID(),
    },
  });
  if (!response.ok) throw new Error(`Payment service error: ${response.status}`);
  return response.json();
}

// DON'T: 내부 서비스 간 인증 없이 직접 호출
const response = await fetch(`http://payment-service:3001/process/${orderId}`);
// 내부 네트워크니까 안전하다? -- 제로 트러스트 위반
```

### 패턴 2: 마이크로 세그먼테이션
```typescript
// DO: 서비스별 전용 API 키 + 접근 범위 제한
const SERVICE_PERMISSIONS: Record<string, string[]> = {
  "order-service":   ["payment:create", "payment:read"],
  "admin-service":   ["payment:create", "payment:read", "payment:refund"],
  "analytics-service": ["payment:read"], // 읽기만 가능
};

function authorizeService(serviceName: string, requiredPermission: string) {
  const perms = SERVICE_PERMISSIONS[serviceName];
  if (!perms?.includes(requiredPermission)) {
    throw Errors.forbidden(`Service ${serviceName} lacks ${requiredPermission}`);
  }
}
```

### 패턴 3: 지속적 검증 (Continuous Verification)
```typescript
// DO: 컨텍스트 변화 감지 시 재인증 요구
async function validateSession(c: Context): Promise<User> {
  const user = c.get("user");
  const session = await sessionStore.get(user.sessionId);

  // 비정상 컨텍스트 변화 감지
  const currentIp = c.req.header("x-forwarded-for");
  const currentUa = c.req.header("user-agent");

  if (session.ip !== currentIp || session.userAgent !== currentUa) {
    // IP 또는 User-Agent 변경 -> 세션 무효화 + 재인증 요구
    await sessionStore.delete(user.sessionId);
    throw Errors.authRequired("보안을 위해 다시 로그인해 주세요");
  }

  // 세션 유효기간 sliding window
  await sessionStore.extend(user.sessionId, SESSION_TTL);
  return user;
}
```

### 패턴 4: 위반 가정 (Assume Breach)
```typescript
// DO: 토큰 탈취에 대비한 단기 토큰 + 블랙리스트
const ACCESS_TOKEN_TTL = "15m";   // Access: 15분
const REFRESH_TOKEN_TTL = "7d";   // Refresh: 7일

// 로그아웃/비밀번호 변경 시 모든 세션 즉시 무효화
async function revokeAllSessions(userId: string) {
  await sessionStore.deleteByUser(userId);
  await tokenBlacklist.addPattern(`user:${userId}:*`);
}
```

### 구현 체크리스트
- [ ] 내부 서비스 간 통신에 mTLS 또는 서비스 토큰 적용
- [ ] Access Token 만료 15분 이하
- [ ] Refresh Token httpOnly + Secure + SameSite=Strict
- [ ] 비정상 접근 패턴 감지 시 세션 무효화
- [ ] 중요 작업(결제, 삭제)에 재인증 또는 MFA 요구
- [ ] 모든 서비스 간 요청에 X-Request-Id 전파 (추적용)

## Connections

### REQUIRES (1)

- ← [[dev.security.role]] `w=0.9`

### FEEDS (2)

- ← [[dev.security.defense-in-depth]] `w=0.7`
- → [[dev.security.verify]] `w=0.8`

### CO_CREATES (9)

- ← [[dev.security.cia-triad]] `w=0.6`
- ← [[dev.security.defense-in-depth]] `w=0.6`
- ← [[dev.security.owasp]] `w=0.6`
- ← [[dev.security.role]] `w=0.6`
- ← [[dev.security.saltzer]] `w=0.6`
- ← [[dev.security.secure-by-design]] `w=0.6`
- ← [[dev.security.stride]] `w=0.6`
- ← [[dev.security.swiss-cheese]] `w=0.6`
- → [[dev.security.verify]] `w=0.6`
