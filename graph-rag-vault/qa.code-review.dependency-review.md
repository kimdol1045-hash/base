---
id: "qa.code-review.dependency-review"
domain: "qa"
type: "pattern"
bloom_level: "의존성 리뷰는 외부 패키지/라이브러리의 보안, 라이선스, 유지보수 상태를 평가하는 프로세스이다. 공급망 공격(Supply Chain Attack) 방지와 기술 부채 관리의 핵심이다."
tags: ["dependency-review", "supply-chain", "packages"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# qa.code-review.dependency-review

> 의존성 리뷰는 외부 패키지/라이브러리의 보안, 라이선스, 유지보수 상태를 평가하는 프로세스이다. 공급망 공격(Supply Chain Attack) 방지와 기술 부채 관리의 핵심이다.

# 의존성 리뷰 가이드

## 핵심 원칙
- 새 의존성 추가는 비용이다 (유지보수, 보안, 번들 크기)
- 추가 전 대안 검토: 직접 구현 가능한가?
- 보안, 라이선스, 유지보수 상태 3가지 필수 확인
- 자동화된 스캔을 CI에 통합

## 의존성 평가 기준
| 기준 | 확인 항목 |
|------|----------|
| 보안 | 알려진 취약점 (CVE) |
| 라이선스 | MIT/Apache/GPL 호환성 |
| 유지보수 | 최근 커밋, 이슈 응답, 릴리즈 주기 |
| 인기도 | 다운로드 수, GitHub 스타 |
| 크기 | 번들 사이즈 영향 |
| 의존성 깊이 | 전이(transitive) 의존성 수 |

## 리뷰 프로세스
1. 새 의존성 추가 시 PR에 근거 작성 필수
2. 평가 기준으로 점수화
3. 대안 검토 (내장 기능, 더 작은 패키지)
4. 승인 또는 대안 제시

## 자동화 도구
- Dependabot / Renovate: 자동 업데이트 PR
- Snyk / npm audit: 취약점 스캔
- License Checker: 라이선스 호환성
- Bundlephobia: 번들 크기 확인

## DO
- lock 파일(package-lock.json) 변경 시 리뷰
- 주간 의존성 업데이트 루틴화
- 허용 라이선스 목록 사전 정의

## DON'T
- 의존성 업데이트를 수개월 미루지 않기
- 취약점 경고를 무시하지 않기
- 유지보수 중단된 패키지에 의존하지 않기
