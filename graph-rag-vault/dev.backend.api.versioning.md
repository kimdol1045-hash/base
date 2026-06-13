---
id: "dev.backend.api.versioning"
domain: "development.backend"
type: "rule"
bloom_level: ""
tags: ["backend", "api", "versioning", "architecture", "evolution"]
brain_region: "BRAINSTEM"
token_estimate: 480
---

# dev.backend.api.versioning

> #104 API Evolution (Amundsen, 2020)

API 버전 관리 전략 (API는 한번 공개되면 계약이다 -- 기존 클라이언트를 깨뜨리지 않아야 한다):

### 버전 관리 방식 비교
| 방식 | 예시 | 장점 | 단점 | 추천 |
|------|------|------|------|------|
| URL Path | `/api/v1/users` | 명확, 라우팅 쉬움, 캐싱 유리 | URL이 지저분 | **기본 선택** |
| Header | `Accept: application/vnd.api.v1+json` | URL 깔끔 | 테스트 어려움, CDN 캐싱 복잡 | 대규모 API |
| Query Param | `/api/users?version=1` | 간단 | 캐싱 어려움, 누락 가능 | 비추천 |

### URL Path 버전 관리 (권장)
```typescript
const app = new Hono();

// v1 라우트
const v1 = new Hono();
v1.get("/users", listUsersV1);
v1.get("/users/:id", getUserV1);

// v2 라우트 (응답 형식 변경)
const v2 = new Hono();
v2.get("/users", listUsersV2);      // 새로운 응답 형식
v2.get("/users/:id", getUserV2);

app.route("/api/v1", v1);
app.route("/api/v2", v2);
```

### 하위 호환성 규칙 (Breaking Change 방지)
버전을 올리지 않아도 되는 변경 (하위 호환):
```
OK: 응답에 새 필드 추가          { data: { name, email, avatar } } → + phone 추가
OK: 선택적 요청 필드 추가        body에 optional 필드 추가
OK: 새 엔드포인트 추가           POST /api/v1/users/export
OK: 에러 메시지 텍스트 변경      "Not found" → "리소스를 찾을 수 없습니다"
```

버전을 올려야 하는 변경 (Breaking Change):
```
BREAKING: 응답 필드 제거/이름 변경    name → fullName
BREAKING: 필수 요청 필드 추가         body에 required 필드 추가
BREAKING: URL 구조 변경              /users/:id → /accounts/:id
BREAKING: 응답 형식 구조 변경        { users: [...] } → { data: [...] }
BREAKING: HTTP 메서드 변경           PUT → PATCH
BREAKING: 상태코드 변경 의미         200 → 201
```

### 버전 전환 구현 패턴
```typescript
// 공유 서비스 레이어 -- 버전 간 비즈니스 로직 재사용
// services/user.service.ts
export async function findUserById(id: string): Promise<UserEntity> {
  return db.query.users.findFirst({ where: eq(users.id, id) });
}

// v1 -- 원래 응답 형식
async function getUserV1(c: Context) {
  const user = await findUserById(c.req.param("id"));
  if (!user) throw Errors.notFound("사용자");
  return c.json({
    data: { id: user.id, name: user.name, email: user.email },
  });
}

// v2 -- 확장된 응답 형식
async function getUserV2(c: Context) {
  const user = await findUserById(c.req.param("id"));
  if (!user) throw Errors.notFound("사용자");
  return c.json({
    data: {
      id: user.id,
      profile: { displayName: user.name, email: user.email, avatar: user.avatarUrl },
      metadata: { createdAt: user.createdAt, updatedAt: user.updatedAt },
    },
  });
}
```

### Deprecation 전략
```typescript
// 더 이상 사용하지 않는 버전/엔드포인트에 경고 헤더 추가
function deprecationWarning(sunset: string) {
  return async (c: Context, next: Next) => {
    c.header("Deprecation", "true");
    c.header("Sunset", sunset);  // RFC 8594 형식: "Sat, 01 Jan 2025 00:00:00 GMT"
    c.header("Link", '</api/v2/docs>; rel="successor-version"');
    await next();
  };
}

// v1 전체에 deprecation 경고
v1.use("*", deprecationWarning("Sat, 01 Jul 2025 00:00:00 GMT"));
```

### 버전 관리 베스트 프랙티스
- 최대 2개 버전만 동시 운영 (v1 + v2)
- 새 버전 출시 후 최소 6개월간 이전 버전 유지
- API 변경 로그(changelog)를 문서화
- 클라이언트에게 마이그레이션 가이드 제공
- 버전 없는 URL(`/api/users`)은 최신 버전으로 리다이렉트하지 말것 -- 암묵적 breaking change

### 흔한 실수
- 응답 필드 이름 변경을 "사소한 수정"으로 여김 -> 클라이언트 파싱 실패
- 버전을 올리지 않고 필수 필드 추가 -> 기존 클라이언트 요청이 422로 실패
- v1, v2, v3... 버전이 계속 늘어남 -> 유지보수 지옥 (설계를 재고할 시점)
- 내부 API에도 과도한 버전 관리 -> 불필요한 복잡도 (내부 API는 동시 배포 가능)

## Connections

- [[dev.backend.api.rest]] — CO_CREATES (weight: 0.6)
- [[dev.backend.api.pagination]] — CO_CREATES (weight: 0.6)
