---
id: "dev.backend.graphql.subscription"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["graphql", "subscription", "realtime", "websocket"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.graphql.subscription

> #203 GraphQL Subscriptions (GraphQL over WebSocket Protocol, 2022)

# GraphQL Subscription 설계 가이드

## 핵심 원칙
- Subscription은 실시간 데이터가 꼭 필요한 경우에만 사용한다
- `graphql-ws` 프로토콜을 사용한다 (deprecated된 `subscriptions-transport-ws` 사용 금지)
- PubSub 백엔드를 분리하여 수평 확장이 가능하도록 한다
- 클라이언트 연결 수에 대한 제한을 반드시 설정한다

## DO
- Redis PubSub 또는 메시지 브로커를 백엔드로 사용한다
- 연결 시 인증 토큰을 검증한다 (`connectionParams`)
- 구독 필터링을 서버 측에서 수행한다 (`withFilter`)
- Heartbeat/keepalive를 구현하여 좀비 연결을 감지한다

## DON'T
- 인메모리 PubSub를 프로덕션에서 사용하지 않는다 (단일 서버에서만 동작)
- 대량의 데이터를 Subscription으로 전송하지 않는다 (변경 알림만 보내고 상세 데이터는 Query)
- 연결 제한 없이 무한 구독을 허용하지 않는다
- 인증 없이 Subscription 연결을 허용하지 않는다

## 코드 예시
```typescript
import { createPubSub, withFilter } from "graphql-yoga";
import { createRedisEventTarget } from "@graphql-yoga/redis-event-target";

const pubSub = createPubSub<{
  "post:created": [{ postCreated: Post }];
  "comment:added": [{ commentAdded: Comment; postId: string }];
}>();

const resolvers = {
  Subscription: {
    commentAdded: {
      subscribe: withFilter(
        () => pubSub.subscribe("comment:added"),
        (payload, variables) => payload.postId === variables.postId,
      ),
    },
  },
  Mutation: {
    addComment: async (_parent, { input }, ctx) => {
      const comment = await ctx.services.comment.create(input);
      pubSub.publish("comment:added", {
        commentAdded: comment,
        postId: input.postId,
      });
      return { comment, userErrors: [] };
    },
  },
};
```
