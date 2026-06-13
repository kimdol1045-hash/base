---
id: "planning.prd.story-mapping"
domain: "planning"
type: "pattern"
region: PREFRONTAL
token_estimate: 380
theory: "#177 User Story Mapping (Jeff Patton, 2014)"
tags: [planning, story-mapping, user-story, release]
---

# planning.prd.story-mapping

> **Region**: 🧠 [[PREFRONTAL]]  
> **Domain**: `planning`  
> **Type**: `pattern`  
> **Theory**: #177 User Story Mapping (Jeff Patton, 2014)  
> **Tokens**: 380

## Content

스토리 맵핑 (사용자 여정을 2차원으로 시각화하여 릴리즈를 계획한다):

### 구조
```
[사용자 활동]  가입하기    상품 탐색    결제하기    리뷰 작성
─────────────────────────────────────────────────────
[MVP]         이메일가입   카테고리목록  카드결제    별점평가
[v1.1]        소셜로그인   검색+필터    간편결제    텍스트리뷰
[v1.2]        프로필설정   추천시스템    정기결제    사진리뷰
```

### 작성 프로세스
1. **Backbone** (상단): 사용자 활동을 좌→우 시간 순서로 나열
2. **Body** (하단): 각 활동의 세부 스토리를 우선순위순으로 아래로 배치
3. **Slicing**: 수평선으로 릴리즈 범위를 구분

### Walking Skeleton
MVP 라인 = 최소 기능 조합으로 전체 여정을 관통하는 경로
- 각 활동에서 최소 1개 스토리가 포함되어야 함
- "얇지만 완전한" 제품

### 규칙
- 사용자 관점으로 작성 (기술 태스크 X)
- 좌→우: 시간 순서 (사용자 여정)
- 위→아래: 우선순위 (필수 → 있으면 좋은)
- 팀 전체가 함께 만들기 (개인 작성 금지)

## Connections

*Connections will be populated by Graph RAG ingest.*
