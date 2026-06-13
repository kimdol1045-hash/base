---
id: "dev.backend.graphql.resolver"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["graphql", "resolver", "backend", "dataloader"]
brain_region: "BRAINSTEM"
token_estimate: 450
---

# dev.backend.graphql.resolver

> #202 Resolver Pattern (GraphQL Spec, 2021)

# GraphQL 리졸버 설계 가이드

## 핵심 원칙
- 리졸버는 얇게 유지한다 (비즈니스 로직은 서비스 레이어에 위임)
- N+1 문제를 DataLoader로 해결한다
- 인증/인가는 리졸버가 아닌 미들웨어 또는 디렉티브에서 처리한다
- 각 필드 리졸버는 독립적으로 에러를 처리할 수 있어야 한다

## DO
- DataLoader를 요청 단위로 생성하여 배칭과 캐싱을 활용한다
- Context 객체에 인증 정보와 DataLoader 인스턴스를 주입한다
- 복잡한 필드는 별도 리졸버로 분리한다
- 에러 발생 시 사용자 친화적 메시지와 에러 코드를 함께 반환한다

## DON'T
- 리졸버 안에서 직접 DB 쿼리를 실행하지 않는다
- 전역 DataLoader 인스턴스를 공유하지 않는다 (요청 간 캐시 오염)
- parent 인자를 무시하고 항상 새 쿼리를 실행하지 않는다
- 에러를 삼키지 않는다 (throw 또는 userErrors로 전파)

## 코드 예시
```typescript
// DataLoader 생성 (요청 단위)
function createLoaders(db: Database) {
  return {
    userLoader: new DataLoader<string, User>(async (ids) => {
      const users = await db.users.findByIds([...ids]);
      const userMap = new Map(users.map(u => [u.id, u]));
      return ids.map(id => userMap.get(id) ?? new Error(`User ${id} not found`));
    }),
  };
}

// 리졸버 구현
const resolvers = {
  Query: {
    user: (_parent, { id }, ctx) => ctx.loaders.userLoader.load(id),
  },
  Post: {
    author: (post, _args, ctx) => ctx.loaders.userLoader.load(post.authorId),
  },
  Mutation: {
    createUser: async (_parent, { input }, ctx) => {
      const user = await ctx.services.user.create(input);
      return { user, userErrors: [] };
    },
  },
};
```
