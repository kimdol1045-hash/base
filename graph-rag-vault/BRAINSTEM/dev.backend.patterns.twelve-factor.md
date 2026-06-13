---
id: "dev.backend.patterns.twelve-factor"
domain: "development.backend"
type: "rule"
region: BRAINSTEM
token_estimate: 500
theory: "#103 12-Factor App (Wiggins, 2011)"
tags: [backend, architecture, twelve-factor, cloud-native]
---

# dev.backend.patterns.twelve-factor

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `rule`  
> **Theory**: #103 12-Factor App (Wiggins, 2011)  
> **Tokens**: 500

## Content

12-Factor App (클라우드 네이티브 앱의 12가지 원칙):

### 필수 준수 (위반 시 배포/운영 문제)
1. **Codebase**: 1 앱 = 1 레포. 공유 코드는 패키지로 분리.
2. **Dependencies**: 명시적 선언. package.json에 전부 기록. 전역 의존 금지.
3. **Config**: 환경변수로 관리. 코드에 하드코딩 절대 금지.
   ```typescript
   // DO
   const dbUrl = process.env.DATABASE_URL;
   // DON'T
   const dbUrl = 'postgresql://user:pass@localhost:5432/db';
   ```
4. **Backing Services**: DB, 캐시, 큐 등을 URL로 연결. 교체 가능하게.
5. **Build/Release/Run**: 빌드(컴파일) → 릴리스(빌드+설정) → 실행 엄격 분리.
6. **Processes**: Stateless. 세션은 Redis 등 외부 저장소에.
   ```typescript
   // DON'T: 메모리에 세션 저장
   const sessions = new Map();
   // DO: Redis 사용
   const session = await redis.get(`session:${sessionId}`);
   ```
7. **Port Binding**: 자체 포트로 서비스 노출. 별도 웹서버 불필요.
8. **Concurrency**: 프로세스 모델로 수평 확장. 멀티스레드보다 멀티프로세스.
9. **Disposability**: 빠른 시작(< 10초), 우아한 종료(SIGTERM 처리).
10. **Dev/Prod Parity**: 개발 ≈ 프로덕션. Docker로 환경 일치.
11. **Logs**: stdout으로 출력. 파일 저장 X. 외부 수집기가 처리.
12. **Admin Processes**: 마이그레이션, 스크립트는 1회성 프로세스로.

### 체크리스트 요약
- [ ] 환경변수만으로 설정 가능한가?
- [ ] 프로세스가 stateless인가?
- [ ] SIGTERM 시 우아하게 종료되는가?
- [ ] 로그가 stdout으로 나가는가?

## Connections

### CO_CREATES (5)

- ← [[dev.backend.patterns.cap-theorem]] `w=0.6`
- → [[dev.backend.patterns.circuit-breaker]] `w=0.6`
- ← [[dev.backend.patterns.cqrs]] `w=0.6`
- ← [[dev.backend.patterns.event-driven]] `w=0.6`
- → [[dev.backend.patterns.saga-pattern]] `w=0.6`
