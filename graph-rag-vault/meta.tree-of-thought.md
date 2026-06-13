---
id: "meta.tree-of-thought"
domain: "meta"
type: "pattern"
bloom_level: "Tree of Thoughts (Yao et al., 2023) — 탐색 기반 추론 프레임워크"
tags: ["tree-of-thought", "reasoning", "search", "deliberation"]
brain_region: "PREFRONTAL"
token_estimate: 380
---

# meta.tree-of-thought

> Tree of Thoughts (Yao et al., 2023) — 탐색 기반 추론 프레임워크

# Tree of Thoughts 프롬프팅

## 핵심 원칙
- 추론을 트리 구조로 확장하여 다양한 경로 탐색
- 각 단계에서 평가 → 유망 경로 선택 → 확장
- BFS/DFS 전략으로 최적 해 탐색

## DO
- 문제를 중간 사고 단계로 분해
- 각 단계별 자체 평가 메커니즘 설계
- 막다른 경로는 백트래킹으로 회피

## DON'T
- 단순 문제에 과도한 트리 확장 적용하지 않기
- 평가 기준 없이 무작위 확장하지 않기
- 깊이 제한 없이 탐색하지 않기
