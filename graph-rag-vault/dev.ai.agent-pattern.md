---
id: "dev.ai.agent-pattern"
domain: "development.ai"
type: "pattern"
bloom_level: ""
tags: ["ai", "agent", "tool-use", "reasoning"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.ai.agent-pattern

> #283 AI Agent Patterns (LangChain ReAct, Yao et al. 2022)

# AI 에이전트 패턴 가이드

## 핵심 원칙
- 에이전트는 LLM이 도구(Tool)를 사용하여 작업을 수행하는 패턴이다
- ReAct(Reasoning + Acting) 루프로 추론과 실행을 반��한다
- 도구 정의를 명확히 하여 LLM이 올바르게 선택하도록 한다
- 에이전트의 행동 범위를 제한하여 안전성을 확보한다

## DO
- 각 도구의 이름, 설명, 파라미터를 명확히 정의한다
- 최대 실행 단계(max iterations)를 설정한다
- 도구 실행 결과를 에이전트에 피드백한다
- 에이전트의 추론 과정(thought)을 로깅한다
- 위험한 도구(삭제, 결제)에는 확인 단계를 추가한다

## DON'T
- 에이전트에게 무제한 도구 접근 권한을 주지 않는다
- 도구 실행 결과를 검증하지 않고 사용자에게 전달하지 않는다
- 무한 루프에 빠질 수 있는 에이전트를 방치하지 않는다
- 모든 작업에 에이전트를 사용하지 않는다 (단순 작업은 직접 처리)

## 코드 예시
```typescript
import Anthropic from "@anthropic-ai/sdk";

const tools = [
  {
    name: "search_database",
    description: "데이터베이스에서 사용자 정보를 검색합니다",
    input_schema: {
      type: "object",
      properties: {
        query: { type: "string", description: "검색 쿼리" },
        limit: { type: "number", description: "최대 결과 수", default: 10 },
      },
      required: ["query"],
    },
  },
  {
    name: "send_email",
    description: "이메일을 전송합니다. 반드시 사용자 확인 후 실행하세요.",
    input_schema: {
      type: "object",
      properties: {
        to: { type: "string" },
        subject: { type: "string" },
        body: { type: "string" },
      },
      required: ["to", "subject", "body"],
    },
  },
];

// ReAct 루프
async function runAgent(userMessage: string, maxSteps = 10) {
  const messages = [{ role: "user", content: userMessage }];

  for (let step = 0; step < maxSteps; step++) {
    const response = await anthropic.messages.create({
      model: "claude-sonnet-4-20250514",
      tools,
      messages,
      max_tokens: 4096,
    });

    if (response.stop_reason === "end_turn") {
      return response.content; // 최종 응답
    }

    // 도구 호출 처리
    for (const block of response.content) {
      if (block.type === "tool_use") {
        const result = await executeTool(block.name, block.input);
        messages.push({ role: "assistant", content: response.content });
        messages.push({
          role: "user",
          content: [{ type: "tool_result", tool_use_id: block.id, content: result }],
        });
      }
    }
  }
}
```
