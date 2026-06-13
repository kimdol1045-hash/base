---
id: "dev.infra.deploy.rollback"
domain: "development.infra"
type: "rule"
region: BRAINSTEM
token_estimate: 500
theory: "#133 Zero-Downtime Deployment, #125 Release It! (Nygard, 2018)"
tags: [infra, deploy, rollback, migration, disaster-recovery, resilience]
---

# dev.infra.deploy.rollback

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `rule`  
> **Theory**: #133 Zero-Downtime Deployment, #125 Release It! (Nygard, 2018)  
> **Tokens**: 500

## Content

롤백 전략 — 모든 배포에는 되돌리기 계획이 필수. 롤백 못하는 배포는 배포가 아니라 도박이다:

### 롤백 유형별 시간/위험도 매트릭스
| 롤백 유형 | 소요 시간 | 위험도 | 자동화 가능 |
|-----------|----------|--------|------------|
| 배포 롤백 (이미지 태그) | < 1분 | 낮음 | O |
| 피처 플래그 Kill Switch | < 10초 | 낮음 | O |
| DB 마이그레이션 롤백 | 5~15분 | 중간 | 부분적 |
| 데이터 복원 (백업) | 30분~2시간 | 높음 | X |
| 전체 인프라 복원 | 1~4시간 | 매우 높음 | X |

### 1. 배포 롤백 — 이전 이미지로 즉시 복귀
```bash
# DO: N-1 이미지 태그를 항상 보관, 즉시 롤백 가능
# Kubernetes
kubectl rollout undo deployment/app --to-revision=3

# Docker Compose
docker compose pull app:v1.2.3  # 이전 태그
docker compose up -d app

# CI/CD에서 자동 롤백 (GitHub Actions 예시)
# deploy.yml
- name: Deploy
  run: kubectl set image deployment/app app=${{ env.IMAGE_TAG }}
- name: Verify
  run: |
    sleep 30
    ERROR_RATE=$(curl -s prometheus:9090/api/v1/query?query=rate(http_errors[5m]))
    if (( $(echo "$ERROR_RATE > 0.01" | bc -l) )); then
      echo "Error rate too high, rolling back"
      kubectl rollout undo deployment/app
      exit 1
    fi
```

### 2. DB 마이그레이션 롤백 — 역방향 마이그레이션 필수
```typescript
// DO: 모든 마이그레이션에 reversible down() 작성
export async function up(db: Kysely<any>) {
  await db.schema
    .alterTable("users")
    .addColumn("phone", "varchar(20)")
    .execute();
}

export async function down(db: Kysely<any>) {
  await db.schema
    .alterTable("users")
    .dropColumn("phone")
    .execute();
}
```

DON'T:
```typescript
// ❌ 되돌릴 수 없는 파괴적 마이그레이션
export async function up(db: Kysely<any>) {
  // 컬럼 삭제 — 데이터 영구 손실
  await db.schema.alterTable("users").dropColumn("legacy_name").execute();
  // 테이블 DROP — 복구 불가
  await db.schema.dropTable("old_orders").execute();
}

export async function down() {
  // down이 비어 있음 = 롤백 불가능
  throw new Error("irreversible migration");
}

// ❌ 롤백 테스트를 안 한 마이그레이션
// up → down → up 사이클 테스트 필수
```

### 3. 피처 롤백 — Feature Flag Kill Switch
```typescript
// DO: 위험도 높은 기능은 반드시 플래그 뒤에 배치
const newPaymentEnabled = await featureFlag.isEnabled("new-payment", {
  userId,
  default: false,
});
// 장애 감지 시: 대시보드에서 플래그 OFF → 즉시 이전 로직 복귀
// 코드 배포 없이 10초 내 롤백 가능
```

### 4. 데이터 롤백 — 백업 복원
```bash
# DO: 자동 백업 + 복원 절차 문서화
# PostgreSQL 포인트-인-타임 복구
pg_restore --dbname=app_production --clean backup_2024_01_15.dump

# 배포 전 체크리스트:
# - [ ] 최근 백업 확인 (< 1시간)
# - [ ] 복원 테스트 최근 실행일 확인 (< 1주)
# - [ ] 예상 복원 시간 확인
```

### 롤백 의사결정 플로우
```
장애 감지 → 피처 플래그 ON? → Kill Switch OFF (10초)
                  ↓ No
          배포 변경 원인? → 이전 이미지 롤백 (1분)
                  ↓ No
          DB 변경 원인? → down 마이그레이션 실행 (5~15분)
                  ↓ No
          데이터 오염? → 백업 복원 (30분+, 경영진 승인 필요)
```

### 핵심 규칙
- 모든 배포 파이프라인에 롤백 단계 포함 필수
- 매 분기 1회 롤백 드릴 실시 (실제 프로덕션 환경에서)
- N-1 이미지 보관 기간: 최소 7일
- DB 마이그레이션 up/down/up 사이클 테스트를 CI에 포함
