---
id: "meta.structured-output"
domain: "meta"
type: "pattern"
bloom_level: "구조화 출력 — JSON/XML 등 정형 데이터 생성 최적화"
tags: ["structured-output", "json", "schema", "parsing"]
brain_region: "PREFRONTAL"
token_estimate: 350
---

# meta.structured-output

> 구조화 출력 — JSON/XML 등 정형 데이터 생성 최적화

# 구조화 출력 프롬프팅

## 핵심 원칙
- 명확한 출력 스키마를 프롬프트에 포함
- JSON Schema 또는 예시 기반으로 형식 지정
- 파싱 가능한 일관된 형식 유도

## DO
- 출력 스키마를 JSON Schema로 명시
- Few-shot 예시에 동일 형식 사용
- 중첩 구조의 각 필드 설명 포함

## DON'T
- 자유 형식 텍스트와 구조화 데이터 혼합 요청하지 않기
- 너무 깊은 중첩 구조 요구하지 않기
- 형식 검증 없이 파싱하지 않기
