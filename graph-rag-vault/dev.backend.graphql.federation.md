---
id: "dev.backend.graphql.federation"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["graphql", "federation", "microservices", "gateway"]
brain_region: "BRAINSTEM"
token_estimate: 430
---

# dev.backend.graphql.federation

> #204 Apollo Federation (Apollo, 2023)

# GraphQL Federation 설계 가이드

## 핵심 원칙
- 각 서브그래프는 자신이 소유한 엔티티만 정의한다 (Separation of Concerns)
- Gateway(Router)는 스키마 조합과 쿼리 계획만 담당한다
- 엔티티 간 참조는 `@key` 디렉티브로 선언한다
- 서브그래프 간 의존성을 최소화하고, 단방향 참조를 지향한다

## DO
- `@key` 디렉티브로 엔티티의 고유 식별자를 명확히 정의한다
- `__resolveReference`를 구현하여 엔티티 해석을 처리한다
- 서브그래프 독립 배포가 가능하도록 스키마를 설계한다
- 공유 타입은 `@shareable` 디렉티브를 활용한다

## DON'T
- 하나의 서브그래프에서 다른 서브그래프의 핵심 타입을 정의하지 않는다
- Gateway에 비즈니스 로직을 넣지 않는다
- 순환 의존성이 있는 서브그래프 구조를 만들지 않는다
- Federation 없이 단일 서비스에서 충분한 경우 무리하게 분리하지 않는다

## 코드 예시
```graphql
# Users 서브그래프
type User @key(fields: "id") {
  id: ID!
  email: String!
  displayName: String
}

type Query {
  user(id: ID!): User
  me: User
}

# Orders 서브그래프
type Order @key(fields: "id") {
  id: ID!
  items: [OrderItem!]!
  totalAmount: Int!
  buyer: User!   # User 엔티티 참조
}

extend type User @key(fields: "id") {
  id: ID! @external
  orders: [Order!]!   # User에 orders 필드 추가
}
```

```typescript
// Orders 서브그래프 리졸버
const resolvers = {
  User: {
    __resolveReference: (ref, ctx) =>
      ctx.loaders.userStub.load(ref.id),
    orders: (user, _args, ctx) =>
      ctx.services.order.findByUserId(user.id),
  },
};
```
