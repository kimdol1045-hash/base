---
id: "dev.backend.patterns.llm-integration"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#109 Event-Driven Architecture, #125 Resilience Engineering"
tags: [backend, llm, anthropic, streaming, token-management, rate-limit]
---

# dev.backend.patterns.llm-integration

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #109 Event-Driven Architecture, #125 Resilience Engineering  
> **Tokens**: 500

## Content

LLM API 연동 패턴 (안정적이고 비용 효율적인 LLM 통합을 구현한다):

### Streaming 응답 (SSE)
```typescript
import Anthropic from '@anthropic-ai/sdk';

// DO: 스트리밍으로 체감 응답 시간 단축 (TTFB < 500ms)
async function streamChat(prompt: string, res: Response) {
  const client = new Anthropic();

  const stream = client.messages.stream({
    model: 'claude-sonnet-4-20250514',
    max_tokens: 1024,
    messages: [{ role: 'user', content: prompt }],
  });

  // SSE 형식으로 클라이언트에 전달
  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    Connection: 'keep-alive',
  });

  stream.on('text', (text) => {
    res.write(`data: ${JSON.stringify({ text })}\n\n`);
  });

  const finalMessage = await stream.finalMessage();
  res.write(`data: ${JSON.stringify({
    done: true,
    usage: finalMessage.usage, // 토큰 사용량 추적
  })}\n\n`);
  res.end();
}
```

### 토큰 예산 관리
```typescript
// DO: 요청별 토큰 예산 설정 + 비용 추적
interface TokenBudget {
  maxInputTokens: number;   // 시스템 + 사용자 프롬프트
  maxOutputTokens: number;  // 응답
  estimatedCost: number;    // USD
}

const BUDGETS: Record<string, TokenBudget> = {
  chat:    { maxInputTokens: 4000,  maxOutputTokens: 1024, estimatedCost: 0.02 },
  summary: { maxInputTokens: 8000,  maxOutputTokens: 2048, estimatedCost: 0.05 },
  analysis:{ maxInputTokens: 16000, maxOutputTokens: 4096, estimatedCost: 0.15 },
};

// 요청 전 토큰 수 검증
function validateTokenBudget(input: string, type: keyof typeof BUDGETS) {
  const budget = BUDGETS[type];
  const estimatedTokens = Math.ceil(input.length / 4); // 근사치
  if (estimatedTokens > budget.maxInputTokens) {
    throw new Error(`입력이 토큰 예산 초과: ${estimatedTokens} > ${budget.maxInputTokens}`);
  }
}
```

### Rate Limit 처리 (429 Retry)
```typescript
// DO: 지수 백오프로 429 재시도
async function callWithRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3,
): Promise<T> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error: any) {
      if (error.status === 429 && attempt < maxRetries) {
        const retryAfter = error.headers?.['retry-after']
          ? parseInt(error.headers['retry-after']) * 1000
          : Math.pow(2, attempt) * 1000; // 1s, 2s, 4s
        await new Promise(r => setTimeout(r, retryAfter));
        continue;
      }
      throw error;
    }
  }
  throw new Error('Max retries exceeded');
}
```

### Structured Output 검증
```typescript
import { z } from 'zod';

// DO: LLM 출력을 스키마로 검증
const AnalysisSchema = z.object({
  sentiment: z.enum(['positive', 'negative', 'neutral']),
  confidence: z.number().min(0).max(1),
  summary: z.string().max(200),
});

const raw = await callLLM('다음 리뷰를 분석해주세요. JSON으로 응답.');
const parsed = AnalysisSchema.safeParse(JSON.parse(raw));
if (!parsed.success) {
  // 재시도 또는 fallback 처리
  logger.warn('LLM 출력 검증 실패', parsed.error);
}
```

DON'T:
```typescript
// ❌ 블로킹 응답 (스트리밍 미사용) → 사용자 10초 대기
const response = await client.messages.create({ ... });
res.json({ text: response.content[0].text });

// ❌ 토큰 예산 없이 무제한 입력 → 비용 폭발
const response = await client.messages.create({
  messages: [{ role: 'user', content: entireDocument }], // 100K 토큰?
});

// ❌ Rate limit 무시 → 연쇄 실패
const response = await client.messages.create({ ... }); // 429 시 그대로 에러

// ❌ LLM 출력 무조건 신뢰 → JSON 파싱 에러, 잘못된 값
const data = JSON.parse(response.content[0].text); // 파싱 실패 가능
await db.insert(data); // 검증 없이 DB 저장
```

### 비용 추적
- 요청마다 input/output 토큰 수 로깅
- 일별/사용자별 비용 대시보드 구축
- 월 예산 한도 설정 + 80% 도달 시 알림

## Connections

### CO_CREATES (1)

- → [[dev.backend.patterns.rag-pattern]] `w=0.6`
