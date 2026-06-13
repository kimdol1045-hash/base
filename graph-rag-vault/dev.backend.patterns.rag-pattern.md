---
id: "dev.backend.patterns.rag-pattern"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "rag", "vector-db", "embedding", "chunking", "llm"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.patterns.rag-pattern

> #108 Data Architecture

RAG 패턴 (외부 지식을 검색하여 LLM 응답의 정확성과 최신성을 보장한다):

### RAG 파이프라인
```
Query → Embed → Retrieve → Rerank → Augment → Generate
  ↓        ↓        ↓          ↓         ↓          ↓
사용자   벡터화   Top-K     관련성    프롬프트    LLM
질문              검색      재정렬    조합       응답
```

### Chunking 전략
| 전략 | 청크 크기 | 용도 | 특징 |
|------|-----------|------|------|
| Fixed-size | 512 tokens | 범용 | 단순, 빠름 |
| Semantic | 문단/섹션 단위 | 문서 | 의미 보존 |
| Recursive | AST 기반 | 코드 | 함수/클래스 단위 |

### 임베딩 + 벡터 저장
```typescript
import OpenAI from 'openai';
import { pgvector } from 'pgvector';

const openai = new OpenAI();

// DO: 청크 간 10-20% 오버랩으로 맥락 유지
function chunkText(text: string, size = 512, overlap = 64): string[] {
  const tokens = tokenize(text);
  const chunks: string[] = [];
  for (let i = 0; i < tokens.length; i += size - overlap) {
    chunks.push(detokenize(tokens.slice(i, i + size)));
  }
  return chunks;
}

// 임베딩 생성
async function embed(texts: string[]): Promise<number[][]> {
  const res = await openai.embeddings.create({
    model: 'text-embedding-3-small', // 1536차원, $0.02/1M tokens
    input: texts,
  });
  return res.data.map(d => d.embedding);
}

// pgvector에 저장
async function storeChunks(chunks: string[], docId: string) {
  const embeddings = await embed(chunks);
  for (let i = 0; i < chunks.length; i++) {
    await db.query(
      `INSERT INTO documents (doc_id, chunk_index, content, embedding)
       VALUES ($1, $2, $3, $4)`,
      [docId, i, chunks[i], pgvector.toSql(embeddings[i])]
    );
  }
}
```

### 검색 + Reranking
```typescript
// DO: Top-K 검색 후 Reranker로 관련성 재정렬
async function retrieve(query: string, topK = 20, finalK = 5) {
  const queryEmbedding = (await embed([query]))[0];

  // 1단계: 벡터 유사도로 후보 검색 (빠르지만 부정확할 수 있음)
  const candidates = await db.query(
    `SELECT content, doc_id, 1 - (embedding <=> $1) as similarity
     FROM documents
     ORDER BY embedding <=> $1
     LIMIT $2`,
    [pgvector.toSql(queryEmbedding), topK]
  );

  // 2단계: Reranker로 정밀 재정렬
  const reranked = await rerank(query, candidates.rows, finalK);

  return reranked;
}

// Cross-encoder reranking (더 정확한 관련성 판단)
async function rerank(query: string, docs: Doc[], topK: number) {
  const scored = await Promise.all(
    docs.map(async (doc) => ({
      ...doc,
      score: await crossEncoderScore(query, doc.content),
    }))
  );
  return scored.sort((a, b) => b.score - a.score).slice(0, topK);
}
```

### 프롬프트 조합 (Augment)
```typescript
// DO: 출처 명시 + 컨텍스트 윈도우 관리
function buildPrompt(query: string, contexts: Doc[]): string {
  const contextBlock = contexts
    .map((c, i) => `[출처 ${i + 1}: ${c.doc_id}]\n${c.content}`)
    .join('\n\n');

  return `다음 참고 자료를 기반으로 질문에 답변하세요.
참고 자료에 없는 내용은 "해당 정보가 없습니다"라고 답하세요.
답변에 사용한 출처 번호를 반드시 표기하세요.

## 참고 자료
${contextBlock}

## 질문
${query}`;
}
```

DON'T:
```typescript
// ❌ 오버랩 없는 청킹 → 문맥 단절
for (let i = 0; i < tokens.length; i += 512) {
  chunks.push(tokens.slice(i, i + 512)); // 경계에서 문장 잘림
}

// ❌ Reranking 없이 벡터 검색 결과만 사용
const results = await vectorSearch(query, 5); // 유사도 높지만 관련 없는 결과 포함 가능

// ❌ 전체 문서를 하나의 청크로
await embed([entireDocument]); // 50페이지 문서를 하나로 → 검색 정밀도 급락

// ❌ 출처 없는 답변 → 할루시네이션 검증 불가
return llmResponse.text; // 어떤 문서에서 왔는지 알 수 없음
```

### 성능 기준
- 검색 지연: p95 < 100ms (pgvector HNSW 인덱스)
- 청크 크기: 256-1024 tokens (도메인별 실험 필요)
- 오버랩: 청크 크기의 10-20%
- Top-K 후보: 20개 검색 → Rerank 후 5개 사용

## Connections

- [[dev.backend.api.verify]] — FEEDS (weight: 0.8)
- [[dev.backend.patterns.llm-integration]] — FEEDS (weight: 0.7)
- [[dev.backend.api.rate-limiting]] — FEEDS (weight: 0.7)
- [[dev.backend.patterns.llm-integration]] — CO_CREATES (weight: 0.6)
