---
id: "design.ui-component.interaction"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ui", "interaction", "feedback", "animation"]
brain_region: "CORTEX"
token_estimate: 420
---

# design.ui-component.interaction

> #48 Feedback Principle (Norman, 1988)

인터랙션 디자인 (모든 사용자 행동에 즉각적 피드백):

### 상태별 스타일 (모든 인터랙티브 요소)
```tsx
// 버튼 상태: default → hover → active → focus → disabled
<Button className="
  bg-primary text-primary-foreground
  hover:bg-primary/90           /* 호버: 약간 어둡게 */
  active:scale-[0.98]           /* 클릭: 미세 축소 */
  focus-visible:ring-2 ring-ring /* 포커스: 링 표시 */
  disabled:opacity-50 disabled:pointer-events-none
  transition-all duration-150   /* 부드러운 전환 */
">
  저장
</Button>
```

### 로딩 상태
```tsx
<Button disabled={isPending}>
  {isPending ? (
    <>
      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
      저장 중...
    </>
  ) : '저장'}
</Button>
```

### 피드백 유형별 사용
| 피드백 | 시간 | 사용 |
|--------|------|------|
| 인라인 (버튼 상태 변화) | 즉시 | 클릭, 호버, 입력 |
| 토스트 | 2-5초 | 성공/실패 알림 |
| 모달 다이얼로그 | 사용자 닫기 | 확인 필요한 행동 (삭제) |
| 스켈레톤 | 로딩 중 | 콘텐츠 로딩 |
| 프로그레스 바 | 긴 작업 | 파일 업로드, 처리 |

### 트랜지션 규칙
- 시간: 150ms (빠른 반응) ~ 300ms (화면 전환)
- 이징: ease-out (나타남), ease-in (사라짐)
- 동시다발 애니메이션 금지 (한 번에 하나씩)

## Connections

- [[design.ui-component.role]] — CO_CREATES (weight: 0.6)
