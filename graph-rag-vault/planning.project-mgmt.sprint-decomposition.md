---
id: "planning.project-mgmt.sprint-decomposition"
domain: "planning"
type: "pattern"
bloom_level: ""
tags: ["planning", "sprint", "decomposition", "story-points", "estimation", "agile", "capacity", "spike", "dod"]
brain_region: "PREFRONTAL"
token_estimate: 500
---

# planning.project-mgmt.sprint-decomposition

> #87 Agile Manifesto (Beck et al., 2001) — 작동하는 소프트웨어를 자주 전달한다

스프린트 분해 패턴 (유저 스토리를 실행 가능한 태스크로 분해하고 추정한다):

### 분해 흐름
```
Epic (대규모 기능)
  → User Story (사용자 가치 단위)
    → Task (개발 작업 단위, 최대 1일)
      → Sub-task (필요 시)
```

### 1. User Story → Task 분해

DO:
```
User Story: "사용자로서 소셜 로그인을 통해 간편하게 가입할 수 있다"
Acceptance Criteria:
- Google OAuth 로그인 가능
- 신규 유저 자동 생성
- 기존 이메일과 자동 연결
- 프로필 이미지 동기화

Task 분해:
┌────┬──────────────────────────────┬────┬──────────┐
│ #  │ Task                          │ SP │ 담당     │
├────┼──────────────────────────────┼────┼──────────┤
│ 1  │ Google OAuth Provider 설정    │ 1  │ Backend  │
│ 2  │ OAuth 콜백 API 구현           │ 2  │ Backend  │
│ 3  │ 유저 생성/연결 로직           │ 3  │ Backend  │
│ 4  │ 프로필 이미지 동기화          │ 2  │ Backend  │
│ 5  │ 소셜 로그인 버튼 UI           │ 1  │ Frontend │
│ 6  │ 로그인 플로우 통합 테스트     │ 2  │ QA       │
└────┴──────────────────────────────┴────┴──────────┘
합계: 11 SP
```

### 2. Story Point 추정 기준 (Fibonacci)

| SP | 기준 | 예시 |
|----|------|------|
| 1 | 설정 변경, 환경변수 추가 | ENV 추가, 패키지 설치 |
| 2 | 단순 CRUD, UI 컴포넌트 | 목록 조회 API, 버튼 컴포넌트 |
| 3 | 표준 기능, 비즈니스 로직 포함 | 폼 유효성 + API 연동 |
| 5 | 복잡한 통합, 외부 API 연동 | OAuth, 결제 연동 |
| 8 | 불확실성 높음, Spike 필요 | 실시간 동기화, 복잡한 마이그레이션 |
| 13 | 스토리 분할 필요 (너무 큼) | 이 크기는 2-3개 스토리로 분리 |

**규칙: 8SP 이상이면 Spike 태스크를 먼저 배정하여 불확실성을 제거한다.**

### 3. Sprint Capacity Planning

```
팀 구성: 개발자 4명
스프린트: 2주 (10 영업일)
Focus Factor: 0.7 (미팅, 코드리뷰, 장애 대응 등 30% 차감)

가용 capacity = 4명 × 10일 × 0.7 = 28 person-days
Velocity (과거 3스프린트 평균): 24 SP

이번 스프린트 계획: 24 SP 이내
버퍼: 20% (약 5SP)를 기술 부채/버그 수정에 예약
실 투입: 19 SP의 새 기능
```

### 4. Spike 태스크 (탐색/학습)

```typescript
// ✅ Spike 정의 예시
// Title: [Spike] WebSocket 기반 실시간 알림 기술 검토
// Time-box: 2일 (최대)
// 목표: 기술 선택 + POC + 추정 가능한 수준의 이해
// 산출물:
//   - 기술 비교표 (Socket.io vs Pusher vs SSE)
//   - POC 코드 (연결/메시지 수신 확인)
//   - 구현 스토리 분해 + SP 추정

// Spike 완료 후 → 본 스토리의 SP 추정이 가능해진다
```

### 5. Definition of Done (완료 정의)

```
개별 Task 완료 기준:
- [ ] 코드 작성 완료 + 셀프 리뷰
- [ ] 유닛 테스트 작성 (커버리지 80%+)
- [ ] PR 생성 + 1명 이상 리뷰 승인
- [ ] CI 파이프라인 통과 (lint, test, build)
- [ ] 스테이징 환경 배포 확인

User Story 완료 기준:
- [ ] 모든 Task 완료
- [ ] Acceptance Criteria 전체 충족
- [ ] QA 테스트 통과
- [ ] PO 수락 (데모)
```

DON'T:
```
❌ 2일 이상 걸리는 태스크:
"OAuth 전체 구현" (5일) → 분할: Provider 설정(1일) + 콜백 API(1일) + ...
태스크가 2일을 초과하면 반드시 분할한다

❌ Acceptance Criteria 없는 스토리:
"로그인 기능 개선" → 무엇이 "개선"인지 정의 없음
→ "Google OAuth 추가, 기존 이메일과 자동 연결" 명시

❌ 추정 패딩:
"혹시 모르니까 5SP에 3SP 더 붙여서 8SP"
→ 불확실하면 Spike로 분리. 추정은 정직하게.

❌ Velocity 무시한 계획:
과거 평균 24SP인데 이번에 40SP 계획
→ 지속 가능한 속도 유지. velocity ±10% 범위 내 계획.
```

## Connections

- [[planning.project-mgmt.agile]] — CO_CREATES (weight: 0.6)
- [[planning.project-mgmt.toc]] — CO_CREATES (weight: 0.6)
