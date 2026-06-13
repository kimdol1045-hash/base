---
id: "qa.test-gen.security-testing"
domain: "qa"
type: "pattern"
bloom_level: "보안 테스트는 OWASP Top 10을 기반으로 애플리케이션의 보안 취약점을 식별하고 검증하는 프로세스이다. SAST(정적 분석), DAST(동적 분석), 의존성 스캔이 핵심 도구이며, Shift-Left 전략으로 개발 초기에 수행한다."
tags: ["security-testing", "owasp", "vulnerability", "sast"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# qa.test-gen.security-testing

> 보안 테스트는 OWASP Top 10을 기반으로 애플리케이션의 보안 취약점을 식별하고 검증하는 프로세스이다. SAST(정적 분석), DAST(동적 분석), 의존성 스캔이 핵심 도구이며, Shift-Left 전략으로 개발 초기에 수행한다.

# 보안 테스트 가이드

## 핵심 원칙
- Shift-Left: 개발 초기부터 보안 테스트 적용
- 자동화: CI/CD에 보안 스캔 통합
- OWASP Top 10 기반 체크리스트
- 취약점 발견 → 심각도 평가 → 수정 → 검증

## OWASP Top 10 체크리스트
| 위험 | 테스트 방법 |
|------|-----------|
| 인젝션 (SQL, XSS) | 입력값 검증, 파라미터화 쿼리 |
| 인증 실패 | 브루트포스, 세션 관리 |
| 민감 데이터 노출 | HTTPS, 암호화, 마스킹 |
| XXE | XML 파서 설정 |
| 접근 제어 | IDOR, 수평/수직 권한 상승 |
| 보안 설정 오류 | 디폴트 설정, 디버그 모드 |
| XSS | 출력 인코딩, CSP |
| 역직렬화 | 신뢰할 수 없는 데이터 |
| 취약 컴포넌트 | 의존성 스캔 |
| 로깅/모니터링 | 감사 로그, 알림 |

## 도구 체인
- SAST: SonarQube, CodeQL, Semgrep
- DAST: OWASP ZAP, Burp Suite
- 의존성: Snyk, Dependabot, npm audit
- 시크릿 스캔: GitLeaks, TruffleHog

## DO
- PR 단계에서 SAST + 의존성 스캔 자동 실행
- 분기별 침투 테스트(Pentest) 실시
- 보안 취약점 SLA 정의 (Critical: 24h 내 수정)

## DON'T
- 보안 테스트를 릴리즈 직전에만 하지 않기
- 자동화 도구에만 의존하지 않기 (수동 리뷰 병행)
- 발견된 취약점을 백로그에 장기 방치하지 않기
