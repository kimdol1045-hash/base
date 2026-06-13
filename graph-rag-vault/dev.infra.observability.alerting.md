---
id: "dev.infra.observability.alerting"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "observability", "alerting", "monitoring"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# dev.infra.observability.alerting

> #272 Alerting Best Practices (Google SRE Book, Chapter 6: Monitoring)

# 알림(Alerting) 설계 가이드

## 핵심 원칙
- 알림은 행동 가능한(Actionable) 것만 보낸다
- 증상(Symptom) 기반으로 알림하고, 원인(Cause)이 아닌 결과를 감지한다
- 알림 피로(Alert Fatigue)를 방지하기 위해 불필요한 알림을 제거한다
- 심각도(Severity)별로 알림 채널을 분리한다

## 심각도 레벨
| 심각도 | 기준 | 채널 | 응답 시간 |
|--------|------|------|-----------|
| P1 Critical | 서비스 장애, 데이터 손실 | PagerDuty + 전화 | 5분 |
| P2 High | 성능 심각 저하, 부분 장애 | Slack + PagerDuty | 30분 |
| P3 Medium | 에러율 증가, 디스크 경고 | Slack | 2시간 |
| P4 Low | 정보성, 최적화 필요 | 이메일/대시보드 | 영업일 |

## DO
- SLO 기반 알림을 설정한다 (에러 예산 소진 속도)
- 알림에 충분한 컨텍스트(대시보드 링크, 런북 링크)를 포함한다
- for/pending 기간을 설정하여 일시적 스파이크를 무시한다
- 알림 규칙을 정기적으로 리뷰하고 정리한다

## DON'T
- CPU 사용률 같은 원인 메트릭으로만 알림하지 않는다
- 알림을 너무 민감하게 설정하지 않는다 (노이즈 유발)
- 모든 알림을 동일한 채널로 보내지 않는다
- 런북 없이 알림을 설정하지 않는다

## 코드 예시
```yaml
# Prometheus Alertmanager 규칙
groups:
  - name: slo-alerts
    rules:
      # 증상 기반: 에러율 SLO 위반
      - alert: HighErrorRate
        expr: |
          sum(rate(http_requests_total{status_code=~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
          > 0.01
        for: 5m    # 5분간 지속될 때만 발화
        labels:
          severity: critical
        annotations:
          summary: "에러율이 SLO(1%)를 초과했습니다"
          description: "현재 에러율: {{ $value | humanizePercentage }}"
          dashboard: "https://grafana.example.com/d/slo"
          runbook: "https://wiki.example.com/runbooks/high-error-rate"

      # 에러 예산 소진 속도 알림
      - alert: ErrorBudgetBurnRate
        expr: |
          error_budget_burn_rate_1h > 14.4
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "에러 예산이 빠르게 소진되고 있습니다"
```
