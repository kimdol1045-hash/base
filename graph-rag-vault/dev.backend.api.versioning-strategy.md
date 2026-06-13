---
id: "dev.backend.api.versioning-strategy"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["api", "versioning", "backward-compatibility", "backend"]
brain_region: "BRAINSTEM"
token_estimate: 400
---

# dev.backend.api.versioning-strategy

> #218 API Versioning (Fielding, REST Dissertation 2000; Sturgeon, API Design Patterns 2022)

# API 버전 관리 전략 가이드

## 핵심 원칙
- API의 하위 호환성(Backward Compatibility)을 최우선으로 유지한다
- 파괴적 변경(Breaking Change)은 새 버전으로 분리한다
- 구 버전의 폐기(Deprecation) 일정을 사전에 공지한다
- 버전 수를 최소화하고, 가능하면 하위 호환적으로 변경한다

## 버전 관리 방식
| 방식 | 예시 | 장점 | 단점 |
|------|------|------|------|
| URL Path | `/api/v2/users` | 명확, 캐싱 용이 | URL 변경 필요 |
| Header | `Accept: application/vnd.api.v2+json` | URL 깔끔 | 발견성 낮음 |
| Query Param | `/api/users?version=2` | 간편 | 캐싱 복잡 |

## DO
- URL Path 방식을 기본으로 사용한다 (`/api/v1/...`)
- 하위 호환적 변경 목록을 정의한다: 필드 추가, 선택적 파라미터 추가, 새 엔드포인트
- Deprecation 헤더(`Sunset`, `Deprecation`)를 응답에 포함한다
- 최소 6개월의 폐기 유예 기간을 제공한다

## DON'T
- 기존 필드의 타입이나 의미를 변경하면서 같은 버전을 유지하지 않는다
- 필수 파라미터를 추가하면서 같은 버전을 유지하지 않는다
- 3개 이상의 버전을 동시에 유지하지 않는다
- 버전별로 완전히 다른 코드베이스를 유지하지 않는다 (어댑터 패턴 활용)

## 코드 예시
```typescript
// 버전별 라우터 분리
import v1Router from "./routes/v1";
import v2Router from "./routes/v2";

app.use("/api/v1", v1Router);
app.use("/api/v2", v2Router);

// v1 Deprecation 미들웨어
v1Router.use((req, res, next) => {
  res.set("Deprecation", "true");
  res.set("Sunset", "Sat, 01 Mar 2025 00:00:00 GMT");
  res.set("Link", '</api/v2>; rel="successor-version"');
  next();
});

// 어댑터 패턴: v1 응답을 v2 서비스에서 변환
v1Router.get("/users/:id", async (req, res) => {
  const user = await userService.getById(req.params.id); // 공유 서비스
  res.json({ data: toV1UserResponse(user) }); // v1 형식으로 변환
});
```
