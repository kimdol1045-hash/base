---
id: "dev.infra.observability.dashboard"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "observability", "dashboard", "grafana"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# dev.infra.observability.dashboard

> #273 Dashboard Design (Grafana Best Practices, 2023)

# 모니터링 대시보드 설계 가이드

## 핵심 원칙
- 대시보드는 질문에 답해야 한다 ("서비스가 정상인가?")
- 계층적으로 구성한다: 개요 → 서비스 → 상세
- 핵심 지표를 한눈에 파악할 수 있도록 설계한다
- 대시보드를 코드로 관리한다 (Grafana Dashboard as Code)

## DO
- 서비스별 RED 메트릭(Rate, Errors, Duration) 대시보드를 만든다
- 시계열 그래프에 적절한 시간 범위와 집계 간격을 설정한다
- 상태 패널로 전체 서비스 헬스를 한눈에 표시한다
- 변수(Variables)로 환경, 서비스, 인스턴스를 필터링한다
- 알림 임계값을 대시보드에 표시한다

## DON'T
- 하나의 대시보드에 너무 많은 패널을 넣지 않는다 (최대 15-20개)
- 같은 메트릭을 여러 대시보드에 중복하지 않는다
- 대시보드를 GUI에서만 편집하지 않는다 (JSON으로 버전 관리)
- 의미 없는 메트릭으로 대시보드를 채우지 않는다

## 대시보드 계층 구조
```
Level 0: 전체 시스템 개요
├── 서비스 헬스 상태 (UP/DOWN)
├── 전체 에러율
└── SLO 현황

Level 1: 서비스별 개요
├── RED 메트릭 (Rate, Errors, Duration)
├── 리소스 사용률 (CPU, Memory)
└── 주요 비즈니스 메트릭

Level 2: 상세 진단
├── 엔드포인트별 지연시간
├── DB 쿼리 성능
└── 외부 서비스 호출 상태
```

## 코드 예시
```json
{
  "dashboard": {
    "title": "Order Service - Overview",
    "templating": {
      "list": [
        { "name": "env", "type": "query", "query": "label_values(environment)" },
        { "name": "instance", "type": "query", "query": "label_values(up{service=\"order\"}, instance)" }
      ]
    },
    "panels": [
      {
        "title": "요청 처리량 (RPS)",
        "type": "timeseries",
        "targets": [{
          "expr": "sum(rate(http_requests_total{service=\"order\",env=\"$env\"}[5m]))"
        }]
      },
      {
        "title": "에러율 (%)",
        "type": "gauge",
        "targets": [{
          "expr": "sum(rate(http_requests_total{status_code=~\"5..\"}[5m])) / sum(rate(http_requests_total[5m])) * 100"
        }],
        "thresholds": { "steps": [
          { "color": "green", "value": 0 },
          { "color": "yellow", "value": 1 },
          { "color": "red", "value": 5 }
        ]}
      }
    ]
  }
}
```
