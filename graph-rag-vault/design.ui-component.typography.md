---
id: "design.ui-component.typography"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ui", "typography", "font"]
brain_region: "CORTEX"
token_estimate: 400
---

# design.ui-component.typography

> #43 Typographic Scale (Bringhurst, 1992)

타이포그래피 (텍스트 위계로 정보 구조를 전달한다):

### Type Scale (1.25 비율 — Tailwind 기본)
| 레벨 | 크기 | Tailwind | 용도 |
|------|------|---------|------|
| Display | 36-48px | text-4xl/5xl | 히어로 헤드라인 |
| H1 | 30px | text-3xl | 페이지 제목 |
| H2 | 24px | text-2xl | 섹션 제목 |
| H3 | 20px | text-xl | 서브 섹션 |
| Body | 16px | text-base | 본문 |
| Small | 14px | text-sm | 보조 텍스트 |
| Caption | 12px | text-xs | 라벨, 타임스탬프 |

### Line Height 규칙
- 제목 (h1-h3): leading-tight (1.25)
- 본문: leading-relaxed (1.625) 또는 leading-normal (1.5)
- 긴 텍스트: leading-loose (2.0)

### 가독성 규칙
- 한 줄 최대 65-75자 (한국어 35-40자). Tailwind: max-w-prose
- 본문 font-weight: 400 (regular). 강조만 600 (semibold)
- 밑줄은 링크에만. 강조는 font-weight 또는 color로.

### 폰트 조합 (권장)
- 제목: Pretendard / Inter (산세리프, 깔끔)
- 코드: JetBrains Mono / Fira Code
- 최대 2개 폰트 (본문+코드 또는 제목+본문)

## Connections

- [[design.ui-component.role]] — REQUIRES (weight: 0.9)
- [[design.ui-component.verify]] — FEEDS (weight: 0.8)
- [[design.ui-component.gestalt]] — FEEDS (weight: 0.7)
- [[design.ui-component.spacing]] — FEEDS (weight: 0.7)
