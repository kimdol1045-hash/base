---
id: "meta.retrieval-augmented"
domain: "meta"
type: "pattern"
bloom_level: "RAG 프롬프팅 — 외부 지식 기반 생성 정확도 향상"
tags: ["rag", "retrieval", "grounding", "context"]
brain_region: "PREFRONTAL"
token_estimate: 380
---

# meta.retrieval-augmented

> RAG 프롬프팅 — 외부 지식 기반 생성 정확도 향상

# RAG 프롬프팅 가이드

## 핵심 원칙
- 검색된 컨텍스트를 프롬프트에 주입하여 환각 감소
- 컨텍스트와 지시의 명확한 구분
- 출처 기반 답변 유도

## DO
- 검색 결과의 관련성 점수 기반 필터링
- "제공된 정보만 사용" 지시 포함
- 출처 인용 형식 지정

## DON'T
- 무관한 컨텍스트를 과도하게 주입하지 않기
- 컨텍스트 윈도우 한계 무시하지 않기
- 검색 실패 시 폴백 전략 없이 진행하지 않기
