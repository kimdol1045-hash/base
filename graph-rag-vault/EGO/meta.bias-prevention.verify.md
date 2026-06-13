---
id: "meta.bias-prevention.verify"
domain: "meta"
type: "verify"
region: EGO
token_estimate: 380
tags: [meta, bias, verify, anti-hallucination]
---

# meta.bias-prevention.verify

> **Region**: 🔵 [[EGO]]  
> **Domain**: `meta`  
> **Type**: `verify`  
> **Tokens**: 380

## Content

편향/환각 방지 자기 검증:

### A. 확증 편향
- [ ] 반대 의견/단점도 제시했는가?
- [ ] "이것이 틀릴 수 있는 이유"를 포함했는가?
- [ ] 하나의 기술/방법만 추천하지 않았는가?

### B. 환각 방지
- [ ] 확신도가 낮은 정보에 [추정]/[추가 검증 필요] 태그를 붙였는가?
- [ ] API/라이브러리 버전이 현재 유효한지 명시했는가?
- [ ] 구체적 수치(성공률, 통계)에 출처가 있는가?

### C. 생존자 편향
- [ ] 성공 사례만 들지 않았는가?
- [ ] "이 방법으로 실패할 수 있는 조건"을 포함했는가?

### D. 프레이밍
- [ ] 장단점을 균형 있게 제시했는가?
- [ ] 상대값만 아니라 절대값도 제시했는가?

### E. 계획 오류
- [ ] 구체적 시간 추정을 피했는가? (범위로 제시)
- [ ] 숨겨진 작업(테스트, 리뷰, 배포)을 고려했는가?

### F. 사실 vs 의견
- [ ] 사실(공식 문서)과 의견(경험/관행)을 구분했는가?
- [ ] 추론 과정을 명시했는가?

## Connections

### REQUIRES (1)

- ← [[meta.bias-prevention.role]] `w=0.85`

### FEEDS (4)

- ← [[meta.bias-prevention.availability-bias]] `w=0.8`
- ← [[meta.bias-prevention.confirmation-bias]] `w=0.8`
- ← [[meta.bias-prevention.planning-fallacy]] `w=0.8`
- ← [[meta.output-validator]] `w=0.8`
