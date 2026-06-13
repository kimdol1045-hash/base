---
id: "content.verify"
domain: "content"
type: "verify"
bloom_level: ""
tags: ["content", "verify"]
brain_region: "WERNICKE"
token_estimate: 300
---

# content.verify

콘텐츠 자기 검증:

### A. 구조
- [ ] 결론/핵심이 첫 1-2문장에 있는가? (역피라미드)
- [ ] 목적에 맞는 구조를 선택했는가? (문제-해결, 단계별, 비교, 원인-결과)
- [ ] H2/H3 제목만 읽어도 전체 흐름이 파악되는가?

### B. 가독성
- [ ] 문장이 30자 이내인가? (최대 50자)
- [ ] 문단이 3-4문장 이내인가?
- [ ] 능동태를 사용했는가?
- [ ] 전문용어에 설명을 병기했는가?

### C. 정확성
- [ ] 검증 불가능한 주장에 [출처 필요] 태그가 있는가?
- [ ] 수치/데이터에 출처가 있는가?
- [ ] 코드 예시가 실제로 동작하는가?

### D. 목적 달성
- [ ] 독자가 이 글을 읽고 다음 행동을 알 수 있는가?
- [ ] CTA가 명확한가?
- [ ] 타겟 독자 수준에 맞는 난이도인가?

## Connections

- [[content.role]] — REQUIRES (weight: 0.85)
- [[content.inverted-pyramid]] — FEEDS (weight: 0.8)
- [[content.readability]] — FEEDS (weight: 0.8)
- [[content.structure]] — FEEDS (weight: 0.8)
- [[content.technical-docs]] — FEEDS (weight: 0.8)
