---
id: "qa.code-review.bug-analysis"
domain: "qa"
type: "pattern"
bloom_level: ""
tags: ["qa", "code-review", "bug-analysis", "root-cause", "postmortem", "5-whys"]
brain_region: "CEREBELLUM"
token_estimate: 500
---

# qa.code-review.bug-analysis

> #128 Error Management as Learning (Reason, 1990)

버그 분석 (근본 원인을 찾아 재발을 방지한다):

### 5 Whys 기법
표면적 증상이 아닌 **구조적 원인**에 도달할 때까지 "왜?"를 반복한다.

```
버그: 결제 완료 후 주문 상태가 '대기중'으로 남음

Why 1: 왜 주문 상태가 업데이트되지 않았는가?
→ 결제 완료 이벤트 핸들러가 실행되지 않았다

Why 2: 왜 이벤트 핸들러가 실행되지 않았는가?
→ 이벤트 큐에서 메시지 처리 실패(타임아웃)

Why 3: 왜 타임아웃이 발생했는가?
→ DB 쿼리가 5초 이상 소요 (타임아웃 3초)

Why 4: 왜 DB 쿼리가 느렸는가?
→ orders 테이블에 status 컬럼 인덱스가 없었다

Why 5: 왜 인덱스가 없었는가?
→ 마이그레이션 리뷰에 성능 체크리스트가 없었다

✅ 근본 원인: DB 마이그레이션 리뷰 프로세스에 성능 체크 누락
✅ 해결: 인덱스 추가 + 마이그레이션 PR 체크리스트에 인덱스 검토 항목 추가
```

### 버그 분류
| 분류 | 설명 | 예시 |
|------|------|------|
| Logic | 비즈니스 로직 오류 | 할인 계산 잘못 |
| Race Condition | 동시성/타이밍 문제 | 중복 결제, 재고 초과 |
| Edge Case | 경계값/예외 미처리 | null 입력, 빈 배열, 0원 |
| Integration | 외부 시스템 연동 오류 | API 스키마 불일치 |
| Configuration | 환경/설정 문제 | 잘못된 환경변수, 타임존 |

### Blameless Postmortem 템플릿
```markdown
## 사고 보고서 — [제목]
**날짜**: YYYY-MM-DD
**심각도**: P1/P2/P3/P4
**영향**: 사용자 N명, 기간 N분

### 타임라인
- HH:MM 최초 감지 (모니터링 알림 / 사용자 제보)
- HH:MM 원인 파악 시작
- HH:MM 임시 조치 적용
- HH:MM 완전 복구

### 근본 원인 (5 Whys)
(위 형식으로 기술)

### 재발 방지 조치
- [ ] 단기: 핫픽스 배포 (담당: OOO, 기한: D+1)
- [ ] 중기: 회귀 테스트 추가 (담당: OOO, 기한: D+7)
- [ ] 장기: 프로세스 개선 (담당: OOO, 기한: D+30)
```

### DO: 회귀 테스트 필수
```typescript
// 모든 버그 수정에는 해당 버그를 재현하는 테스트가 동반되어야 한다
describe('BUG-1234: 0원 상품 결제 시 에러', () => {
  it('0원 상품은 결제 없이 주문 완료', async () => {
    const order = await createOrder({
      items: [{ productId: 'free-sample', price: 0 }],
    });
    // 이전에는 여기서 ZeroDivisionError 발생
    expect(order.status).toBe('completed');
    expect(order.paymentRequired).toBe(false);
  });
});
```

### Fix 검증 체크리스트
- [ ] 원래 버그가 재현되는 테스트를 먼저 작성했는가?
- [ ] 수정 후 해당 테스트가 통과하는가?
- [ ] 관련 edge case도 추가로 커버했는가?
- [ ] 수정이 다른 기능에 영향을 주지 않는가? (기존 테스트 통과)

DON'T:
```typescript
// ❌ 증상만 치료 (근본 원인 미해결)
if (order.total === 0) return; // 0원이면 그냥 무시
// → 왜 0원 주문이 발생하는지 원인 분석 없이 회피

// ❌ 회귀 테스트 없이 수정만
// "급하니까 테스트 나중에 추가할게요" → 영원히 추가 안 됨

// ❌ 개인 비난
// "누가 이런 코드를 짰어?" → 시스템/프로세스 관점으로 전환
```

## Connections

- [[qa.code-review.role]] — REQUIRES (weight: 0.9)
- [[qa.code-review.verify]] — FEEDS (weight: 0.8)
- [[qa.code-review.security]] — FEEDS (weight: 0.7)
- [[qa.code-review.performance]] — FEEDS (weight: 0.7)
