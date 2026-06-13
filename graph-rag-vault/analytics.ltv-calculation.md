---
id: "analytics.ltv-calculation"
domain: "analytics"
type: "pattern"
bloom_level: "고객 생애 가치(LTV/CLV)는 한 고객이 전체 관계 기간 동안 창출하는 총 수익이다. CAC(고객 획득 비용) 대비 LTV 비율이 3:1 이상이면 건전한 유닛 이코노믹스로 평가한다."
tags: ["ltv", "clv", "unit-economics", "revenue"]
brain_region: "THALAMUS"
token_estimate: 400
---

# analytics.ltv-calculation

> 고객 생애 가치(LTV/CLV)는 한 고객이 전체 관계 기간 동안 창출하는 총 수익이다. CAC(고객 획득 비용) 대비 LTV 비율이 3:1 이상이면 건전한 유닛 이코노믹스로 평가한다.

# LTV(고객 생애 가치) 산출 가이드

## 핵심 원칙
- LTV > 3 x CAC 이면 건전한 비즈니스 모델
- 세그먼트별 LTV 차이가 전략적 의사결정의 핵심
- 예측 LTV와 실현 LTV를 구분하여 추적
- 할인율을 적용하여 현재 가치로 환산

## 산출 공식
### 기본 공식
LTV = ARPU x Gross Margin x 평균 고객 수명

### 구독 모델
LTV = 월 구독료 x Gross Margin / 월간 이탈률

### 거래 모델
LTV = 평균 주문 금액 x 연간 구매 횟수 x 평균 고객 수명

## 분석 프로세스
1. 세그먼트별 ARPU 산출
2. 코호트별 리텐션 곡선에서 평균 수명 추정
3. 총이익률(Gross Margin) 적용
4. 할인율 적용 (보통 10%)
5. CAC 대비 비율 산출
6. 세그먼트별 LTV/CAC 비교

## DO
- 월 단위로 LTV 추적 및 트렌드 분석
- 채널별, 세그먼트별 LTV 분리 산출
- LTV 기반 마케팅 예산 배분

## DON'T
- LTV를 과도하게 낙관적으로 추정하지 않기
- 이탈률 변화를 무시하고 과거 데이터만 사용하지 않기
- 전체 평균 LTV만으로 의사결정하지 않기
