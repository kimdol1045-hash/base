---
id: "dev.ai.rag-pattern"
domain: "development.ai"
type: "pattern"
bloom_level: ""
tags: ["ai", "rag", "retrieval", "embedding", "vector-search"]
brain_region: "CORTEX"
token_estimate: 450
---

# dev.ai.rag-pattern

> #280 RAG (Lewis et al., Retrieval-Augmented Generation 2020)

# RAG (Retrieval-Augmented Generation) 가이드

## 핵심 원칙
- 외부 지식을 검색하여 LLM의 응답 정확도를 높인다
- 문서를 청크로 분할 → 임베딩 → 벡터 DB 저장 → 검색 → 생성
- 환각(Hallucination)을 줄이고, 근거 기반 응답을 생성한다
- 검색 품질이 전체 성능을 결정한다

## DO
- 청크 크기를 실험적으로 조정한다 (보통 500-1000 토큰)
- 청크 간 오버랩(20%)을 두어 문맥 손실을 방지한다
- Hybrid Search(키워드 + 벡터)를 활용한다
- 검색된 문서의 관련성 점수를 필터링한다
- 출처(source)를 응답에 포함한다

## DON'T
- 모든 문서를 하나의 벡터 공간에 혼합하지 않는다 (네임스페이스 분리)
- 검색 결과를 검증 없이 모두 컨텍스트에 넣지 않는다
- 컨텍스트 윈도우를 초과하는 양의 문서를 넣지 않는다
- 임베딩 모델과 검색 대상의 언어/도메인 불일치를 무시하지 않는다

## 코드 예시
```typescript
import { OpenAIEmbeddings } from "@langchain/openai";
import { QdrantVectorStore } from "@langchain/qdrant";

// 1. 문서 청킹 및 임베딩
const splitter = new RecursiveCharacterTextSplitter({
  chunkSize: 800,
  chunkOverlap: 200,
});
const chunks = await splitter.splitDocuments(documents);

const vectorStore = await QdrantVectorStore.fromDocuments(chunks, embeddings, {
  collectionName: "knowledge-base",
});

// 2. 검색 + 생성
async function ragQuery(question: string): Promise<RAGResponse> {
  // 관련 문서 검색
  const retrieved = await vectorStore.similaritySearchWithScore(question, 5);
  const relevant = retrieved.filter(([_, score]) => score > 0.7);

  // 컨텍스트 구성
  const context = relevant
    .map(([doc]) => `[출처: ${doc.metadata.source}]\n${doc.pageContent}`)
    .join("\n\n---\n\n");

  const response = await llm.chat({
    messages: [
      {
        role: "system",
        content: `참고 문서를 기반으로 질문에 답하세요.
        문서에 없는 내용은 "관련 정보를 찾을 수 없습니다"라고 답하세요.
        답변 마지막에 참조한 출처를 나열하세요.`,
      },
      { role: "user", content: `참고 문서:\n${context}\n\n질문: ${question}` },
    ],
  });

  return {
    answer: response.content,
    sources: relevant.map(([doc]) => doc.metadata.source),
  };
}
```
