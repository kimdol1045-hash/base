---
id: "dev.infra.observability.logging"
domain: "development.infra"
type: "pattern"
bloom_level: ""
tags: ["infra", "observability", "logging", "structured-log"]
brain_region: "CEREBELLUM"
token_estimate: 420
---

# dev.infra.observability.logging

> #269 Structured Logging (12-Factor App, Factor XI: Logs)

# 구조화된 로깅 가이드

## 핵심 원칙
- 모든 로그를 JSON 형식의 구조화된 데이터로 출력한다
- 로그 레벨을 일관되게 사용한다 (ERROR, WARN, INFO, DEBUG)
- 요청 ID(Correlation ID)를 모든 로그에 포함한다
- 로그를 stdout으로 출력하고, 수집은 인프라 레벨에서 처리한다

## DO
- 구조화된 로그 라이브러리(pino, winston)를 사용한다
- 요청별 컨텍스트(userId, requestId, traceId)를 자동 주입한다
- 에러 로그에 스택 트레이스를 포함한다
- 민감 정보(비밀번호, 토큰)를 로그에서 마스킹한다

## DON'T
- `console.log`를 프로덕션에서 사용하지 않는다
- 로그에 개인정보(PII)를 평문으로 기록하지 않는다
- DEBUG 레벨 로그를 프로덕션에서 활성화하지 않는다
- 로그 파일을 애플리케이션에서 직접 관리하지 않는다 (stdout → 수집기)

## 코드 예시
```typescript
import pino from "pino";

const logger = pino({
  level: process.env.LOG_LEVEL ?? "info",
  formatters: {
    level: (label) => ({ level: label }),
  },
  redact: {
    paths: ["password", "token", "authorization", "cookie"],
    censor: "[REDACTED]",
  },
});

// 요청별 자식 로거
function requestLogger(req: Request) {
  return logger.child({
    requestId: req.headers.get("x-request-id") ?? generateId(),
    userId: req.user?.id,
    method: req.method,
    url: req.url,
  });
}

// 미들웨어
app.use(async (req, res, next) => {
  const log = requestLogger(req);
  req.log = log;
  const start = performance.now();

  res.on("finish", () => {
    const duration = performance.now() - start;
    log.info({ statusCode: res.statusCode, duration }, "요청 완료");
  });

  next();
});

// 사용
req.log.info({ orderId: order.id }, "주문 생성 완료");
req.log.error({ err, orderId }, "주문 처리 실패");

// 출력 예시
// {"level":"info","requestId":"abc-123","userId":"user-1","orderId":"ord-456","msg":"주문 생성 완료"}
```
