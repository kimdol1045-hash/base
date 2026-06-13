---
id: "dev.ai.embedding"
domain: "development.ai"
type: "pattern"
bloom_level: ""
tags: ["ai", "embedding", "vector", "similarity"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.ai.embedding

> #282 Text Embeddings (Sentence-BERT, Reimers 2019; text-embedding-3, OpenAI 2024)

# 임베딩(Embedding) 가이드

## 핵심 원칙
- 텍스트를 의미론적 벡터 공간에 매핑하여 유사도를 계산한다
- 임베딩 모델 선택은 성능에 큰 영향을 미친다
- 용도(검색, 분류, 클러스터링)에 맞는 모델을 선택한다
- 벡터 DB에 저장하여 근사 최근접 이웃(ANN) 검색을 수행한다

## DO
- 용도에 맞는 임베딩 모델을 선택한다 (다국어: multilingual-e5-large)
- 입력 텍스트를 전처리하여 노이즈를 제거한다
- 차원 축소가 필요하면 PCA나 Matryoshka 표현을 활용한다
- 임베딩 결과를 캐시하여 비용을 절감한다
- 코사인 유사도를 기본 유사도 메트릭으로 사용한���

## DON'T
- 모든 용도에 동일한 임베딩 모델을 사용하지 않는다
- 너무 긴 텍스트를 임베딩하지 않는다 (모델별 최대 토큰 확인)
- 임베딩 모델을 자주 변경하지 않는다 (변경 시 전체 재임베딩 필요)
- 유클리드 거리로 정규화되지 않은 임베딩을 비교하지 않는다

## 코드 예��
```typescript
import OpenAI from "openai";
import { QdrantClient } from "@qdrant/js-client-rest";

const openai = new OpenAI();
const qdrant = new QdrantClient({ url: process.env.QDRANT_URL });

// 임베딩 생성
async function embed(texts: string[]): Promise<number[][]> {
  const response = await openai.embeddings.create({
    model: "text-embedding-3-small",
    input: texts,
    dimensions: 512, // 차원 축소 (비용/성능 트레이드오프)
  });
  return response.data.map(d => d.embedding);
}

// 벡터 DB에 저장
async function indexDocuments(docs: Document[]) {
  const texts = docs.map(d => d.content);
  const embeddings = await embed(texts);

  await qdrant.upsert("documents", {
    points: docs.map((doc, i) => ({
      id: doc.id,
      vector: embeddings[i],
      payload: { content: doc.content, source: doc.source },
    })),
  });
}

// 유사 문서 검색
async function search(query: string, limit = 5) {
  const [queryVector] = await embed([query]);
  return qdrant.search("documents", {
    vector: queryVector,
    limit,
    score_threshold: 0.7,
  });
}
```
