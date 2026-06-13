---
id: "dev.security.nist-framework"
domain: "development.security"
type: "rule"
bloom_level: ""
tags: ["security", "nist", "framework", "governance"]
brain_region: "CORTEX"
token_estimate: 450
---

# dev.security.nist-framework

> #150 NIST Cybersecurity Framework 2.0 (2024)

NIST 사이버보안 프레임워크 (보안 체계를 구조화한다):

### 6가지 핵심 기능 (CSF 2.0)
| 기능 | 설명 | 실무 예시 |
|------|------|----------|
| Govern | 보안 거버넌스 수립 | 보안 정책, 역할 정의, 위험 관리 전략 |
| Identify | 자산 및 위험 식별 | 자산 인벤토리, 데이터 분류, 위협 모델링 |
| Protect | 보호 조치 구현 | 접근제어, 암호화, 보안 교육 |
| Detect | 이상 탐지 | 모니터링, 로그 분석, IDS/IPS |
| Respond | 사고 대응 | 인시던트 플랜, 격리, 커뮤니케이션 |
| Recover | 복구 | 백업 복원, 사후 분석, 개선 |

### 웹 애플리케이션 적용 체크리스트
**Identify:**
- 민감 데이터 목록화 (PII, 결제 정보, 인증 정보)
- 외부 의존성 목록 및 취약점 스캔 (npm audit, Snyk)

**Protect:**
- 인증/인가 적용 (JWT + RBAC)
- 전송 암호화 (TLS 1.3) + 저장 암호화 (AES-256)
- CSP, HSTS, X-Frame-Options 헤더

**Detect:**
- 비정상 로그인 시도 탐지 (5회 실패 → 알림)
- API 응답시간 이상 탐지 (P99 > 2x baseline)

**Respond:**
- 침해 시 토큰 일괄 만료 절차
- 사고 발생 시 이해관계자 알림 프로세스

**Recover:**
- 데이터 백업 주기 및 복구 테스트
- 포스트모템 프로세스 (비난 없는 회고)

## Connections

- [[dev.security.role]] — REQUIRES (weight: 0.9)
- [[dev.security.verify]] — FEEDS (weight: 0.8)
- [[dev.security.stride]] — FEEDS (weight: 0.7)
- [[dev.security.defense-in-depth]] — FEEDS (weight: 0.7)
- [[dev.security.role]] — CO_CREATES (weight: 0.6)
