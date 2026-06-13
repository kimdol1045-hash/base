---
id: "dev.ai.eval-pipeline"
domain: "development.ai"
type: "pattern"
bloom_level: ""
tags: ["ai", "evaluation", "metrics", "quality"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.ai.eval-pipeline

> #284 LLM Evaluation (LMSYS, Chatbot Arena 2023; RAGAS Framework)

# AI 평가 파이프라인 가이드

## 핵심 원칙
- 배포 전 모든 AI 기능을 자동화된 평가로 검증한다
- 정량적 메트릭과 정성적 평가를 병행한다
- 회귀 테스트로 기존 성능이 저하되지 않음을 보장한다
- 평가 데이터셋을 지속적으로 확장한다

## 주요 평가 메트릭
| 메트릭 | 대상 | 측정 방법 |
|--------|------|-----------|
| Faithfulness | RAG | 생성 응답이 검색 문서에 근거하는지 |
| Relevance | RAG | 검색된 문서가 질문과 관련 있는지 |
| Accuracy | 분류 | 정답과의 일치율 |
| Latency | 전체 | 응답 시간 p50, p95 |
| Cost | 전체 | 토큰 사용량 / 요청 |

## DO
- 골든 테스트 세트(정답이 있는)를 100개 이상 구축한다
- CI/CD에 평가 파이프라인을 통합한다
- LLM-as-Judge로 주관적 품질을 평가한다
- A/B 테스트로 프로덕션 성능을 비교한다

## DON'T
- 수동 검토만으로 평가하지 않는다 (확장성 부족)
- 하나의 메트릭만으로 전체 품질을 판단하지 않는다
- 테스트 데이터를 학습에 사용하지 않는다 (오염 방지)
- 평가 없이 프롬프트를 변경하지 않는다

## ���드 예시
```typescript
interface EvalCase {
  input: string;
  expectedOutput?: string;
  context?: string[];
  metadata: Record<string, unknown>;
}

interface EvalResult {
  score: number;
  metrics: Record<string, number>;
  details: string;
}

// 평가 파이프라인
async function evaluateRAG(testCases: EvalCase[]): Promise<EvalResult[]> {
  const results: EvalResult[] = [];

  for (const testCase of testCases) {
    const response = await ragQuery(testCase.input);

    // Faithfulness: 응답이 소스에 근거하는지
    const faithfulness = await llmJudge(
      `응답이 주어진 문서에만 근거하여 작성되었나요?
      문서: ${testCase.context?.join("\n")}
      응답: ${response.answer}
      점수 (0-1):`,
    );

    // Relevance: 검색 문서의 관련성
    const relevance = await computeRelevance(testCase.input, response.sources);

    // Accuracy: 정답과의 일치
    const accuracy = testCase.expectedOutput
      ? await semanticSimilarity(response.answer, testCase.expectedOutput)
      : null;

    results.push({
      score: (faithfulness + relevance + (accuracy ?? 0)) / (accuracy ? 3 : 2),
      metrics: { faithfulness, relevance, ...(accuracy ? { accuracy } : {}) },
      details: response.answer,
    });
  }

  // 요약 보고
  const avgScore = results.reduce((s, r) => s + r.score, 0) / results.length;
  console.log(`평균 점수: ${avgScore.toFixed(3)} (${results.length}건)`);
  return results;
}
```
