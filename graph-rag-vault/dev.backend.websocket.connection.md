---
id: "dev.backend.websocket.connection"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["websocket", "connection", "realtime", "backend"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.websocket.connection

> #206 WebSocket Protocol (RFC 6455, IETF 2011)

# WebSocket 연결 관리 가이드

## 핵심 원칙
- 연결 수명주기를 명확히 관리한다 (open → message → close)
- 재연결 로직은 클라이언트 측에 지수 백오프로 구현한다
- 서버 측에서 연결 상태를 추적하고 비정상 연결을 정리한다
- 프로토콜 레벨 핑/퐁으로 연결 상태를 확인한다

## DO
- 연결 시 핸드셰이크 단계에서 인증을 수행한다
- 연결 ID를 부여하여 개별 연결을 추적한다
- 연결 풀 크기에 제한을 설정한다
- 비정상 종료 시 리소스를 정리하는 cleanup 로직을 구현한다
- 메시지 형식을 JSON 스키마로 정의한다

## DON'T
- 인증 없이 WebSocket 연결을 허용하지 않는다
- 연결 수 제한 없이 무한정 연결을 수락하지 않는다
- 메시지 크기 제한을 설정하지 않고 방치하지 않는다
- HTTP 폴링으로 충분한 경우 WebSocket을 사용하지 않는다

## 코드 예시
```typescript
import { WebSocketServer } from "ws";

const wss = new WebSocketServer({ noServer: true });
const connections = new Map<string, WebSocket>();

server.on("upgrade", async (req, socket, head) => {
  try {
    const user = await authenticateFromHeaders(req.headers);
    wss.handleUpgrade(req, socket, head, (ws) => {
      const connId = generateId();
      connections.set(connId, ws);

      ws.on("message", (data) => handleMessage(connId, user, data));
      ws.on("close", () => {
        connections.delete(connId);
        cleanupResources(connId);
      });
      ws.on("pong", () => markAlive(connId));
    });
  } catch {
    socket.write("HTTP/1.1 401 Unauthorized\r\n\r\n");
    socket.destroy();
  }
});

// Heartbeat: 30초마다 ping 전송
setInterval(() => {
  for (const [id, ws] of connections) {
    if (!isAlive(id)) { ws.terminate(); return; }
    markDead(id);
    ws.ping();
  }
}, 30_000);
```
