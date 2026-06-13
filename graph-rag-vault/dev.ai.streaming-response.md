---
id: "dev.ai.streaming-response"
domain: "development.ai"
type: "pattern"
bloom_level: ""
tags: ["ai", "streaming", "sse", "ux"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.ai.streaming-response

> #286 Server-Sent Events (HTML5 Spec, W3C 2015; OpenAI Streaming API)

# AI 스트리밍 응답 가��드

## 핵심 원칙
- LLM 응답을 토큰 단위로 스트리밍하여 체감 응답 시간을 단축한다
- Server-Sent Events(SSE)를 기본 프로토콜로 사용한다
- 스트리밍 중 에러 처리와 연결 끊김을 안전하게 처리한다
- 전체 응답을 기다리지 않고 점진적으로 UI를 업데이트한다

## DO
- SSE(`text/event-stream`)로 스트리밍 엔드포인트를 구현한다
- 클라이언트에서 `ReadableStream`으로 토큰을 실시간 렌더링한다
- 스트리밍 중단(abort) 기능을 제공한다
- 스트리밍 완료 후 전체 응답을 저장/캐시한다

## DON'T
- 짧은 응답(한 문장)에 스트리밍을 불필요하게 적용하지 않는다
- 스트리밍 중 에러를 무시하지 않는다
- SSE 연결을 타임아웃 없이 유지하지 않는다
- 스트리밍 응답을 파싱하지 않고 raw로 출력하지 않는다

## 코드 예시
```typescript
// 서버: SSE 스트리밍 엔드포인트
app.post("/api/chat", async (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");

  const stream = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: req.body.messages,
    stream: true,
  });

  for await (const chunk of stream) {
    const content = chunk.choices[0]?.delta?.content;
    if (content) {
      res.write(`data: ${JSON.stringify({ content })}\n\n`);
    }
  }
  res.write("data: [DONE]\n\n");
  res.end();
});

// 클라이언트: 스트리밍 읽기
async function streamChat(messages: Message[], onToken: (token: string) => void) {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }),
  });

  const reader = response.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split("\n\n");
    buffer = lines.pop()!;

    for (const line of lines) {
      const data = line.replace("data: ", "");
      if (data === "[DONE]") return;
      const { content } = JSON.parse(data);
      onToken(content);
    }
  }
}
```
