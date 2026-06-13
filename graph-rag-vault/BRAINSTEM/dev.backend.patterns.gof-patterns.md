---
id: "dev.backend.patterns.gof-patterns"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 430
theory: "#172 GoF Design Patterns (Gang of Four, 1994)"
tags: [backend, design-patterns, gof, strategy, observer]
---

# dev.backend.patterns.gof-patterns

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #172 GoF Design Patterns (Gang of Four, 1994)  
> **Tokens**: 430

## Content

GoF 디자인 패턴 (자주 발생하는 설계 문제의 검증된 해법):

### 가장 자주 쓰는 패턴 (TypeScript)

**Strategy** (행동을 런타임에 교체):
```typescript
interface PricingStrategy {
  calculate(amount: number): number;
}
class RegularPricing implements PricingStrategy {
  calculate(amount: number) { return amount; }
}
class VIPPricing implements PricingStrategy {
  calculate(amount: number) { return amount * 0.9; }
}
```

**Observer** (이벤트 기반 알림):
```typescript
class EventEmitter<T> {
  private listeners: ((data: T) => void)[] = [];
  on(listener: (data: T) => void) { this.listeners.push(listener); }
  emit(data: T) { this.listeners.forEach(l => l(data)); }
}
```

**Factory** (객체 생성 캡슐화):
```typescript
function createNotifier(type: 'email' | 'sms' | 'push'): Notifier {
  switch (type) {
    case 'email': return new EmailNotifier();
    case 'sms': return new SMSNotifier();
    case 'push': return new PushNotifier();
  }
}
```

### 패턴 선택 가이드
| 문제 | 패턴 |
|------|------|
| 알고리즘 교체 | Strategy |
| 객체 생성 분리 | Factory / Builder |
| 상태 변화 알림 | Observer |
| 인터페이스 변환 | Adapter |
| 복잡한 객체 트리 | Composite |
| 접근 제어/캐싱 | Proxy / Decorator |

### 안티패턴
- 패턴을 위한 패턴 (코드 2줄로 되는 걸 패턴으로 감싸지 말 것)
- 과도한 추상화 — YAGNI 원칙 우선

## Connections

*Connections will be populated by Graph RAG ingest.*
