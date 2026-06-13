---
id: "dev.security.owasp-api"
domain: "development.security"
type: "rule"
bloom_level: ""
tags: ["security", "owasp", "api-security", "top-10"]
brain_region: "CORTEX"
token_estimate: 450
---

# dev.security.owasp-api

> #164 OWASP API Security Top 10 (2023)

OWASP API Security Top 10 (API 특화 보안 위협을 방어한다):

| 순위 | 위협 | 대응 |
|------|------|------|
| API1 | Broken Object Level Auth | 모든 요청에서 리소스 소유자 검증 |
| API2 | Broken Authentication | JWT 만료, Rate limit, MFA |
| API3 | Broken Object Property Level Auth | 응답 필드 필터링, 민감 필드 제외 |
| API4 | Unrestricted Resource Consumption | Rate limiting, Pagination, 페이로드 크기 제한 |
| API5 | Broken Function Level Auth | RBAC, 엔드포인트별 권한 검증 |
| API6 | Unrestricted Access to Sensitive Business Flows | 봇 감지, CAPTCHA, 비즈니스 로직 Rate limit |
| API7 | Server Side Request Forgery (SSRF) | URL 화이트리스트, 내부 IP 차단 |
| API8 | Security Misconfiguration | CORS 제한, 에러 메시지 최소화, 불필요한 메서드 비활성화 |
| API9 | Improper Inventory Management | API 버전 관리, 사용되지 않는 엔드포인트 제거 |
| API10 | Unsafe Consumption of APIs | 서드파티 API 응답 검증, 타임아웃, Circuit Breaker |

### 필수 구현 패턴
```typescript
// API1: Object Level Authorization
async function getOrder(userId: string, orderId: string) {
  const order = await db.order.findUnique({ where: { id: orderId } });
  if (order.userId !== userId) throw new ForbiddenError();
  return order;
}

// API4: Resource Consumption 제한
app.use(rateLimit({ windowMs: 15 * 60 * 1000, max: 100 }));
app.use(express.json({ limit: '1mb' }));
```

### API 보안 헤더
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: default-src 'self'
```

## Connections

- [[dev.security.owasp]] — CO_CREATES (weight: 0.6)
