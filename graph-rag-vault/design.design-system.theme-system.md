---
id: "design.design-system.theme-system"
domain: "design"
type: "pattern"
bloom_level: "테마 시스템은 디자인 토큰(색상, 타이포, 간격 등)을 추상화하여 다크 모드, 브랜드 변형, 화이트 라벨링을 지원하는 구조이다. CSS Custom Properties 또는 ThemeProvider 패턴이 핵심 구현 방식이다."
tags: ["theme", "design-tokens", "dark-mode", "customization"]
brain_region: "CORTEX"
token_estimate: 400
---

# design.design-system.theme-system

> 테마 시스템은 디자인 토큰(색상, 타이포, 간격 등)을 추상화하여 다크 모드, 브랜드 변형, 화이트 라벨링을 지원하는 구조이다. CSS Custom Properties 또는 ThemeProvider 패턴이 핵심 구현 방식이다.

# 테마 시스템 가이드

## 핵심 원칙
- 시맨틱 토큰: 역할 기반 이름 (--color-primary, 아닌 --blue-500)
- 계층 구조: Global → Alias → Component 토큰
- 런타임 전환: 테마 변경 시 리렌더링 불필요
- 접근성: 모든 테마에서 WCAG AA 충족

## 토큰 계층
| 레벨 | 예시 | 설명 |
|------|------|------|
| Global | blue-500: #3B82F6 | 원시 색상값 |
| Alias | color-primary: blue-500 | 의미 부여 |
| Component | button-bg: color-primary | 컴포넌트 매핑 |

## 다크 모드 전략
1. 시맨틱 토큰만 재정의 (Global 토큰은 유지)
2. 밝은 테마의 색상을 그대로 반전하지 않기
3. 다크 모드 전용 elevation/shadow 조정
4. 이미지/일러스트도 다크 모드 대응

## 구현 패턴
```css
:root {
  --color-bg: #FFFFFF;
  --color-text: #1A1A1A;
}
[data-theme="dark"] {
  --color-bg: #1A1A1A;
  --color-text: #F5F5F5;
}
```

## DO
- 토큰을 JSON/YAML로 관리하고 코드 자동 생성
- 시스템 설정 감지 (prefers-color-scheme)
- 모든 테마에서 컴포넌트 시각적 회귀 테스트

## DON'T
- 하드코딩된 색상값을 컴포넌트에 사용하지 않기
- 다크 모드에서 순수 흰색(#FFF)이나 순수 검정(#000) 사용하지 않기
- 토큰 없이 직접 색상을 참조하지 않기
