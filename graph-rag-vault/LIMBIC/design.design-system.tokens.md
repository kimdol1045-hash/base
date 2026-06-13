---
id: "design.design-system.tokens"
domain: "design"
type: "rule"
region: LIMBIC
token_estimate: 500
theory: "#29 게슈탈트 유사성 원리 (Wertheimer, 1923) — 일관된 시각 언어가 인지 부하를 줄인다"
tags: [design, design-tokens, css-variables, tailwind, spacing, typography, color-system, theming]
---

# design.design-system.tokens

> **Region**: 💜 [[LIMBIC]]  
> **Domain**: `design`  
> **Type**: `rule`  
> **Theory**: #29 게슈탈트 유사성 원리 (Wertheimer, 1923) — 일관된 시각 언어가 인지 부하를 줄인다  
> **Tokens**: 500

## Content

디자인 토큰 관리 규칙 (단일 소스에서 디자인 속성을 체계적으로 관리한다):

### 토큰 계층 구조
```
Global Token (원시값)
  → Semantic Token (의미 부여)
    → Component Token (컴포넌트별)

예시:
blue-600 (#2563EB)               ← Global: 원시 색상값
  → --color-primary (#2563EB)    ← Semantic: "주요 액션" 의미
    → --button-bg (#2563EB)      ← Component: 버튼 배경
```

절대 원칙: **컴포넌트 코드에서 Global Token을 직접 참조하지 않는다.**
항상 Semantic Token을 통해 접근한다.

### 1. 색상 토큰 — Semantic Naming

DO:
```typescript
// ✅ tailwind.config.ts — CSS Variable 기반 시맨틱 색상
const config = {
  theme: {
    extend: {
      colors: {
        // Semantic tokens — 의미 기반 이름
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        border: "hsl(var(--border))",
        ring: "hsl(var(--ring))",
      },
    },
  },
};
```

```css
/* ✅ globals.css — HSL 변수 (다크모드 전환 용이) */
:root {
  --background: 0 0% 100%;        /* white */
  --foreground: 240 10% 3.9%;     /* near-black */
  --primary: 240 5.9% 10%;        /* dark navy */
  --primary-foreground: 0 0% 98%; /* near-white */
  --muted: 240 4.8% 95.9%;        /* light gray */
  --muted-foreground: 240 3.8% 46.1%;
  --border: 240 5.9% 90%;
  --radius: 0.5rem;
}
.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  --primary: 0 0% 98%;
  --primary-foreground: 240 5.9% 10%;
  --muted: 240 3.7% 15.9%;
  --muted-foreground: 240 5% 64.9%;
  --border: 240 3.7% 15.9%;
}
```

### 2. 간격 토큰 — 4px 기반 스케일

| 토큰 | 값 | 용도 |
|------|------|------|
| spacing-1 | 4px | 아이콘-텍스트 간격 |
| spacing-2 | 8px | 같은 그룹 내 요소 간격 |
| spacing-3 | 12px | 폼 필드-라벨 간격 |
| spacing-4 | 16px | 카드 내부 패딩 |
| spacing-6 | 24px | 섹션 내부 패딩 |
| spacing-8 | 32px | 그룹 간 간격 |
| spacing-12 | 48px | 섹션 간 간격 |
| spacing-16 | 64px | 페이지 섹션 간격 |

규칙: Tailwind 기본 스케일(4px 단위)을 준수. **임의값([13px]) 사용 금지.**

### 3. 타이포그래피 토큰

```typescript
// ✅ 체계적인 타입 스케일 (1.25 비율)
// text-xs:   12px / 16px (캡션, 보조 텍스트)
// text-sm:   14px / 20px (본문 보조, 라벨)
// text-base: 16px / 24px (본문)
// text-lg:   18px / 28px (서브 헤딩)
// text-xl:   20px / 28px (카드 제목)
// text-2xl:  24px / 32px (섹션 제목)
// text-3xl:  30px / 36px (페이지 제목)
// text-4xl:  36px / 40px (히어로 헤딩)

// ✅ 폰트 패밀리 토큰
// fontFamily: {
//   sans: ["var(--font-pretendard)", "system-ui", "sans-serif"],
//   mono: ["var(--font-jetbrains-mono)", "monospace"],
// }
```

### 4. 라운딩 토큰

```typescript
// ✅ 일관된 border-radius
// borderRadius: {
//   sm: "calc(var(--radius) - 4px)",  // 4px — 작은 요소 (태그, 배지)
//   md: "calc(var(--radius) - 2px)",  // 6px — 입력 필드, 버튼
//   lg: "var(--radius)",              // 8px — 카드, 모달
//   xl: "calc(var(--radius) + 4px)",  // 12px — 대형 카드
//   full: "9999px",                   // 원형 (아바타, 토글)
// }
```

DON'T:
```typescript
// ❌ 매직 넘버 — 의미 불명, 일관성 없음
<div className="p-[13px] mt-[17px] text-[#3B82F6]" />
// → p-3 mt-4 text-primary 사용

// ❌ 컴포넌트에서 직접 색상값 사용
<div className="bg-blue-600 text-white" />
// → bg-primary text-primary-foreground 사용

// ❌ 일관성 없는 스케일 — 5px, 7px, 11px 등
// 4px 기반 스케일만 사용: 4, 8, 12, 16, 20, 24, 32, 48, 64
```
