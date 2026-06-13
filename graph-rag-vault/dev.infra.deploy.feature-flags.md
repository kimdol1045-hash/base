---
id: "dev.infra.deploy.feature-flags"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "deploy", "feature-flags", "rollout", "kill-switch", "ab-test"]
brain_region: "CEREBELLUM"
token_estimate: 480
---

# dev.infra.deploy.feature-flags

> #134 Feature Flag Strategy

피처 플래그 — 코드 배포와 기능 릴리즈를 분리하여 점진적 출시와 즉각 롤백을 가능하게 하는 패턴:

### 플래그 4가지 유형
| 유형 | 수명 | 용도 | 예시 |
|------|------|------|------|
| Release Flag | 1~2주 | 점진적 기능 출시 | `new-checkout-flow` |
| Experiment Flag | 2~4주 | A/B 테스트 | `pricing-page-variant-b` |
| Ops Flag | 영구 | 운영 제어 (Kill Switch) | `enable-external-api` |
| Permission Flag | 영구 | 사용자/플랜 권한 | `enterprise-analytics` |

### 점진적 롤아웃 전략
```
1% → 내부 QA 팀 (dogfooding)
10% → 얼리 어답터 코호트
50% → 전체 사용자 절반 (안정성 확인)
100% → 전체 출시
각 단계에서 에러율 > 0.5% 또는 p95 레이턴시 > 500ms 시 자동 롤백
```

### 구현 패턴 (LaunchDarkly / Unleash / Custom)
```typescript
// DO: 플래그 평가를 edge에서, 기본값 항상 명시
import { getFlag } from "@/lib/feature-flags";

async function checkoutPage(userId: string) {
  const useNewCheckout = await getFlag("new-checkout-flow", {
    userId,
    default: false,           // 플래그 서버 장애 시 기본값
    percentage: 10,           // 10% 롤아웃
  });

  if (useNewCheckout) {
    return renderNewCheckout();
  }
  return renderLegacyCheckout();
}

// Kill Switch: Ops 플래그로 외부 의존성 즉시 차단
const externalApiEnabled = await getFlag("enable-external-api", {
  default: true,              // 기본은 활성
  killSwitch: true,           // 대시보드에서 즉시 비활성화 가능
});
```

DON'T:
```typescript
// ❌ 중첩 플래그 조건 — 디버깅 불가능
if (flagA && !flagB && (flagC || flagD)) {
  // 16가지 조합... 테스트 불가능
}

// ❌ 플래그를 영구 설정으로 사용
if (getFlag("dark-mode-enabled")) { ... }
// → 이건 user preference이지 feature flag가 아님

// ❌ 정리 계획 없는 플래그
// 6개월 된 release flag 200개 → 기술 부채 폭발
```

### 플래그 정리 라이프사이클
```
생성 → TTL 설정 (release: 14일, experiment: 30일)
→ 100% 롤아웃 완료 → Jira 티켓 자동 생성
→ 코드에서 플래그 분기 제거 → 플래그 아카이브
월 1회 stale flag 감사: 마지막 평가 > 30일인 플래그 자동 알림
```

### 플래그 네이밍 컨벤션
- Release: `release-{feature-name}` (예: `release-new-checkout`)
- Experiment: `exp-{test-name}` (예: `exp-pricing-v2`)
- Ops: `ops-{system-name}` (예: `ops-external-payment`)
- Permission: `perm-{capability}` (예: `perm-advanced-analytics`)
