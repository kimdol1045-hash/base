---
id: "dev.backend.websocket.scaling"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["websocket", "scaling", "redis", "horizontal-scaling"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.websocket.scaling

> #208 Horizontal Scaling Patterns (Kleppmann, Designing Data-Intensive Applications 2017)

# WebSocket 수평 확장 가이드

## 핵심 원칙
- WebSocket은 상태를 가지므로 수평 확장 시 특별한 고려가 필요하다
- Redis Pub/Sub 또는 메시지 브로커로 서버 간 메시지를 중계한다
- Sticky Session으로 동일 클라이언트가 같은 서버에 연결되도록 한다
- 연결 상태를 공유 저장소(Redis)에 관리한다

## DO
- Redis Pub/Sub를 통해 서버 인스턴스 간 메시지를 중계한다
- 로드밸런서에 Sticky Session(IP Hash 또는 Cookie 기반)을 설정한다
- 서버별 연결 수를 모니터링하고 불균형을 감지한다
- 연결 메타데이터를 Redis에 저장하여 어떤 서버에서도 조회 가능하게 한다

## DON'T
- 단일 서버의 인메모리 상태에만 의존하지 않는다
- Sticky Session 없이 라운드로빈 로드밸런싱을 사용하지 않는다
- 서버 간 직접 통신(P2P)으로 메시지를 전달하지 않는다
- 연결 수를 무한정 증가시키지 않는다 (서버당 최대 연결 수 설정)

## 코드 예시
```typescript
import Redis from "ioredis";

const pub = new Redis();
const sub = new Redis();
const SERVER_ID = process.env.SERVER_ID!;

// 메시지 수신: 다른 서버에서 발행한 메시지를 로컬 클라이언트에 전달
sub.subscribe("ws:broadcast");
sub.on("message", (_channel, raw) => {
  const { roomId, message, fromServer } = JSON.parse(raw);
  if (fromServer === SERVER_ID) return; // 자기 자신이 발행한 메시지 무시
  localRoomManager.broadcast(roomId, message);
});

// 메시지 발행: 로컬 전송 + 다른 서버에 중계
function publishToRoom(roomId: string, message: unknown) {
  localRoomManager.broadcast(roomId, message);
  pub.publish("ws:broadcast", JSON.stringify({
    roomId,
    message,
    fromServer: SERVER_ID,
  }));
}
```

```nginx
# Nginx Sticky Session 설정
upstream websocket_servers {
  ip_hash;  # 클라이언트 IP 기반 고정
  server ws1:8080;
  server ws2:8080;
  server ws3:8080;
}
```
