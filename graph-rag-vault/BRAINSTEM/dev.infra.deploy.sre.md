---
id: "dev.infra.deploy.sre"
domain: "development.infra"
type: "rule"
region: BRAINSTEM
token_estimate: 440
theory: "#166 Site Reliability Engineering (Google, 2016)"
tags: [infra, sre, slo, error-budget, incident]
---

# dev.infra.deploy.sre

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `rule`  
> **Theory**: #166 Site Reliability Engineering (Google, 2016)  
> **Tokens**: 440

## Content

SRE 원칙 (안정성을 엔지니어링 문제로 접근한다):

### SLI / SLO / SLA
| 개념 | 정의 | 예시 |
|------|------|------|
| SLI (Indicator) | 측정 가능한 서비스 품질 지표 | 요청 성공률, P99 레이턴시 |
| SLO (Objective) | SLI의 목표 값 | 성공률 99.9%, P99 < 500ms |
| SLA (Agreement) | 고객과의 계약 (위반 시 패널티) | SLO 미달 시 크레딧 제공 |

### Error Budget
```
SLO = 99.9% → Error Budget = 0.1% (월 ~43분 다운타임 허용)
```
- Budget 남음 → 새 기능 배포 가속
- Budget 소진 → 배포 동결, 안정성 집중
- 개발 속도와 안정성의 균형 도구

### 인시던트 대응
1. **탐지**: 모니터링 알림 → On-call 담당자
2. **대응**: 즉시 영향 범위 파악 + 의사소통 채널 개설
3. **완화**: 임시 조치 (롤백, 스케일업, 기능 비활성화)
4. **해결**: 근본 원인 수정
5. **포스트모템**: 비난 없는 회고 → 액션 아이템

### 포스트모템 템플릿
- 타임라인 (분 단위)
- 영향 범위 (사용자 수, 기간)
- 근본 원인 (Why 5회)
- 재발 방지 액션 아이템 (담당자 + 기한)

### 토일 (Toil) 제거
- 수동, 반복적, 자동화 가능한 운영 작업 = Toil
- SRE 시간의 50% 미만을 Toil에 사용해야 함
- 자동화 대상: 배포, 알림 대응, 스케일링, 인증서 갱신

## Connections

*Connections will be populated by Graph RAG ingest.*
