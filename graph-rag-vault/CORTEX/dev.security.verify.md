---
id: "dev.security.verify"
domain: "development.security"
type: "verify"
region: CORTEX
token_estimate: 500
theory: "#8 Flavell MGV (Metacognitive Verification)"
tags: [security, verification, checklist, owasp, quality]
---

# dev.security.verify

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.security`  
> **Type**: `verify`  
> **Theory**: #8 Flavell MGV (Metacognitive Verification)  
> **Tokens**: 500

## Content

보안 자기 검증 체크리스트 (코드 생성/수정 후 반드시 각 항목을 점검한다):

### A. OWASP Top 10 점검
- [ ] A01 접근 제어: 모든 엔드포인트에 인증/인가 미들웨어가 적용되어 있는가?
  - PASS: `authMiddleware` 적용 + 리소스 소유권 검증 존재
  - FAIL: 인증 없는 비공개 엔드포인트, IDOR 취약점 존재
- [ ] A02 암호화: 비밀번호가 bcrypt(cost>=12)/argon2id로 해싱되는가?
  - FAIL: MD5, SHA1, SHA256 단독 사용, 평문 저장
- [ ] A03 인젝션: 모든 DB 쿼리가 parameterized인가?
  - FAIL: 문자열 연결(`${}`)로 SQL 구성, `eval()` 사용
- [ ] A05 설정: CORS origin이 명시적 허용 목록인가?
  - FAIL: `origin: "*"`, `debug: true` 프로덕션 배포
- [ ] A07 인증: JWT 만료 시간이 15분 이하인가?
  - FAIL: 만료 없는 토큰, 24시간 이상 만료
- [ ] A09 로깅: 보안 이벤트(로그인 실패, 권한 변경)가 기록되는가?
  - FAIL: 빈 catch 블록, 로그 없는 인증 실패
- [ ] A10 SSRF: 사용자 입력 URL을 fetch할 때 허용 목록 검증이 있는가?
  - FAIL: `fetch(body.url)` 검증 없이 호출

### B. 인증/인가 (Authentication & Authorization)
- [ ] 비공개 엔드포인트에 `authMiddleware`가 적용되어 있는가?
- [ ] JWT secret이 환경변수이며 256bit 이상인가?
  - FAIL: 하드코딩된 시크릿, 짧은 시크릿 (`"secret"`, `"123"`)
- [ ] Refresh Token이 httpOnly + Secure + SameSite=Strict 쿠키인가?
- [ ] 리소스 접근 시 소유권/권한 검증이 있는가? (IDOR 방지)
- [ ] 관리자 작업에 추가 인증(MFA/비밀번호 재입력)이 있는가?
- [ ] 로그아웃 시 서버 측 세션/토큰이 무효화되는가?
- [ ] 비밀번호 시도 제한이 있는가? (5회/15분 초과 시 잠금)

### C. 데이터 보호 (Data Protection)
- [ ] PII(이메일, 전화번호, 주민번호)가 암호화 저장되는가?
- [ ] 로그에 비밀번호, 토큰, 카드번호 등 민감 정보가 포함되지 않는가?
  - PASS: `logger.info({ email: mask(email) })`
  - FAIL: `logger.info({ password: body.password })`
- [ ] API 응답에서 불필요한 내부 필드(passwordHash, __v 등)가 제거되었는가?
- [ ] 에러 응답에 스택 트레이스, DB 쿼리, 파일 경로가 노출되지 않는가?
- [ ] 파일 업로드 시 타입/크기(10MB) 제한이 있는가?
- [ ] 데이터 보존 기간이 정의되고 자동 삭제가 구현되어 있는가?

### D. 입력 검증 (Input Validation)
- [ ] 모든 외부 입력이 Zod 스키마로 검증되는가?
- [ ] 배열 입력에 `.max()` 크기 제한이 있는가? (DoS 방지)
  - PASS: `z.array(ItemSchema).max(100)`
  - FAIL: `z.array(ItemSchema)` 크기 제한 없음
- [ ] 문자열 입력에 `.max()` 길이 제한이 있는가?
  - PASS: `z.string().max(1000)` 또는 `z.string().max(255)`
  - FAIL: `z.string()` 길이 무제한
- [ ] HTML/JS 특수문자가 이스케이프 처리되는가? (XSS 방지)
- [ ] URL 입력 시 허용 목록(hostname, protocol) 검증이 있는가?

### E. 보안 설정 (Security Configuration)
- [ ] 보안 헤더가 설정되어 있는가?
  - `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`, `Content-Security-Policy`
- [ ] Rate Limiting이 적용되어 있는가?
  - 일반 API: 100 req/min, 인증 API: 5 req/min
- [ ] 환경변수에 하드코딩된 시크릿이 없는가?
- [ ] `npm audit` 결과에 high/critical 취약점이 없는가?
- [ ] Dockerfile에서 non-root 사용자로 실행하는가?

### F. 로깅과 모니터링 (Logging & Monitoring)
- [ ] 인증 실패, 인가 실패, 비정상 접근이 로깅되는가?
- [ ] 로그에 요청 ID(X-Request-Id)가 포함되어 추적 가능한가?
- [ ] 연속 인증 실패 시 알림이 발생하는가? (10회/분 초과)
- [ ] 감사 로그(audit log)가 변경 불가(append-only)인가?

### G. 의존성 보안 (Dependency Security)
- [ ] `package-lock.json`이 커밋되어 있는가?
- [ ] CI에서 `npm audit`가 실행되는가?
- [ ] 사용하지 않는 의존성이 제거되었는가?
- [ ] 라이선스 호환성이 확인되었는가?

### 심각도 기준
| 수준 | 조건 | 조치 |
|------|------|------|
| CRITICAL | 인증 없는 비공개 API, SQL Injection, 평문 비밀번호 | 즉시 수정 필수 |
| HIGH | IDOR, XSS, 약한 암호화, 보안 헤더 누락 | 배포 전 수정 |
| MEDIUM | Rate limit 미적용, 불충분한 로깅, 긴 토큰 만료 | 다음 스프린트 수정 |
| LOW | 보안 관련 주석 부족, 테스트 커버리지 부족 | 백로그 등록 |

## Connections

### REQUIRES (1)

- ← [[dev.security.role]] `w=0.85`

### FEEDS (5)

- ← [[dev.security.cia-triad]] `w=0.8`
- ← [[dev.security.defense-in-depth]] `w=0.8`
- ← [[dev.security.owasp]] `w=0.8`
- ← [[dev.security.stride]] `w=0.8`
- ← [[dev.security.zero-trust]] `w=0.8`

### CO_CREATES (9)

- ← [[dev.security.cia-triad]] `w=0.6`
- ← [[dev.security.defense-in-depth]] `w=0.6`
- ← [[dev.security.owasp]] `w=0.6`
- ← [[dev.security.role]] `w=0.6`
- ← [[dev.security.saltzer]] `w=0.6`
- ← [[dev.security.secure-by-design]] `w=0.6`
- ← [[dev.security.stride]] `w=0.6`
- ← [[dev.security.swiss-cheese]] `w=0.6`
- ← [[dev.security.zero-trust]] `w=0.6`
