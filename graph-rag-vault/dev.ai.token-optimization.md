---
id: "dev.ai.token-optimization"
domain: "development.ai"
type: "pattern"
bloom_level: ""
tags: ["ai", "token", "optimization", "cost"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.ai.token-optimization

> #287 Token Optimization (Anthropic Prompt Engineering Guide, 2024)

# 토큰 최적화 가이드

## 핵심 ��칙
- 토큰 사용량은 비용과 지연시간에 직접 영향을 미친다
- 프롬프트를 간결하게 작성하되 정보 손실은 방지한다
- 용도에 맞는 모델 크기를 선택한다 (소형 모델 우선 시도)
- 토큰 사용량을 모니터링하고 예산을 설정한다

## DO
- 시스템 프롬프트를 캐싱하여 반복 토큰을 절약한다
- 입력 텍스트를 전처리하여 불필요한 공백, 반복을 제거한다
- 단순 작업은 소형 모델(Haiku), 복잡한 작업은 대형 모델(Opus)을 사용한다
- `max_tokens`를 적절히 설정하여 불필요한 출력을 방지한다
- 토큰 사용량을 요청별로 추적한다

## DON'T
- 모든 요청에 최대 성능 모델을 사용하지 않는다
- 불필요하게 긴 시스템 프롬프트를 매 요청마다 전송하지 않는다
- 토큰 제한 없이 모델을 호출하지 않는다
- 응답 형식을 지정하지 않아 모델이 불필요하게 길게 답변하도록 하지 않는다

## 모델 선택 가이드
| 작업 | 권장 모델 | 이유 |
|------|-----------|------|
| 분류/태깅 | Haiku | 빠르고 저비용 |
| 요약/변환 | Sonnet | 비용 대비 성능 |
| 복잡한 추론 | Opus | 최고 성능 필요 |
| 코드 생성 | Sonnet/Opus | 정확도 중요 |

## 코드 예���
```typescript
// 토큰 사용량 추적 미들웨어
async function trackTokenUsage<T>(
  fn: () => Promise<{ result: T; usage: TokenUsage }>,
  metadata: { userId: string; feature: string },
): Promise<T> {
  const start = performance.now();
  const { result, usage } = await fn();
  const duration = performance.now() - start;

  await db.tokenUsage.create({
    data: {
      userId: metadata.userId,
      feature: metadata.feature,
      inputTokens: usage.input_tokens,
      outputTokens: usage.output_tokens,
      model: usage.model,
      costUsd: calculateCost(usage),
      durationMs: duration,
      timestamp: new Date(),
    },
  });

  return result;
}

// 모델 라우터: 복잡도에 따라 모델 선택
function selectModel(task: TaskType): string {
  const modelMap: Record<TaskType, string> = {
    classification: "claude-haiku-4-5-20251001",
    summarization: "claude-sonnet-4-6",
    complex_reasoning: "claude-opus-4-6",
  };
  return modelMap[task];
}
```
