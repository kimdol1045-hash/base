---
id: "dev.infra.deploy.canary"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "canary", "deploy", "progressive-delivery"]
brain_region: "CEREBELLUM"
token_estimate: 420
---

# dev.infra.deploy.canary

> #263 Canary Deployment (Netflix, 2013)

# 카나리 배포(Canary Deployment) 가이드

## 핵심 원칙
- 새 버전을 소수의 트래픽(1-10%)에 먼저 노출하여 안전성을 검증한다
- 핵심 메트릭(에러율, 지연시간)을 자동 모니터링하여 배포를 판단한다
- 문제 발생 시 자동으로 롤백한다 (Automated Rollback)
- 점진적으로 트래픽 비율을 증가시킨다 (Progressive Delivery)

## DO
- Argo Rollouts 또는 Flagger로 자동화된 카나리를 구현한다
- 성공 기준(SLI)을 명확히 정의한다 (에러율 < 1%, p99 < 500ms)
- 분석 단계(Analysis)를 자동화하여 사람의 개입을 최소화한다
- 카나리 트래픽의 메트릭을 별도로 추적한다

## DON'T
- 메트릭 없이 수동으로만 카나리 배포를 판단하지 않는다
- 카나리 비율을 처음부터 높게 설정하지 않는다
- 롤백 기준을 설정하지 않고 카나리를 진행하지 않는다
- 데이터베이스 스키마 변경과 카나리 배포를 동시에 하지 않는다

## 코드 예시
```yaml
# Argo Rollouts 카나리 설정
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 10
  strategy:
    canary:
      steps:
        - setWeight: 5          # 5% 트래픽
        - pause: { duration: 5m }
        - analysis:
            templates:
              - templateName: success-rate
            args:
              - name: service-name
                value: my-app
        - setWeight: 20         # 20% 트래픽
        - pause: { duration: 10m }
        - analysis:
            templates:
              - templateName: success-rate
        - setWeight: 50         # 50% 트래픽
        - pause: { duration: 10m }
        - setWeight: 100        # 전체 전환
      canaryService: my-app-canary
      stableService: my-app-stable

# 분석 템플릿
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate
spec:
  metrics:
    - name: success-rate
      interval: 60s
      successCondition: result[0] >= 0.99
      failureLimit: 3
      provider:
        prometheus:
          address: http://prometheus:9090
          query: |
            sum(rate(http_requests_total{service="{{args.service-name}}",status=~"2.."}[5m]))
            /
            sum(rate(http_requests_total{service="{{args.service-name}}"}[5m]))
```
