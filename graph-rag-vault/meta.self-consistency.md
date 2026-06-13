---
id: "meta.self-consistency"
domain: "meta"
type: "pattern"
bloom_level: "Self-Consistency Prompting (Wang et al., 2022) — 다수 추론 경로의 합의 활용"
tags: ["self-consistency", "reasoning", "ensemble", "prompting"]
brain_region: "PREFRONTAL"
token_estimate: 350
---

# meta.self-consistency

> Self-Consistency Prompting (Wang et al., 2022) — 다수 추론 경로의 합의 활용

# Self-Consistency 프롬프팅

## 핵심 원칙
- 동일 문제에 대해 다수의 추론 경로를 생성
- 최종 답변은 다수결(majority vote)로 결정
- Chain-of-Thought와 결합하여 추론 품질 향상

## DO
- temperature를 높여 다양한 추론 경로 생성
- 최소 3-5개 경로를 샘플링
- 경로별 중간 단계의 일관성 확인

## DON'T
- 단일 경로의 결과만 신뢰하지 않기
- 너무 적은 샘플로 합의를 판단하지 않기
- 모든 경로가 동일하면 temperature 조정 필요
