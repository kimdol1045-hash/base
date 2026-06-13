---
id: "dev.backend.api.websocket"
domain: "development.backend"
type: "pattern"
region: BRAINSTEM
token_estimate: 500
theory: "#109 Event-Driven Architecture"
tags: [backend, api, websocket, socket.io, realtime, event-driven]
---

# dev.backend.api.websocket

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `pattern`  
> **Theory**: #109 Event-Driven Architecture  
> **Tokens**: 500

## Content

WebSocket 패턴 (실시간 양방향 통신은 연결 생명주기를 반드시 관리해야 한다 -- 끊어진 연결은 유령이 된다):

### 연결 생명주기
`connect → authenticate → join rooms → exchange messages → heartbeat → disconnect`

DO:
```typescript
// Socket.io 서버 설정 (인증 + 룸 + 하트비트)
import { Server } from "socket.io";
import { verifyToken } from "./auth";

const io = new Server(httpServer, {
  cors: { origin: env.ALLOWED_ORIGINS, credentials: true },
  pingInterval: 25_000,   // 25초마다 ping
  pingTimeout: 10_000,    // 10초 내 pong 없으면 연결 끊기
  maxHttpBufferSize: 1e6, // 메시지 최대 1MB
});

// 1단계: 연결 시 인증 미들웨어
io.use(async (socket, next) => {
  const token = socket.handshake.auth?.token;
  if (!token) return next(new Error("인증 토큰이 필요합니다"));

  try {
    const payload = await verifyToken(token);
    socket.data.userId = payload.sub;
    socket.data.role = payload.role;
    next();
  } catch {
    next(new Error("유효하지 않은 토큰입니다"));
  }
});

// 2단계: 이벤트 핸들링
io.on("connection", (socket) => {
  const userId = socket.data.userId;

  // 개인 룸 자동 입장 (1:1 알림용)
  socket.join(`user:${userId}`);

  // 채팅방 입장
  socket.on("room:join", async (roomId: string) => {
    const hasAccess = await checkRoomAccess(userId, roomId);
    if (!hasAccess) {
      socket.emit("error", { code: "FORBIDDEN", message: "접근 권한이 없습니다" });
      return;
    }
    socket.join(`room:${roomId}`);
    socket.to(`room:${roomId}`).emit("room:user-joined", { userId, roomId });
  });

  // 메시지 전송 (룸 기반)
  socket.on("message:send", async (data: { roomId: string; content: string }) => {
    const validated = MessageSchema.safeParse(data);
    if (!validated.success) {
      socket.emit("error", { code: "VALIDATION_ERROR", message: "잘못된 메시지 형식" });
      return;
    }

    const message = await saveMessage({ ...validated.data, senderId: userId });
    io.to(`room:${data.roomId}`).emit("message:new", message);
  });

  // 타이핑 인디케이터
  socket.on("typing:start", (roomId: string) => {
    socket.to(`room:${roomId}`).emit("typing:update", { userId, isTyping: true });
  });

  // 연결 해제
  socket.on("disconnect", (reason) => {
    console.log(`User ${userId} disconnected: ${reason}`);
    // 온라인 상태 업데이트
    updateUserPresence(userId, "offline");
  });
});
```

### 클라이언트 재연결 (Exponential Backoff)
```typescript
// 클라이언트 측 재연결 전략
import { io, Socket } from "socket.io-client";

function createSocket(token: string): Socket {
  const socket = io(env.WS_URL, {
    auth: { token },
    reconnection: true,
    reconnectionAttempts: 10,
    reconnectionDelay: 1_000,     // 최초 1초
    reconnectionDelayMax: 30_000, // 최대 30초
    randomizationFactor: 0.5,     // jitter 추가
    timeout: 10_000,              // 연결 타임아웃 10초
  });

  socket.on("connect", () => {
    console.log("Connected, re-joining rooms...");
    // 재연결 시 룸 재입장
    socket.emit("room:rejoin", { lastMessageId });
  });

  socket.on("connect_error", (err) => {
    if (err.message === "유효하지 않은 토큰입니다") {
      // 토큰 만료 시 갱신 후 재연결
      refreshToken().then((newToken) => {
        socket.auth = { token: newToken };
        socket.connect();
      });
    }
  });

  return socket;
}
```

### 스케일링 (Redis Adapter)
```typescript
// 다중 서버 환경에서 Socket.io Redis Adapter
import { createAdapter } from "@socket.io/redis-adapter";

const pubClient = new Redis(env.REDIS_URL);
const subClient = pubClient.duplicate();
io.adapter(createAdapter(pubClient, subClient));
// 이제 서버 A의 socket이 서버 B의 룸으로 메시지 전송 가능
```

DON'T:
```typescript
// ❌ 인증 없이 연결 허용 -- 누구나 메시지 수신 가능
io.on("connection", (socket) => {
  socket.on("message", (data) => { /* userId 없이 처리 */ });
});

// ❌ 하트비트 없이 연결 유지 -- 좀비 연결 누적
const io = new Server(httpServer, {
  pingInterval: 0,  // 하트비트 비활성화
});

// ❌ 전체 브로드캐스트 -- 모든 연결에 불필요한 메시지 전송
io.emit("message", data);  // 룸 구분 없이 전체 전송

// ❌ 메시지 크기 제한 없음 -- 대용량 메시지로 서버 과부하
const io = new Server(httpServer, { maxHttpBufferSize: Infinity });
```

### 연결 관리 기준
| 설정 | 값 | 이유 |
|------|-----|------|
| pingInterval | 25초 | 클라이언트 생존 확인 |
| pingTimeout | 10초 | 무응답 연결 정리 |
| maxHttpBufferSize | 1MB | 메모리 보호 |
| reconnectionAttempts | 10회 | 과도한 재시도 방지 |
| reconnectionDelayMax | 30초 | 서버 부하 분산 |

### 흔한 실수
- 재연결 시 이전 룸을 자동 복구하지 않음 -> 메시지 수신 누락
- 서버 스케일아웃 시 Redis Adapter 미적용 -> 다른 서버의 룸에 메시지 도달 불가
- 메시지 입력값 검증 누락 -> XSS 공격 벡터
- disconnect 이벤트에서 리소스 정리 누락 -> 메모리 누수
- 인증 토큰 만료 후에도 연결 유지 -> 주기적 토큰 재검증 필요 (1시간 간격)
