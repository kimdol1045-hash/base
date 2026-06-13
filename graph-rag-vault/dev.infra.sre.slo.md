---
id: "dev.infra.sre.slo"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "sre", "slo", "sli", "sla"]
brain_region: "CEREBELLUM"
token_estimate: 420
---

# dev.infra.sre.slo

> #275 SLI/SLO/SLA (Google SRE Workbook, Chapter 2)

# SLI/SLO/SLA 설계 가이드

## 핵심 원칙
- SLI(Service Level Indicator): 서비스 품질을 측정하는 지표
- SLO(Service Level Objective): SLI의 목표 범위
- SLA(Service Level Agreement): 외부 고객과의 공식 약속 (SLO보다 느슨)
- SLO는 사용자 경험과 직결되는 지표를 기반으로 설정한다

## 주요 SLI 유형
| 서비스 유형 | SLI | 측정 방법 |
|-------------|-----|-----------|
| API 서버 | 가용성 | 성공 응답(2xx) / 전체 응답 |
| API 서버 | 지연시간 | p99 < 500ms인 요청 비율 |
| 배치 잡 | 완료율 | 성공 완료 / 전체 실행 |
| 데이터 파이프라인 | 신선도 | 마지막 처리 후 경과 시간 |

## DO
- SLO를 달성 가능하면서도 사용자 경험을 보장하는 수준으로 설정한다
- SLO를 윈도우 기반(Rolling 28일)으로 측정한다
- SLO 대시보드를 팀 전체가 볼 수 있게 공유한다
- 에러 예산 소진 시 안정성 작업에 집중하는 정책을 수립한다

## DON'T
- SLO를 너무 높게(99.99%) 설정하여 개발 속도를 저해하지 않는다
- 내부 메트릭만으로 SLI를 측정하지 않는다 (사용자 관점 측정)
- SLO를 설정하고 모니터링하지 않은 채 방치하지 않는다
- 모든 서비스에 동일한 SLO를 적용하지 않는다

## 코드 예시
```yaml
# SLO 정의 문서
service: order-service
slos:
  - name: "API 가용성"
    sli:
      type: availability
      good_events: "http_requests_total{status_code!~'5..'}"
      total_events: "http_requests_total"
    objective: 99.9
    window: 28d

  - name: "API 지연시간"
    sli:
      type: latency
      good_events: "http_request_duration_seconds_bucket{le='0.5'}"
      total_events: "http_request_duration_seconds_count"
    objective: 99.0  # 99%의 요청이 500ms 이내
    window: 28d
```

```typescript
// SLO 에러 예산 계산
function calculateErrorBudget(slo: number, totalEvents: number, badEvents: number) {
  const sloDecimal = slo / 100;
  const allowedBadEvents = totalEvents * (1 - sloDecimal);
  const remainingBudget = allowedBadEvents - badEvents;
  const budgetPercentage = (remainingBudget / allowedBadEvents) * 100;
  return {
    allowedBadEvents: Math.floor(allowedBadEvents),
    actualBadEvents: badEvents,
    remainingBudget: Math.max(0, remainingBudget),
    budgetPercentage: Math.max(0, budgetPercentage),
    isViolated: budgetPercentage <= 0,
  };
}
```
