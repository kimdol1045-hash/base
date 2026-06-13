---
id: "qa.code-review.verify"
domain: "qa"
type: "verify"
bloom_level: ""
tags: ["qa", "code-review", "verification", "quality-gate"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# qa.code-review.verify

코드 리뷰 자기 검증 체크리스트:

### 리뷰 완성도 검증 (PASS: 전부 충족 / FAIL: 하나라도 미충족)
- [ ] 모든 이슈에 위치(파일:라인)가 명시되어 있는가?
- [ ] 모든 이슈에 "왜 문제인지" 기술적 이유가 포함되어 있는가?
- [ ] 모든 이슈에 구체적인 수정 코드(Before/After)가 제시되어 있는가?
- [ ] 품질 점수(1-10)를 부여하고 근거를 설명했는가?

### 정확성 검증
- [ ] 수정 제안 코드가 실제로 컴파일/실행 가능한가?
- [ ] 프로젝트 기술 스택에 맞는 제안인가? (React 프로젝트에 Vue 문법 등 혼동 없는가?)
- [ ] 제안한 라이브러리/API가 실제로 존재하고, 현재 버전에서 사용 가능한가?
- [ ] TypeScript 타입이 올바른가? (any 사용을 지적했으면서 제안 코드에 any가 있지 않은가?)

### 우선순위 검증
- [ ] 보안 이슈를 Critical/High로 분류했는가? (Low로 내리지 않았는가?)
- [ ] 코드 스타일을 Critical로 올리지 않았는가?
- [ ] 이슈 목록이 심각도 순으로 정렬되어 있는가?
- [ ] Critical/High 이슈 개수와 품질 점수가 일관되는가?
  - Critical 있으면 점수 1-2
  - High 있으면 점수 3-4
  - Medium만 있으면 점수 5-6

### 톤 & 균형 검증
- [ ] 잘된 점을 최소 1개 이상 언급했는가?
- [ ] "틀렸다/잘못됐다" 대신 "이렇게 하면 더 좋다" 톤인가?
- [ ] 사소한 이슈에 과도한 분량을 할애하지 않았는가?
- [ ] 같은 패턴의 반복 이슈는 대표 1개 + "외 N건" 형식으로 그룹핑했는가?

### PASS/FAIL 판정
- **PASS**: 리뷰가 정확하고, 실행 가능한 제안을 포함하며, 우선순위가 적절
- **FAIL**: 하나라도 미충족 시 해당 항목 명시 후 리뷰 보완
- Critical FAIL: 보안 이슈를 놓침, 컴파일 불가능한 코드 제안 → 리뷰 재작성

## Connections

- [[qa.code-review.role]] — REQUIRES (weight: 0.85)
- [[qa.test-gen.role]] — REQUIRES (weight: 0.85)
- [[qa.code-review.priority]] — FEEDS (weight: 0.8)
- [[qa.code-review.readability]] — FEEDS (weight: 0.8)
- [[qa.code-review.security]] — FEEDS (weight: 0.8)
- [[qa.test-gen.integration]] — FEEDS (weight: 0.8)
- [[qa.code-review.bug-analysis]] — FEEDS (weight: 0.8)
- [[qa.code-review.performance]] — FEEDS (weight: 0.8)
