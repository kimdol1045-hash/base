---
id: "dev.frontend.performance.bundle-optimization"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "performance", "bundle", "optimization"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.performance.bundle-optimization

> #251 Bundle Analysis (Webpack Bundle Analyzer, Sean Larkin 2017)

# 번들 최적화 가이드

## 핵심 원칙
- 번들 크기는 사용자 경험에 직접적인 영향을 미친다
- 정기적으로 번들을 분석하여 불필요한 의존성을 제거한다
- Tree-shaking이 효과적으로 동작하도록 ESM 모듈을 사용한다
- 번들 크기 예산(Budget)을 설정하고 CI에서 검증한다

## DO
- `@next/bundle-analyzer`로 정기적으로 번들을 분석한다
- barrel export(index.ts)를 피하고 직접 임포트한다
- 무거운 라이브러리는 경량 대안으로 교체한다 (moment → dayjs, lodash → lodash-es)
- `sideEffects: false`를 package.json에 설정하여 Tree-shaking을 돕는다

## DON'T
- 전체 라이브러리를 임포트하지 않는다 (`import _ from 'lodash'` 금지)
- 사용하지 않는 의존성을 package.json에 남겨두지 않는다
- 번들 분석 없이 라이브러리를 무분별하게 추가하지 않는다
- polyfill을 무조건 전체 포함하지 않는다 (타겟 브라우저 기반)

## 코드 예시
```typescript
// ❌ 전체 임포트 (Tree-shaking 불가)
import _ from "lodash";
const sorted = _.sortBy(users, "name");

// ✅ 개별 임포트
import sortBy from "lodash-es/sortBy";
const sorted = sortBy(users, "name");

// ❌ barrel export 체인
// utils/index.ts - 하나만 쓰더라도 전부 번들링
export { formatDate } from "./date";
export { formatCurrency } from "./currency";
export { formatNumber } from "./number";

// ✅ 직접 임포트
import { formatDate } from "@/utils/date";
```

```js
// next.config.js - 번들 분석 설정
const withBundleAnalyzer = require("@next/bundle-analyzer")({
  enabled: process.env.ANALYZE === "true",
});
module.exports = withBundleAnalyzer({ /* ... */ });

// 실행: ANALYZE=true next build
```

```yaml
# CI 번들 크기 예산 검증
- name: Check bundle size
  run: |
    npx next build
    SIZE=$(du -sk .next/static | cut -f1)
    if [ $SIZE -gt 500 ]; then
      echo "번들 크기 초과: ${SIZE}KB > 500KB"
      exit 1
    fi
```
