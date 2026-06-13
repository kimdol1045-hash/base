---
id: "dev.infra.deploy.blue-green"
domain: "development.infra"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#133 Zero-Downtime Deployment"
tags: [infra, deploy, blue-green, canary, zero-downtime, rollback]
---

# dev.infra.deploy.blue-green

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `pattern`  
> **Theory**: #133 Zero-Downtime Deployment  
> **Tokens**: 500

## Content

Blue-Green / Canary 배포 — 무중단 배포로 사용자 영향 없이 새 버전을 릴리즈하는 전략:

### Blue-Green 배포 흐름
```
┌──────────────┐     DNS/LB     ┌──────────────┐
│  Blue (v1)   │ ◀── 100% ──── │   Load        │
│  (현재 운영)  │               │   Balancer    │
└──────────────┘               └──────┬───────┘
┌──────────────┐                      │
│  Green (v2)  │ ◀── 0% (대기) ──────┘
│  (새 버전)    │
└──────────────┘

전환 절차:
1. Green 환경에 v2 배포 + smoke test 실행
2. Health check 통과 확인 (HTTP 200, DB 연결, 의존 서비스)
3. LB 트래픽을 Green으로 전환 (DNS TTL: 60초 이하)
4. 5분 모니터링 → 이상 없으면 Blue 환경 제거
5. 이상 시 → LB를 Blue로 즉시 복귀 (롤백 < 30초)
```

### Canary 배포 — 트래픽 점진적 분할
```yaml
# Kubernetes Ingress Canary 설정 예시
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: app-canary
  annotations:
    nginx.ingress.kubernetes.io/canary: "true"
    nginx.ingress.kubernetes.io/canary-weight: "5"
spec:
  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            backend:
              service:
                name: app-v2
                port:
                  number: 80

# 트래픽 분할 단계
# 5% → 에러율/레이턴시 확인 (15분)
# 25% → 비즈니스 지표 확인 (30분)
# 50% → 전체 안정성 확인 (1시간)
# 100% → 완전 전환
```

### DO: 안전한 배포 규칙
```typescript
// Backward-compatible DB migration (v1, v2 동시 호환)
// Step 1 (v2 배포 전): 새 컬럼 추가 (nullable)
ALTER TABLE users ADD COLUMN display_name VARCHAR(255);

// Step 2 (v2 배포 후): 데이터 마이그레이션
UPDATE users SET display_name = name WHERE display_name IS NULL;

// Step 3 (v1 완전 제거 후): 기존 컬럼 제거
ALTER TABLE users DROP COLUMN name;
```

```bash
# Health check 통과 후에만 트래픽 전환
curl -f http://green:3000/health || exit 1
curl -f http://green:3000/readiness || exit 1
# smoke test
curl -f http://green:3000/api/v1/status || exit 1
```

DON'T:
```sql
-- ❌ 배포 중 Breaking DB 변경
ALTER TABLE users RENAME COLUMN name TO display_name;
-- v1이 아직 트래픽 받는 중이면 즉시 장애

-- ❌ NOT NULL 제약조건 즉시 추가
ALTER TABLE orders ADD COLUMN tracking_id VARCHAR(255) NOT NULL;
-- v1에서 INSERT 시 에러 발생
```

```bash
# ❌ 헬스체크 없이 빅뱅 전환
kubectl set image deployment/app app=app:v2  # 롤백 불가
```

### 자동 롤백 기준
| 지표 | 임계값 | 조치 |
|------|--------|------|
| 에러율 (5xx) | > 1% | 즉시 롤백 |
| p99 레이턴시 | > 2초 | 트래픽 증가 중단 |
| CPU 사용률 | > 80% | 스케일아웃 후 재평가 |
| 비즈니스 지표 | 전환율 10% 하락 | 수동 판단 후 롤백 |
