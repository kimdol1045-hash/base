---
id: "design.ui-component.dark-mode"
domain: "design"
type: "pattern"
bloom_level: ""
tags: ["design", "ui", "dark-mode", "theme"]
brain_region: "CORTEX"
token_estimate: 420
---

# design.ui-component.dark-mode

다크모드 설계 (시스템 설정 연동 + 수동 토글):

### CSS 변수 기반 테마
```css
:root {
  --background: 0 0% 100%;
  --foreground: 222 84% 5%;
  --card: 0 0% 100%;
  --border: 214 32% 91%;
}
.dark {
  --background: 222 84% 5%;
  --foreground: 210 40% 98%;
  --card: 222 84% 5%;
  --border: 217 33% 17%;
}
```

### Tailwind dark: 접두사
```tsx
<div className="bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-50">
  <p className="text-gray-600 dark:text-gray-400">보조 텍스트</p>
</div>
```

### 다크모드 색상 규칙
- 순수 검정(#000) 배경 금지 → gray-950 (#0a0a0a) 사용
- 순수 흰색(#fff) 텍스트 금지 → gray-50 (#fafafa) 사용
- 채도 10-20% 낮추기 (눈부심 방지)
- 그림자 대신 보더로 계층 구분 (dark에서 shadow 안 보임)
- 이미지: brightness(0.9) 적용 또는 다크용 에셋 준비

### 시스템 연동 + 수동 토글
```tsx
// next-themes 사용
import { ThemeProvider } from 'next-themes';
<ThemeProvider attribute="class" defaultTheme="system">
  {children}
</ThemeProvider>
```

### 흔한 실수
- 다크모드에서 테스트 안 함 (라이트만 보고 배포)
- 하드코딩된 색상 (bg-white 대신 bg-background 사용)
- 다크모드에서 텍스트 대비 부족
