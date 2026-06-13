---
id: "dev.infra.deploy.observability"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "observability", "opentelemetry", "monitoring"]
brain_region: "CEREBELLUM"
token_estimate: 460
---

# dev.infra.deploy.observability

> #165 Three Pillars of Observability + OpenTelemetry

관측성 (시스템 내부 상태를 외부에서 추론 가능하게 한다):

### 3 Pillars
| 필러 | 설명 | 도구 |
|------|------|------|
| Logs | 이벤트 기록 (구조화 JSON) | Loki, ELK, CloudWatch |
| Metrics | 수치 시계열 데이터 | Prometheus, Datadog, CloudWatch |
| Traces | 요청의 전체 경로 추적 | Jaeger, Zipkin, Tempo |

### 구조화 로깅 (필수)
```json
{
  "timestamp": "2024-03-15T10:30:00Z",
  "level": "error",
  "message": "Payment failed",
  "service": "payment-api",
  "traceId": "abc123",
  "userId": "user-456",
  "errorCode": "INSUFFICIENT_FUNDS",
  "amount": 50000
}
```
- 절대 금지: 비밀번호, 토큰, 카드번호 로깅
- 필수: traceId (분산 추적 연결), 구조화 JSON

### OpenTelemetry 계측
```typescript
import { trace } from '@opentelemetry/api';

const tracer = trace.getTracer('order-service');
const span = tracer.startSpan('createOrder');
span.setAttribute('order.amount', amount);
try {
  // 비즈니스 로직
} catch (error) {
  span.recordException(error);
  span.setStatus({ code: SpanStatusCode.ERROR });
} finally {
  span.end();
}
```

### Four Golden Signals (Google SRE)
| 신호 | 설명 | 알림 기준 |
|------|------|----------|
| Latency | 요청 응답시간 | P99 > 2초 |
| Traffic | 요청 수 | RPM 급증/급감 |
| Errors | 에러율 | > 1% |
| Saturation | 리소스 포화도 | CPU/Memory > 80% |

### 대시보드 설계
- L0: 전체 시스템 상태 (SLO 준수 여부)
- L1: 서비스별 상태 (각 서비스 Golden Signals)
- L2: 상세 디버깅 (로그, 트레이스)

## Connections

- [[dev.infra.deploy.monitoring]] — CO_CREATES (weight: 0.6)
