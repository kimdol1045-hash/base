---
id: "design.ui-component.spacing"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ui", "spacing", "grid", "layout"]
brain_region: "CORTEX"
token_estimate: 380
---

# design.ui-component.spacing

> #45 8pt Grid (Google Material Design, 2014)

스페이싱 시스템 (일관된 간격으로 시각적 질서를 만든다):

### 8px 기반 스케일 (Tailwind)
| 값 | px | Tailwind | 용도 |
|----|-----|---------|------|
| 0.5 | 2px | gap-0.5 | 아이콘-텍스트 미세 간격 |
| 1 | 4px | gap-1 | 인라인 요소 간 |
| 1.5 | 6px | gap-1.5 | 라벨-입력 간격 |
| 2 | 8px | gap-2 | 같은 그룹 내 요소 |
| 4 | 16px | gap-4 | 관련 요소 그룹 간 |
| 6 | 24px | gap-6 | 카드 내 섹션 간 |
| 8 | 32px | gap-8 | 독립 섹션 간 |
| 12 | 48px | gap-12 | 페이지 섹션 간 |
| 16 | 64px | gap-16 | 주요 페이지 영역 간 |

### 패딩 규칙
- 카드: p-4 (모바일) / p-6 (데스크톱)
- 페이지: px-4 (모바일) / px-6 md:px-8 (태블릿+)
- 버튼: px-4 py-2 (기본) / px-3 py-1.5 (작은)
- 입력 필드: px-3 py-2

### 일관성 규칙
- 같은 레벨의 간격은 같은 값 사용 (혼용 금지)
- 간격을 줄이려면 한 단계씩 (gap-4 → gap-2, gap-4 → gap-1 ❌)
- 외부 여백 > 내부 여백 (카드 간격 > 카드 내 간격)

## Connections

- [[design.ui-component.role]] — REQUIRES (weight: 0.9)
- [[design.ui-component.verify]] — FEEDS (weight: 0.8)
- [[design.ui-component.typography]] — FEEDS (weight: 0.7)
- [[design.ui-component.responsive]] — FEEDS (weight: 0.7)
