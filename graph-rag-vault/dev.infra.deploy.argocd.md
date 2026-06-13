---
id: "dev.infra.deploy.argocd"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "argocd", "gitops", "kubernetes", "deploy"]
brain_region: "CEREBELLUM"
token_estimate: 420
---

# dev.infra.deploy.argocd

> #262 GitOps (Weaveworks, GitOps Principles 2017)

# Argo CD GitOps 가이드

## 핵심 원칙
- Git을 배포의 단일 진실 원천(Single Source of Truth)으로 사용한다
- Git 커밋으로 배포를 트리거하고, 롤백은 Git revert로 수행한다
- Argo CD가 Git 상태와 클러스터 상태를 자동으로 동기화한다
- 선언적 배포로 재현 가능성과 감사 추적을 보장한다

## DO
- Application 매니페스트로 배포 대상을 선언한다
- 자동 동기화(auto-sync)를 프로덕션에서는 비활성화한다 (수동 승인)
- 헬스 체크를 커스텀하여 배포 성공 여부를 정확히 판단한다
- App of Apps 패턴으로 여러 서비스를 관리한다

## DON'T
- kubectl apply를 직접 실행하지 않는다 (Git을 통해서만 변경)
- Git 저장소에 시크릿을 평문으로 커밋하지 않는다 (Sealed Secrets 사용)
- 프로덕션에서 auto-sync + auto-prune을 동시에 활성화하지 않는다
- 하나의 Application에 모든 서비스를 포함하지 않는다

## 코드 예시
```yaml
# Argo CD Application 매니페스트
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app-production
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/k8s-manifests.git
    targetRevision: main
    path: apps/my-app/overlays/production
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: false       # 프로덕션: 자동 삭제 비활성화
      selfHeal: true     # 수동 변경 자동 복구
    syncOptions:
      - CreateNamespace=true
      - PruneLast=true
    retry:
      limit: 3
      backoff:
        duration: 5s
        maxDuration: 3m

# App of Apps 패턴 (루트 앱)
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root-app
spec:
  source:
    repoURL: https://github.com/org/k8s-manifests.git
    path: apps
  destination:
    server: https://kubernetes.default.svc
```

```
# 디렉토리 구조 (Kustomize)
apps/
├── my-app/
│   ├── base/
│   │   ├── deployment.yaml
│   │   ├── service.yaml
│   │   └── kustomization.yaml
│   └── overlays/
│       ├── staging/
│       │   └── kustomization.yaml
│       └── production/
│           └── kustomization.yaml
```
