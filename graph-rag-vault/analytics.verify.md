---
id: "analytics.verify"
domain: "analytics"
type: "verify"
bloom_level: ""
tags: ["analytics", "verify"]
brain_region: "THALAMUS"
token_estimate: 350
---

# analytics.verify

데이터 분석 자기 검증:

### A. 실험 설계
- [ ] 가설이 검증 가능한 형태로 명확한가?
- [ ] 1차 지표(primary metric)가 정의되었는가?
- [ ] 표본 크기가 충분한가? (최소 감지 효과 기반)
- [ ] 실험 기간이 요일 효과를 포함하는가? (최소 1주)

### B. 분석 품질
- [ ] 세그먼트별 분석을 했는가? (심슨의 역설 방지)
- [ ] 통계적 유의성을 확인했는가? (p < 0.05 또는 95% CI)
- [ ] 효과 크기(실질적 의미)도 확인했는가?
- [ ] 교란 변수를 고려했는가?

### C. 해석
- [ ] 상관관계를 인과관계로 혼동하지 않았는가?
- [ ] 허영 지표가 아닌 실행 지표를 사용했는가?
- [ ] 결론에 한계점을 명시했는가?

### D. 윤리
- [ ] 데이터에서 개인 식별 정보가 제거되었는가?
- [ ] 결과를 cherry-picking하지 않았는가?

## Connections

- [[analytics.role]] — REQUIRES (weight: 0.85)
- [[analytics.ab-testing]] — FEEDS (weight: 0.8)
- [[analytics.metrics]] — FEEDS (weight: 0.8)
- [[analytics.funnel-analysis]] — FEEDS (weight: 0.8)
- [[analytics.cohort-analysis]] — FEEDS (weight: 0.8)
- [[analytics.bayesian]] — FEEDS (weight: 0.8)
