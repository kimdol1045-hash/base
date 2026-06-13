---
id: "qa.test-gen.testing-trophy"
domain: "qa"
type: "rule"
bloom_level: ""
tags: ["qa", "testing-trophy", "test-pyramid", "strategy"]
brain_region: "CEREBELLUM"
token_estimate: 420
---

# qa.test-gen.testing-trophy

> #154 Testing Trophy (Kent C. Dodds) + Test Pyramid (Mike Cohn)

테스트 전략 프레임워크 (무엇을 얼마나 테스트할지 결정한다):

### Testing Trophy (프론트엔드 권장)
```
     E2E (소수)          ← 핵심 유저 플로우만
    Integration (다수)    ← 컴포넌트 조합 테스트 (가장 ROI 높음)
   Unit (적당히)          ← 순수 함수, 유틸리티
  Static (기본)           ← TypeScript, ESLint
```

### Test Pyramid (백엔드 권장)
```
     E2E (소수)
    Integration (중간)
   Unit (다수)            ← 비즈니스 로직 집중
  Static (기본)
```

### 유형별 가이드
| 유형 | 대상 | 속도 | 비율 |
|------|------|------|------|
| Static | 타입 에러, 린트 규칙 | 즉시 | 항상 |
| Unit | 순수 함수, 유틸 | ms | 20-30% |
| Integration | API+DB, 컴포넌트+훅 | 100ms~1s | 40-50% |
| E2E | 사용자 시나리오 | 수초~분 | 10-20% |

### 테스트 작성 우선순위
1. 버그가 발생한 곳 (회귀 방지)
2. 비즈니스 크리티컬 경로 (결제, 인증)
3. 복잡한 로직 (조건 분기 많은 곳)
4. 자주 변경되는 코드

### 안티패턴
- 100% 커버리지 집착 (유지보수 비용 > 가치)
- 구현 디테일 테스트 (리팩토링 시 전부 깨짐)
- Snapshot 남용 (변경 시 무조건 업데이트)
- 느린 테스트 방치 (10초 넘으면 분리)

## Connections

- [[qa.test-gen.role]] — REQUIRES (weight: 0.9)
- [[qa.test-gen.verify]] — FEEDS (weight: 0.8)
- [[qa.test-gen.integration]] — FEEDS (weight: 0.7)
- [[qa.code-review.role]] — FEEDS (weight: 0.5)
- [[qa.code-review.priority]] — FEEDS (weight: 0.5)
- [[qa.code-review.performance]] — FEEDS (weight: 0.5)
- [[qa.test-gen.role]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.unit]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.integration]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.component-test]] — CO_CREATES (weight: 0.6)
- [[qa.test-gen.verify]] — CO_CREATES (weight: 0.6)
