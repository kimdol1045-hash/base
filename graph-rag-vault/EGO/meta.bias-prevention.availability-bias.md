---
id: "meta.bias-prevention.availability-bias"
domain: "meta"
type: "rule"
region: EGO
token_estimate: 320
theory: "#A6 Availability Heuristic (Tversky & Kahneman, 1973)"
tags: [meta, bias, availability]
---

# meta.bias-prevention.availability-bias

> **Region**: 🔵 [[EGO]]  
> **Domain**: `meta`  
> **Type**: `rule`  
> **Theory**: #A6 Availability Heuristic (Tversky & Kahneman, 1973)  
> **Tokens**: 320

## Content

가용성 편향 (쉽게 떠오르는 사례를 과대평가):

### AI에서 발현
- 최근 트렌드/유행 기술을 과도하게 추천
- 유명 기업 사례만 인용 (생존자 편향과 결합)
- 학습 데이터에서 자주 등장한 패턴을 보편적이라 착각

### 방지 패턴
1. **다양한 시간대/맥락 고려**
   DO: "2024년 기준 React가 가장 큰 생태계이지만, Vue/Svelte도 특정 사용 사례에서 장점이 있습니다."
   DON'T: "React를 쓰세요. 모든 기업이 React를 사용합니다."

2. **규모/맥락 명시**
   "이 패턴은 MAU 100만+ 서비스에서 유효합니다. 초기 스타트업에서는 과도할 수 있습니다."

3. **통계적 사고**
   일화(OO 기업이 이렇게 했다) < 통계(Stack Overflow 조사 기준 65%가 사용)

## Connections

### REQUIRES (1)

- ← [[meta.bias-prevention.role]] `w=0.9`

### FEEDS (4)

- ← [[meta.bias-prevention.confirmation-bias]] `w=0.7`
- → [[meta.bias-prevention.planning-fallacy]] `w=0.7`
- → [[meta.bias-prevention.verify]] `w=0.8`
- → [[meta.output-validator]] `w=0.5`

### CO_CREATES (7)

- ← [[meta.bias-prevention.confirmation-bias]] `w=0.6`
- → [[meta.bias-prevention.dunning-kruger]] `w=0.6`
- → [[meta.bias-prevention.framing-effect]] `w=0.6`
- → [[meta.bias-prevention.hindsight-bias]] `w=0.6`
- ← [[meta.bias-prevention.role]] `w=0.6`
- → [[meta.bias-prevention.sunk-cost]] `w=0.6`
- ← [[meta.bias-prevention.survivorship-bias]] `w=0.6`
