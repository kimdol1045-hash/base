---
id: "dev.backend.websocket.room"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["websocket", "room", "pubsub", "realtime"]
brain_region: "BRAINSTEM"
token_estimate: 400
---

# dev.backend.websocket.room

> #207 Pub/Sub Messaging Pattern (Enterprise Integration Patterns, Hohpe 2003)

# WebSocket 룸(채널) 관리 가이드

## 핵심 원칙
- 룸은 메시지 브로드캐스트의 논리적 단위이다
- 룸 참여/퇴장은 명시적 이벤트로 처리한다
- 룸 단위로 권한을 검사한다
- 메모리 누수 방지를 위해 빈 룸은 자동 정리한다

## DO
- 룸 ID를 리소스 기반으로 설계한다 (예: `project:123`, `chat:456`)
- 룸별 참여자 목록을 관리하고 presence 정보를 제공한다
- 메시지 전송 시 발신자를 제외하는 옵션을 제공한다
- 룸 크기 제한을 설정한다

## DON'T
- 모든 사용자를 하나의 글로벌 룸에 넣지 않는다
- 룸 참여 시 권한 검사를 생략하지 않는다
- 룸 상태를 서버 메모리에만 저장하지 않는다 (Redis 활용)
- 대용량 파일을 WebSocket 룸으로 전송하지 않는다

## 코드 예시
```typescript
class RoomManager {
  private rooms = new Map<string, Set<string>>();

  join(roomId: string, connId: string): void {
    if (!this.rooms.has(roomId)) {
      this.rooms.set(roomId, new Set());
    }
    this.rooms.get(roomId)!.add(connId);
    this.broadcast(roomId, {
      type: "user:joined",
      connId,
      memberCount: this.rooms.get(roomId)!.size,
    }, connId);
  }

  leave(roomId: string, connId: string): void {
    this.rooms.get(roomId)?.delete(connId);
    if (this.rooms.get(roomId)?.size === 0) {
      this.rooms.delete(roomId); // 빈 룸 정리
    }
  }

  broadcast(roomId: string, message: unknown, excludeId?: string): void {
    const members = this.rooms.get(roomId);
    if (!members) return;
    const data = JSON.stringify(message);
    for (const connId of members) {
      if (connId === excludeId) continue;
      getConnection(connId)?.send(data);
    }
  }
}
```
