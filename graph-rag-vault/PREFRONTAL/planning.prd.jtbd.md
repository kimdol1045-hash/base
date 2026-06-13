---
id: "planning.prd.jtbd"
domain: "planning"
type: "rule"
region: PREFRONTAL
token_estimate: 480
theory: "#56 JTBD (Christensen, 2003)"
tags: [planning, prd, jtbd, framework]
---

# planning.prd.jtbd

> **Region**: 🧠 [[PREFRONTAL]]  
> **Domain**: `planning`  
> **Type**: `rule`  
> **Theory**: #56 JTBD (Christensen, 2003)  
> **Tokens**: 480

## Content

Jobs-to-be-Done (고객이 제품을 "고용"하는 이유를 파악한다):

### 왜 JTBD인가?
고객은 제품의 기능을 사는 것이 아니라, 자신의 삶에서 진전(Progress)을
만들기 위해 제품을 "고용"한다. 기능 중심이 아닌 고객의 Job 중심으로
문제를 정의해야 진짜 해결할 문제를 놓치지 않는다.

### JTBD 스토리 작성법
형식: "When [상황], I want to [동기], so I can [기대결과]"

DO:
- "When 퇴근 후 저녁을 준비할 때, I want to 15분 내로 만들 수 있는
  레시피를 찾고 싶다, so I can 가족과 저녁 시간을 더 보낼 수 있다"
- 상황(When)이 구체적일수록 좋다. 시간, 장소, 감정 상태를 포함할 것.
- "When 월말 정산 마감 전날 밤, I want to 자동으로 경비를 분류하고 싶다,
  so I can 실수 없이 마감 시간을 맞출 수 있다"

DON'T:
- "When 앱을 사용할 때, I want to 좋은 경험을 하고 싶다, so I can 만족할 수 있다"
  → 어디서든 적용 가능한 문장은 JTBD가 아니다.
- "When 업무를 할 때, I want to 효율적으로 일하고 싶다, so I can 성과를 낼 수 있다"
  → 구체적 상황과 감정이 빠져 있다.

### JTBD 계층 구조
하나의 큰 Job은 여러 하위 Job으로 분해된다:
```
Core Job: 건강한 식단을 유지하고 싶다
├── Functional Job: 영양 균형 잡힌 식사를 준비한다
│   ├── Sub-Job: 재료를 빠르게 구매한다
│   └── Sub-Job: 조리 시간을 단축한다
├── Emotional Job: 건강 관리를 잘 하고 있다는 안심감
└── Social Job: 가족에게 좋은 음식을 제공하는 사람으로 인정받기
```

### 경쟁 분석과 연결
현재 고객이 이 Job을 어떻게 해결하는지 반드시 파악:
- 직접 경쟁: 같은 Job을 해결하는 다른 앱/서비스
- 간접 경쟁: 엑셀, 수기, 카톡 그룹 등 비전통적 수단
- 무소비(Non-consumption): 아예 해결하지 않고 포기하는 경우

### 전환 장벽 분석 (Forces of Progress)
고객이 새 솔루션으로 전환하는 데 작용하는 4가지 힘:
| 추진력 (전환 촉진) | 저항력 (전환 방해) |
|---------------------|---------------------|
| Push: 현재 솔루션 불만 | Habit: 기존 습관의 관성 |
| Pull: 새 솔루션의 매력 | Anxiety: 전환 시 불안감 |

작성 템플릿:
- Push: "현재 [대안]을 쓸 때 [구체적 불만]이 있다"
- Pull: "새 솔루션이 [구체적 이점]을 제공한다"
- Habit: "이미 [기존 방식]에 [N개월/N년] 익숙하다"
- Anxiety: "[전환 시 우려사항]이 걱정된다"

### 주의사항
- JTBD는 페르소나가 아니다: 같은 페르소나라도 상황에 따라 다른 Job을 가진다
- 솔루션을 JTBD 안에 넣지 말 것: "앱으로 주문하고 싶다"는 Job이 아니라 솔루션이다
- 반드시 현장 인터뷰 또는 리뷰 데이터로 검증 필요 → 데이터 없으면 "[가설]" 표기

## Connections

### REQUIRES (1)

- ← [[planning.prd.role]] `w=0.9`

### FEEDS (2)

- → [[planning.prd.mvp]] `w=0.7`
- → [[planning.prd.verify]] `w=0.8`
