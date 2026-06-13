---
id: "dev.frontend.component.stack"
domain: "development.frontend"
type: "rule"
bloom_level: ""
tags: ["frontend", "component", "nextjs", "tailwind", "typescript", "stack"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.frontend.component.stack

기술 스택 규칙 (일관성을 유지하고 번들 크기를 최소화한다):

### 1. Next.js 14+ App Router
- `app/` 디렉토리만 사용한다 (`pages/` 금지).
- Server Component가 기본이다. `'use client'`는 인터랙션이 필요할 때만 추가한다.
- `'use client'`는 **가능한 한 하위 컴포넌트에** 적용한다 (트리의 말단으로).

DO:
```tsx
// ✅ Server Component (기본) — 데이터 페칭 가능
// app/users/page.tsx
export default async function UsersPage() {
  const users = await getUsers(); // 직접 async/await
  return <UserList users={users} />;
}

// ✅ Client Component는 인터랙션 부분만
// components/LikeButton.tsx
"use client";
export function LikeButton({ postId }: { postId: string }) {
  const [liked, setLiked] = useState(false);
  return <button onClick={() => setLiked(!liked)}>♥</button>;
}
```

DON'T:
```tsx
// ❌ 페이지 전체를 Client Component로 만들기
"use client";
export default function UsersPage() {
  const [users, setUsers] = useState([]);
  useEffect(() => { fetchUsers().then(setUsers); }, []);
  return <div>{users.map(u => <UserCard key={u.id} user={u} />)}</div>;
}
```

### 2. TypeScript Strict
- `tsconfig.json`에서 `strict: true` 필수.
- `any` 타입 금지. 타입 불확실 시 `unknown` + type guard 사용.
- 외부 API 응답은 반드시 zod로 runtime validation 수행.

DO:
```tsx
// ✅ unknown + type guard
function isUser(data: unknown): data is User {
  return typeof data === "object" && data !== null && "id" in data;
}

// ✅ zod로 API 응답 검증
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
});
type User = z.infer<typeof UserSchema>;
const user = UserSchema.parse(await res.json());
```

### 3. Tailwind CSS
- 유틸리티 클래스만 사용한다 (인라인 style 금지, CSS 모듈 금지).
- 조건부 클래스는 `cn()` 유틸리티 (clsx + tailwind-merge) 사용.
- 반응형은 `sm → md → lg → xl` 순서로 mobile-first 작성.

DO:
```tsx
// ✅ cn() 유틸리티로 조건부 클래스
import { cn } from "@/lib/utils";
<div className={cn(
  "rounded-lg border p-4",
  isActive && "border-primary bg-primary/10",
  className
)} />
```

DON'T:
```tsx
// ❌ 인라인 스타일 + CSS 모듈
<div style={{ padding: 16, borderRadius: 8 }} />
import styles from "./Card.module.css";
```

### 4. 이미지 처리
- `next/image`만 사용한다 (`<img>` 태그 금지).
- `width`, `height` 또는 `fill` 속성을 반드시 지정한다.
- 외부 이미지 도메인은 `next.config.js`의 `images.remotePatterns`에 등록한다.

### 5. 환경변수
- 클라이언트 노출: `NEXT_PUBLIC_` 접두사 필수.
- 서버 전용: 접두사 없이 사용 (API Route, Server Component에서만 접근).
- 하드코딩 금지. `.env.local` 파일로 관리하고 `.env.example` 유지.

## Connections

- [[dev.frontend.component.role]] — REQUIRES (weight: 0.9)
- [[dev.frontend.page.role]] — REQUIRES (weight: 0.9)
- [[dev.frontend.component.verify]] — FEEDS (weight: 0.8)
- [[dev.frontend.page.verify]] — FEEDS (weight: 0.8)
- [[dev.frontend.component.solid]] — FEEDS (weight: 0.7)
- [[dev.frontend.page.routing]] — FEEDS (weight: 0.7)
- [[dev.frontend.component.role]] — CO_CREATES (weight: 0.6)
- [[dev.frontend.page.data-fetching]] — CO_CREATES (weight: 0.6)
