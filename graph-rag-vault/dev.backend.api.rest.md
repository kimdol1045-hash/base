---
id: "dev.backend.api.rest"
domain: "development.backend"
type: "rule"
bloom_level: ""
tags: ["backend", "api", "rest", "architecture", "http"]
brain_region: "BRAINSTEM"
token_estimate: 480
---

# dev.backend.api.rest

> #101 REST (Fielding, 2000)

REST 아키텍처 원칙 (클라이언트-서버 간 일관되고 예측 가능한 인터페이스를 보장하기 위함):

### 리소스 기반 URL 설계
명사 복수형을 사용하며, 행위는 HTTP 메서드로 표현한다.

DO:
```
GET    /api/v1/users          # 목록 조회
GET    /api/v1/users/:id      # 단건 조회
POST   /api/v1/users          # 생성
PATCH  /api/v1/users/:id      # 부분 수정
DELETE /api/v1/users/:id      # 삭제
POST   /api/v1/users/:id/ban  # 커스텀 액션 (동사 허용하는 유일한 경우)
```

DON'T:
```
GET  /api/getUsers           # ❌ 동사 사용
POST /api/user/delete/:id    # ❌ DELETE 메서드를 써야 함
GET  /api/v1/User            # ❌ 단수형 + PascalCase
```

### HTTP 상태코드 규칙
| 코드 | 의미 | 사용 시점 |
|------|------|-----------|
| 200  | OK | GET, PATCH 성공 |
| 201  | Created | POST로 리소스 생성 성공 (Location 헤더 포함) |
| 204  | No Content | DELETE 성공 (body 없음) |
| 400  | Bad Request | 잘못된 요청 형식 |
| 401  | Unauthorized | 인증 토큰 없음/만료 |
| 403  | Forbidden | 권한 부족 (인증은 됐으나 접근 불가) |
| 404  | Not Found | 리소스 없음 |
| 409  | Conflict | 중복 생성 시도 |
| 422  | Unprocessable Entity | 검증 실패 (Zod 에러) |
| 429  | Too Many Requests | Rate limit 초과 |
| 500  | Internal Server Error | 예상치 못한 서버 오류 |

### 응답 형식 통일
```typescript
// 성공 응답
type SuccessResponse<T> = {
  data: T;
  meta?: { cursor?: string; hasMore?: boolean; total?: number };
};

// 에러 응답
type ErrorResponse = {
  error: {
    code: string;       // 예: "VALIDATION_ERROR"
    message: string;    // 사람이 읽을 수 있는 메시지
    details?: unknown;  // Zod 에러 등 상세 정보
  };
};
```

### 무상태 원칙
- 서버에 세션/상태를 저장하지 않는다
- 매 요청에 인증 정보(JWT)를 포함한다
- 서버 간 공유 상태가 필요하면 Redis/DB를 사용한다

### 흔한 실수
- PUT vs PATCH 혼동: PUT은 전체 교체, PATCH는 부분 수정 (대부분 PATCH가 적절)
- 204 응답에 body를 넣는 것 (body 없어야 함)
- 401과 403 혼동: 인증 문제 vs 인가 문제
- 중첩 리소스 과다: `/users/:id/posts/:pid/comments/:cid/likes` 3단계 이상 지양

## Connections

- [[dev.backend.api.role]] — REQUIRES (weight: 0.9)
- [[dev.backend.api.verify]] — FEEDS (weight: 0.8)
- [[dev.backend.api.validation]] — FEEDS (weight: 0.7)
- [[dev.backend.api.validation]] — CO_CREATES (weight: 0.6)
- [[dev.backend.api.versioning]] — CO_CREATES (weight: 0.6)
- [[dev.backend.api.pagination]] — CO_CREATES (weight: 0.6)
