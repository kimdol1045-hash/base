---
id: "planning.business.flow"
domain: "planning"
type: "rule"
bloom_level: ""
tags: ["planning", "business", "flow", "ux", "engagement"]
brain_region: "PREFRONTAL"
token_estimate: 420
---

# planning.business.flow

> #B6 Flow (Csikszentmihalyi, 1990)

플로우 이론 (사용자가 몰입하는 제품을 설계한다):

### 플로우 조건
1. **도전 ≈ 능력**: 너무 쉬우면 지루, 너무 어려우면 불안
2. **명확한 목표**: 지금 무엇을 해야 하는지 알 수 있어야
3. **즉각적 피드백**: 행동의 결과가 바로 보여야

### UX 적용
도전-능력 균형:
- 온보딩: 쉬운 작업부터 점진적 난이도 증가
- 가이드 투어 → 자유 탐색 전환
- 난이도 자동 조절 (사용 패턴 기반)

명확한 목표:
- 프로그레스 바: "3/5 단계 완료"
- 다음 행동 명확히: "프로필을 완성하세요"
- 대시보드: 현재 상태 + 다음 할 일

즉각적 피드백:
- 저장 시 토스트 알림 (< 1초)
- 입력 시 실시간 유효성 검증
- 스켈레톤 UI → 콘텐츠 전환 (로딩 인지)
- 마이크로 애니메이션 (체크, 좋아요, 전환)

### 플로우 파괴 요소 (반드시 피하기)
- 불필요한 인터럽트 (팝업, 모달, 알림 과다)
- 긴 로딩 시간 (> 400ms, 도허티 임계값)
- 혼란스러운 네비게이션 (현재 위치 불분명)
- 강제 회원가입 (가치 경험 전 차단)

## Connections

- [[planning.business.innovation-diffusion]] — CO_CREATES (weight: 0.6)
- [[planning.business.sdt]] — CO_CREATES (weight: 0.6)
