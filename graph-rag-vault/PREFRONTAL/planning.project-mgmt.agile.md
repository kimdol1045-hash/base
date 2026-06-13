---
id: "planning.project-mgmt.agile"
domain: "planning"
type: "rule"
region: PREFRONTAL
token_estimate: 500
theory: "#143 애자일 선언문 (Beck et al., 2001) + #142 스크럼 (Schwaber & Sutherland, 1995)"
tags: [planning, project-management, agile, scrum, sprint, retrospective]
---

# planning.project-mgmt.agile

> **Region**: 🧠 [[PREFRONTAL]]  
> **Domain**: `planning`  
> **Type**: `rule`  
> **Theory**: #143 애자일 선언문 (Beck et al., 2001) + #142 스크럼 (Schwaber & Sutherland, 1995)  
> **Tokens**: 500

## Content

애자일 + 스크럼 (변화에 대응하는 반복적 개발 프레임워크):

### 애자일 선언문 4가지 핵심 가치
1. 프로세스와 도구보다 **개인과 상호작용**을 중시한다
2. 포괄적 문서보다 **작동하는 소프트웨어**를 중시한다
3. 계약 협상보다 **고객과의 협력**을 중시한다
4. 계획을 따르기보다 **변화에 대응**하는 것을 중시한다

### 12원칙 핵심 요약 (실무 적용 관점)
- **조기 + 지속적 전달**: 2주마다 동작하는 소프트웨어를 전달한다
- **변화 환영**: 후반부 요구사항 변경도 경쟁 우위를 위해 수용한다
- **자기 조직화 팀**: 최고의 설계와 아키텍처는 자기 조직화 팀에서 나온다
- **지속 가능한 속도**: 일정한 속도를 무한히 유지할 수 있어야 한다
- **정기적 회고**: 팀은 정기적으로 효율성을 개선할 방법을 숙고하고 조율한다

### 스크럼 프레임워크 (2주 스프린트 기준)
```
스프린트 구조:
Day 0 (월): 스프린트 플래닝 (2-4시간)
Day 1-8:    개발 + 데일리 스크럼 (매일 15분)
Day 9 (금): 스프린트 리뷰 (1시간) + 회고 (1시간)

역할:
- Product Owner: 백로그 우선순위 결정, 스토리 수락/거절
- Scrum Master: 장애물 제거, 프로세스 코칭
- Dev Team: 자기 조직화, 스프린트 목표 달성

산출물:
- Product Backlog: PO가 관리하는 전체 요구사항 목록
- Sprint Backlog: 이번 스프린트에서 수행할 항목
- Increment: 스프린트 종료 시 잠재적으로 출시 가능한 제품
```

### 백로그 그루밍 (Refinement)
스프린트 중간에 1-2시간 진행. 다음 스프린트 준비:
```
그루밍 체크리스트:
- [ ] 스토리가 INVEST 기준을 충족하는가?
      I: Independent (독립적)
      N: Negotiable (협상 가능)
      V: Valuable (가치 있음)
      E: Estimable (추정 가능)
      S: Small (작은 단위)
      T: Testable (테스트 가능)
- [ ] 수락 기준(Acceptance Criteria)이 명확한가?
- [ ] 기술적 의존성이 파악되었는가?
- [ ] Story Point 추정이 완료되었는가?
```

### 회고 (Retrospective) 형식
```
형식: Start / Stop / Continue

Start (새로 시작할 것):
- "PR 크기를 300줄 이하로 제한하자"

Stop (그만할 것):
- "금요일 오후에 새로운 기능 개발 시작하는 것"

Continue (계속할 것):
- "데일리 스크럼에서 블로커 먼저 공유하는 것"

액션 아이템 (최대 3개, 담당자 + 기한 명시):
- [ ] [담당] [기한]: [구체적 액션]
```

### DO / DON'T
DO: "이번 스프린트 velocity가 20SP였으므로, 다음 스프린트도
     20SP 이내로 계획한다. 버퍼 포함 시 16SP를 목표로 한다."
DON'T: "팀이 열심히 하면 30SP도 가능하다"
       → 지속 가능한 속도를 초과하는 계획은 번아웃과 품질 저하를 유발한다

## Connections

### REQUIRES (1)

- ← [[planning.project-mgmt.role]] `w=0.9`

### FEEDS (2)

- → [[planning.project-mgmt.kanban]] `w=0.7`
- → [[planning.project-mgmt.verify]] `w=0.8`

### CO_CREATES (2)

- ← [[planning.project-mgmt.sprint-decomposition]] `w=0.6`
- → [[planning.project-mgmt.toc]] `w=0.6`
