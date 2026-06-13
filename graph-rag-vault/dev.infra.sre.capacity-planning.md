---
id: "dev.infra.sre.capacity-planning"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "sre", "capacity-planning", "scaling"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# dev.infra.sre.capacity-planning

> #278 Capacity Planning (Google SRE Book, Chapter 18)

# 용량 계획(Capacity Planning) 가이드

## 핵심 원칙
- 현재 사용량 추세를 기반으로 미래 리소스 수요를 예측한다
- 유기적 성장(Organic)과 비유기적 성장(Inorganic: 캠페인, 신기능)을 구분한다
- 피크 대비 최소 2배의 헤드룸을 확보한다
- 정기적으로(분기별) 용량 계획을 갱신한다

## DO
- 핵심 리소스(CPU, 메모리, DB 연결, 스토리지)의 추세를 모니터링한다
- 부하 테스트로 시스템의 최대 처리량을 파악한다
- 오토스케일링을 설정하되, 확장 한도를 정의한다
- 비용 대비 성능을 고려하여 인스턴스 타입을 선택한다

## DON'T
- 현재 트래픽만 보고 리소스를 프로비저닝하지 않는다
- 부하 테스트 없이 피크 대응 능력을 가정하지 않는다
- 오토스케일링만 믿고 용량 계획을 생략하지 않는다
- DB, 메시지 큐 같은 상태 저장 컴포넌트의 확장을 간과하지 않는다

## 용량 계획 체크리스트
```
1. 현재 상태 파악
   - 일별/주별 피크 트래픽
   - 리소스 사용률 (CPU, 메모리, 디스크, 네트워크)
   - DB 쿼리 처리량 및 연결 수
   - 지연시간 p50, p95, p99

2. 성장 예측
   - 지난 3개월 트래픽 증가율
   - 예정된 마케팅 캠페인/이벤트
   - 신규 기능 출시 예정

3. 부하 테스트
   - 현재 피크의 2배 부하에서 성능 확인
   - 병목 지점 식별 (DB? 네트워크? CPU?)
   - 스케일링 한계점 파악

4. 조치 계획
   - 6개월 후 필요 리소스 산정
   - 비용 추정 및 승인
   - 확장 시점과 방법 결정 (수직/수평)
```

## 코드 예시
```yaml
# Kubernetes HPA (Horizontal Pod Autoscaler)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: order-service
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-service
  minReplicas: 3
  maxReplicas: 20    # 확장 한도
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 60
    - type: Pods
      pods:
        metric:
          name: http_requests_per_second
        target:
          type: AverageValue
          averageValue: "100"
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 3
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
```
