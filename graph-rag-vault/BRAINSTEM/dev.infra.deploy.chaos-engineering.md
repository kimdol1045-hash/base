---
id: "dev.infra.deploy.chaos-engineering"
domain: "development.infra"
type: "pattern"
region: BRAINSTEM
token_estimate: 420
theory: "#152 Principles of Chaos Engineering (Netflix, 2011)"
tags: [infra, chaos-engineering, resilience, netflix]
---

# dev.infra.deploy.chaos-engineering

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `pattern`  
> **Theory**: #152 Principles of Chaos Engineering (Netflix, 2011)  
> **Tokens**: 420

## Content

카오스 엔지니어링 (장애를 의도적으로 주입하여 복원력을 검증한다):

### 원칙 (Netflix)
1. 정상 상태에 대한 가설을 세운다 (baseline 정의)
2. 실제 세계 이벤트를 시뮬레이션한다
3. 프로덕션에서 실험한다 (가능할 때)
4. 자동화하여 지속 실행한다
5. 폭발 반경을 최소화한다

### 실험 유형
| 유형 | 방법 | 검증 항목 |
|------|------|----------|
| 서버 종료 | 랜덤 인스턴스 kill | Auto-healing, 무중단 |
| 네트워크 지연 | 100~500ms 지연 주입 | 타임아웃, 서킷 브레이커 |
| 디스크 가득 참 | /dev/full | 알림, graceful degradation |
| DNS 실패 | 외부 DNS 차단 | 캐시 폴백, 에러 처리 |
| 의존성 장애 | 외부 API 다운 | Circuit Breaker, 폴백 |

### GameDay 프로세스
1. **계획**: 가설, 폭발 반경, 중단 기준 정의
2. **알림**: 관련 팀에 실험 공지
3. **실행**: 장애 주입 + 실시간 모니터링
4. **관찰**: 시스템 반응 기록
5. **정리**: 장애 제거, 결과 분석
6. **개선**: 발견된 약점 수정

### 시작 단계 (소규모 팀)
- 프로덕션 전에 스테이징에서 시작
- 단일 서비스 장애부터 (전체 장애 X)
- 모니터링/알림이 먼저 갖춰져야 함
- 롤백 절차 사전 준비 필수

## Connections

*Connections will be populated by Graph RAG ingest.*
