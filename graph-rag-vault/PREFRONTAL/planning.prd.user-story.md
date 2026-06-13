---
id: "planning.prd.user-story"
domain: "planning"
type: "pattern"
region: PREFRONTAL
token_estimate: 500
theory: "#79 User Story Mapping (Patton, 2014)"
tags: [planning, prd, user-story, story-mapping, pattern]
---

# planning.prd.user-story

> **Region**: 🧠 [[PREFRONTAL]]  
> **Domain**: `planning`  
> **Type**: `pattern`  
> **Theory**: #79 User Story Mapping (Patton, 2014)  
> **Tokens**: 500

## Content

User Story Mapping (사용자의 여정을 스토리로 분해하고 MVP를 슬라이싱한다):

### 왜 User Story Mapping인가?
플랫 백로그(기능 목록)만으로는 사용자 경험의 전체 그림을 볼 수 없다.
스토리 맵은 사용자의 활동 흐름 위에 기능을 배치하여,
"무엇을 먼저 만들어야 하는가?"를 시각적으로 판단하게 해준다.

### 스토리 맵 구조 (3계층)
```
[활동(Activity)] ─────────────────────────────────
    │
    ├── [태스크(Task)] ── [태스크] ── [태스크]
    │       │                │           │
    │   [스토리]         [스토리]     [스토리]
    │   [스토리]         [스토리]
    │   [스토리]
```

**Level 1: 활동(Activity)** — 사용자가 달성하려는 큰 목표
- 예: "식단 계획 세우기", "장보기", "요리하기", "기록하기"
- 좌에서 우로 시간/프로세스 순서대로 배치

**Level 2: 태스크(Task)** — 활동을 달성하기 위한 단계
- 예: "레시피 검색" → "재료 확인" → "장바구니 추가"
- 각 활동 아래에 순서대로 나열

**Level 3: 유저 스토리(User Story)** — 태스크의 구체적 구현 방식
- 형식: "As a [페르소나], I want to [행동], so that [가치]"
- 위에서 아래로 우선순위 순서 (위=필수, 아래=선택)

### 스토리 맵 작성 프로세스

**Step 1: 백본(Backbone) 만들기**
- 사용자 여정의 핵심 활동을 좌→우로 나열
- 각 활동 아래에 필수 태스크를 배치
- 질문: "사용자가 목표를 달성하려면 어떤 단계를 거치는가?"

**Step 2: 스토리 채우기**
- 각 태스크 아래에 구현 가능한 스토리를 위→아래로 나열
- 위쪽 = 더 기본적이고 필수적인 기능
- 아래쪽 = 더 고급이고 선택적인 기능

**Step 3: 슬라이싱(Release 구분)**
- 수평선으로 릴리즈를 구분한다:
```
─── MVP (Release 1) ────────────────────
[스토리A] [스토리D] [스토리G]
─── Release 2 ──────────────────────────
[스토리B] [스토리E] [스토리H]
─── Release 3 ──────────────────────────
[스토리C] [스토리F] [스토리I]
```

### 슬라이싱 기법

**수평 슬라이싱 (Walking Skeleton)**
- 각 활동에서 가장 기본적인 스토리 1개씩 선택
- 전체 여정을 "얇게" 관통하는 최소 경험을 구성
- 핵심 원칙: "좁지만 완전한 경험"

DO: MVP 슬라이스 — "레시피 검색(텍스트) → 재료 목록 보기 → 장바구니 추가 → 주문"
DON'T: "레시피 검색(텍스트+사진+AI추천+필터)"만 MVP에 넣기
  → 한 기능만 깊게 파는 것은 스토리 맵의 목적이 아니다

**MVP 스코핑 질문**
- "이 슬라이스만으로 사용자가 핵심 Job을 해결할 수 있는가?"
- "이 슬라이스에서 하나라도 빠지면 여정이 끊기는가?"
- "각 활동마다 최소 1개의 스토리가 포함되어 있는가?"

### 유저 스토리 작성 규칙

좋은 스토리의 INVEST 기준:
- Independent: 다른 스토리와 독립적으로 개발 가능
- Negotiable: 구현 방식은 협의 가능
- Valuable: 사용자에게 가치를 제공
- Estimable: 추정 가능한 크기
- Small: 1 스프린트 내 완료 가능
- Testable: 완료 기준이 명확

### 스토리 템플릿
```
스토리: As a [페르소나], I want to [행동], so that [가치]
인수 기준(Acceptance Criteria):
- Given [전제 조건]
- When [행동]
- Then [기대 결과]
우선순위: Must / Should / Could / Won't (MoSCoW)
예상 크기: S / M / L
```

### 주의사항
- 스토리는 기술 태스크가 아닌 사용자 가치로 작성 ("API 연동"이 아니라 "소셜 로그인")
- 활동이 6개를 초과하면 범위가 너무 넓은 것 → 재정의 필요
- MVP 슬라이스에 모든 활동의 스토리가 최소 1개씩 있어야 한다

## Connections

### REQUIRES (1)

- ← [[planning.prd.role]] `w=0.9`

### FEEDS (3)

- ← [[planning.prd.mvp]] `w=0.7`
- → [[planning.prd.risk]] `w=0.7`
- → [[planning.prd.verify]] `w=0.8`

### CO_CREATES (1)

- → [[planning.prd.role]] `w=0.6`
