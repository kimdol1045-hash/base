---
id: "analytics.event-tracking"
domain: "analytics"
type: "pattern"
bloom_level: ""
tags: ["analytics", "event-tracking", "segment", "amplitude"]
brain_region: "THALAMUS"
token_estimate: 400
---

# analytics.event-tracking

> #183 Event Tracking Design (Segment, Amplitude)

이벤트 트래킹 설계 (무엇을 측정할지 체계적으로 정의한다):

### 트래킹 플랜 템플릿
| 이벤트 | 트리거 | 속성 | 우선순위 |
|--------|--------|------|---------|
| page_viewed | 페이지 로드 | page, referrer | P0 |
| signup_completed | 가입 완료 | method, source | P0 |
| feature_used | 핵심 기능 사용 | feature_name | P0 |
| purchase_completed | 결제 완료 | amount, plan | P0 |
| button_clicked | CTA 클릭 | button_id, page | P1 |

### 이벤트 분류
- **P0 (필수)**: 퍼널 전환, 핵심 지표 계산에 필요
- **P1 (중요)**: 사용자 행동 분석, A/B 테스트
- **P2 (선택)**: 세부 인터랙션, 디버깅용

### 구현 패턴
```typescript
// 중앙 집중 트래킹 함수
function track(event: string, properties?: Record<string, unknown>) {
  const enriched = {
    ...properties,
    timestamp: new Date().toISOString(),
    sessionId: getSessionId(),
    userId: getUserId(),
    pageUrl: window.location.href,
  };
  analytics.track(event, enriched);
}
```

### 검증 체크리스트
- [ ] 모든 P0 이벤트가 구현되었는가?
- [ ] 이벤트 이름이 컨벤션을 따르는가?
- [ ] 필수 속성이 누락 없이 전송되는가?
- [ ] 개인정보(PII)가 이벤트에 포함되지 않았는가?
- [ ] 스테이징에서 이벤트 발화 검증했는가?

## Connections

- [[analytics.role]] — FEEDS (weight: 0.5)
