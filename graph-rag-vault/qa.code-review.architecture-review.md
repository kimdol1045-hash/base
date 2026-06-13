---
id: "qa.code-review.architecture-review"
domain: "qa"
type: "pattern"
bloom_level: "아키텍처 리뷰는 시스템의 구조적 결정이 비기능 요구사항(확장성, 성능, 보안, 유지보수성)을 충족하는지 평가하는 프로세스이다. ATAM(Architecture Tradeoff Analysis Method)이 대표적 방법론이다."
tags: ["architecture-review", "code-review", "quality-attributes"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# qa.code-review.architecture-review

> 아키텍처 리뷰는 시스템의 구조적 결정이 비기능 요구사항(확장성, 성능, 보안, 유지보수성)을 충족하는지 평가하는 프로세스이다. ATAM(Architecture Tradeoff Analysis Method)이 대표적 방법론이다.

# 아키텍처 리뷰 가이드

## 핵심 원칙
- 기능보다 품질 속성(Quality Attributes) 중심 평가
- 트레이드오프를 명시적으로 문서화
- 리스크 기반 우선순위: 고위험 결정 집중 리뷰
- 이해관계자 참여: 개발자, 아키텍트, PM

## 평가 품질 속성
| 속성 | 평가 기준 |
|------|----------|
| 확장성 | 10x 트래픽 처리 가능한 구조인가? |
| 성능 | SLA 목표 응답 시간 달성 가능한가? |
| 보안 | OWASP Top 10 대응 구조인가? |
| 유지보수성 | 모듈 교체/수정 영향 범위가 제한적인가? |
| 가용성 | 단일 장애점(SPOF)이 없는가? |
| 테스트 용이성 | 의존성 격리와 모킹이 가능한가? |

## 리뷰 프로세스
1. 아키텍처 결정 문서(ADR) 검토
2. 품질 속성 시나리오 도출
3. 현재 아키텍처로 시나리오 충족 여부 분석
4. 리스크 및 트레이드오프 식별
5. 개선 권고사항 도출
6. 우선순위화 및 실행 계획

## DO
- 아키텍처 결정 기록(ADR)을 코드 레포에 유지
- 다이어그램(C4 모델) 기반 리뷰
- 결합도(Coupling)와 응집도(Cohesion) 분석

## DON'T
- 코드 레벨 디테일에만 집중하지 않기
- 성능 추정을 벤치마크 없이 하지 않기
- 모든 결정을 완벽하게 만들려 하지 않기 (Good Enough)
