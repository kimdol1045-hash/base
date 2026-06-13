---
id: "dev.frontend.hook.optimistic-update"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "hooks", "optimistic-update", "ux"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.hook.optimistic-update

> #238 Optimistic UI (CQRS UI Patterns, Facebook 2014)

# 낙관적 업데이트(Optimistic Update) 가이드

## 핵심 원칙
- 서버 응답을 기다리지 않고 UI를 즉시 업데이트하여 체감 속도를 높인다
- 서버 실패 시 이전 상태로 롤백한다
- 사용자에게 실패를 명확히 알린다
- 데이터 일관성이 중요한 경우(결제 등)에는 사용하지 않는다

## DO
- 좋아요, 즐겨찾기, 목록 순서 변경 등 빈번한 인터랙션에 적용한다
- 롤백 시 이전 데이터를 정확히 복원한다
- SWR의 `optimisticData` 옵션을 활용한다
- 에러 발생 시 토스트로 사용자에게 알린다

## DON'T
- 결제, 삭제 등 되돌리기 어려운 작업에 낙관적 업데이트를 적용하지 않는다
- 롤백 로직을 구현하지 않고 낙관적 업데이트만 적용하지 않는다
- 여러 단계의 연쇄 업데이트를 낙관적으로 처리하지 않는다
- 서버 응답과 클라이언트 상태가 불일치할 가능성을 무시하지 않는다

## 코드 예시
```tsx
import useSWRMutation from "swr/mutation";
import { toast } from "sonner";

function useLikePost(postId: string) {
  const { data: post, mutate } = usePost(postId);

  const toggleLike = useCallback(async () => {
    if (!post) return;
    const previousPost = post;
    const newLiked = !post.isLiked;

    // 1. 즉시 UI 업데이트 (낙관적)
    await mutate(
      { ...post, isLiked: newLiked, likeCount: post.likeCount + (newLiked ? 1 : -1) },
      { revalidate: false },
    );

    try {
      // 2. 서버 요청
      await fetch(`/api/v1/posts/${postId}/like`, {
        method: newLiked ? "POST" : "DELETE",
      });
      // 3. 서버 데이터로 갱신
      await mutate();
    } catch {
      // 4. 실패 시 롤백
      await mutate(previousPost, { revalidate: false });
      toast.error("요청에 실패했습니다. 다시 시도해주세요.");
    }
  }, [post, postId, mutate]);

  return { toggleLike, isLiked: post?.isLiked ?? false };
}

// 사용
function LikeButton({ postId }: { postId: string }) {
  const { toggleLike, isLiked } = useLikePost(postId);
  return (
    <button onClick={toggleLike}>
      {isLiked ? "❤️" : "🤍"}
    </button>
  );
}
```
