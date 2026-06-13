---
id: "dev.infra.deploy.monitoring"
domain: "development.infra"
type: "rule"
bloom_level: ""
tags: ["infra", "monitoring", "sre", "observability"]
brain_region: "CEREBELLUM"
token_estimate: 380
---

# dev.infra.deploy.monitoring

> #132 Four Golden Signals (Google SRE, 2016)

모니터링 (문제를 사용자보다 먼저 발견한다):

### 4대 골든 시그널
| 시그널 | 측정 대상 | 알림 기준 |
|--------|----------|----------|
| Latency | 요청 응답 시간 | p95 > 1초 |
| Traffic | 초당 요청 수 (RPS) | 평소 대비 200% 이상 |
| Errors | 에러율 | > 1% |
| Saturation | 리소스 사용률 | CPU/메모리 > 80% |

### 로그 vs 메트릭 vs 트레이스
- **로그**: 이벤트 상세 기록 (디버깅용). 구조화 JSON.
- **메트릭**: 수치 시계열 (대시보드용). Prometheus/Datadog.
- **트레이스**: 요청 흐름 추적 (분산 시스템). OpenTelemetry.

### 알림 규칙
- 즉시 알림: 에러율 > 5%, 서버 다운
- 30분 알림: p95 > 2초, 디스크 > 90%
- 일간 리포트: 비용, 트래픽 추이, 에러 패턴

### 대시보드 구성
1. 서비스 상태 (UP/DOWN)
2. 응답 시간 (p50, p95, p99)
3. 에러율 (시간별)
4. 리소스 사용량 (CPU, 메모리, 디스크)

## Connections

- [[dev.infra.deploy.observability]] — CO_CREATES (weight: 0.6)
