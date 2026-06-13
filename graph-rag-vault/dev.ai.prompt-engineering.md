---
id: "dev.ai.prompt-engineering"
domain: "development.ai"
type: "pattern"
bloom_level: ""
tags: ["ai", "prompt-engineering", "llm", "gpt"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.ai.prompt-engineering

> #279 Prompt Engineering (OpenAI Best Practices, 2023)

# 프롬프트 엔지니어링 가이드

## 핵심 원칙
- 명확하고 구체적인 지시를 제공한다
- 역할(Role), 맥락(Context), 형식(Format)을 구조화한다
- Few-shot 예시로 기대 출력을 보여준다
- 반복 실험으로 최적의 프롬프트를 찾는다

## DO
- 시스템 프롬프트에 역할과 제약 조건을 명시한다
- 구분자(```, ---, ###)로 입력 데이터를 분리한다
- 출력 형식을 JSON Schema 등으로 명확히 지정한다
- Chain-of-Thought(CoT)로 복잡한 추론을 유도한다
- 프롬프트를 버전 관리하고 성능을 측정한다

## DON'T
- 모호한 지시("잘 해줘")를 사용하지 않는다
- 하나의 프롬프트에 너무 많은 작업을 요구하지 않는다
- 프롬프트를 코드에 하드코딩하지 않는다 (설정 파일로 분리)
- 프롬프트 인젝션 방어를 무시하��� 않는다

## 코드 예시
```typescript
// 구조화된 프롬프트 템플릿
const systemPrompt = `당신은 코드 리뷰 전문가입니다.

## 역할
주어진 코드의 잠재적 문제를 찾아 개선안을 제시합니다.

## 출력 형식
반드시 아래 JSON 형식으로 응답하세요:
{
  "issues": [
    {
      "severity": "critical" | "warning" | "info",
      "line": number,
      "description": "문제 설명",
      "suggestion": "개선 코드"
    }
  ],
  "summary": "전체 코드 품질 요약 (1-2문장)"
}

## 제약 조건
- 최대 5개의 이슈만 보고합니다
- 스타일 관련 이슈는 제외합니다
- 보안 이슈는 반드시 포함합니다`;

const userPrompt = `다음 코드를 리뷰해주세요:

\`\`\`typescript
${code}
\`\`\``;

const response = await llm.chat({
  messages: [
    { role: "system", content: systemPrompt },
    { role: "user", content: userPrompt },
  ],
  response_format: { type: "json_object" },
  temperature: 0.2, // 일관성을 위해 낮은 temperature
});
```
