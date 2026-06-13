---
id: "dev.backend.api.verify"
domain: "development.backend"
type: "verify"
bloom_level: ""
tags: ["backend", "api", "verification", "checklist", "quality"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.api.verify

> #8 Flavell MGV (Metacognitive Verification)

API 코드 자기 검증 체크리스트 (코드 생성/수정 후 반드시 각 항목을 점검한다):

### A. 입력 검증 (Input Validation)
- [ ] 모든 request body가 Zod 스키마로 검증되는가?
  - PASS: `const body = Schema.parse(await c.req.json())` 형태 존재
  - FAIL: `req.body`를 직접 사용하거나 `as` 타입 캐스팅으로 대체
- [ ] query params가 `z.coerce`를 사용해 타입 변환하는가?
  - PASS: `z.coerce.number().int().min(1).max(100)`
  - FAIL: `Number(req.query.page)` 또는 `parseInt()` 직접 사용
- [ ] path params (id 등)의 형식을 검증하는가?
  - PASS: `z.string().uuid()` 또는 `z.string().min(1)`
  - FAIL: `req.params.id`를 검증 없이 DB 쿼리에 사용
- [ ] 배열 입력에 `.max()` 크기 제한이 있는가?
  - PASS: `.array().max(100)`
  - FAIL: `.array()` 크기 제한 없음 (DoS 가능)

### B. 인증/인가 (Auth)
- [ ] 비공개 엔드포인트에 인증 미들웨어가 적용되어 있는가?
  - PASS: `app.use("*", authMiddleware)` 또는 개별 라우트에 적용
  - FAIL: 핸들러 내에서 인증 체크 누락
- [ ] 리소스 소유권 검증이 있는가? (본인 리소스만 수정/삭제)
  - PASS: `if (resource.userId !== currentUserId) throw Errors.forbidden()`
  - FAIL: 인증만 하고 인가(소유권) 체크 없음
- [ ] 공개 엔드포인트가 의도적이며 명시적으로 분리되어 있는가?

### C. 에러 핸들링 (Error Handling)
- [ ] 글로벌 에러 핸들러가 있는가? (app.onError)
  - PASS: Zod, AppError, 예상치 못한 에러를 각각 처리
  - FAIL: 각 핸들러마다 try-catch 중복, 또는 에러 처리 없음
- [ ] 에러 응답 형식이 `{ error: { code, message, details? } }`로 통일되어 있는가?
  - FAIL: `{ msg: "..." }`, `{ error: "string" }` 등 비일관적
- [ ] 5xx 에러에서 스택 트레이스나 내부 정보가 노출되지 않는가?
  - PASS: 클라이언트에는 일반 메시지, 서버에는 상세 로깅
  - FAIL: `c.json({ error: err.message })` 또는 `err.stack` 반환
- [ ] 빈 catch 블록 `catch {}` 이 없는가?

### D. 보안 (Security)
- [ ] SQL 쿼리가 parameterized인가? (문자열 연결 없음)
- [ ] 환경변수가 하드코딩되지 않았는가?
  - PASS: `c.env.JWT_SECRET` 또는 `process.env.JWT_SECRET`
  - FAIL: `const secret = "abc123"` 하드코딩
- [ ] CORS origin이 명시적으로 나열되어 있는가? (와일드카드 * 금지)
- [ ] 민감 정보(비밀번호, 토큰, 카드번호)가 로그에 포함되지 않는가?
- [ ] Rate limiting이 인증 엔드포인트에 적용되어 있는가?

### E. REST 설계 (REST Design)
- [ ] HTTP 메서드가 의미에 맞게 사용되는가? (GET=조회, POST=생성, PATCH=수정, DELETE=삭제)
- [ ] 상태코드가 정확한가? (201=생성, 204=삭제, 422=검증실패)
- [ ] URL이 복수형 명사이며 동사가 포함되지 않는가?
- [ ] 응답에 적절한 메타정보(pagination 등)가 포함되는가?

### F. 코드 품질 (Code Quality)
- [ ] `any` 타입이 사용되지 않는가?
  - PASS: 모든 변수/파라미터에 명시적 타입 또는 Zod 추론 타입
  - FAIL: `as any`, `req.body as any`, 타입 없는 파라미터
- [ ] 매직 넘버/스트링이 상수로 추출되어 있는가?
  - PASS: `const MAX_PAGE_SIZE = 100`
  - FAIL: `if (page > 100)` 하드코딩된 숫자
- [ ] 함수가 단일 책임 원칙을 지키는가? (한 함수 50줄 이하)
- [ ] 비즈니스 로직이 프레임워크 코드와 분리되어 있는가?
  - PASS: service 레이어에 로직 분리
  - FAIL: 핸들러 안에 DB 쿼리 + 비즈니스 로직 + 응답 처리 혼재

## Connections

- [[dev.backend.api.role]] — REQUIRES (weight: 0.85)
- [[dev.backend.api.rest]] — FEEDS (weight: 0.8)
- [[dev.backend.api.validation]] — FEEDS (weight: 0.8)
- [[dev.backend.api.error]] — FEEDS (weight: 0.8)
- [[dev.backend.api.middleware]] — FEEDS (weight: 0.8)
- [[dev.backend.patterns.llm-integration]] — FEEDS (weight: 0.8)
- [[dev.backend.patterns.rag-pattern]] — FEEDS (weight: 0.8)
- [[dev.backend.api.rate-limiting]] — FEEDS (weight: 0.8)
- [[dev.backend.api.caching]] — FEEDS (weight: 0.8)
