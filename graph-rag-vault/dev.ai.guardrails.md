---
id: "dev.ai.guardrails"
domain: "development.ai"
type: "pattern"
bloom_level: ""
tags: ["ai", "guardrails", "safety", "security"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.ai.guardrails

> #285 AI Safety Guardrails (OWASP Top 10 for LLM Applications, 2023)

# AI 가드레일(Guardrails) 가이��

## 핵심 원칙
- LLM 입출력에 안전장치를 설정하여 유해한 사용을 방지한다
- 프롬프트 인젝션, 데이터 유출, 유해 콘텐츠를 차단한다
- 입력 검증(Input Guard)과 출력 검증(Output Guard)을 모두 적용한다
- 가드레일 우회 시도를 로깅하고 모니터링한다

## DO
- 입력에서 프롬프트 인젝션 패턴을 감지한다
- 출력에서 개인정보(PII), 민감 데이터를 필터링한다
- 허용된 주제/도메인을 벗어나는 요청을 차단한다
- 토큰 사용량에 상한을 설정한다
- 콘텐츠 안전성 분류기를 출력에 적용한다

## DON'T
- LLM의 자체 판단만으로 안전성을 보장하지 않는다
- 시스템 프롬프트에 민감한 정보를 포함하지 않는다
- 가드레일 없이 LLM을 사용자 입력에 직접 노출하지 않는다
- 모든 가드레일을 LLM 기반으로만 구현하지 않는다 (규칙 기반 병행)

## 코드 예시
```typescript
// 입력 가드레일
function validateInput(input: string): { safe: boolean; reason?: string } {
  // 1. 길이 제한
  if (input.length > 10_000) {
    return { safe: false, reason: "입력이 너무 깁니다" };
  }

  // 2. 프롬프트 인젝션 패턴 감지
  const injectionPatterns = [
    /ignore\s+(previous|above|all)\s+instructions/i,
    /you\s+are\s+now/i,
    /system\s*:\s*/i,
    /\[INST\]/i,
  ];
  for (const pattern of injectionPatterns) {
    if (pattern.test(input)) {
      return { safe: false, reason: "잠재적 프롬프트 인젝션 감지" };
    }
  }

  return { safe: true };
}

// 출력 가드레일
function validateOutput(output: string): string {
  // PII 마스킹
  let sanitized = output
    .replace(/\b\d{3}-\d{2}-\d{4}\b/g, "[SSN]")
    .replace(/\b[\w.-]+@[\w.-]+\.\w{2,}\b/g, "[EMAIL]")
    .replace(/\b\d{13,16}\b/g, "[CARD]");

  return sanitized;
}

// 전체 파이프라인
async function safeLLMCall(userInput: string) {
  const inputCheck = validateInput(userInput);
  if (!inputCheck.safe) {
    logger.warn({ reason: inputCheck.reason }, "입력 가드레일 차단");
    return { error: "요청을 처리할 수 없습니다" };
  }

  const response = await llm.chat({ messages: [/* ... */] });
  const safeOutput = validateOutput(response.content);

  return { result: safeOutput };
}
```
