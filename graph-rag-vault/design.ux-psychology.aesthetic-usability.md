---
id: "design.ux-psychology.aesthetic-usability"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ux", "aesthetics", "trust"]
brain_region: "CORTEX"
token_estimate: 380
---

# design.ux-psychology.aesthetic-usability

> #50 Aesthetic-Usability Effect (Tractinsky et al., 2000)

심미적 사용성 효과 (아름다운 디자인은 사용하기 쉽다고 느끼게 한다):

### 핵심 원리
- 시각적으로 매력적인 디자인 → 사용자가 사소한 문제를 더 관용적으로 대함
- 첫인상이 전체 사용 경험을 프레이밍
- 아름다운 디자인은 신뢰감 형성 (특히 이커머스, 금융)

### 최소 시각 품질 기준
1. **일관된 디자인 시스템**: shadcn/ui 같은 검증된 컴포넌트 라이브러리 사용
2. **타이포그래피**: 최대 2개 폰트, 명확한 위계 (h1 > h2 > body)
3. **색상**: 60-30-10 비율, 시맨틱 컬러 (success/error/warning)
4. **여백**: 충분한 화이트스페이스, 요소 간 일관된 간격 (8px 기반)
5. **마이크로 인터랙션**: 호버, 포커스, 전환 애니메이션

### Tailwind로 빠르게 달성
```tsx
// 최소한의 코드로 세련된 카드
<div className="rounded-xl border bg-card p-6 shadow-sm
  transition-shadow hover:shadow-md">
  <h3 className="text-lg font-semibold tracking-tight">제목</h3>
  <p className="mt-2 text-sm text-muted-foreground">설명 텍스트</p>
</div>
```

### 주의
- 심미성이 사용성을 대체하지는 않음. 보조적 역할.
- 과도한 애니메이션은 오히려 방해

## Connections

- [[design.ux-psychology.role]] — REQUIRES (weight: 0.9)
- [[design.ux-psychology.verify]] — FEEDS (weight: 0.8)
- [[design.ux-psychology.serial-position]] — FEEDS (weight: 0.7)
- [[design.ux-psychology.doherty-threshold]] — FEEDS (weight: 0.7)
