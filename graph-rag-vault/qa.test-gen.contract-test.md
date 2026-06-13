---
id: "qa.test-gen.contract-test"
domain: "qa"
type: "pattern"
bloom_level: ""
tags: ["qa", "test", "contract-test", "pact", "api-compatibility", "openapi"]
brain_region: "CEREBELLUM"
token_estimate: 500
---

# qa.test-gen.contract-test

> #126 Testing Trophy (Dodds, 2019)

계약 테스트 (API 소비자와 제공자 간 호환성을 보장한다):

### Consumer-Driven Contracts (CDC)
소비자가 기대하는 요청/응답 형식을 **계약(Contract)**으로 정의하고,
제공자가 CI에서 이 계약을 검증한다. E2E 없이도 API 호환성 보장.

### Pact — Consumer 테스트
```typescript
import { PactV3, MatchersV3 } from '@pact-foundation/pact';

const provider = new PactV3({
  consumer: 'OrderService',
  provider: 'UserService',
});

// DO: Consumer가 기대하는 계약을 정의
describe('UserService API Contract', () => {
  it('GET /api/users/:id — 사용자 정보 반환', async () => {
    await provider
      .given('사용자 ID 1이 존재')
      .uponReceiving('사용자 조회 요청')
      .withRequest({
        method: 'GET',
        path: '/api/users/1',
        headers: { Accept: 'application/json' },
      })
      .willRespondWith({
        status: 200,
        headers: { 'Content-Type': 'application/json' },
        body: MatchersV3.like({
          id: 1,
          name: MatchersV3.string('홍길동'),
          email: MatchersV3.email(),
          createdAt: MatchersV3.iso8601DateTime(),
        }),
      })
      .executeTest(async (mockServer) => {
        const res = await fetch(`${mockServer.url}/api/users/1`, {
          headers: { Accept: 'application/json' },
        });
        expect(res.status).toBe(200);
        const body = await res.json();
        expect(body.id).toBe(1);
        expect(body.email).toContain('@');
      });
  });
});
```

### Pact — Provider 검증
```typescript
// DO: Provider CI에서 계약 검증
import { Verifier } from '@pact-foundation/pact';

describe('Provider Verification', () => {
  it('OrderService 계약을 충족한다', async () => {
    await new Verifier({
      providerBaseUrl: 'http://localhost:3000',
      pactUrls: ['./pacts/OrderService-UserService.json'],
      stateHandlers: {
        '사용자 ID 1이 존재': async () => {
          await seedUser({ id: 1, name: '홍길동' });
        },
      },
    }).verifyProvider();
  });
});
```

### OpenAPI Schema 호환성 검사
```bash
# DO: 스키마 변경 시 breaking change 감지
npx openapi-diff old-spec.yaml new-spec.yaml

# CI에서 자동 검사
# breaking: 필드 삭제, 타입 변경, 필수 파라미터 추가
# non-breaking: 필드 추가, optional 파라미터 추가
```

### Breaking Change 분류
| 변경 | 영향 | 판정 |
|------|------|------|
| 응답 필드 추가 | 없음 | Non-breaking |
| 응답 필드 삭제 | Consumer 에러 | **Breaking** |
| 필수 파라미터 추가 | 기존 요청 실패 | **Breaking** |
| optional 파라미터 추가 | 없음 | Non-breaking |
| 타입 변경 (string→number) | 파싱 에러 | **Breaking** |

DON'T:
```typescript
// ❌ E2E만으로 API 호환성 의존 (느리고 불안정)
test('사용자 조회', async () => {
  // 실제 UserService 호출 → 네트워크, 데이터 의존성
  const res = await fetch('https://user-service.prod/api/users/1');
  expect(res.status).toBe(200);
});

// ❌ API 문서 수동 동기화
// swagger.yaml은 3개월 전 버전이고 실제 API는 다른 상태
```

### CI 통합
- Consumer: PR마다 계약 생성 → Pact Broker에 퍼블리시
- Provider: Consumer 계약 변경 시 자동 검증 트리거
- 계약 버전: Git commit SHA 기반으로 관리
