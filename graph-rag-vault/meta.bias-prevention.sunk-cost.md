---
id: "meta.bias-prevention.sunk-cost"
domain: "meta"
type: "pattern"
bloom_level: "매몰 비용 오류는 이미 투자한 비용(시간, 돈, 노력)을 회수하려는 심리로 인해 비합리적 결정을 지속하는 편향이다. 경제학에서 매몰 비용은 의사결정에 무관해야 하지만, 인간은 아까워서 멈추지 못한다."
tags: ["sunk-cost", "cognitive-bias", "decision-making"]
brain_region: "PREFRONTAL"
token_estimate: 380
---

# meta.bias-prevention.sunk-cost

> 매몰 비용 오류는 이미 투자한 비용(시간, 돈, 노력)을 회수하려는 심리로 인해 비합리적 결정을 지속하는 편향이다. 경제학에서 매몰 비용은 의사결정에 무관해야 하지만, 인간은 아까워서 멈추지 못한다.

# 매몰 비용 오류 방지 가이드

## 정의
이미 쓴 비용(시간/돈/노력)이 아까워서 손해 보는 결정을 계속하는 편향.
예: "이미 6개월 개발했으니 출시해야 한다" (시장 적합성 무시)

## 발생 시나리오
- 프로젝트 지속: 실패 징후에도 투자 계속
- 기술 선택: 잘못된 스택을 교체하지 않음
- 기능 유지: 사용률 0%인 기능을 삭제하지 않음
- 인력 배치: 성과 없는 팀에 계속 인원 투입

## 방지 전략
1. **제로 베이스 질문**: "지금 새로 시작한다면 같은 선택을 할까?"
2. **킬 크라이테리아**: 프로젝트 시작 시 중단 조건 사전 정의
3. **기회비용 산정**: 이 리소스로 다른 무엇을 할 수 있는가?
4. **외부 관점**: 이 상황을 처음 보는 사람이라면 어떤 결정?

## 체크리스트
- [ ] "이미 투자했으니까"가 계속하는 유일한 이유는 아닌가?
- [ ] 지금 새로 시작해도 같은 선택을 할 것인가?
- [ ] 사전에 정한 중단 기준을 충족했는가?
- [ ] 기회비용을 계산했는가?

## DO
- 프로젝트 시작 시 "실패 시 중단 조건" 사전 합의
- 분기별 "계속 vs 중단" 리뷰 실시
- 중단 결정을 실패가 아닌 학습으로 프레이밍

## DON'T
- "여기까지 왔는데"를 의사결정 근거로 사용하지 않기
- 감정적 애착으로 객관적 판단을 흐리지 않기

## Connections

- [[meta.bias-prevention.role]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.confirmation-bias]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.survivorship-bias]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.availability-bias]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.dunning-kruger]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.framing-effect]] — CO_CREATES (weight: 0.6)
- [[meta.bias-prevention.hindsight-bias]] — CO_CREATES (weight: 0.6)
- [[meta.output-validator]] — FEEDS (weight: 0.5)
