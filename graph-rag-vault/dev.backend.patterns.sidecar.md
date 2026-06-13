---
id: "dev.backend.patterns.sidecar"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["patterns", "sidecar", "microservices", "kubernetes"]
brain_region: "BRAINSTEM"
token_estimate: 400
---

# dev.backend.patterns.sidecar

> #222 Sidecar Pattern (Burns, Designing Distributed Systems 2018)

# Sidecar 패턴 가이드

## 핵심 원칙
- 주 애플리케이션과 별도의 프로세스/컨테이너로 부가 기능을 제공한다
- 로깅, 모니터링, 프록시, 설정 관리 등 횡단 관심사를 분리한다
- 주 애플리케이션과 동일한 호스트/Pod에서 실행되어 로컬 통신이 가능하다
- 주 애플리케이션의 언어/프레임워크에 종속되지 않는다

## DO
- Kubernetes Pod에서 Sidecar 컨테이너로 구현한다
- 주 애플리케이션과 볼륨 또는 localhost 네트워크를 공유한다
- 로그 수집(Fluentd), 프록시(Envoy), 인증서 관리 등에 활용한다
- Sidecar의 수명주기를 주 애플리케이션과 연동한다

## DON'T
- 비즈니스 로직을 Sidecar에 넣지 않는다
- Sidecar 장애가 주 애플리케이션을 중단시키도록 설계하지 않는다
- 과도한 수의 Sidecar를 붙이지 않는다 (리소스 오버헤드)
- 단일 서비스에서만 필요한 기능을 Sidecar로 분리하지 않는다

## 코드 예시
```yaml
# Kubernetes Pod - Envoy Sidecar 예시
apiVersion: v1
kind: Pod
metadata:
  name: my-app
spec:
  containers:
    - name: app
      image: my-app:latest
      ports:
        - containerPort: 8080
    - name: envoy-proxy
      image: envoyproxy/envoy:v1.28
      ports:
        - containerPort: 9901  # admin
        - containerPort: 8443  # TLS 종료
      volumeMounts:
        - name: envoy-config
          mountPath: /etc/envoy
    - name: log-collector
      image: fluent/fluentd:v1.16
      volumeMounts:
        - name: app-logs
          mountPath: /var/log/app
  volumes:
    - name: app-logs
      emptyDir: {}
    - name: envoy-config
      configMap:
        name: envoy-config
```

**적용 기준**: 여러 서비스에서 공통으로 필요하고, 주 애플리케이션 코드 변경 없이 적용해야 할 때 Sidecar 패턴을 선택한다.
