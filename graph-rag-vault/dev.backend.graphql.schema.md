---
id: "dev.backend.graphql.schema"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["graphql", "schema", "api", "backend"]
brain_region: "BRAINSTEM"
token_estimate: 450
---

# dev.backend.graphql.schema

> #201 GraphQL Schema Design (Principled GraphQL, Apollo 2019)

# GraphQL 스키마 설계 가이드

## 핵심 원칙
- 스키마는 클라이언트 관점에서 설계한다 (Demand-Driven Design)
- 타입 이름은 비즈니스 도메인 용어를 사용한다
- Nullable 필드를 기본으로 하되, 반드시 존재하는 필드만 Non-Null로 선언한다
- Relay Connection 스펙을 따라 페이지네이션을 구현한다

## DO
- 모든 Mutation의 반환 타입에 `userErrors` 필드를 포함한다
- Input 타입은 `[MutationName]Input` 네이밍을 따른다
- Enum 값은 SCREAMING_SNAKE_CASE로 작성한다
- `ID` 스칼라 타입은 외부 노출용, 내부 키는 별도 처리한다

## DON'T
- REST 엔드포인트를 그대로 GraphQL로 매핑하지 않는다
- 하나의 Query에 너무 많은 인자를 넣지 않는다 (filter Input 타입 분리)
- `Any`나 `JSON` 스칼라를 남용하지 않는다
- 중첩 깊이 제한 없이 순환 참조를 허용하지 않는다

## 코드 예시
```graphql
type Query {
  user(id: ID!): User
  users(first: Int!, after: String, filter: UserFilter): UserConnection!
}

type User implements Node {
  id: ID!
  email: String!
  displayName: String
  posts(first: Int!, after: String): PostConnection!
}

input UserFilter {
  role: UserRole
  createdAfter: DateTime
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type Mutation {
  createUser(input: CreateUserInput!): CreateUserPayload!
}

type CreateUserPayload {
  user: User
  userErrors: [UserError!]!
}
```
