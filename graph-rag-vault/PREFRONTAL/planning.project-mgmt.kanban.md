---
id: "planning.project-mgmt.kanban"
domain: "planning"
type: "pattern"
region: PREFRONTAL
token_estimate: 500
theory: "#141 칸반 (Ohno, 1988)"
tags: [planning, project-management, kanban, wip, flow]
---

# planning.project-mgmt.kanban

> **Region**: 🧠 [[PREFRONTAL]]  
> **Domain**: `planning`  
> **Type**: `pattern`  
> **Theory**: #141 칸반 (Ohno, 1988)  
> **Tokens**: 500

## Content

칸반 (WIP 제한을 통한 흐름 최적화):

### 왜 칸반인가?
작업을 시작하기는 쉽지만 완료하기는 어렵다. WIP(Work In Progress) 제한이
없으면 모든 사람이 여러 작업을 동시에 시작하고, 어떤 것도 완료하지 못하는
상태에 빠진다. 칸반은 "시작한 것을 먼저 끝내라"는 원칙을 시스템으로 강제한다.

### 칸반 보드 기본 구조
```
| Backlog | Todo | In Progress | Review | Done |
|         | (∞)  | (WIP: 3)    | (WIP: 2)| (∞) |
|---------|------|-------------|---------|------|
|         |      |             |         |      |
```

### WIP 제한 설정 기준
팀 규모와 역할에 따른 WIP 제한 가이드라인:
```
공식: WIP Limit = 팀원 수 × (1.0 ~ 1.5)

예시:
- 개발자 3명 → In Progress WIP: 3~4
- 리뷰어 2명 → Review WIP: 2~3
- 1인 프로젝트 → In Progress WIP: 2 (컨텍스트 스위칭 최소화)

WIP 초과 시 규칙:
1. 새 작업을 시작하지 않는다
2. 다른 사람의 진행 중인 작업을 돕는다 (특히 리뷰)
3. 블로커가 있는 작업을 해결한다
```

### 핵심 메트릭: 사이클 타임 (Cycle Time)
```
사이클 타임 = 작업 시작 시점 ~ 작업 완료 시점

측정 방법:
- 각 카드에 "시작일"과 "완료일" 기록
- 주 단위로 평균 사이클 타임 추적
- 사이클 타임 추이 차트로 개선 여부 확인

예시:
| 주차 | 완료 항목 | 평균 사이클 타임 | WIP 준수율 |
|------|-----------|------------------|------------|
| W1   | 5개       | 4.2일            | 80%        |
| W2   | 7개       | 3.1일            | 95%        |
| W3   | 8개       | 2.8일            | 100%       |
→ WIP 준수율이 올라갈수록 사이클 타임이 단축된다
```

### 칸반 컬럼별 규칙
- **Backlog**: 우선순위 정렬, 상위 10개만 유지 (나머지는 아이스박스)
- **Todo**: 다음으로 착수할 작업. 완료 정의(DoD)가 명확한 것만 진입
- **In Progress**: 활발히 작업 중. WIP 제한 엄격 적용
- **Review**: 코드 리뷰/QA 대기. 24시간 내 리뷰 완료 목표
- **Done**: 완료 정의를 모두 충족한 항목

### DO / DON'T
DO: "In Progress가 WIP 한도에 도달했으므로, 새 작업 대신
     Review 컬럼의 PR 리뷰를 먼저 진행한다"
DON'T: "급해서 WIP 제한을 일시적으로 해제한다"
       → 한 번 해제하면 규칙이 무너진다. 정말 필요하면 팀 합의 후 WIP 수를 조정

### 스크럼과의 차이점
| 항목 | 스크럼 | 칸반 |
|------|--------|------|
| 주기 | 고정 스프린트 (2주) | 연속 흐름 |
| 역할 | 스크럼 마스터, PO | 명시적 역할 없음 |
| 변경 | 스프린트 중 변경 불가 | 언제든 우선순위 변경 가능 |
| 핵심 제약 | 타임박스 | WIP 제한 |

## Connections

### REQUIRES (1)

- ← [[planning.project-mgmt.role]] `w=0.9`

### FEEDS (3)

- ← [[planning.project-mgmt.agile]] `w=0.7`
- → [[planning.project-mgmt.estimation]] `w=0.7`
- → [[planning.project-mgmt.verify]] `w=0.8`
