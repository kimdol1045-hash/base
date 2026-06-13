---
id: "qa.test-gen.integration"
domain: "qa"
type: "pattern"
region: EGO
token_estimate: 420
theory: "#124 Testing Trophy (Dodds, 2019)"
tags: [qa, test, integration-test, api]
---

# qa.test-gen.integration

> **Region**: 🔵 [[EGO]]  
> **Domain**: `qa`  
> **Type**: `pattern`  
> **Theory**: #124 Testing Trophy (Dodds, 2019)  
> **Tokens**: 420

## Content

통합 테스트 (모듈 간 상호작용을 검증한다):

### Testing Trophy (Kent C. Dodds)
단위 < **통합** < E2E
통합 테스트가 가장 투자 대비 효과가 높다.

### API 통합 테스트
```typescript
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import { app } from '../src/app';

describe('POST /api/users', () => {
  it('유효한 데이터로 사용자 생성', async () => {
    const res = await app.request('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: 'test@test.com', name: 'Test' }),
    });

    expect(res.status).toBe(201);
    const body = await res.json();
    expect(body.data).toMatchObject({
      email: 'test@test.com',
      name: 'Test',
    });
    expect(body.data.id).toBeDefined();
  });

  it('중복 이메일 시 409 반환', async () => {
    // 첫 번째 생성
    await app.request('/api/users', {
      method: 'POST',
      body: JSON.stringify({ email: 'dup@test.com', name: 'A' }),
    });
    // 중복 시도
    const res = await app.request('/api/users', {
      method: 'POST',
      body: JSON.stringify({ email: 'dup@test.com', name: 'B' }),
    });
    expect(res.status).toBe(409);
  });
});
```

### 테스트 격리
- 각 테스트 전 DB 초기화 (트랜잭션 롤백 또는 테스트 DB)
- 테스트 간 상태 공유 금지
- 외부 서비스: MSW(Mock Service Worker)로 mocking

### 테스트 대상 우선순위
1. 인증/인가 플로우 (가장 중요)
2. 핵심 비즈니스 로직 (결제, 주문)
3. 데이터 무결성 (CRUD 정합성)
4. 에러 핸들링 (잘못된 입력, 서버 에러)

## Connections

### REQUIRES (2)

- ← [[qa.code-review.role]] `w=0.9`
- ← [[qa.test-gen.role]] `w=0.9`

### FEEDS (6)

- ← [[qa.code-review.performance]] `w=0.5`
- ← [[qa.code-review.priority]] `w=0.5`
- ← [[qa.code-review.role]] `w=0.5`
- ← [[qa.code-review.security]] `w=0.7`
- → [[qa.code-review.verify]] `w=0.8`
- → [[qa.test-gen.verify]] `w=0.8`

### CO_CREATES (4)

- → [[qa.test-gen.component-test]] `w=0.6`
- ← [[qa.test-gen.role]] `w=0.6`
- ← [[qa.test-gen.unit]] `w=0.6`
- → [[qa.test-gen.verify]] `w=0.6`
