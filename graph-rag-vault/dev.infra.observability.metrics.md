---
id: "dev.infra.observability.metrics"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "observability", "metrics", "prometheus"]
brain_region: "CEREBELLUM"
token_estimate: 420
---

# dev.infra.observability.metrics

> #271 Metrics Collection (Prometheus, CNCF 2012; RED/USE Method)

# 메트릭 수집 가이드

## 핵심 원칙
- RED(Rate, Errors, Duration) 메서드를 서비스 메트릭에 적용한다
- USE(Utilization, Saturation, Errors) 메서드를 리소스 메트릭에 적용한다
- Prometheus + Grafana를 메트릭 수집/시각화 표준으로 사용한다
- 비즈니스 메트릭과 기술 메트릭을 모두 수집한다

## DO
- 4가지 골든 시그널(지연시간, 트래픽, 에러, 포화도)을 수집한다
- 히스토그램을 사용하여 백분위수(p50, p95, p99)를 계산한다
- 메트릭 이름에 일관된 네이밍 규칙을 적용한다
- 레이블 카디널리티를 관리한다 (고유 값이 많은 레이블 주의)

## DON'T
- 사용자 ID 같은 높은 카디널리티 값을 레이블에 넣지 않는다
- 평균값에만 의존하지 않는다 (백분위수 확인)
- 메트릭 수집이 애플리케이션 성능에 영향을 미치도록 하지 않는다
- Counter와 Gauge를 혼동하지 않는다

## 코드 예시
```typescript
import { Registry, Histogram, Counter, Gauge } from "prom-client";

const register = new Registry();
register.setDefaultLabels({ service: "order-service" });

// RED 메트릭
const httpRequestDuration = new Histogram({
  name: "http_request_duration_seconds",
  help: "HTTP 요청 처리 시간",
  labelNames: ["method", "route", "status_code"],
  buckets: [0.01, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5],
  registers: [register],
});

const httpRequestTotal = new Counter({
  name: "http_requests_total",
  help: "총 HTTP 요청 수",
  labelNames: ["method", "route", "status_code"],
  registers: [register],
});

// 비즈니스 메트릭
const ordersCreated = new Counter({
  name: "orders_created_total",
  help: "생성된 주문 수",
  labelNames: ["payment_method"],
  registers: [register],
});

const activeConnections = new Gauge({
  name: "websocket_active_connections",
  help: "활성 WebSocket 연결 수",
  registers: [register],
});

// 미들웨어
app.use((req, res, next) => {
  const end = httpRequestDuration.startTimer();
  res.on("finish", () => {
    const labels = { method: req.method, route: req.route?.path ?? "unknown", status_code: res.statusCode };
    end(labels);
    httpRequestTotal.inc(labels);
  });
  next();
});

// /metrics 엔드포인트
app.get("/metrics", async (req, res) => {
  res.set("Content-Type", register.contentType);
  res.end(await register.metrics());
});
```
