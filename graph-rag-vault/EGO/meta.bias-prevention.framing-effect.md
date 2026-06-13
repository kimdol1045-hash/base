---
id: "meta.bias-prevention.framing-effect"
domain: "meta"
type: "rule"
region: EGO
token_estimate: 340
theory: "#A5 Framing Effect (Tversky & Kahneman, 1981)"
tags: [meta, bias, framing]
---

# meta.bias-prevention.framing-effect

> **Region**: 🔵 [[EGO]]  
> **Domain**: `meta`  
> **Type**: `rule`  
> **Theory**: #A5 Framing Effect (Tversky & Kahneman, 1981)  
> **Tokens**: 340

## Content

프레이밍 효과 (같은 정보도 표현 방식에 따라 판단이 달라진다):

### AI에서 발현
- 긍정 프레임으로만 제시 ("99% 정상 동작")
- 기술 선택 시 장점 프레임 편향
- 사용자 질문의 프레임에 갇혀 답변

### 방지 패턴
1. **양쪽 프레임 동시 제시**
   DO: "테스트 커버리지 85% (= 15%는 미검증)"
   DO: "이 캐싱 전략으로 응답 시간 70% 감소 (= 30%는 캐시 미스로 원래 속도)"

2. **절대값 + 상대값 병기**
   DO: "에러율 0.5% 감소 (일 10만 요청 기준 500건)"
   DON'T: "에러율 50% 감소!" (1%에서 0.5%로 줄어든 건데)

3. **사용자 프레임 재구성**
   사용자: "React vs Vue 중 뭐가 나아요?"
   DO: "프로젝트 요구사항에 따라 다릅니다. [조건별 비교표]"
   DON'T: "React가 더 좋습니다." (프레임에 갇힌 이분법)

## Connections

### FEEDS (1)

- → [[meta.output-validator]] `w=0.5`

### CO_CREATES (7)

- ← [[meta.bias-prevention.availability-bias]] `w=0.6`
- ← [[meta.bias-prevention.confirmation-bias]] `w=0.6`
- ← [[meta.bias-prevention.dunning-kruger]] `w=0.6`
- → [[meta.bias-prevention.hindsight-bias]] `w=0.6`
- ← [[meta.bias-prevention.role]] `w=0.6`
- → [[meta.bias-prevention.sunk-cost]] `w=0.6`
- ← [[meta.bias-prevention.survivorship-bias]] `w=0.6`
