---
id: "design.design-system.versioning"
domain: "design"
type: "pattern"
bloom_level: "디자인 시스템 버전 관리는 시맨틱 버전닝(SemVer)을 기반으로 하위 호환성을 유지하면서 시스템을 발전시키는 전략이다. Breaking Change 관리와 마이그레이션 가이드가 핵심이다."
tags: ["versioning", "semver", "design-system", "migration"]
brain_region: "CORTEX"
token_estimate: 380
---

# design.design-system.versioning

> 디자인 시스템 버전 관리는 시맨틱 버전닝(SemVer)을 기반으로 하위 호환성을 유지하면서 시스템을 발전시키는 전략이다. Breaking Change 관리와 마이그레이션 가이드가 핵심이다.

# 디자인 시스템 버전 관리 가이드

## 핵심 원칙
- 시맨틱 버전닝: MAJOR.MINOR.PATCH
- Breaking Change는 사전 공지 + 마이그레이션 가이드
- Deprecation 경고 → 2버전 유지 → 제거
- 소비자(사용 팀)의 업그레이드 부담 최소화

## 버전 규칙
| 변경 유형 | 버전 | 예시 |
|----------|------|------|
| 버그 수정 | PATCH | 1.0.0 → 1.0.1 |
| 새 컴포넌트/Props | MINOR | 1.0.1 → 1.1.0 |
| Breaking Change | MAJOR | 1.1.0 → 2.0.0 |

## Breaking Change 관리
1. RFC(Request for Comments) 작성
2. 팀 리뷰 및 영향 분석
3. Deprecation 마크 추가 (console.warn)
4. 마이그레이션 가이드 작성
5. 코드모드(Codemod) 제공 (가능한 경우)
6. 최소 2 MINOR 버전 유지 후 제거

## 릴리즈 프로세스
1. 변경 사항을 Changeset으로 기록
2. PR 머지 시 자동 버전 범프
3. 릴리즈 노트 자동 생성
4. npm/패키지 레지스트리 배포
5. 문서 사이트 갱신

## DO
- 모든 변경에 Changeset 기록 필수
- 캐너리(Canary) 릴리즈로 사전 검증
- 주요 소비자와 Breaking Change 사전 협의

## DON'T
- PATCH 버전에 Breaking Change 포함하지 않기
- Deprecation 없이 API 제거하지 않기
- 다수의 Breaking Change를 한 번에 릴리즈하지 않기
