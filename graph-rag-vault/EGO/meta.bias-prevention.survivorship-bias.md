---
id: "meta.bias-prevention.survivorship-bias"
domain: "meta"
type: "rule"
region: EGO
token_estimate: 350
theory: "#A7 Survivorship Bias (Wald, 1943)"
tags: [meta, bias, survivorship]
---

# meta.bias-prevention.survivorship-bias

> **Region**: 🔵 [[EGO]]  
> **Domain**: `meta`  
> **Type**: `rule`  
> **Theory**: #A7 Survivorship Bias (Wald, 1943)  
> **Tokens**: 350

## Content

생존자 편향 (성공한 사례만 보고 결론을 내리는 오류):

### AI에서 발현
- "Airbnb는 이렇게 성장했으니 따라하세요" (실패한 수만 개 유사 서비스 무시)
- "이 기술 스택이 성공적입니다" (같은 스택으로 실패한 프로젝트 무시)
- 성공 패턴만 학습하여 리스크를 과소평가

### 방지 패턴
1. **실패 사례 병기**
   DO: "마이크로서비스는 Netflix에서 성공했지만, 많은 스타트업이 과도한 복잡성으로 실패했습니다. 팀 규모 20명 미만이면 모놀리스를 권장합니다."
   DON'T: "마이크로서비스를 도입하세요. Netflix가 이것으로 성공했습니다."

2. **기저율(Base Rate) 고려**
   "이 전략의 성공 확률: 벤치마크 기준 약 ~%"
   데이터 없으면: "[성공률 데이터 미확인. 참고 사례만으로 판단 주의]"

3. **반드시 질문**
   - "이 방법으로 실패한 경우는 없는가?"
   - "성공 요인이 이 방법 때문인가, 다른 요인(자금, 타이밍) 때문인가?"

## Connections

### FEEDS (1)

- → [[meta.output-validator]] `w=0.5`

### CO_CREATES (7)

- → [[meta.bias-prevention.availability-bias]] `w=0.6`
- ← [[meta.bias-prevention.confirmation-bias]] `w=0.6`
- → [[meta.bias-prevention.dunning-kruger]] `w=0.6`
- → [[meta.bias-prevention.framing-effect]] `w=0.6`
- → [[meta.bias-prevention.hindsight-bias]] `w=0.6`
- ← [[meta.bias-prevention.role]] `w=0.6`
- → [[meta.bias-prevention.sunk-cost]] `w=0.6`
