---
id: "dev.infra.sre.chaos-engineering"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "sre", "chaos-engineering", "resilience"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# dev.infra.sre.chaos-engineering

> #277 Chaos Engineering (Netflix, Principles of Chaos Engineering 2014)

# 카오스 엔지니어링 가이드

## 핵심 원칙
- 실험을 통해 시스템의 약점을 사전에 발견한다
- 정상 상태(Steady State)를 먼저 정의하고, 실험 후 비교한다
- 실 환경에서 수행하되, 폭발 반경(Blast Radius)을 제한한다
- 자동 중단 조건(Abort Condition)을 설정한다

## DO
- 정상 상태 가설을 먼저 세운다 ("서버 1대가 죽어도 에러율 < 1%")
- 스테이징에서 충분히 검증한 후 프로덕션에서 수행한다
- 소규모부터 시작하여 점진적으로 범위를 넓힌다
- Game Day를 정기적으로 수행한다
- Litmus, Chaos Mesh 같은 도구를 활용한다

## DON'T
- 모니터링/알림 없이 카오스 실험을 수행하지 않는다
- 자동 중단 조건 없이 실험하지 않는다
- 팀에 알리지 않고 프로덕션에서 실험하지 않는다
- 한 번에 여러 장애를 동시에 주입하지 않는다

## 실험 유형
| 실험 | 방법 | 검증 대상 |
|------|------|-----------|
| 인스턴스 종료 | Pod/VM 랜덤 종료 | 자동 복구, 로드밸런싱 |
| 네트워크 지연 | tc 명령으로 지연 주입 | 타임아웃, 서킷브레이커 |
| 네트워크 파티션 | iptables로 통신 차단 | 장애 격리, 폴백 |
| CPU/메모리 압박 | stress-ng 실행 | 오토스케일링, OOM 처리 |
| DNS 장애 | DNS 응답 차단 | DNS 캐싱, 폴백 |

## 코드 예시
```yaml
# Chaos Mesh - Pod 장애 실험
apiVersion: chaos-mesh.org/v1alpha1
kind: PodChaos
metadata:
  name: pod-kill-experiment
spec:
  action: pod-kill
  mode: one                # 1개 Pod만 대상
  selector:
    namespaces: [production]
    labelSelectors:
      app: order-service
  scheduler:
    cron: "@every 4h"     # 4시간마다 실행
  duration: "30s"

# 네트워크 지연 실험
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-delay-experiment
spec:
  action: delay
  mode: all
  selector:
    labelSelectors:
      app: payment-service
  delay:
    latency: "500ms"
    jitter: "100ms"
  duration: "5m"
```
