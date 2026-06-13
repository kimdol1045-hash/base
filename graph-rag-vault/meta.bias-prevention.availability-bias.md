---
id: "meta.bias-prevention.availability-bias"
domain: "meta"
type: "rule"
bloom_level: ""
tags: ["meta", "bias", "availability"]
brain_region: "PREFRONTAL"
token_estimate: 320
---

# meta.bias-prevention.availability-bias

> #A6 Availability Heuristic (Tversky & Kahneman, 1973)

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

- [[meta.bias-prevention.role]] — REQUIRES (weight: 0.9)
- [[meta.bias-prevention.verify]] — FEEDS (weight: 0.8)
- [[meta.bias-prevention.confirmation-bias]] — FEEDS (weight: 0.7)
- [[meta.bias-prevention.planning-fallacy]] — FEEDS (weight: 0.7)
- [[meta.bias-prevention.role]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.confirmation-bias]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.survivorship-bias]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.dunning-kruger]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.framing-effect]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.hindsight-bias]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.sunk-cost]] — CO_CREATES (weight: 0.6)
- [[meta.output-validator]] — FEEDS (weight: 0.5)
