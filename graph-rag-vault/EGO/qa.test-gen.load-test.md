---
id: "qa.test-gen.load-test"
domain: "qa"
type: "pattern"
region: EGO
token_estimate: 500
theory: "#135 Amdahl's Law, #137 Little's Law"
tags: [qa, test, load-test, k6, performance, slo]
---

# qa.test-gen.load-test

> **Region**: 🔵 [[EGO]]  
> **Domain**: `qa`  
> **Type**: `pattern`  
> **Theory**: #135 Amdahl's Law, #137 Little's Law  
> **Tokens**: 500

## Content

부하 테스트 (시스템의 성능 한계와 SLO 충족 여부를 검증한다):

### 이론 배경
- **Amdahl's Law**: 병렬화 불가능한 부분이 전체 성능 상한을 결정한다
- **Little's Law**: L = λ × W (동시 사용자 = 도착률 × 평균 응답시간)
  → p95 응답시간 200ms, 목표 100 RPS라면 동시 연결 ≈ 100 × 0.2 = 20

### 테스트 유형
| 유형 | VUs | 기간 | 목적 |
|------|-----|------|------|
| Smoke | 1-5 | 1분 | 기본 동작 확인 |
| Load | 50-100 | 10분 | 기준선(baseline) 측정 |
| Stress | 200+ | 5분 | 한계점 파악 |
| Spike | 0→500→0 | 2분 | 급증 복구 능력 |
| Soak | 50 | 2시간 | 메모리 누수/장기 안정성 |

### k6 스크립트
```typescript
import http from 'k6/http';
import { check, sleep } from 'k6';

// DO: SLO 기반 threshold 설정
export const options = {
  stages: [
    { duration: '2m', target: 50 },   // ramp-up
    { duration: '5m', target: 50 },   // steady state
    { duration: '2m', target: 100 },  // stress
    { duration: '1m', target: 0 },    // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<200', 'p(99)<500'],  // ms
    http_req_failed: ['rate<0.001'],                  // 0.1% 미만
    http_reqs: ['rate>100'],                          // 100 RPS 이상
  },
};

// DO: 현실적 시나리오 + think time
export default function () {
  const loginRes = http.post('https://api.example.com/auth/login', JSON.stringify({
    email: `user${__VU}@test.com`,
    password: 'loadtest123',
  }), { headers: { 'Content-Type': 'application/json' } });

  check(loginRes, {
    'login 200': (r) => r.status === 200,
    'token exists': (r) => !!r.json('token'),
  });

  const token = loginRes.json('token');

  // 실제 사용자처럼 think time 추가
  sleep(Math.random() * 3 + 1); // 1-4초

  const listRes = http.get('https://api.example.com/products', {
    headers: { Authorization: `Bearer ${token}` },
  });

  check(listRes, {
    'list 200': (r) => r.status === 200,
    'has items': (r) => r.json('items').length > 0,
  });

  sleep(Math.random() * 2 + 1);
}
```

### SLO 기준값 (서비스 수준 목표)
- **응답 시간**: p95 < 200ms, p99 < 500ms
- **에러율**: < 0.1% (1,000 요청 중 1건 미만)
- **처리량**: 목표 RPS의 2배까지 안정적

DON'T:
```typescript
// ❌ warm-up 없이 즉시 최대 부하
export const options = {
  vus: 500,           // 갑자기 500명 → 서버 초기화 실패
  duration: '5m',
};

// ❌ think time 없음 → 비현실적 부하
export default function () {
  http.get('https://api.example.com/products');
  // sleep 없이 연속 호출 → 실제 사용 패턴과 다름
}
```

### 실행 및 분석
```bash
# 실행
k6 run --out json=results.json load-test.js

# CI 통합: threshold 실패 시 exit code 99
k6 run --ci load-test.js
```

### 주의사항
- 프로덕션 테스트는 반드시 사전 승인 후 실행
- 최소 2개 리전에서 테스트 (단일 리전 결과는 편향)
- ramp-up은 전체 시간의 20% 이상 할당
