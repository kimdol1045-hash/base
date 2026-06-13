---
id: "planning.user-persona.persona-template"
domain: "planning"
type: "pattern"
bloom_level: ""
tags: ["planning", "persona", "user-research", "jtbd", "template"]
brain_region: "PREFRONTAL"
token_estimate: 500
---

# planning.user-persona.persona-template

> #57 JTBD (Jobs to Be Done), #7 Jakob's Law

페르소나 생성 템플릿 — 데이터 기반 사용자 원형 정의:

### 페르소나 구성 요소
```
## [이름] — [한줄 요약]

### 인구통계
- 나이: [범위]
- 직업: [구체적]
- 기술 수준: [초급/중급/고급]
- 디바이스: [주 사용 기기]

### 목표 (Goals)
1. 기능적 목표: [무엇을 달성하려 하는가]
2. 감정적 목표: [어떤 기분을 느끼고 싶은가]
3. 사회적 목표: [어떻게 보이고 싶은가]

### 고통점 (Pain Points)
1. [현재 가장 큰 불편]
2. [기존 솔루션의 한계]
3. [포기한 것들]

### JTBD (Jobs to Be Done)
- "나는 [상황]일 때, [목표]를 달성하고 싶다.
   그래야 [기대 결과]를 얻을 수 있으니까."

### 행동 패턴
- 정보 탐색: [어디서 정보를 얻는가]
- 의사결정: [무엇이 구매를 결정하게 하는가]
- 사용 빈도: [일/주/월 몇 회]

### 인용구
"[이 페르소나가 실제로 할 법한 말]"
```

### 페르소나 생성 규칙
| 항목 | 기준 |
|------|------|
| 페르소나 수 | 주요 3-5개 (7개 초과 금지) |
| 데이터 근거 | 인터뷰 5명+ 또는 설문 50명+ |
| JTBD | 반드시 1개 이상 포함 |
| 우선순위 | Primary (1) → Secondary (1-2) → Tertiary |
| 안티 페르소나 | 1개 이상 (대상이 아닌 사용자) |

DO:
- 실제 인터뷰/데이터 기반으로 작성 (가설이면 [가설] 태그)
- JTBD 형식으로 목표를 "상황 → 동기 → 기대 결과"로 구조화
- 안티 페르소나 정의 (이 사람을 위해 만들지 않는다)
- 페르소나별 핵심 시나리오 1-3개 매핑

DON'T:
- 상상으로 페르소나 생성 (데이터 없이 [검증 필요] 태그 필수)
- 인구통계만으로 정의 (행동/목표/고통점이 핵심)
- 7개 초과 페르소나 (의사결정 마비)
- 모든 사용자를 포함하려는 "평균 사용자" 페르소나

### 검증 방법
- 팀 내 "이 사람을 아는가?" 테스트 — 실제 사용자와 대조
- 6개월마다 재검증 (시장/제품 변화 반영)
- 기능 기획 시 "이 페르소나가 사용할까?" 질문 필수화

## Connections

- [[planning.user-persona.role]] — CO_CREATES (weight: 0.6)
- [[planning.user-persona.empathy-map]] — CO_CREATES (weight: 0.6)
- [[planning.user-persona.verify]] — CO_CREATES (weight: 0.6)
