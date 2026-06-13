---
id: "dev.infra.deploy.secrets"
domain: "development.infra"
type: "rule"
region: BRAINSTEM
token_estimate: 500
theory: "#116 OWASP A02 Cryptographic Failures"
tags: [infra, deploy, secrets, vault, rotation, security, ci-cd]
---

# dev.infra.deploy.secrets

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.infra`  
> **Type**: `rule`  
> **Theory**: #116 OWASP A02 Cryptographic Failures  
> **Tokens**: 500

## Content

시크릿 관리 — 모든 민감 정보는 암호화 저장, 환경별 분리, 자동 로테이션이 원칙:

### 시크릿 유형별 로테이션 주기
| 시크릿 유형 | 로테이션 주기 | 저장소 | 자동화 |
|------------|-------------|--------|--------|
| API 키 (외부 서비스) | 90일 | Vault / CI Secrets | 가능 |
| DB 비밀번호 | 30일 | Vault + 동적 생성 | 가능 |
| JWT 서명 키 | 180일 | Vault | 가능 (dual key) |
| TLS 인증서 | 90일 (Let's Encrypt) | cert-manager | 자동 |
| 암호화 키 (AES) | 365일 | KMS / Vault | 가능 (envelope) |
| OAuth 클라이언트 시크릿 | 180일 | CI Secrets | 수동 |

### 시크릿 계층 구조 (환경별 완전 분리)
```
├── development/
│   ├── DATABASE_URL=postgresql://dev:dev@localhost:5432/app_dev
│   ├── REDIS_URL=redis://localhost:6379
│   └── API_KEY=<dev-api-key>
├── staging/
│   ├── DATABASE_URL=postgresql://stg:***@stg-db:5432/app_stg
│   └── API_KEY=<staging-api-key>      # 프로덕션과 다른 키
└── production/
    ├── DATABASE_URL=vault://secret/prod/db  # Vault 참조
    └── API_KEY=vault://secret/prod/api-key
```

### CI/CD 시크릿 주입 (GitHub Actions)
```yaml
# DO: GitHub Environments + Secrets 사용
name: Deploy
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: production         # 환경별 시크릿 격리
    steps:
      - name: Deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
          API_KEY: ${{ secrets.API_KEY }}
        run: |
          echo "Deploying with environment-specific secrets"
          # 시크릿은 로그에 자동 마스킹됨
```

### HashiCorp Vault 기본 패턴
```typescript
// DO: 애플리케이션에서 Vault 동적 시크릿 사용
import Vault from "node-vault";

const vault = Vault({
  endpoint: process.env.VAULT_ADDR,
  token: process.env.VAULT_TOKEN,  // 이것만 환경변수로 주입
});

// 동적 DB 자격증명 (TTL: 1시간, 자동 갱신)
const { data } = await vault.read("database/creds/app-role");
const dbUrl = `postgresql://${data.username}:${data.password}@db:5432/app`;

// 시크릿 캐싱 (TTL 존중)
const cachedSecret = await vault.read("secret/data/api-keys");
// lease_duration 내에서만 캐시, 만료 전 자동 갱신
```

### .env 관리 규칙
```bash
# DO: .env.example은 커밋 (키 이름만, 값은 비움)
# .env.example
DATABASE_URL=
API_KEY=
JWT_SECRET=
REDIS_URL=

# .gitignore에 반드시 포함
.env
.env.local
.env.*.local
```

DON'T:
```typescript
// ❌ 코드에 시크릿 하드코딩
const API_KEY = "<hardcoded-api-key>";  // git history에 영구 기록

// ❌ 환경 간 시크릿 공유
// staging과 production이 같은 DB 비밀번호 사용
// staging 침해 → production도 침해

// ❌ 로테이션 없는 시크릿
// 2년 전 생성된 API 키가 아직 유효
// 퇴사자가 알고 있을 수 있음

// ❌ 시크릿 로깅
console.log("Connecting with:", process.env.DATABASE_URL);
// 로그 시스템에 비밀번호 노출
```

### 시크릿 유출 대응 절차
```
1. 즉시 해당 시크릿 무효화 (revoke)
2. 새 시크릿 생성 + 배포
3. git history에서 제거 (git filter-branch 또는 BFG)
4. 영향 범위 조사 (접근 로그 확인)
5. 포스트모템 작성 + 방지 대책 수립
```
