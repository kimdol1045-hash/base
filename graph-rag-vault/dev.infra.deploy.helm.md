---
id: "dev.infra.deploy.helm"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "helm", "kubernetes", "deploy"]
brain_region: "CEREBELLUM"
token_estimate: 420
---

# dev.infra.deploy.helm

> #261 Helm Charts (CNCF, Helm 3 Documentation 2019)

# Helm 차트 설계 가이드

## 핵심 원칙
- Helm은 Kubernetes 리소스의 패키지 매니저이다
- values.yaml로 환경별 설정을 분리한다
- 차트를 재사용 가능하고 구성 가능하게 설계한다
- Chart.lock으로 의존성 버전을 고정한다

## DO
- 환경별(dev, staging, prod) values 파일을 분리한다
- 필수 값에 required 검증을 추가한다
- _helpers.tpl에 공통 라벨, 이름 생성 로직을 정의한다
- Chart 버전과 appVersion을 분리 관리한다

## DON'T
- values.yaml에 시크릿을 평문으로 포함하지 않는다
- 하나의 차트에 너무 많은 리소스를 포함하지 않는다
- Helm hooks를 남용하지 않는다
- `helm install --set`으로 많은 값을 오버라이드하지 않는다 (values 파일 사용)

## 코드 예시
```yaml
# Chart.yaml
apiVersion: v2
name: my-app
version: 1.2.0
appVersion: "2.5.0"
dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"

# values.yaml
replicaCount: 2
image:
  repository: my-app
  tag: ""  # CI에서 주입
  pullPolicy: IfNotPresent
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
autoscaling:
  enabled: false
  minReplicas: 2
  maxReplicas: 10

# templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "my-app.fullname" . }}
  labels: {{- include "my-app.labels" . | nindent 4 }}
spec:
  replicas: {{ .Values.replicaCount }}
  template:
    spec:
      containers:
        - name: {{ .Chart.Name }}
          image: "{{ .Values.image.repository }}:{{ .Values.image.tag | default .Chart.AppVersion }}"
          resources: {{- toYaml .Values.resources | nindent 14 }}
```

```bash
# 환경별 배포
helm upgrade --install my-app ./charts/my-app \
  -f values/production.yaml \
  --set image.tag=$CI_COMMIT_SHA \
  --namespace production
```
