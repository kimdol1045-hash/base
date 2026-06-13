---
id: "dev.frontend.hook.intersection-observer"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "hooks", "intersection-observer", "lazy-loading"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.hook.intersection-observer

> #240 Intersection Observer API (W3C, 2016)

# Intersection Observer 훅 가이드

## 핵심 원칙
- 요소가 뷰포트에 진입/이탈할 때 콜백을 실행한다
- 무한 스크롤, 지연 로딩, 애니메이션 트리거에 활용한다
- scroll 이벤트 리스너보다 성능이 월등히 좋다 (비동기 동작)
- threshold로 가시 비율을 세밀하게 제어한다

## DO
- 이미지 지연 로딩에 활용한다 (뷰포트 근처에서 로드 시작)
- 무한 스크롤의 센티넬(sentinel) 요소에 적용한다
- rootMargin으로 미리 로딩을 시작한다 (예: 200px 전에 트리거)
- observer를 재사용하고, cleanup에서 해제한다

## DON'T
- scroll 이벤트 리스너로 가시성 감지를 구현하지 않는다
- 매 렌더링마다 새로운 observer를 생성하지 않는다
- SSR 환경에서 IntersectionObserver를 직접 호출하지 않는다
- threshold를 너무 세밀하게 설정하지 않는다 (성능 저하)

## 코드 예시
```tsx
import { useEffect, useRef, useState, useCallback } from "react";

interface UseInViewOptions {
  threshold?: number;
  rootMargin?: string;
  triggerOnce?: boolean;
}

function useInView(options: UseInViewOptions = {}) {
  const { threshold = 0, rootMargin = "0px", triggerOnce = false } = options;
  const ref = useRef<HTMLDivElement>(null);
  const [isInView, setIsInView] = useState(false);

  useEffect(() => {
    const element = ref.current;
    if (!element) return;

    const observer = new IntersectionObserver(
      ([entry]) => {
        const inView = entry.isIntersecting;
        setIsInView(inView);
        if (inView && triggerOnce) observer.unobserve(element);
      },
      { threshold, rootMargin },
    );

    observer.observe(element);
    return () => observer.disconnect();
  }, [threshold, rootMargin, triggerOnce]);

  return { ref, isInView };
}

// 무한 스크롤
function InfiniteList() {
  const { data, fetchNextPage, hasNextPage } = useInfiniteUsers();
  const { ref, isInView } = useInView({ rootMargin: "200px" });

  useEffect(() => {
    if (isInView && hasNextPage) fetchNextPage();
  }, [isInView, hasNextPage, fetchNextPage]);

  return (
    <div>
      {data.map(user => <UserCard key={user.id} user={user} />)}
      <div ref={ref} /> {/* 센티넬 요소 */}
    </div>
  );
}
```
