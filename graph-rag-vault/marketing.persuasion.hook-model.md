---
id: "marketing.persuasion.hook-model"
domain: "marketing"
type: "pattern"
bloom_level: ""
tags: ["marketing", "persuasion", "hook-model", "retention", "saas", "habit"]
brain_region: "SENSORS"
token_estimate: 500
---

# marketing.persuasion.hook-model

> #58 Hook Model (Eyal, 2014)

Hook Model — 습관 형성 4단계 (사용자가 의식하지 않아도 돌아오게 만드는 리텐션 루프):

### 1. Trigger (촉발) — 행동의 시작점
**외부 트리거**: 사용자에게 직접 도달하는 자극
- 푸시 알림: "김민수님, 어제 작성 중이던 리포트가 있어요"
- 이메일: "팀원 3명이 새 댓글을 남겼습니다"
- SMS: "장바구니에 담긴 상품이 곧 품절됩니다"

**내부 트리거**: 감정/상황이 자동으로 행동을 유발
- 지루함 → 인스타그램 열기
- 불안 → 이메일 확인
- 외로움 → 카카오톡 열기
- SaaS 설계 목표: 외부 → 내부 트리거로 전환 (3~4주 반복 사용 후)

### 2. Action (행동) — 최소 노력의 행동
포그 행동 모델 적용: 동기 충분 + 행동 쉬움 + 촉발 존재
- 스크롤 한 번으로 피드 확인
- 원클릭 좋아요/북마크
- 로그인 없이 미리보기
- **핵심**: 행동까지의 단계를 최소화 (클릭 수 3회 이내)

### 3. Variable Reward (가변 보상) — 예측 불가능한 보상
| 보상 유형 | 설명 | SaaS 예시 |
|----------|------|----------|
| 부족의 보상 | 사회적 인정/소속감 | 좋아요 수, 댓글, @멘션 알림 |
| 수렵의 보상 | 정보/자원 획득 | 새로운 인사이트, 맞춤 추천 |
| 자아의 보상 | 숙달/완성/성취감 | 진행률 바, 레벨업, 배지 |

**가변성이 핵심**: 매번 같은 보상 X → 예측 불가능한 보상 O
- 피드: 스크롤할 때마다 다른 콘텐츠
- 대시보드: 매일 다른 인사이트/수치
- 알림: "누가" "무엇을" 했는지 매번 다름

### 4. Investment (투자) — 다음 루프를 위한 씨앗
사용자가 시간/노력/데이터를 투입 → 이탈 비용 증가
- 데이터 입력: 프로필, 프로젝트 설정, 팀원 초대
- 콘텐츠 생성: 게시물, 문서, 대시보드 커스터마이징
- 사회적 자본: 팔로워, 협업 네트워크
- **핵심**: 투자가 다음 Trigger를 자동 생성 (팀원 초대 → 팀원 활동 알림 → 재방문)

### SaaS 온보딩 Hook 설계 예시
```
Trigger: 가입 완료 이메일 "첫 프로젝트를 만들어보세요" (외부)
Action: 템플릿 선택 → 원클릭 프로젝트 생성
Reward: "프로젝트가 준비되었습니다!" + 맞춤 인사이트 미리보기
Investment: 팀원 초대, 데이터 연동
→ 다음 Trigger: "팀원 박지영님이 댓글을 남겼습니다"
```

## Connections

- [[marketing.persuasion.role]] — REQUIRES (weight: 0.9)
- [[marketing.persuasion.verify]] — FEEDS (weight: 0.8)
- [[marketing.persuasion.social-proof]] — FEEDS (weight: 0.7)
- [[marketing.persuasion.role]] — CO_CREATES (weight: 0.6)
- [[marketing.persuasion.nudge]] — CO_CREATES (weight: 0.6)
- [[marketing.persuasion.social-proof]] — CO_CREATES (weight: 0.6)
- [[marketing.persuasion.reciprocity]] — CO_CREATES (weight: 0.6)
- [[marketing.persuasion.authority]] — CO_CREATES (weight: 0.6)
- [[marketing.persuasion.anchoring]] — CO_CREATES (weight: 0.6)
- [[design.ux-psychology.endowed-progress]] — FEEDS (weight: 0.5)
- [[design.ux-psychology.zeigarnik]] — FEEDS (weight: 0.5)
- [[marketing.persuasion.commitment]] — CO_CREATES (weight: 0.6)
- [[marketing.persuasion.mere-exposure]] — CO_CREATES (weight: 0.6)
