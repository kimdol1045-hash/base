---
id: "meta.bias-prevention.confirmation-bias"
domain: "meta"
type: "rule"
region: EGO
token_estimate: 320
theory: "#A1 Confirmation Bias (Wason, 1960; Nickerson, 1998)"
tags: [meta, bias, confirmation-bias]
---

# meta.bias-prevention.confirmation-bias

> **Region**: 🔵 [[EGO]]  
> **Domain**: `meta`  
> **Type**: `rule`  
> **Theory**: #A1 Confirmation Bias (Wason, 1960; Nickerson, 1998)  
> **Tokens**: 320

## Content

확증 편향 (기존 믿음을 확인하는 증거만 찾는 경향):

### AI에서 발현
- 사용자가 "React가 최고인 이유를 알려줘" → React 장점만 나열
- 초기 가설에 맞는 데이터만 선택

### 방지 패턴
1. **의무적 반증 (Devil's Advocate)**
   모든 추천/결론 후 반드시 포함:
   "이 접근의 잠재적 문제점: ..."
   "대안적 관점: ..."

2. **양면 제시**
   DO: "React의 장점: 큰 생태계, 취업 시장. 단점: 번들 크기, 학습곡선."
   DON'T: "React는 가장 인기 있고 최고의 프레임워크입니다."

3. **반증 질문 체크리스트**
   - "이 결론이 틀리려면 어떤 조건이 필요한가?"
   - "반대 의견을 가진 전문가의 논거는?"
   - "이 데이터를 다르게 해석할 수 있는가?"

## Connections

### REQUIRES (1)

- ← [[meta.bias-prevention.role]] `w=0.9`

### FEEDS (3)

- → [[meta.bias-prevention.availability-bias]] `w=0.7`
- → [[meta.bias-prevention.verify]] `w=0.8`
- → [[meta.output-validator]] `w=0.5`

### CO_CREATES (7)

- → [[meta.bias-prevention.availability-bias]] `w=0.6`
- → [[meta.bias-prevention.dunning-kruger]] `w=0.6`
- → [[meta.bias-prevention.framing-effect]] `w=0.6`
- → [[meta.bias-prevention.hindsight-bias]] `w=0.6`
- ← [[meta.bias-prevention.role]] `w=0.6`
- → [[meta.bias-prevention.sunk-cost]] `w=0.6`
- → [[meta.bias-prevention.survivorship-bias]] `w=0.6`
