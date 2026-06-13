---
id: "meta.bias-prevention.survivorship-bias"
domain: "meta"
type: "pattern"
bloom_level: "생존자 편향은 성공 사례만 관찰하고 실패 사례를 무시하여 잘못된 결론을 도출하는 편향이다. Abraham Wald의 2차 세계대전 항공기 분석이 대표 사례로, 돌아온 비행기가 아닌 돌아오지 못한 비행기에 주목해야 한다."
tags: ["survivorship-bias", "cognitive-bias", "analysis"]
brain_region: "PREFRONTAL"
token_estimate: 380
---

# meta.bias-prevention.survivorship-bias

> 생존자 편향은 성공 사례만 관찰하고 실패 사례를 무시하여 잘못된 결론을 도출하는 편향이다. Abraham Wald의 2차 세계대전 항공기 분석이 대표 사례로, 돌아온 비행기가 아닌 돌아오지 못한 비행기에 주목해야 한다.

# 생존자 편향 방지 가이드

## 정의
성공한 사례만 보고 일반화하여, 실패·이탈·소멸한 사례를 간과하는 편향.
예: "성공한 CEO는 모두 중퇴했다" → 중퇴 후 실패한 수만 명은 보이지 않음.

## 발생 시나리오
- 제품 분석: 활성 사용자만 분석, 이탈자 무시
- 벤치마킹: 성공 기업만 연구, 같은 전략으로 실패한 기업 무시
- 기능 평가: 사용 중인 기능만 보고, 미사용 기능 방치
- 투자 판단: 성공 포트폴리오만 공개, 손실은 숨김

## 방지 전략
1. **이탈자 분석**: 떠난 사용자/실패한 사례를 적극 조사
2. **모수 확인**: 전체 모집단 대비 성공 비율 계산
3. **반증 탐색**: "이 전략을 따랐지만 실패한 사례는?"
4. **사전 등록**: 분석 시작 전 전체 데이터셋 확정

## 체크리스트
- [ ] 분석 대상에 실패/이탈 사례가 포함되어 있는가?
- [ ] 전체 모집단 대비 성공률을 계산했는가?
- [ ] 동일 조건에서 실패한 사례를 탐색했는가?
- [ ] "보이지 않는 데이터"가 있는지 확인했는가?

## DO
- 이탈 사용자 인터뷰 또는 이탈 설문 실시
- 전체 코호트 기반 분석 수행
- 실패 사례를 의사결정에 동등한 비중으로 포함

## DON'T
- 성공 사례만으로 전략을 일반화하지 않기
- "우리 사용자는 만족합니다" (떠난 사람은 말하지 않음)

## Connections

- [[meta.bias-prevention.role]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.confirmation-bias]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.availability-bias]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.dunning-kruger]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.framing-effect]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.hindsight-bias]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.sunk-cost]] — CO_CREATES (weight: 0.6)
- [[meta.output-validator]] — FEEDS (weight: 0.5)
