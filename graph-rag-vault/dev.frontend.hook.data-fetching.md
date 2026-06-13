---
id: "dev.frontend.hook.data-fetching"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "hooks", "data-fetching", "swr"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.hook.data-fetching

> #237 SWR Strategy (Vercel, stale-while-revalidate HTTP Cache 2019)

# 데이터 페칭 훅 가이드

## 핵심 원칙
- Server Components에서는 async/await로 직접 페칭한다
- Client Components에서는 SWR 또는 React Query를 사용한다
- 로딩, 에러, 데이터 상태를 일관되게 처리한다
- 캐싱과 재검증 전략을 명확히 설정한다

## DO
- SWR의 stale-while-revalidate 전략을 활용한다
- 에러 발생 시 재시도 횟수를 제한한다
- 뮤테이션 후 관련 캐시를 갱신(mutate)한다
- 요청 중복 제거(deduplication)를 활용한다

## DON'T
- useEffect + useState로 직접 데이터 페칭을 구현하지 않는다
- 전역 에러 처리를 설정하지 않고 각 컴포넌트에서 개별 처리하지 않는다
- 불필요한 폴링(revalidateOnInterval)을 설정하지 않는다
- 캐시 키를 일관되지 않게 사용하지 않는다

## 코드 예시
```tsx
import useSWR, { mutate } from "swr";

// 타입 안전한 fetcher
async function fetcher<T>(url: string): Promise<T> {
  const res = await fetch(url);
  if (!res.ok) {
    const error = await res.json();
    throw new ApiError(error.error.code, error.error.message);
  }
  return (await res.json()).data;
}

// 데이터 조회 훅
function useUser(id: string | undefined) {
  return useSWR<User>(
    id ? `/api/v1/users/${id}` : null,
    fetcher,
    {
      revalidateOnFocus: false,
      errorRetryCount: 3,
      dedupingInterval: 5000,
    },
  );
}

// 뮤테이션과 캐시 갱신
async function updateUserName(id: string, displayName: string) {
  await fetch(`/api/v1/users/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ displayName }),
  });
  // 캐시 갱신
  await mutate(`/api/v1/users/${id}`);
  await mutate("/api/v1/users"); // 목록도 갱신
}

// 컴포넌트에서 사용
function UserProfile({ userId }: { userId: string }) {
  const { data: user, error, isLoading } = useUser(userId);

  if (isLoading) return <ProfileSkeleton />;
  if (error) return <ErrorMessage error={error} />;
  if (!user) return null;

  return <ProfileCard user={user} />;
}
```
