---
id: "dev.backend.websocket.auth"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["websocket", "auth", "security", "jwt"]
brain_region: "BRAINSTEM"
token_estimate: 400
---

# dev.backend.websocket.auth

> #209 WebSocket Security (OWASP WebSocket Security Cheat Sheet, 2023)

# WebSocket 인증/인가 가이드

## 핵심 원칙
- WebSocket 연결 수립 시 반드시 인증을 수행한다
- 토큰 만료 시 연결을 종료하고 재인증을 요구한다
- 메시지 단위로 권한을 검사한다 (연결 인증만으로 불충분)
- Origin 헤더를 검증하여 CSWSH(Cross-Site WebSocket Hijacking)를 방지한다

## DO
- 핸드셰이크 단계에서 JWT를 검증한다 (쿼리 파라미터 또는 프로토콜 헤더)
- 토큰 갱신 메커니즘을 구현한다 (만료 전 refresh)
- 허용된 Origin만 연결을 수락한다
- Rate limiting을 메시지 단위로 적용한다

## DON'T
- URL 쿼리스트링에 토큰을 전달한 후 로그에 기록되도록 방치하지 않는다
- 한번 인증된 연결에 대해 이후 권한 검사를 생략하지 않는다
- 모든 Origin을 허용하지 않는다
- 평문(ws://)으로 프로덕션 WebSocket을 운영하지 않는다 (wss:// 필수)

## 코드 예시
```typescript
import { verify } from "jsonwebtoken";

function authenticateWebSocket(req: IncomingMessage): User {
  // 1. Origin 검증
  const origin = req.headers.origin;
  if (!ALLOWED_ORIGINS.includes(origin!)) {
    throw new Error("Origin not allowed");
  }

  // 2. 토큰 추출 (Sec-WebSocket-Protocol 헤더 활용)
  const protocols = req.headers["sec-websocket-protocol"]?.split(", ");
  const token = protocols?.find(p => p.startsWith("auth."))?.slice(5);
  if (!token) throw new Error("No auth token");

  // 3. 토큰 검증
  const payload = verify(token, JWT_SECRET) as JwtPayload;
  return { id: payload.sub, roles: payload.roles };
}

// 메시지 단위 권한 검사
function handleMessage(user: User, msg: WsMessage) {
  if (msg.type === "admin:action" && !user.roles.includes("admin")) {
    return { error: "FORBIDDEN", message: "관리자 권한이 필요합니다" };
  }
  // ... 메시지 처리
}
```
