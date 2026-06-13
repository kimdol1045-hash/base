---
id: "dev.backend.api.third-party"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#103 Hexagonal Architecture"
tags: [backend, api, third-party, adapter, circuit-breaker, hexagonal, resilience]
---

# dev.backend.api.third-party

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #103 Hexagonal Architecture  
> **Tokens**: 500

## Content

외부 API 연동 패턴 (비즈니스 로직이 외부 서비스에 직접 의존하면 안 된다 -- 어댑터로 격리하라):

### Adapter 패턴 (Port & Adapter)
```
Business Logic → Port (Interface) → Adapter (Implementation) → External API
```

DO:
```typescript
// 1. Port (인터페이스) 정의
interface EmailProvider {
  send(params: {
    to: string;
    subject: string;
    html: string;
  }): Promise<{ messageId: string }>;
}

interface StorageProvider {
  upload(key: string, data: Buffer, contentType: string): Promise<{ url: string }>;
  download(key: string): Promise<Buffer>;
  delete(key: string): Promise<void>;
}

interface PaymentProvider {
  createCharge(params: ChargeParams): Promise<ChargeResult>;
  refund(chargeId: string, amount?: number): Promise<RefundResult>;
}

// 2. Adapter 구현 (외부 SDK 캡슐화)
class ResendEmailAdapter implements EmailProvider {
  private client: Resend;

  constructor(apiKey: string) {
    this.client = new Resend(apiKey);
  }

  async send(params: { to: string; subject: string; html: string }) {
    try {
      const result = await this.client.emails.send({
        from: env.EMAIL_FROM,
        to: params.to,
        subject: params.subject,
        html: params.html,
      });
      return { messageId: result.id };
    } catch (err) {
      // 외부 에러를 도메인 에러로 변환
      throw new ExternalServiceError("email", "send", err);
    }
  }
}

// SendGrid로 교체 시 이 어댑터만 변경하면 됨
class SendGridEmailAdapter implements EmailProvider {
  async send(params: { to: string; subject: string; html: string }) {
    const result = await sgMail.send({
      to: params.to,
      from: env.EMAIL_FROM,
      subject: params.subject,
      html: params.html,
    });
    return { messageId: result[0].headers["x-message-id"] };
  }
}

// 3. 타임아웃 + 재시도 래퍼
function withResilience<T extends (...args: any[]) => Promise<any>>(
  fn: T,
  options: {
    timeout: number;    // ms
    retries: number;
    backoff: number;    // 기본 대기 ms
    retryOn?: (err: any) => boolean;
  },
): T {
  return (async (...args: any[]) => {
    let lastError: Error;
    for (let attempt = 0; attempt <= options.retries; attempt++) {
      try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), options.timeout);

        const result = await fn(...args, { signal: controller.signal });
        clearTimeout(timer);
        return result;
      } catch (err) {
        lastError = err as Error;

        // 재시도 가능한 에러인지 확인
        if (options.retryOn && !options.retryOn(err)) throw err;
        if (attempt < options.retries) {
          const delay = options.backoff * Math.pow(2, attempt) * (1 + Math.random() * 0.1);
          await sleep(delay);
        }
      }
    }
    throw lastError!;
  }) as T;
}

// 4. Circuit Breaker 통합
class CircuitBreaker {
  private failures = 0;
  private lastFailure = 0;
  private state: "closed" | "open" | "half-open" = "closed";

  constructor(
    private readonly threshold: number = 5,     // 연속 실패 5회 시 open
    private readonly resetTimeout: number = 30_000, // 30초 후 half-open
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === "open") {
      if (Date.now() - this.lastFailure > this.resetTimeout) {
        this.state = "half-open";
      } else {
        throw new CircuitBreakerOpenError("Circuit breaker is open");
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (err) {
      this.onFailure();
      throw err;
    }
  }

  private onSuccess() {
    this.failures = 0;
    this.state = "closed";
  }

  private onFailure() {
    this.failures++;
    this.lastFailure = Date.now();
    if (this.failures >= this.threshold) {
      this.state = "open";
      logger.warn(`Circuit breaker opened after ${this.failures} failures`);
    }
  }
}

// 5. DI 컨테이너에서 주입
const emailProvider: EmailProvider =
  env.NODE_ENV === "test"
    ? new MockEmailAdapter()
    : new ResendEmailAdapter(env.RESEND_API_KEY);

// 비즈니스 로직은 인터페이스에만 의존
class OrderService {
  constructor(
    private email: EmailProvider,
    private storage: StorageProvider,
  ) {}

  async completeOrder(order: Order) {
    const receipt = await generateReceipt(order);
    await this.storage.upload(`receipts/${order.id}.pdf`, receipt, "application/pdf");
    await this.email.send({
      to: order.userEmail,
      subject: "주문이 완료되었습니다",
      html: renderOrderEmail(order),
    });
  }
}
```

### 외부 API 설정 기준
| 설정 | 값 | 이유 |
|------|-----|------|
| 연결 타임아웃 | 5초 | 외부 서비스 응답 대기 한도 |
| 읽기 타임아웃 | 10초 | 응답 수신 최대 대기 |
| 최대 재시도 | 3회 | 일시 오류 복구 |
| Circuit Breaker 임계값 | 5회 연속 실패 | 장애 전파 차단 |
| Circuit Breaker 리셋 | 30초 | 복구 확인 간격 |
| 응답 캐시 TTL | 60~300초 | 외부 호출 횟수 절감 |

### 에러 매핑
```typescript
// 외부 에러를 도메인 에러로 변환
class ExternalServiceError extends Error {
  constructor(
    public service: string,
    public operation: string,
    public originalError: unknown,
  ) {
    super(`External service error: ${service}.${operation}`);
  }
}

// 에러 매핑 미들웨어
function mapExternalError(err: ExternalServiceError): AppError {
  if (err.originalError instanceof TimeoutError) {
    return Errors.serviceUnavailable(`${err.service} 서비스 응답 지연`);
  }
  if (isRateLimitError(err.originalError)) {
    return Errors.tooManyRequests("외부 서비스 호출 한도 초과");
  }
  return Errors.internalServer("외부 서비스 오류가 발생했습니다");
}
```

DON'T:
```typescript
// ❌ 비즈니스 로직에서 SDK 직접 호출 -- 교체/테스트 불가
class OrderService {
  async sendReceipt(order: Order) {
    const resend = new Resend(env.RESEND_API_KEY);  // 하드코딩 의존성
    await resend.emails.send({ /* ... */ });
  }
}

// ❌ 타임아웃 없이 외부 호출 -- 외부 장애 시 무한 대기
const response = await fetch("https://api.external.com/data");

// ❌ 외부 에러를 그대로 사용자에게 노출
try {
  await externalApi.call();
} catch (err) {
  return c.json({ error: err.message }, 500);  // 내부 구조 노출
}

// ❌ Circuit Breaker 없이 장애 전파 -- 외부 서비스 다운 시 우리 서비스도 다운
for (const user of users) {
  await externalApi.notify(user);  // 외부 장애 시 전체 루프 실패
}
```

### 흔한 실수
- Adapter 인터페이스 없이 SDK를 직접 사용 -> 외부 서비스 교체 시 비즈니스 로직 수정 필요
- 타임아웃 미설정으로 요청 스레드 점유 -> 연쇄 장애 발생
- 외부 API 에러 메시지를 그대로 클라이언트에 전달 -> 내부 구조 및 키 노출 위험
- 재시도 시 jitter 없이 동일 간격 -> 외부 서비스에 thundering herd 발생
- 테스트에서 실제 외부 API 호출 -> Mock Adapter로 격리 필수

## Connections

### CO_CREATES (2)

- → [[dev.backend.api.background-jobs]] `w=0.6`
- → [[dev.backend.patterns.circuit-breaker]] `w=0.6`
