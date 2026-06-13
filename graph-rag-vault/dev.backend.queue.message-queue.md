---
id: "dev.backend.queue.message-queue"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["queue", "message-queue", "async", "backend"]
brain_region: "BRAINSTEM"
token_estimate: 430
---

# dev.backend.queue.message-queue

> #210 Message Queue Fundamentals (Enterprise Integration Patterns, Hohpe 2003)

# 메시지 큐 설계 가이드

## 핵심 원칙
- 동기 처리가 불필요한 작업은 메시지 큐로 비동기 처리한다
- 메시지는 멱등성(idempotent)을 보장하도록 설계한다
- 메시지 순서 보장이 필요한 경우 파티션 키를 활용한다
- 소비자(Consumer)는 at-least-once 전달을 가정하고 중복 처리를 대비한다

## DO
- 메시지에 고유 ID를 부여하여 중복 감지에 사용한다
- 메시지 스키마를 버전 관리한다 (하위 호환성 유지)
- Consumer 그룹을 활용하여 수평 확장한다
- 처리 실패 시 재시도 횟수와 간격을 설정한다

## DON'T
- 메시지 본문에 대용량 데이터를 직접 포함하지 않는다 (참조 URL 사용)
- 무한 재시도를 설정하지 않는다 (최대 재시도 후 DLQ로 이동)
- 단일 큐에 모든 종류의 메시지를 혼합하지 않는다
- 메시지 처리 순서에 의존하는 로직을 기본으로 하지 않는다

## 코드 예시
```typescript
import { SQSClient, SendMessageCommand } from "@aws-sdk/client-sqs";

interface QueueMessage<T> {
  id: string;
  type: string;
  version: number;
  payload: T;
  timestamp: string;
  metadata: { correlationId: string; source: string };
}

// Producer
async function publishMessage<T>(queueUrl: string, msg: QueueMessage<T>) {
  const client = new SQSClient({});
  await client.send(new SendMessageCommand({
    QueueUrl: queueUrl,
    MessageBody: JSON.stringify(msg),
    MessageDeduplicationId: msg.id,
    MessageGroupId: msg.type,
  }));
}

// Consumer (멱등성 보장)
async function handleMessage(msg: QueueMessage<OrderCreated>) {
  const processed = await redis.get(`processed:${msg.id}`);
  if (processed) return; // 중복 메시지 무시

  await processOrder(msg.payload);
  await redis.set(`processed:${msg.id}`, "1", "EX", 86400);
}
```
