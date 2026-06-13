---
id: "design.ui-component.color"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ui", "color", "accessibility"]
brain_region: "CORTEX"
token_estimate: 420
---

# design.ui-component.color

> #42 Color Harmony (Itten, 1961)

색상 설계 (색상은 감정과 행동을 유도한다):

### 60-30-10 규칙
- 60% 주색 (배경, 큰 영역): neutral/background
- 30% 보조색 (카드, 섹션): muted/card
- 10% 강조색 (CTA, 링크): primary/accent

### 시맨틱 컬러 시스템
```css
:root {
  --background: 0 0% 100%;       /* 흰색 배경 */
  --foreground: 222 84% 5%;      /* 거의 검정 텍스트 */
  --primary: 222 47% 11%;        /* 핵심 CTA */
  --secondary: 210 40% 96%;      /* 보조 요소 */
  --destructive: 0 84% 60%;      /* 삭제/에러 */
  --muted: 210 40% 96%;          /* 비활성 영역 */
  --accent: 210 40% 96%;         /* 호버/선택 */
}
.dark {
  --background: 222 84% 5%;
  --foreground: 210 40% 98%;
  /* 다크모드: 채도 낮추고 명도 반전 */
}
```

### 접근성 대비
- 일반 텍스트: 4.5:1 이상 (WCAG AA)
- 큰 텍스트(18px+): 3:1 이상
- UI 요소(아이콘, 보더): 3:1 이상
- 확인 도구: Chrome DevTools → Rendering → CSS contrast

### 색상 의미 (국제적 기준)
| 색상 | 의미 | 사용 |
|------|------|------|
| 파랑 | 신뢰, 전문성 | 링크, 정보 |
| 초록 | 성공, 안전 | 완료, 저장 |
| 빨강 | 위험, 긴급 | 에러, 삭제 |
| 노랑/주황 | 주의, 경고 | 경고 메시지 |
| 회색 | 중립, 비활성 | 비활성 요소 |

## Connections

- [[design.ui-component.accessibility]] — CO_CREATES (weight: 0.6)
- [[dev.frontend.component.accessibility-impl]] — FEEDS (weight: 0.5)
