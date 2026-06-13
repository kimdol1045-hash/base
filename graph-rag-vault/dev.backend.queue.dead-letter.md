---
id: "dev.backend.queue.dead-letter"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["queue", "dead-letter", "error-handling", "reliability"]
brain_region: "BRAINSTEM"
token_estimate: 400
---

# dev.backend.queue.dead-letter

> #211 Dead Letter Queue Pattern (AWS Well-Architected, 2023)

# Dead Letter Queue(DLQ) 설계 가이드

## 핵심 원칙
- 최대 재시도 횟수를 초과한 메시지는 DLQ로 이동시킨다
- DLQ 메시지를 모니터링하고 알림을 설정한다
- DLQ 메시지를 분석하여 근본 원인을 파악한다
- 원인 해결 후 DLQ 메시지를 원래 큐로 재처리(redrive)한다

## DO
- 각 메인 큐에 대응하는 DLQ를 생성한다
- DLQ 메시지에 실패 원인과 재시도 횟수를 메타데이터로 기록한다
- DLQ 메시지 수에 대한 알림 임계값을 설정한다
- 재처리(redrive) 스크립트를 준비한다
- DLQ 보존 기간을 메인 큐보다 길게 설정한다

## DON'T
- DLQ 메시지를 무시하고 방치하지 않는다
- DLQ 없이 무한 재시도를 설정하지 않는다
- 재처리 시 동일한 에러가 반복되지 않는지 확인하지 않고 일괄 재처리하지 않는다
- DLQ의 보존 기간을 너무 짧게 설정하지 않는다

## 코드 예시
```typescript
// DLQ 설정 (AWS SQS)
const mainQueueConfig = {
  RedrivePolicy: JSON.stringify({
    deadLetterTargetArn: dlqArn,
    maxReceiveCount: 3, // 3회 실패 시 DLQ로 이동
  }),
};

// DLQ 모니터링
async function monitorDLQ(dlqUrl: string) {
  const attrs = await sqs.getQueueAttributes({
    QueueUrl: dlqUrl,
    AttributeNames: ["ApproximateNumberOfMessages"],
  });
  const count = Number(attrs.Attributes?.ApproximateNumberOfMessages ?? 0);
  if (count > 0) {
    await alerting.notify({
      severity: "warning",
      message: `DLQ에 ${count}개의 미처리 메시지가 있습니다`,
      queue: dlqUrl,
    });
  }
}

// DLQ 재처리 (redrive)
async function redriveDLQ(dlqUrl: string, mainQueueUrl: string) {
  const messages = await sqs.receiveMessage({
    QueueUrl: dlqUrl, MaxNumberOfMessages: 10,
  });
  for (const msg of messages.Messages ?? []) {
    await sqs.sendMessage({ QueueUrl: mainQueueUrl, MessageBody: msg.Body! });
    await sqs.deleteMessage({ QueueUrl: dlqUrl, ReceiptHandle: msg.ReceiptHandle! });
  }
}
```
