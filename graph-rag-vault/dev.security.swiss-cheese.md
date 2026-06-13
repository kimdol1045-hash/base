---
id: "dev.security.swiss-cheese"
domain: "development.security"
type: "pattern"
bloom_level: ""
tags: ["security", "defense-in-depth", "layered-security", "pattern", "swiss-cheese"]
brain_region: "CORTEX"
token_estimate: 480
---

# dev.security.swiss-cheese

> #113 스위스 치즈 모델 (Reason, 1990)

다층 방어 설계 (각 레이어는 구멍이 있는 치즈 슬라이스 -- 겹치면 구멍을 막는다):

James Reason의 스위스 치즈 모델은 단일 방어 레이어는 반드시 구멍(취약점)이 있으며,
여러 레이어를 겹쳐야 공격이 모든 구멍을 동시에 통과하는 확률을 극소화할 수 있다는 원리이다.

### 5-Layer 방어 체인

| Layer | 역할 | 실패 시 결과 |
|-------|------|------------|
| L1. 입력 검증 | 악성 데이터 차단 | SQL Injection, XSS 가능 |
| L2. 인증 (Authentication) | 신원 확인 | 비인가 접근 |
| L3. 인가 (Authorization) | 권한 확인 | 권한 상승(Privilege Escalation) |
| L4. 비즈니스 로직 검증 | 도메인 규칙 적용 | 잔고 부족 이체, 재고 초과 주문 |
| L5. 출력 필터링 | 민감 정보 제거 | 내부 구조/개인정보 노출 |

### DO: 모든 레이어 적용
```typescript
// L1: 입력 검증 (Zod)
const TransferSchema = z.object({
  fromAccountId: z.string().uuid(),
  toAccountId: z.string().uuid(),
  amount: z.number().positive().max(10_000_000),
});

// L2~L3: 인증 + 인가 미들웨어
app.post("/transfers", authMiddleware, async (c) => {
  const body = TransferSchema.parse(await c.req.json());     // L1
  const user = c.get("user");                                 // L2
  if (body.fromAccountId !== user.accountId) {                // L3
    throw Errors.forbidden("본인 계좌만 출금 가능합니다");
  }

  // L4: 비즈니스 로직 검증
  const account = await accountService.findById(body.fromAccountId);
  if (account.balance < body.amount) {
    throw Errors.validation({ amount: "잔고 부족" });
  }

  const result = await transferService.execute(body);

  // L5: 출력 필터링 -- 내부 필드 제거
  return c.json({ data: { id: result.id, status: result.status, amount: result.amount } });
});
```

### DON'T: 단일 레이어에 의존
```typescript
// L1만 존재, L2~L5 전부 누락
app.post("/transfers", async (c) => {
  const body = TransferSchema.parse(await c.req.json());
  // 인증 없음 -- 누구나 이체 가능
  // 인가 없음 -- 타인 계좌에서 출금 가능
  // 비즈니스 검증 없음 -- 잔고 마이너스 가능
  const result = await db.executeTransfer(body);
  return c.json(result); // 출력 필터링 없음 -- 내부 DB 컬럼 전체 노출
});
```

### 적용 규칙
- 최소 3개 레이어가 동시에 적용되어야 한다 (L1 + L2/L3 + L5는 필수)
- 레이어 간 의존성 금지: 각 레이어는 이전 레이어가 실패했다고 가정하고 독립 검증한다
- 레이어 통과/실패 이벤트를 감사 로그에 기록한다

## Connections

- [[dev.security.role]] — CO_CREATES (weight: 0.6)
- [[dev.security.owasp]] — CO_CREATES (weight: 0.6)
- [[dev.security.cia-triad]] — CO_CREATES (weight: 0.6)
- [[dev.security.stride]] — CO_CREATES (weight: 0.6)
- [[dev.security.saltzer]] — CO_CREATES (weight: 0.6)
- [[dev.security.secure-by-design]] — CO_CREATES (weight: 0.6)
- [[dev.security.defense-in-depth]] — CO_CREATES (weight: 0.6)
- [[dev.security.zero-trust]] — CO_CREATES (weight: 0.6)
- [[dev.security.verify]] — CO_CREATES (weight: 0.6)
