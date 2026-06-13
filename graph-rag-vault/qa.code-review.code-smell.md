---
id: "qa.code-review.code-smell"
domain: "qa.testing"
type: "pattern"
bloom_level: "코드 스멜 감지 — Martin Fowler의 리팩터링 카탈로그"
tags: ["code-smell", "refactoring", "maintainability"]
brain_region: "CEREBELLUM"
token_estimate: 380
---

# qa.code-review.code-smell

> 코드 스멜 감지 — Martin Fowler의 리팩터링 카탈로그

# 코드 스멜 리뷰 가이드

## 핵심 원칙
- Long Method, God Class, Feature Envy 등 감지
- 복잡도 지표(Cyclomatic, Cognitive) 기반 판단
- 스멜 감지 → 리팩터링 패턴 제안

## DO
- 함수 길이 20줄, 클래스 200줄 기준 적용
- 순환 복잡도 10 초과 시 분리 권장
- 중복 코드 3회 이상 반복 시 추출

## DON'T
- 모든 스멜을 즉시 수정 요구하지 않기
- 컨텍스트 없이 기계적 규칙 적용하지 않기
- 성능 핫패스를 가독성만으로 리팩터링하지 않기
