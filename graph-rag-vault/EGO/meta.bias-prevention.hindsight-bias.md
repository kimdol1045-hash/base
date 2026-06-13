---
id: "meta.bias-prevention.hindsight-bias"
domain: "meta"
type: "rule"
region: EGO
token_estimate: 450
theory: "#A10 Hindsight Bias (Fischhoff, 1975)"
tags: [meta, bias, hindsight, postmortem, blameless, decision-making]
---

# meta.bias-prevention.hindsight-bias

> **Region**: 🔵 [[EGO]]  
> **Domain**: `meta`  
> **Type**: `rule`  
> **Theory**: #A10 Hindsight Bias (Fischhoff, 1975)  
> **Tokens**: 450

## Content

사후 확신 편향 — 결과를 알고 난 후 "그럴 줄 알았다"고 느끼는 편향:

### 핵심 원리
- 결과가 나온 후, 그 결과가 예측 가능했다고 착각
- "I knew it all along" 효과 — 실제로는 알지 못했음
- 실패 원인 분석 시 특히 위험 (과도한 비난, 잘못된 교훈)

### 소프트웨어 개발에서의 영향
| 상황 | 사후 확신 편향 | 실제 |
|------|--------------|------|
| 장애 분석 | "그 코드가 위험한 건 당연했지" | 당시 정보로는 합리적 판단이었음 |
| 기술 선택 회고 | "그 기술이 망할 줄 알았어" | 당시 시장 평가는 긍정적이었음 |
| 스프린트 회고 | "그 일정이 무리인 건 뻔했지" | 추정 시점의 정보는 제한적이었음 |
| 버그 리뷰 | "이 엣지 케이스를 놓치다니" | 수천 개 경로 중 하나였음 |

### 방지 전략
```
1. 의사결정 로그 (Decision Log):
   - 결정 시점의 정보, 대안, 근거를 기록
   - 회고 시 "당시 알 수 있었던 것"만으로 판단

2. Pre-mortem (사전 부검):
   - 프로젝트 시작 시 "실패 시나리오" 미리 작성
   - 기록된 예측과 실제 결과 비교 → 편향 인식

3. Blameless postmortem:
   - "누가 잘못했나" → "시스템이 어떻게 실패를 허용했나"
   - 당시 상황에서의 합리성을 인정
```

DO:
- 모든 주요 결정에 의사결정 로그 작성 (날짜, 맥락, 대안, 근거)
- 장애 분석 시 "당시 가용 정보"만으로 판단 평가
- Blameless culture — 개인이 아닌 시스템/프로세스 개선
- 예측을 기록하고 나중에 정확도 측정

DON'T:
- "당연히 예측 가능했다"는 전제로 비난
- 결과론적으로 의사결정 품질 평가
- 장애 원인을 개인의 부주의로만 귀결
- 사후 확신으로 만든 규칙을 과도하게 추가 (규칙 비대화)

### Postmortem 템플릿 보강
- 섹션 추가: "당시 알 수 있었던 정보 vs 알 수 없었던 정보"
- 질문: "같은 정보를 가진 다른 팀이라도 같은 판단을 했을까?"

## Connections

### FEEDS (1)

- → [[meta.output-validator]] `w=0.5`

### CO_CREATES (7)

- ← [[meta.bias-prevention.availability-bias]] `w=0.6`
- ← [[meta.bias-prevention.confirmation-bias]] `w=0.6`
- ← [[meta.bias-prevention.dunning-kruger]] `w=0.6`
- ← [[meta.bias-prevention.framing-effect]] `w=0.6`
- ← [[meta.bias-prevention.role]] `w=0.6`
- → [[meta.bias-prevention.sunk-cost]] `w=0.6`
- ← [[meta.bias-prevention.survivorship-bias]] `w=0.6`
