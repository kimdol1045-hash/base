---
id: "dev.frontend.page.verify"
domain: "development.frontend"
type: "verify"
bloom_level: ""
tags: ["frontend", "page", "verification", "checklist", "nextjs"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.frontend.page.verify

> #8 Flavell MGV

페이지 자기 검증 체크리스트 (출력 전 반드시 모든 항목을 점검한다):

### A. 파일 구조 완전성 (FAIL 시 수정 필수)
- [ ] `page.tsx`가 존재하는가?
- [ ] `loading.tsx`가 존재하고 Skeleton UI를 제공하는가?
- [ ] `error.tsx`가 존재하고 `'use client'` + `reset` 버튼이 있는가?
- [ ] 동적 라우트에서 `not-found.tsx` 또는 `notFound()` 호출이 있는가?

PASS: page.tsx + loading.tsx + error.tsx 모두 존재
FAIL: 하나라도 누락

### B. Server/Client 분리 (FAIL 시 수정 필수)
- [ ] `page.tsx`가 Server Component인가? (불필요한 `'use client'` 없음)
- [ ] `'use client'`가 트리의 말단(최하위 인터랙션 컴포넌트)에만 있는가?
- [ ] Server Component에서 `useState`, `useEffect`를 사용하지 않았는가?
- [ ] Client Component에서 `async/await`로 직접 데이터를 가져오지 않았는가?

DO:
```tsx
// ✅ 올바른 분리
// page.tsx (Server Component)
export default async function Page() {
  const data = await getData();
  return <InteractiveSection data={data} />;
}

// InteractiveSection.tsx (Client Component)
"use client";
export function InteractiveSection({ data }: { data: Data }) {
  const [filter, setFilter] = useState("");
  return <FilteredList data={data} filter={filter} onFilterChange={setFilter} />;
}
```

DON'T:
```tsx
// ❌ 페이지 전체를 Client Component로 만듦
"use client";
export default function Page() {
  const [data, setData] = useState(null);
  useEffect(() => { fetch("/api/data").then(r => r.json()).then(setData); }, []);
  return <div>{data?.title}</div>;
}
```

PASS: Server Component에서 데이터 페칭, Client는 인터랙션만
FAIL: 페이지 레벨에서 `'use client'` 사용 또는 `useEffect`로 데이터 페칭

### C. 메타데이터 & SEO (FAIL 시 수정 권장)
- [ ] `Metadata` 객체 또는 `generateMetadata` 함수가 설정되었는가?
- [ ] `title`과 `description`이 모두 있는가?
- [ ] 동적 페이지에서 `generateMetadata`로 동적 메타데이터를 생성하는가?
- [ ] Open Graph 이미지가 설정되었는가? (공유 가능 페이지)

PASS: title + description 최소 설정
FAIL: 메타데이터 완전 누락

### D. 성능 (FAIL 시 수정 권장)
- [ ] 정적 생성 가능한 페이지에 `generateStaticParams`를 사용하는가?
- [ ] 무거운 컴포넌트에 `dynamic import` (next/dynamic)를 사용하는가?
- [ ] 이미지에 `next/image`를 사용하는가?
- [ ] 페이지에 불필요한 JavaScript 번들이 포함되지 않았는가?

```tsx
// ✅ 무거운 컴포넌트 dynamic import
import dynamic from "next/dynamic";
const HeavyChart = dynamic(() => import("@/components/HeavyChart"), {
  loading: () => <ChartSkeleton />,
  ssr: false,
});
```

PASS: 최적화 패턴 적용
FAIL: 불필요한 클라이언트 번들 포함

### E. 네비게이션 & UX (FAIL 시 수정 권장)
- [ ] `Link` 컴포넌트를 사용하는가? (`<a>` 태그 직접 사용 금지)
- [ ] 뒤로 가기가 자연스럽게 동작하는가?
- [ ] 로딩 상태가 실제 레이아웃과 유사한 Skeleton인가? (스피너만 X)
- [ ] 에러 상태에서 복구 방법(다시 시도 버튼)을 제공하는가?

PASS: 모든 네비게이션이 Link + 자연스러운 UX
FAIL: `<a>` 태그 사용 또는 스피너만 제공

## Connections

- [[dev.frontend.component.role]] — REQUIRES (weight: 0.85)
- [[dev.frontend.page.role]] — REQUIRES (weight: 0.85)
- [[dev.frontend.component.solid]] — FEEDS (weight: 0.8)
- [[dev.frontend.component.stack]] — FEEDS (weight: 0.8)
- [[dev.frontend.page.routing]] — FEEDS (weight: 0.8)
