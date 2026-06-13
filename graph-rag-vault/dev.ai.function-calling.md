---
id: "dev.ai.function-calling"
domain: "development.ai"
type: "pattern"
bloom_level: ""
tags: ["ai", "function-calling", "tool-use", "api"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.ai.function-calling

> #289 Function Calling (OpenAI Function Calling, 2023; Anthropic Tool Use, 2024)

# Function Calling(Tool Use) 가이드

## 핵심 원칙
- LLM이 구조화된 함수 호출을 생성하여 외부 시스템과 상호작용한다
- 함수 스키마를 명확히 정의하여 LLM이 올바르게 호출하도록 한다
- 함수 실행 결과를 LLM에 다시 제공하여 최종 응답을 생성한다
- 병렬 함수 호출을 지원하여 효율성을 높인다

## DO
- 함수 이름, 설명, 파라미터를 명확하고 구체적으로 정의한다
- 파라미터에 enum, description을 포함하여 호출 정확도를 높인다
- 함수 실행 전 파라미터를 유효성 검사한다
- 함수 결과를 구조화된 형식으로 LLM에 반환한다

## DON'T
- 너무 많은 함수(20개 이상)를 한 번에 제공하지 않는다
- 함수 설명을 모호하게 작성하지 않는다
- LLM이 생성한 파라미터를 검증 없이 실행하지 않는다 (SQL 인젝션 등)
- 부작용이 있는 함수를 확인 없이 자동 실행하지 않는다

## ��드 예시
```typescript
import Anthropic from "@anthropic-ai/sdk";

const tools: Anthropic.Tool[] = [
  {
    name: "get_weather",
    description: "특정 도시의 현재 날씨 정보를 조회합니다",
    input_schema: {
      type: "object",
      properties: {
        city: { type: "string", description: "도시명 (예: 서울, 부산)" },
        unit: {
          type: "string",
          enum: ["celsius", "fahrenheit"],
          description: "온도 단위",
          default: "celsius",
        },
      },
      required: ["city"],
    },
  },
  {
    name: "search_products",
    description: "상품을 검색합니다",
    input_schema: {
      type: "object",
      properties: {
        query: { type: "string" },
        category: { type: "string", enum: ["전자기기", "의류", "식품"] },
        maxPrice: { type: "number", description: "최대 가격 (원)" },
      },
      required: ["query"],
    },
  },
];

// 함수 실행 맵
const toolHandlers: Record<string, (input: unknown) => Promise<string>> = {
  get_weather: async (input: { city: string; unit?: string }) => {
    const weather = await weatherApi.getCurrent(input.city);
    return JSON.stringify(weather);
  },
  search_products: async (input: { query: string; category?: string }) => {
    const products = await productApi.search(input);
    return JSON.stringify(products.slice(0, 5)); // 상위 5개만
  },
};

// Tool Use 루프
async function chat(userMessage: string) {
  let messages: Anthropic.MessageParam[] = [
    { role: "user", content: userMessage },
  ];

  while (true) {
    const response = await anthropic.messages.create({
      model: "claude-sonnet-4-6",
      tools,
      messages,
      max_tokens: 1024,
    });

    if (response.stop_reason === "end_turn") {
      return response.content[0].text;
    }

    messages.push({ role: "assistant", content: response.content });
    const toolResults = [];
    for (const block of response.content) {
      if (block.type === "tool_use") {
        const result = await toolHandlers[block.name](block.input);
        toolResults.push({ type: "tool_result", tool_use_id: block.id, content: result });
      }
    }
    messages.push({ role: "user", content: toolResults });
  }
}
```
