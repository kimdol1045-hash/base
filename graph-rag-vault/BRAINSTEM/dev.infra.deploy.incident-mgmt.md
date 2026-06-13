---
id: "dev.infra.deploy.incident-mgmt"
domain: "development.infra"
type: "pattern"
region: BRAINSTEM
token_estimate: 400
theory: "#189 Incident Management (PagerDuty, Google SRE)"
tags: [infra, incident, sre, postmortem]
---

# dev.infra.deploy.incident-mgmt

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `pattern`  
> **Theory**: #189 Incident Management (PagerDuty, Google SRE)  
> **Tokens**: 400

## Content

인시던트 관리 (장애를 체계적으로 대응하고 재발을 방지한다):

### 심각도 분류
| 레벨 | 설명 | 대응 시간 | 예시 |
|------|------|----------|------|
| SEV1 | 서비스 전면 장애 | 즉시 | 전체 다운, 데이터 유출 |
| SEV2 | 핵심 기능 장애 | 15분 | 결제 불가, 로그인 불가 |
| SEV3 | 부분 기능 저하 | 1시간 | 검색 느림, 알림 지연 |
| SEV4 | 경미한 이슈 | 영업일 | UI 깨짐, 오타 |

### 대응 프로세스
1. **탐지**: 모니터링 알림 또는 사용자 리포트
2. **선언**: 인시던트 채널 개설, 역할 할당
3. **진단**: 타임라인 작성, 영향 범위 파악
4. **완화**: 즉시 조치 (롤백, 스케일업, 기능 비활성화)
5. **해결**: 근본 원인 수정
6. **포스트모템**: 비난 없는 회고 + 액션 아이템

### 역할
- **Incident Commander**: 전체 조율, 의사결정
- **Communications Lead**: 이해관계자 커뮤니케이션
- **Operations Lead**: 기술적 진단 및 조치

### 포스트모템 필수 항목
- 타임라인 (분 단위)
- 영향: 사용자 N명, M분간
- 근본 원인 (5 Whys)
- 재발 방지 액션 (담당자 + 기한)
- 잘된 점 / 개선할 점

## Connections

*Connections will be populated by Graph RAG ingest.*
