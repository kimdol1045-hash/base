---
id: "meta.bias-prevention.confirmation-bias"
domain: "meta"
type: "rule"
bloom_level: ""
tags: ["meta", "bias", "confirmation-bias"]
brain_region: "PREFRONTAL"
token_estimate: 320
---

# meta.bias-prevention.confirmation-bias

> #A1 Confirmation Bias (Wason, 1960; Nickerson, 1998)

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

- [[meta.bias-prevention.role]] — REQUIRES (weight: 0.9)
- [[meta.bias-prevention.verify]] — FEEDS (weight: 0.8)
- [[meta.bias-prevention.availability-bias]] — FEEDS (weight: 0.7)
- [[meta.bias-prevention.role]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.survivorship-bias]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.availability-bias]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.dunning-kruger]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.framing-effect]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.hindsight-bias]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.sunk-cost]] — CO_CREATES (weight: 0.6)
- [[meta.output-validator]] — FEEDS (weight: 0.5)
