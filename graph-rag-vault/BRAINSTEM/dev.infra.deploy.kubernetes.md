---
id: "dev.infra.deploy.kubernetes"
domain: "development.infra"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#131 Immutable Infrastructure"
tags: [infra, deploy, kubernetes, k8s, hpa, deployment, container]
---

# dev.infra.deploy.kubernetes

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `pattern`  
> **Theory**: #131 Immutable Infrastructure  
> **Tokens**: 500

## Content

Kubernetes 핵심 패턴 — 불변 인프라 원칙 위에서 선언적으로 애플리케이션을 배포하고 운영하는 패턴:

### Deployment + Rolling Update
```yaml
# DO: 리소스 제한, 프로브, 롤링 업데이트 전략 모두 명시
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1            # 최대 1개 초과 Pod 허용
      maxUnavailable: 0      # 항상 최소 3개 유지 (무중단)
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      securityContext:
        runAsNonRoot: true        # root 실행 금지
        runAsUser: 1000
      containers:
        - name: app
          image: registry.example.com/app:v1.2.3  # 명시적 태그
          resources:
            requests:              # 스케줄링 기준
              cpu: 100m
              memory: 128Mi
            limits:                # 최대 사용량
              cpu: 500m
              memory: 512Mi
          livenessProbe:           # 컨테이너 생존 확인
            httpGet:
              path: /health
              port: 3000
            initialDelaySeconds: 10
            periodSeconds: 15
            failureThreshold: 3
          readinessProbe:          # 트래픽 수신 준비 확인
            httpGet:
              path: /readiness
              port: 3000
            initialDelaySeconds: 5
            periodSeconds: 5
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: app-secrets
                  key: database-url
```

### Service (ClusterIP / LoadBalancer)
```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-service
spec:
  type: ClusterIP              # 클러스터 내부 통신
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 3000
---
# 외부 노출 시 LoadBalancer 또는 Ingress 사용
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-ingress
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
    - hosts: [app.example.com]
      secretName: app-tls
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: app-service
                port:
                  number: 80
```

### HPA (Horizontal Pod Autoscaler)
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 3
  maxReplicas: 20
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70    # CPU 70% 초과 시 스케일아웃
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
```

### Pod Disruption Budget
```yaml
# 유지보수/업데이트 중에도 최소 가용성 보장
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: app-pdb
spec:
  minAvailable: 2              # 항상 최소 2개 Pod 유지
  selector:
    matchLabels:
      app: my-app
```

DON'T:
```yaml
# ❌ latest 태그 사용 — 어떤 버전인지 추적 불가
image: registry.example.com/app:latest

# ❌ 리소스 제한 없음 — 단일 Pod가 노드 전체 자원 소진
containers:
  - name: app
    image: app:v1
    # resources 섹션 없음

# ❌ root로 실행 — 컨테이너 탈출 시 노드 장악
securityContext:
  runAsUser: 0

# ❌ 프로브 없음 — 죽은 Pod에 트래픽 계속 전달
# livenessProbe, readinessProbe 모두 미설정
```

### 핵심 체크리스트
- requests와 limits 모두 설정 (limits만 ≠ requests + limits)
- liveness + readiness 프로브 분리 (같은 엔드포인트 사용 금지)
- 이미지 태그에 git SHA 또는 시맨틱 버전 사용
- ConfigMap: 비밀이 아닌 설정, Secret: 민감 정보
- Namespace로 환경 분리 (dev / staging / production)
