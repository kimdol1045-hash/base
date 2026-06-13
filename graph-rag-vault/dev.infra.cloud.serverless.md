---
id: "dev.infra.cloud.serverless"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "cloud", "serverless", "lambda", "functions"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# dev.infra.cloud.serverless

> #266 Serverless Architecture (AWS Lambda, 2014; Serverless Framework)

# 서버리스 아키텍처 가이드

## 핵심 원칙
- 서버 관리 없이 코드 실행에만 집중한다 (FaaS)
- 사용한 만큼만 비용을 지불한다 (Pay per invocation)
- Cold Start를 최소화하는 설계를 한다
- 상태를 함수 외부(DB, S3, Redis)에 저장한다

## DO
- 이벤트 기반 처리(API Gateway, SQS, S3 이벤트)에 활용한다
- 함수 크기를 작게 유지한다 (번들 최소화)
- Provisioned Concurrency로 중요 API의 Cold Start를 제거한다
- 환경변수로 설정을 주입한다

## DON'T
- 장시간 실행되는 작업에 Lambda를 사용하지 않는다 (15분 제한)
- VPC 내부 Lambda를 불필요하게 사용하지 않는다 (Cold Start 증가)
- 함수 안에서 전역 상태에 의존하지 않는다
- 동기 호출 체인을 길게 만들지 않는다 (비동기 이벤트 활용)

## 코드 예시
```typescript
// AWS Lambda 핸들러 (Node.js)
import { APIGatewayProxyHandler } from "aws-lambda";
import { DynamoDBClient } from "@aws-sdk/client-dynamodb";

// 핸들러 외부: Cold Start 시 한 번만 초기화
const dynamodb = new DynamoDBClient({});

export const handler: APIGatewayProxyHandler = async (event) => {
  try {
    const { id } = event.pathParameters ?? {};
    if (!id) {
      return { statusCode: 400, body: JSON.stringify({ error: "ID 필수" }) };
    }

    const result = await dynamodb.send(new GetItemCommand({
      TableName: process.env.TABLE_NAME!,
      Key: { id: { S: id } },
    }));

    if (!result.Item) {
      return { statusCode: 404, body: JSON.stringify({ error: "Not found" }) };
    }

    return {
      statusCode: 200,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ data: unmarshall(result.Item) }),
    };
  } catch (err) {
    console.error(err);
    return { statusCode: 500, body: JSON.stringify({ error: "서버 오류" }) };
  }
};
```
