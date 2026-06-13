---
id: "meta.bias-prevention.sunk-cost"
domain: "meta"
type: "rule"
region: EGO
token_estimate: 450
theory: "#A8 Sunk Cost Fallacy (Arkes & Blumer, 1985)"
tags: [meta, bias, sunk-cost, decision-making, project-management]
---

# meta.bias-prevention.sunk-cost

> **Region**: 🔵 [[EGO]]  
> **Domain**: `meta`  
> **Type**: `rule`  
> **Theory**: #A8 Sunk Cost Fallacy (Arkes & Blumer, 1985)  
> **Tokens**: 450

## Content

매몰 비용 오류 — 이미 투자한 비용 때문에 잘못된 방향을 계속 추구하는 편향:

### 핵심 원리
- "이미 3개월 개발했으니 계속 가자" → 전형적 매몰 비용 오류
- 합리적 판단 기준: 과거 투자가 아닌 미래 기대 가치
- Concorde Fallacy (콩코드 오류)라고도 불림

### 소프트웨어 개발에서 흔한 매몰 비용 패턴
| 상황 | 매몰 비용 사고 | 올바른 판단 |
|------|--------------|------------|
| 레거시 리팩토링 | "이미 많이 고쳤으니 계속" | 나머지 비용 vs 새로 쓰는 비용 비교 |
| 기능 개발 | "80% 완성했으니 마무리" | 나머지 20%의 ROI가 양수인가? |
| 기술 선택 | "팀이 이미 학습했으니" | 전환 비용 vs 장기 생산성 비교 |
| 채용 | "온보딩에 투자했으니" | 현재 성과와 미래 기여도 기준 |

### 방지 체크리스트
```
의사결정 시 다음 질문을 강제:
1. "지금 새로 시작한다면, 같은 선택을 할 것인가?"
2. "과거 투자를 제외하고, 앞으로의 비용 대비 이익은?"
3. "계속 진행의 기회비용은? (다른 일을 못 하는 비용)"
4. "중단 시 실제 손실은? (대부분 심리적 손실만 있음)"
```

DO:
- Kill criteria를 프로젝트 시작 시 미리 정의
- 정기 회고에서 "중단 옵션" 명시적으로 검토
- 의사결정을 "투자한 사람"이 아닌 "제3자"에게 위임
- Pre-mortem: "이 프로젝트가 실패한다면 이유는?"

DON'T:
- "여기까지 왔는데" → 감정적 근거로 계속 진행
- 투자 규모로 프로젝트 중요도 판단
- 중단을 "실패"로 프레이밍 (중단은 자원 재배분)
- 의사결정자가 최초 투자 결정자와 동일인 (편향 증폭)

### 조직 수준 방지
- Quarterly kill review: 모든 진행 중 프로젝트에 "중단 시 영향" 명시
- Red team: 프로젝트 중단 논거를 전담으로 만드는 역할 배정
- Escalation path: 담당자가 중단을 건의할 수 있는 안전한 채널

## Connections

### FEEDS (1)

- → [[meta.output-validator]] `w=0.5`

### CO_CREATES (7)

- ← [[meta.bias-prevention.availability-bias]] `w=0.6`
- ← [[meta.bias-prevention.confirmation-bias]] `w=0.6`
- ← [[meta.bias-prevention.dunning-kruger]] `w=0.6`
- ← [[meta.bias-prevention.framing-effect]] `w=0.6`
- ← [[meta.bias-prevention.hindsight-bias]] `w=0.6`
- ← [[meta.bias-prevention.role]] `w=0.6`
- ← [[meta.bias-prevention.survivorship-bias]] `w=0.6`
