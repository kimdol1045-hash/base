---
id: "dev.backend.database.nosql-patterns"
domain: "development.database"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#108 CAP Theorem (Brewer, 2000)"
tags: [database, nosql, mongodb, dynamodb, denormalization, document-db, data-modeling]
---

# dev.backend.database.nosql-patterns

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.database`  
> **Type**: `pattern`  
> **Theory**: #108 CAP Theorem (Brewer, 2000)  
> **Tokens**: 500

## Content

NoSQL 데이터 모델링 패턴 (액세스 패턴 중심으로 데이터를 설계한다):

### RDBMS vs NoSQL 설계 사고방식
- RDBMS: "데이터가 어떤 구조인가?" → 정규화 → 쿼리 작성
- NoSQL: "어떤 쿼리가 필요한가?" → 액세스 패턴 정의 → 데이터 구조 결정

### 1. Document DB (MongoDB) — 임베딩 vs 참조

| 기준 | 임베딩 (Embed) | 참조 (Reference) |
|------|---------------|-----------------|
| 읽기 패턴 | 함께 조회 (1:1, 1:few) | 독립 조회 (1:many, M:N) |
| 문서 크기 | 16MB 미만 유지 | 무제한 |
| 업데이트 빈도 | 부모와 함께 갱신 | 독립 갱신이 잦음 |
| 일관성 요구 | 강한 일관성 필요 | 결과적 일관성 허용 |

DO:
```typescript
// ✅ 임베딩 — 주문과 주문 항목은 항상 함께 조회
interface Order {
  _id: ObjectId;
  userId: ObjectId;
  status: "pending" | "confirmed" | "shipped";
  items: Array<{            // 임베딩 (bounded array, 최대 50개)
    productId: ObjectId;
    name: string;           // 비정규화 (조회 시 JOIN 불필요)
    price: number;
    quantity: number;
  }>;
  shippingAddress: {        // 임베딩 (1:1 관계)
    street: string;
    city: string;
    zipCode: string;
  };
  totalAmount: number;
  createdAt: Date;
}

// ✅ 참조 — 상품 리뷰는 독립적으로 조회/페이지네이션
interface Review {
  _id: ObjectId;
  productId: ObjectId;      // 참조 (1:many, 수천 개 가능)
  userId: ObjectId;
  rating: number;
  content: string;
  createdAt: Date;
}
```

### 2. Single-Table Design (DynamoDB)
하나의 테이블에 여러 엔티티를 PK/SK 패턴으로 저장한다.

```typescript
// ✅ 유저 + 주문을 단일 테이블에 저장
// PK: USER#<userId>, SK: PROFILE            → 유저 프로필
// PK: USER#<userId>, SK: ORDER#<orderId>    → 유저의 주문
// PK: ORDER#<orderId>, SK: ITEM#<itemId>    → 주문 항목

const params = {
  TableName: "AppTable",
  KeyConditionExpression: "PK = :pk AND begins_with(SK, :sk)",
  ExpressionAttributeValues: {
    ":pk": `USER#${userId}`,
    ":sk": "ORDER#",        // 해당 유저의 모든 주문 조회
  },
};
```

### 3. 비정규화 전략
```typescript
// ✅ 자주 함께 조회되는 데이터를 복제 (읽기 최적화)
interface Post {
  _id: ObjectId;
  title: string;
  content: string;
  author: {
    _id: ObjectId;
    name: string;           // 비정규화: Users에서 복제
    avatarUrl: string;      // 비정규화: Users에서 복제
  };
  commentCount: number;     // 비정규화: 카운트 캐싱
}

// ✅ 업데이트 시 비정규화 데이터 동기화 (Change Streams)
db.collection("users").watch().on("change", async (change) => {
  if (change.operationType === "update") {
    await db.collection("posts").updateMany(
      { "author._id": change.documentKey._id },
      { $set: { "author.name": change.fullDocument.name } }
    );
  }
});
```

DON'T:
```typescript
// ❌ NoSQL을 RDBMS처럼 정규화 — 매 조회마다 N+1 쿼리
interface Post { authorId: ObjectId; }  // 참조만
// 목록 조회 시: posts 조회 → 각 post의 author 개별 조회 (N+1)

// ❌ 무한 증가 배열 — 문서 크기 16MB 초과 위험
interface User {
  followers: ObjectId[];    // 팔로워 100만 명이면? → 별도 컬렉션으로 분리
}

// ❌ 액세스 패턴 분석 없이 설계 — 나중에 전체 재설계 필요
```

### 선택 기준
- 읽기/쓰기 비율 8:2 이상 → 비정규화 적극 활용
- 관계가 복잡 (3단계 이상 JOIN) → RDBMS 유지 검토
- 수평 확장 필수 → DynamoDB, Cassandra (AP 시스템)
