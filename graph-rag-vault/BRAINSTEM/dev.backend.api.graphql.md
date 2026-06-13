---
id: "dev.backend.api.graphql"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#102 API Design Principles"
tags: [backend, api, graphql, dataloader, n+1, schema-design]
---

# dev.backend.api.graphql

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #102 API Design Principles  
> **Tokens**: 500

## Content

GraphQL 패턴 (쿼리의 자유를 허용하되 비용을 제어한다 -- 제한 없는 GraphQL은 DB를 무너뜨리는 무기가 된다):

### Schema-First 설계

DO:
```typescript
// 1. 스키마 정의 (SDL-first)
const typeDefs = `#graphql
  type Query {
    user(id: ID!): User
    users(filter: UserFilter, pagination: PaginationInput): UserConnection!
    post(id: ID!): Post
  }

  type Mutation {
    createPost(input: CreatePostInput!): Post!
    updatePost(id: ID!, input: UpdatePostInput!): Post!
  }

  type User {
    id: ID!
    name: String!
    email: String!
    posts(first: Int = 10, after: String): PostConnection!
    followers: [User!]!
  }

  type Post {
    id: ID!
    title: String!
    body: String!
    author: User!
    comments(first: Int = 10): [Comment!]!
    createdAt: DateTime!
  }

  type UserConnection {
    edges: [UserEdge!]!
    pageInfo: PageInfo!
    totalCount: Int!
  }

  type UserEdge {
    cursor: String!
    node: User!
  }

  type PageInfo {
    hasNextPage: Boolean!
    endCursor: String
  }

  input PaginationInput {
    first: Int = 20
    after: String
  }

  input UserFilter {
    name: String
    status: UserStatus
  }
`;

// 2. DataLoader를 사용한 N+1 방지
import DataLoader from "dataloader";

function createLoaders() {
  return {
    userLoader: new DataLoader<string, User>(async (ids) => {
      const users = await db.query.users.findMany({
        where: inArray(users.id, [...ids]),
      });
      // DataLoader는 입력 순서와 동일한 순서로 반환해야 함
      const userMap = new Map(users.map((u) => [u.id, u]));
      return ids.map((id) => userMap.get(id) ?? new Error(`User ${id} not found`));
    }),

    postsByAuthorLoader: new DataLoader<string, Post[]>(async (authorIds) => {
      const posts = await db.query.posts.findMany({
        where: inArray(posts.authorId, [...authorIds]),
      });
      const grouped = new Map<string, Post[]>();
      posts.forEach((p) => {
        const list = grouped.get(p.authorId) ?? [];
        list.push(p);
        grouped.set(p.authorId, list);
      });
      return authorIds.map((id) => grouped.get(id) ?? []);
    }),
  };
}

// 요청마다 새 DataLoader 인스턴스 생성 (캐시 격리)
const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => ({
    user: req.user,
    loaders: createLoaders(),
  }),
});

// 3. Resolver에서 DataLoader 사용
const resolvers = {
  Query: {
    user: (_, { id }, { loaders }) => loaders.userLoader.load(id),
    users: async (_, { filter, pagination }) => {
      const { first = 20, after } = pagination ?? {};
      // cursor-based pagination 구현
      const results = await db.query.users.findMany({
        where: filter?.status ? eq(users.status, filter.status) : undefined,
        limit: first + 1,
        ...(after ? { cursor: decodeCursor(after) } : {}),
      });
      const hasNext = results.length > first;
      const edges = (hasNext ? results.slice(0, -1) : results).map((u) => ({
        cursor: encodeCursor(u.id),
        node: u,
      }));
      return {
        edges,
        pageInfo: { hasNextPage: hasNext, endCursor: edges.at(-1)?.cursor },
        totalCount: await db.$count(users),
      };
    },
  },
  User: {
    posts: (parent, { first }, { loaders }) => loaders.postsByAuthorLoader.load(parent.id),
    followers: (parent, _, { loaders }) => loaders.followersLoader.load(parent.id),
  },
  Post: {
    author: (parent, _, { loaders }) => loaders.userLoader.load(parent.authorId),
  },
};
```

### 쿼리 보안: Depth Limit + Complexity Analysis
```typescript
import depthLimit from "graphql-depth-limit";
import { createComplexityLimitRule } from "graphql-validation-complexity";

const server = new ApolloServer({
  typeDefs,
  resolvers,
  validationRules: [
    depthLimit(7),  // 최대 깊이 7단계
    createComplexityLimitRule(1000, {
      scalarCost: 1,
      objectCost: 2,
      listFactor: 10,  // 리스트는 10배 가중
      onCost: (cost) => {
        if (cost > 800) logger.warn(`High complexity query: ${cost}`);
      },
    }),
  ],
  plugins: [
    {
      requestDidStart: async () => ({
        didResolveOperation: async ({ request }) => {
          logger.info("GraphQL query", {
            query: request.query,
            variables: request.variables,
          });
        },
      }),
    },
  ],
});
```

### 복잡도 예산
| 항목 | 비용 | 설명 |
|------|------|------|
| Scalar 필드 | 1 | id, name, email 등 |
| Object 필드 | 2 | 중첩 객체 resolve 비용 |
| List 필드 | x10 배수 | 리스트 내 각 항목에 배수 적용 |
| 최대 총 복잡도 | 1000 | 초과 시 쿼리 거부 |
| 최대 깊이 | 7 | 무한 중첩 방지 |

DON'T:
```typescript
// ❌ DataLoader 없이 직접 DB 호출 -- N+1 쿼리 발생
const resolvers = {
  Post: {
    author: async (parent) => {
      return db.query.users.findFirst({ where: eq(users.id, parent.authorId) });
      // posts 100개 조회 시 user 쿼리 100번 실행
    },
  },
};

// ❌ Depth Limit 없음 -- 재귀 쿼리로 서버 과부하
// query { user { followers { followers { followers { ... } } } } }

// ❌ DataLoader를 전역 싱글톤으로 생성 -- 요청 간 캐시 오염
const globalLoader = new DataLoader(batchFn);  // 모든 요청이 같은 캐시 공유

// ❌ 에러 메시지에 내부 구조 노출
throw new Error(`Column users.password_hash not found`);
```

### 흔한 실수
- DataLoader 인스턴스를 요청 간 공유 -> 캐시 오염으로 다른 유저 데이터 반환
- 리스트 필드에 기본 limit 미설정 -> `users { posts { comments } }` 시 전체 로드
- 쿼리 복잡도 분석 없이 배포 -> 악의적 중첩 쿼리로 DB 과부하
- Introspection을 프로덕션에서 활성화 -> 스키마 구조 전체 노출
- mutation 응답에서 변경된 객체 미반환 -> 클라이언트 캐시 무효화 불가
