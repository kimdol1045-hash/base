---
id: "qa.test-gen.snapshot-testing"
domain: "qa"
type: "pattern"
bloom_level: "스냅샷 테스트는 컴포넌트의 렌더링 결과를 직렬화하여 저장하고, 이후 변경 시 차이를 감지하는 테스트 기법이다. Jest의 toMatchSnapshot이 대표적이며, 의도치 않은 UI 변경을 조기에 발견한다."
tags: ["snapshot-testing", "jest", "component-testing"]
brain_region: "CEREBELLUM"
token_estimate: 380
---

# qa.test-gen.snapshot-testing

> 스냅샷 테스트는 컴포넌트의 렌더링 결과를 직렬화하여 저장하고, 이후 변경 시 차이를 감지하는 테스트 기법이다. Jest의 toMatchSnapshot이 대표적이며, 의도치 않은 UI 변경을 조기에 발견한다.

# 스냅샷 테스트 가이드

## 핵심 원칙
- 스냅샷은 보조 수단이지 주요 테스트가 아님
- 작은 단위의 스냅샷이 효과적 (전체 페이지 X)
- 의도된 변경 시 스냅샷 업데이트 리뷰 필수
- 동적 데이터는 고정값으로 대체

## 적용 가이드
### 적합한 경우
- 순수 UI 컴포넌트 (프레젠테이션 컴포넌트)
- 직렬화된 데이터 구조 (설정 파일, API 응답 스키마)
- 작고 안정적인 출력

### 부적합한 경우
- 자주 변하는 컴포넌트
- 큰 컴포넌트 (수백 줄 스냅샷)
- 비즈니스 로직 검증

## 스냅샷 관리
1. 스냅샷 파일을 코드 리뷰 대상에 포함
2. 의미 없는 스냅샷 업데이트(update -u) 남발 방지
3. 인라인 스냅샷 활용 (작은 출력)
4. 동적 값은 expect.any() 또는 목킹으로 처리

## DO
- 컴포넌트 단위의 작은 스냅샷 유지
- 스냅샷 변경 시 "왜 변했는지" 리뷰
- toMatchInlineSnapshot으로 가독성 향상

## DON'T
- 수백 줄짜리 스냅샷 생성하지 않기
- --updateSnapshot을 무분별하게 실행하지 않기
- 스냅샷만으로 테스트 커버리지를 채우지 않기
- 날짜/ID 등 동적 값을 포함하지 않기
