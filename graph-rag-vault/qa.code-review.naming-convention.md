---
id: "qa.code-review.naming-convention"
domain: "qa.testing"
type: "rule"
bloom_level: "네이밍 컨벤션 — 의도를 드러내는 이름 짓기"
tags: ["naming", "convention", "readability", "clean-code"]
brain_region: "CEREBELLUM"
token_estimate: 350
---

# qa.code-review.naming-convention

> 네이밍 컨벤션 — 의도를 드러내는 이름 짓기

# 네이밍 컨벤션 리뷰 가이드

## 핵심 원칙
- 이름만으로 역할과 의도를 파악 가능해야 함
- 일관된 컨벤션 (camelCase, snake_case 등) 적용
- 약어 최소화, 도메인 용어 통일

## DO
- 함수: 동사+명사 (getUserById, calculateTotal)
- 불리언: is/has/can 접두사 (isValid, hasPermission)
- 상수: UPPER_SNAKE_CASE

## DON'T
- 한글자 변수명 (i, j 루프 변수 제외) 사용하지 않기
- 타입을 이름에 인코딩하지 않기 (strName → name)
- 너무 긴 이름 (30자 초과) 사용하지 않기
