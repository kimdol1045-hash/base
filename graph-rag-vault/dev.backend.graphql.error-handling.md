---
id: "dev.backend.graphql.error-handling"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["graphql", "error-handling", "backend", "validation"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.graphql.error-handling

> #205 GraphQL Error Handling Best Practices (Sasha Solomon, 2020)

# GraphQL 에러 처리 가이드

## 핵심 원칙
- 예상 가능한 에러는 스키마의 Union/Interface로 표현한다 (유저 에러)
- 예상 불가능한 에러만 `errors` 배열에 포함시킨다 (시스템 에러)
- 에러 코드를 표준화하여 클라이언트가 프로그래밍적으로 처리할 수 있게 한다
- 내부 에러 상세를 클라이언트에 노출하지 않는다

## DO
- Mutation 결과를 Result Union 패턴으로 설계한다
- 에러 코드를 Enum으로 정의하여 타입 안전성을 확보한다
- `extensions` 필드에 에러 메타데이터를 포함한다
- Validation 에러는 필드 단위로 반환한다

## DON'T
- 모든 에러를 top-level `errors` 배열에만 의존하지 않는다
- 스택 트레이스를 프로덕션 에러 응답에 포함하지 않는다
- HTTP 상태 코드로 GraphQL 에러를 구분하지 않는다 (항상 200)
- 에러 메시지를 하드코딩하지 않는다 (i18n 키 사용)

## 코드 예시
```graphql
type UserError {
  field: [String!]!
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  VALIDATION_FAILED
  NOT_FOUND
  ALREADY_EXISTS
  UNAUTHORIZED
  RATE_LIMITED
}

union CreateUserResult = CreateUserSuccess | ValidationError | AlreadyExistsError

type CreateUserSuccess {
  user: User!
}

type ValidationError implements BaseError {
  message: String!
  code: ErrorCode!
  fieldErrors: [FieldError!]!
}
```

```typescript
// 에러 포매터
function formatError(error: GraphQLError) {
  const code = error.extensions?.code ?? "INTERNAL_ERROR";
  if (code === "INTERNAL_ERROR") {
    logger.error(error.originalError);
    return { message: "서버 오류가 발생했습니다", extensions: { code } };
  }
  return error;
}
```
