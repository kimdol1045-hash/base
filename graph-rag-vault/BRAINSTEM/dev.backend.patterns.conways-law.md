---
id: "dev.backend.patterns.conways-law"
domain: "development.backend"
type: "rule"
region: BRAINSTEM
token_estimate: 380
theory: "#149 Conway's Law (Melvin Conway, 1967) + Inverse Conway Maneuver"
tags: [backend, architecture, conways-law, organization]
---

# dev.backend.patterns.conways-law

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `rule`  
> **Theory**: #149 Conway's Law (Melvin Conway, 1967) + Inverse Conway Maneuver  
> **Tokens**: 380

## Content

Conway's Law (조직 구조가 시스템 아키텍처를 결정한다):

### 핵심 법칙
"시스템을 설계하는 조직은 그 조직의 커뮤니케이션 구조를 복제한 설계를 만든다."

### 실무 영향
| 조직 구조 | 결과 아키텍처 |
|----------|-------------|
| 기능별 팀 (FE/BE/DB) | 3-tier 모놀리스 |
| 도메인별 팀 (주문/결제/배송) | 마이크로서비스 |
| 1인 개발 | 밀결합 모놀리스 |
| 원격 분산 팀 | 느슨한 결합 + API 기반 |

### Inverse Conway Maneuver
원하는 아키텍처에 맞게 조직을 재구성:
- 마이크로서비스 원하면 → 도메인별 크로스펑셔널 팀 구성
- 공유 플랫폼 원하면 → 플랫폼 팀 별도 구성

### 설계 시 체크
- 서비스 경계가 팀 경계와 일치하는가?
- 팀 간 API 계약이 명확한가?
- 공유 DB 사용 시 어떤 팀이 소유하는가?

### 관련 법칙
- Hyrum's Law: "충분한 사용자가 있으면 API의 모든 관찰 가능한 행동에 누군가 의존한다"
- Brooks's Law: "늦어진 프로젝트에 인력을 추가하면 더 늦어진다"

## Connections

*Connections will be populated by Graph RAG ingest.*
