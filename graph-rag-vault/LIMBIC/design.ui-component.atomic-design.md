---
id: "design.ui-component.atomic-design"
domain: "design"
type: "pattern"
region: LIMBIC
token_estimate: 420
theory: "#170 Atomic Design (Brad Frost, 2016)"
tags: [design, atomic-design, component, design-system]
---

# design.ui-component.atomic-design

> **Region**: 💜 [[LIMBIC]]  
> **Domain**: `design`  
> **Type**: `pattern`  
> **Theory**: #170 Atomic Design (Brad Frost, 2016)  
> **Tokens**: 420

## Content

Atomic Design (UI를 5단계 계층으로 체계적으로 구성한다):

### 5단계 계층
```
Atoms → Molecules → Organisms → Templates → Pages
```

| 단계 | 설명 | 예시 |
|------|------|------|
| Atoms | 더 이상 분해 불가한 기본 요소 | Button, Input, Label, Icon |
| Molecules | Atom 조합의 단일 기능 | SearchBar (Input + Button), FormField (Label + Input) |
| Organisms | Molecule/Atom 조합의 섹션 | Header (Logo + Nav + SearchBar), ProductCard |
| Templates | 레이아웃 구조 (콘텐츠 없이) | DashboardTemplate, AuthTemplate |
| Pages | Template + 실제 콘텐츠 | HomePage, ProductDetailPage |

### 디렉토리 구조
```
components/
  atoms/
    Button/
      Button.tsx
      Button.styles.ts
      Button.test.tsx
      index.ts
  molecules/
    SearchBar/
  organisms/
    Header/
  templates/
    DashboardTemplate/
```

### 네이밍 규칙
- Atom: 역할 기반 (`PrimaryButton`, `TextInput`)
- Molecule: 기능 기반 (`SearchBar`, `UserAvatar`)
- Organism: 영역 기반 (`SiteHeader`, `ProductGrid`)
- Template: 레이아웃 기반 (`TwoColumnTemplate`)

### 주의사항
- 5단계를 엄격히 따를 필요 없음 — 팀에 맞게 조정
- Atom이 너무 세분화되면 조합 비용 증가
- 중요한 건 계층 사고방식 (상향식 구성)

## Connections

*Connections will be populated by Graph RAG ingest.*
