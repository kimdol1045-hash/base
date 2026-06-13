---
id: "dev.frontend.component.virtual-list"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "virtual-list", "performance", "rendering"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.component.virtual-list

> #233 Virtual Scrolling (Windowing, react-window 2018)

# 가상 리스트(Virtual List) 가이드

## 핵심 원칙
- 화면에 보이는 항목만 렌더링하여 대량 데이터 목록의 성능을 확보한다
- DOM 노드 수를 최소화하여 메모리와 렌더링 비용을 절감한다
- 스크롤 위치에 따라 동적으로 항목을 마운트/언마운트한다
- 고정 높이와 가변 높이 항목 모두 지원한다

## DO
- 1000개 이상의 목록에는 가상화를 적용한다
- `@tanstack/react-virtual`을 기본 라이브러리로 사용한다
- 항목 높이가 고정이면 `estimateSize`를 정확히 설정한다
- 무한 스크롤과 조합하여 페이징을 구현한다
- 오버스캔(overscan)을 설정하여 빠른 스크롤 시 빈 화면을 방지한다

## DON'T
- 소규모 목록(50개 미만)에 가상화를 적용하지 않는다 (오버엔지니어링)
- 항목 내부에서 무거운 계산을 수행하지 않는다 (memo 활용)
- 스크롤 컨테이너의 높이를 미설정하지 않는다
- 키보드 네비게이션을 무시하지 않는다 (접근성)

## 코드 예시
```tsx
import { useVirtualizer } from "@tanstack/react-virtual";
import { useRef } from "react";

interface VirtualListProps<T> {
  items: T[];
  renderItem: (item: T, index: number) => React.ReactNode;
  estimateSize?: number;
}

export function VirtualList<T>({
  items,
  renderItem,
  estimateSize = 50,
}: VirtualListProps<T>) {
  const parentRef = useRef<HTMLDivElement>(null);

  const virtualizer = useVirtualizer({
    count: items.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => estimateSize,
    overscan: 5,
  });

  return (
    <div ref={parentRef} className="h-full overflow-auto">
      <div
        className="relative w-full"
        style={{ height: `${virtualizer.getTotalSize()}px` }}
      >
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            className="absolute left-0 top-0 w-full"
            style={{
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            {renderItem(items[virtualItem.index], virtualItem.index)}
          </div>
        ))}
      </div>
    </div>
  );
}

// 사용
<VirtualList
  items={users}
  estimateSize={64}
  renderItem={(user) => <UserCard user={user} />}
/>
```
