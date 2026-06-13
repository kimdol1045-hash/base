---
id: "dev.ai.memory-pattern"
domain: "development.ai"
type: "pattern"
bloom_level: ""
tags: ["ai", "memory", "conversation", "context"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.ai.memory-pattern

> #290 Conversational Memory (LangChain Memory, 2023; MemGPT, Packer et al. 2023)

# AI 대화 메모리 패턴 가이드

## 핵심 원칙
- 대화 맥락을 유지하여 자연스러운 멀티턴 대화를 지원한다
- 컨텍스트 윈도우 한계를 극복하기 위해 메모리 전략을 사용한다
- 단기 메모리(대화 내)와 장기 메모리(대화 간)를 분리한다
- 메모리 압축과 요약으로 토큰 효율성을 관리한다

## 메모리 유형
| 유형 | 설명 | 적합한 경우 |
|------|------|-------------|
| Buffer | 최근 N개 메시지 유지 | 짧은 대화 |
| Summary | 대화 요약을 유지 | 긴 대화 |
| Vector | 관련 메시지를 벡터 검색 | 광범위한 대화 이력 |
| Entity | 엔티티별 정보를 추출/유지 | 고객 상담 |

## DO
- 대화 길이에 따라 메모리 전략을 동적으로 선택한다
- 오래된 메시지를 요약하여 토큰을 절약한다
- 중요 정보(사용자 선호, 결정 사항)를 장기 메모리에 저장한다
- 메모리 검색 시 시간과 관련성을 모두 고려한다

## DON'T
- 모든 대화 이력을 컨텍스트에 넣지 않는다 (토큰 폭발)
- 민감한 개인 정보를 장기 메모리에 평문 저장하지 않는다
- 메모리가 오래되어 부정확해진 정보를 갱신하지 않고 방치하지 않는다
- 메모리 크기를 무한정 증가시키지 않는다

## 코드 예시
```typescript
interface Memory {
  shortTerm: Message[];      // 최근 대화 (Buffer)
  summary: string | null;    // 이전 대화 요약
  longTerm: VectorStore;     // 벡터 기반 장기 메모리
  entities: Map<string, string>; // 엔티티 메모리
}

class ConversationMemory {
  private maxShortTerm = 10;
  private memory: Memory;

  async addMessage(message: Message) {
    this.memory.shortTerm.push(message);

    // Buffer가 넘치면 요약 후 압축
    if (this.memory.shortTerm.length > this.maxShortTerm) {
      const oldest = this.memory.shortTerm.splice(0, 5);
      this.memory.summary = await this.summarize(
        this.memory.summary,
        oldest,
      );
    }

    // 중요 정보는 장기 메모리에 저장
    const entities = await this.extractEntities(message);
    for (const [key, value] of entities) {
      this.memory.entities.set(key, value);
    }
  }

  async buildContext(currentQuery: string): Promise<string> {
    const parts: string[] = [];

    // 1. 대화 요약
    if (this.memory.summary) {
      parts.push(`[이전 대화 요약]\n${this.memory.summary}`);
    }

    // 2. 관련 장기 메모리 검색
    const relevant = await this.memory.longTerm.search(currentQuery, 3);
    if (relevant.length > 0) {
      parts.push(`[관련 이전 대화]\n${relevant.map(r => r.content).join("\n")}`);
    }

    // 3. 최근 대화
    parts.push(`[최근 대화]\n${this.memory.shortTerm.map(formatMessage).join("\n")}`);

    return parts.join("\n\n");
  }

  private async summarize(existingSummary: string | null, messages: Message[]) {
    return llm.chat({
      messages: [{
        role: "user",
        content: `기존 요약: ${existingSummary ?? "없음"}
        새 메시지: ${messages.map(formatMessage).join("\n")}
        위 내용을 통합하여 200자 이내로 요약하세요.`,
      }],
    });
  }
}
```
