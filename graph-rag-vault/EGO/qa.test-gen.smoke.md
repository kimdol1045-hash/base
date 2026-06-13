---
id: "qa.test-gen.smoke"
domain: "qa"
type: "pattern"
region: EGO
token_estimate: 380
theory: "#185 Smoke Testing / Sanity Testing"
tags: [qa, smoke-test, deployment, ci-cd]
---

# qa.test-gen.smoke

> **Region**: 🔵 [[EGO]]  
> **Domain**: `qa`  
> **Type**: `pattern`  
> **Theory**: #185 Smoke Testing / Sanity Testing  
> **Tokens**: 380

## Content

스모크 테스트 (배포 후 핵심 기능의 정상 동작을 빠르게 확인한다):

### 목적
- 배포 직후 "시스템이 살아있는가?" 검증
- 전체 테스트 실행 전 기본 기능 확인
- 1~5분 내 완료

### 스모크 테스트 체크리스트
```
1. 서버 응답: GET /health → 200 OK
2. 인증: POST /auth/login → 토큰 반환
3. 핵심 CRUD: POST /api/items → 201 Created
4. DB 연결: SELECT 1 → 성공
5. 외부 서비스: 결제 API ping → 응답
```

### 구현 예시
```typescript
describe('Smoke Tests', () => {
  it('서버 헬스체크', async () => {
    const res = await fetch(`${BASE_URL}/health`);
    expect(res.status).toBe(200);
  });

  it('로그인 가능', async () => {
    const res = await fetch(`${BASE_URL}/auth/login`, {
      method: 'POST',
      body: JSON.stringify({ email: 'test@test.com', password: 'test' }),
    });
    expect(res.status).toBe(200);
    expect(await res.json()).toHaveProperty('token');
  });
});
```

### CI/CD 통합
```yaml
deploy:
  steps:
    - deploy_to_staging
    - run_smoke_tests    # 실패 시 자동 롤백
    - deploy_to_production
    - run_smoke_tests    # 실패 시 자동 롤백
```

### vs 다른 테스트
| 스모크 | 회귀 | E2E |
|--------|------|-----|
| 핵심만 | 전체 기능 | 사용자 시나리오 |
| 1~5분 | 10~30분 | 10~60분 |
| 배포마다 | PR마다 | 릴리즈 전 |

## Connections

*Connections will be populated by Graph RAG ingest.*
