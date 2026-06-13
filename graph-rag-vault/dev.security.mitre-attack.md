---
id: "dev.security.mitre-attack"
domain: "development.security"
type: "rule"
bloom_level: ""
tags: ["security", "mitre", "attack", "threat-modeling"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.security.mitre-attack

> #176 MITRE ATT&CK Framework

MITRE ATT&CK (공격자의 전술과 기법을 체계적으로 이해한다):

### 웹 앱 관련 주요 전술
| 전술 | 공격 기법 | 방어 |
|------|----------|------|
| Initial Access | 피싱, 공개 앱 취약점 | WAF, 패치 관리, 보안 교육 |
| Execution | 코드 인젝션(SQL, XSS, RCE) | 입력 검증, CSP, 파라미터 바인딩 |
| Persistence | 백도어 계정, 웹셸 | 파일 무결성 모니터링, 계정 감사 |
| Privilege Escalation | IDOR, 수직/수평 권한 상승 | RBAC, 리소스 소유자 검증 |
| Credential Access | 브루트포스, 토큰 탈취 | Rate limit, MFA, 토큰 만료 |
| Lateral Movement | API 키 재사용, SSRF | 최소 권한, 네트워크 세분화 |
| Exfiltration | 대량 데이터 조회 | Pagination 강제, 이상 쿼리 탐지 |

### 웹 개발자 핵심 방어
1. **입력 검증**: 모든 외부 입력은 서버에서 검증
2. **최소 권한**: API 키, DB 권한, 파일 접근 모두
3. **깊이 있는 방어**: 한 계층 돌파해도 다음 계층이 방어
4. **감사 로그**: 누가, 언제, 무엇을 했는지 기록
5. **보안 헤더**: CSP, HSTS, X-Frame-Options 등

### 위협 모델링 활용
STRIDE로 위협 식별 → ATT&CK으로 구체적 공격 시나리오 매핑 → 방어 우선순위 결정

## Connections

- [[dev.security.role]] — CO_CREATES (weight: 0.6)
