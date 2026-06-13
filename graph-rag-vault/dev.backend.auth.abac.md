---
id: "dev.backend.auth.abac"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["auth", "abac", "authorization", "policy"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.auth.abac

> #224 ABAC (NIST SP 800-162, Attribute Based Access Control 2014)

# ABAC (속성 기반 접근 제어) 가이드

## 핵심 원칙
- 사용자, 리소스, 환경의 속성(Attribute) 조합으로 접근 권한을 결정한다
- RBAC보다 유연하며, 복잡한 권한 로직을 정책(Policy)으로 표현한다
- 정책 엔진을 분리하여 비즈니스 로직과 권한 로직을 독립시킨다
- 감사 로그에 어떤 정책이 적용되었는지 기록한다

## DO
- 정책을 코드 외부(JSON, YAML, OPA Rego)에서 관리한다
- 주체(Subject), 리소스(Resource), 행위(Action), 환경(Environment) 4요소로 평가한다
- 정책 변경 시 코드 배포 없이 적용 가능하도록 설계한다
- 기본 거부(Default Deny) 원칙을 적용한다

## DON'T
- if-else 체인으로 권한 로직을 하드코딩하지 않는다
- 속성 평가에 외부 API 호출을 동기적으로 수행하지 않는다 (캐시 활용)
- 정책을 테스트하지 않고 프로덕션에 적용하지 않는다
- 모든 경우에 ABAC를 사용하지 않는다 (단순 역할만 필요하면 RBAC)

## 코드 예시
```typescript
interface PolicyContext {
  subject: { id: string; role: string; department: string; clearanceLevel: number };
  resource: { type: string; ownerId: string; sensitivity: string; department: string };
  action: "read" | "write" | "delete" | "approve";
  environment: { time: Date; ipAddress: string; location: string };
}

type Policy = {
  name: string;
  condition: (ctx: PolicyContext) => boolean;
  effect: "allow" | "deny";
};

const policies: Policy[] = [
  {
    name: "부서 내 문서 읽기",
    effect: "allow",
    condition: (ctx) =>
      ctx.action === "read" &&
      ctx.subject.department === ctx.resource.department,
  },
  {
    name: "기밀 문서는 높은 보안등급만",
    effect: "deny",
    condition: (ctx) =>
      ctx.resource.sensitivity === "confidential" &&
      ctx.subject.clearanceLevel < 3,
  },
  {
    name: "업무 시간 외 쓰기 금지",
    effect: "deny",
    condition: (ctx) => {
      const hour = ctx.environment.time.getHours();
      return ctx.action === "write" && (hour < 9 || hour > 18);
    },
  },
];

function evaluate(ctx: PolicyContext): boolean {
  for (const policy of policies) {
    if (policy.condition(ctx)) {
      if (policy.effect === "deny") return false;
    }
  }
  return policies.some(p => p.effect === "allow" && p.condition(ctx));
}
```
