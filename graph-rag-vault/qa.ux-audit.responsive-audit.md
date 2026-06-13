---
id: "qa.ux-audit.responsive-audit"
domain: "qa.testing"
type: "pattern"
bloom_level: "반응형 감사 — 다양한 뷰포트에서의 레이아웃 검증"
tags: ["responsive", "viewport", "mobile", "audit"]
brain_region: "CEREBELLUM"
token_estimate: 350
---

# qa.ux-audit.responsive-audit

> 반응형 감사 — 다양한 뷰포트에서의 레이아웃 검증

# 반응형 감사 가이드

## 핵심 원칙
- 주요 브레이크포인트(320, 768, 1024, 1440px)별 검증
- 터치 타겟 크기, 스크롤 동작, 콘텐츠 리플로우 확인
- 실제 디바이스와 에뮬레이터 병행 테스트

## DO
- 최소 320px 뷰포트에서 콘텐츠 접근 가능 확인
- 터치 타겟 최소 44×44px 확보
- 가로/세로 방향 전환 시 레이아웃 검증

## DON'T
- 데스크탑만 테스트하고 모바일 무시하지 않기
- 고정 px 너비로 레이아웃 잡지 않기
- 호버 전용 인터랙션 설계하지 않기
