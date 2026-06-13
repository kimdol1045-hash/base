---
id: "dev.frontend.component.styling"
domain: "development.frontend"
type: "rule"
region: CORTEX
token_estimate: 500
theory: "#101 DRY + Single Source of Truth (Hunt & Thomas, 1999)"
tags: [frontend, styling, tailwind, css-variables, cva, design-tokens, dark-mode, responsive]
---

# dev.frontend.component.styling

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.frontend`  
> **Type**: `rule`  
> **Theory**: #101 DRY + Single Source of Truth (Hunt & Thomas, 1999)  
> **Tokens**: 500

## Content

스타일 아키텍처 규칙 (일관된 디자인 시스템을 코드로 구현한다):

### 기술 스택 선택
- **Tailwind CSS**: 유틸리티-퍼스트, 빌드 타임 최적화, 디자인 토큰 내장
- **CSS Modules**: 스코프 격리가 필요한 복잡한 컴포넌트
- **CSS Variables**: 테마, 다크모드, 런타임 동적 값

### 1. cn() 유틸리티 — 조건부 클래스 병합

DO:
```typescript
// ✅ clsx + tailwind-merge = cn()
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// 사용: 충돌하는 클래스를 자동 병합
cn("px-4 py-2", "px-6")          // → "py-2 px-6" (px-4 제거)
cn("text-red-500", isActive && "text-blue-500") // 조건부
```

### 2. cva — 컴포넌트 Variant 시스템

DO:
```typescript
// ✅ class-variance-authority로 variant 관리
import { cva, type VariantProps } from "class-variance-authority";

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "bg-primary text-primary-foreground hover:bg-primary/90",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
      },
      size: {
        sm: "h-8 px-3 text-xs",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base",
      },
    },
    defaultVariants: { variant: "primary", size: "md" },
  }
);

interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

function Button({ variant, size, className, ...props }: ButtonProps) {
  return <button className={cn(buttonVariants({ variant, size }), className)} {...props} />;
}
```

### 3. 디자인 토큰 — CSS Variables

```typescript
// ✅ tailwind.config.ts — CSS Variable 기반 테마
// theme: {
//   extend: {
//     colors: {
//       primary: "hsl(var(--primary))",
//       "primary-foreground": "hsl(var(--primary-foreground))",
//       muted: "hsl(var(--muted))",
//       destructive: "hsl(var(--destructive))",
//     },
//     spacing: {
//       // 4px base system: 4, 8, 12, 16, 24, 32, 48, 64
//     },
//     borderRadius: {
//       lg: "var(--radius)",
//       md: "calc(var(--radius) - 2px)",
//       sm: "calc(var(--radius) - 4px)",
//     },
//   },
// }
```

### 4. 다크모드 — CSS Variable 전환

```css
/* ✅ globals.css — 라이트/다크 변수 정의 */
:root {
  --background: 0 0% 100%;
  --foreground: 240 10% 3.9%;
  --primary: 240 5.9% 10%;
  --muted: 240 4.8% 95.9%;
}
.dark {
  --background: 240 10% 3.9%;
  --foreground: 0 0% 98%;
  --primary: 0 0% 98%;
  --muted: 240 3.7% 15.9%;
}
```

### 5. 반응형 — Mobile-First

```tsx
// ✅ Tailwind 반응형 — 모바일 기본, 브레이크포인트로 확장
<div className="
  grid grid-cols-1 gap-4
  sm:grid-cols-2
  lg:grid-cols-3
  xl:grid-cols-4
">
```

DON'T:
```typescript
// ❌ 인라인 스타일 — 캐싱 불가, 미디어쿼리 불가
<div style={{ padding: "16px", color: "#333" }} />

// ❌ !important — 우선순위 전쟁 유발
<div className="!text-red-500" />

// ❌ 일관성 없는 간격값 — 13px, 17px, 22px 등 임의 값
<div className="p-[13px] mt-[17px]" />  // 디자인 토큰 사용할 것

// ❌ 깊은 CSS 중첩 — 3단계 이상 중첩은 특이도 문제
// .card .header .title .icon { ... } → 직접 클래스 적용
```
