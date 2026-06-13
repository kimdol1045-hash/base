---
id: "dev.frontend.mobile.offline-first"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "mobile", "offline", "sync", "pwa"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.mobile.offline-first

> #250 Offline-First Architecture (Hoodie.js, 2013; Service Workers, W3C 2014)

# 오프라인 퍼스트(Offline-First) 가이드

## 핵심 원칙
- 네트워크가 없어도 앱의 핵심 기능이 동작하도록 설계한다
- 로컬 저장소를 진실의 원천(Source of Truth)으로 사용한다
- 온라인 복귀 시 서버와 자동 동기화한다
- 충돌(Conflict) 해결 전략을 미리 정의한다

## DO
- CRDT 또는 Last-Write-Wins로 충돌 해결 전략을 선택한다
- 오프라인 변경 사항을 큐에 저장하고 온라인 시 순서대로 동기화한다
- 동기화 상태(동기화됨, 동기화 중, 미동기화)를 사용자에게 표시한다
- 네트워크 상태 변화를 감지하여 자동 동기화를 트리거한다

## DON'T
- 오프라인 상태에서 앱 전체가 동작하지 않도록 하지 않는다
- 무한정 오프라인 데이터를 쌓지 않는다 (저장소 한도 관리)
- 충돌 해결 없이 덮어쓰기만 하지 않는다
- 동기화 실패를 사용자에게 알리지 않고 묵인하지 않는다

## 코드 예시
```typescript
// 오프라인 큐 기반 동기화
interface PendingOperation {
  id: string;
  type: "create" | "update" | "delete";
  entity: string;
  data: unknown;
  createdAt: number;
}

class OfflineSyncManager {
  private queue: PendingOperation[] = [];

  async performOperation(op: Omit<PendingOperation, "id" | "createdAt">) {
    // 1. 로컬 저장소에 즉시 반영
    await localDb.apply(op);

    // 2. 큐에 추가
    const pending = { ...op, id: generateId(), createdAt: Date.now() };
    this.queue.push(pending);
    await AsyncStorage.setItem("sync_queue", JSON.stringify(this.queue));

    // 3. 온라인이면 즉시 동기화 시도
    if (navigator.onLine) await this.sync();
  }

  async sync() {
    const queue = [...this.queue];
    for (const op of queue) {
      try {
        await api.sync(op);
        this.queue = this.queue.filter(q => q.id !== op.id);
      } catch (err) {
        if (isConflict(err)) {
          await this.resolveConflict(op, err.serverData);
        } else {
          break; // 네트워크 에러면 중단
        }
      }
    }
    await AsyncStorage.setItem("sync_queue", JSON.stringify(this.queue));
  }

  private async resolveConflict(local: PendingOperation, serverData: unknown) {
    // Last-Write-Wins: 타임스탬프 비교
    if (local.createdAt > (serverData as any).updatedAt) {
      await api.forceUpdate(local);
    }
    this.queue = this.queue.filter(q => q.id !== local.id);
  }
}

// 네트워크 상태 감지
window.addEventListener("online", () => syncManager.sync());
```
