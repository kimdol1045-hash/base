---
id: "dev.infra.observability.tracing"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "observability", "tracing", "opentelemetry"]
brain_region: "CEREBELLUM"
token_estimate: 420
---

# dev.infra.observability.tracing

> #270 Distributed Tracing (OpenTelemetry, CNCF 2019; Jaeger, Uber 2017)

# 분산 추적(Distributed Tracing) 가이드

## 핵심 원칙
- 요청이 여러 서비스를 거치는 전체 경로를 추적한다
- OpenTelemetry를 표준 계측 프레임워크로 사용한다
- 트레이스 ID로 관련된 모든 서비스의 로그와 메트릭을 연결한다
- 샘플링으로 비용을 관리하면서 중요한 요청은 반드시 추적한다

## DO
- OpenTelemetry SDK로 자동 계측(auto-instrumentation)을 적용한다
- 서비스 간 호출 시 트레이스 컨텍스트(W3C Trace Context)를 전파한다
- 에러가 발생한 트레이스는 항상 수집한다
- 커스텀 스팬에 비즈니스 관련 속성을 추가한다

## DON'T
- 모든 요청을 100% 추적하지 않는다 (비용 관리, 1-10% 샘플링)
- 스팬에 개인정보나 민감 데이터를 포함하지 않는다
- 트레이싱 장애가 애플리케이션에 영향을 미치도록 하지 않는다
- 자체 트레이싱 솔루션을 구축하지 않는다 (OpenTelemetry 사용)

## 코드 예시
```typescript
import { NodeSDK } from "@opentelemetry/sdk-node";
import { OTLPTraceExporter } from "@opentelemetry/exporter-trace-otlp-http";
import { getNodeAutoInstrumentations } from "@opentelemetry/auto-instrumentations-node";
import { trace, SpanStatusCode } from "@opentelemetry/api";

// SDK 초기화
const sdk = new NodeSDK({
  traceExporter: new OTLPTraceExporter({
    url: process.env.OTEL_EXPORTER_OTLP_ENDPOINT,
  }),
  instrumentations: [getNodeAutoInstrumentations()],
  serviceName: "order-service",
});
sdk.start();

// 커스텀 스팬 생성
const tracer = trace.getTracer("order-service");

async function processOrder(orderId: string) {
  return tracer.startActiveSpan("processOrder", async (span) => {
    try {
      span.setAttribute("order.id", orderId);

      const order = await tracer.startActiveSpan("fetchOrder", async (s) => {
        const result = await db.orders.findById(orderId);
        s.end();
        return result;
      });

      await tracer.startActiveSpan("processPayment", async (s) => {
        await paymentService.charge(order);
        s.setAttribute("payment.amount", order.totalAmount);
        s.end();
      });

      span.setStatus({ code: SpanStatusCode.OK });
    } catch (err) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: err.message });
      span.recordException(err);
      throw err;
    } finally {
      span.end();
    }
  });
}
```
