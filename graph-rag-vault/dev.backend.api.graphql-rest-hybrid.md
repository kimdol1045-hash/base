---
id: "dev.backend.api.graphql-rest-hybrid"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["api", "graphql", "rest", "hybrid", "gateway"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.api.graphql-rest-hybrid

> #216 API Gateway Pattern (Richardson, Microservices Patterns 2018)

# GraphQL + REST 하이브리드 API 설계 가이드

## 핵심 원칙
- GraphQL과 REST를 용도에 맞게 혼용한다
- 복잡한 데이터 조회는 GraphQL, 단순 CRUD와 파일 업로드는 REST를 사용한다
- API Gateway에서 두 프로토콜을 통합 관리한다
- 인증/인가 로직은 프로토콜과 무관하게 공유한다

## 사용 기준
| 용도 | 권장 프로토콜 | 이유 |
|------|-------------|------|
| 복잡한 데이터 조회 | GraphQL | 유연한 필드 선택, N+1 방지 |
| 파일 업로드/다운로드 | REST | 스트리밍, multipart 지원 |
| Webhook 수신 | REST | 외부 서비스 호환성 |
| 단순 CRUD | REST | 단순성, 캐싱 용이 |
| 실시간 데이터 | GraphQL Subscription | 타입 안전한 실시간 통신 |

## DO
- 비즈니스 로직을 서비스 레이어에 두어 두 프로토콜에서 재사용한다
- API 버전 관리 전략을 통일한다
- 공통 에러 형식을 정의한다
- OpenAPI와 GraphQL 스키마를 모두 제공한다

## DON'T
- 동일한 기능을 두 프로토콜로 중복 구현하지 않는다
- GraphQL resolver에서 내부 REST API를 호출하지 않는다 (서비스 레이어 직접 호출)
- 한쪽 프로토콜에만 인증을 적용하고 다른 쪽을 방치하지 않는다

## 코드 예시
```typescript
// 공유 서비스 레이어
class UserService {
  async getById(id: string): Promise<User> { /* ... */ }
  async create(input: CreateUserInput): Promise<User> { /* ... */ }
}

// REST 컨트롤러
app.get("/api/v1/users/:id", async (req, res) => {
  const user = await userService.getById(req.params.id);
  res.json({ data: user });
});

// GraphQL 리졸버
const resolvers = {
  Query: {
    user: (_, { id }) => userService.getById(id),
  },
};

// 파일 업로드는 REST 전용
app.post("/api/v1/uploads", upload.single("file"), handleFileUpload);
```
