---
id: "dev.frontend.mobile.responsive-patterns"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "mobile", "responsive", "tailwind"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.frontend.mobile.responsive-patterns

> #247 Responsive Design (Ethan Marcotte, A List Apart 2010)

# 반응형 디자인 패턴 가이드

## 핵심 원칙
- Mobile-First로 설계하고, 큰 화면으로 확장한다
- Tailwind CSS의 반응형 접두사(sm, md, lg, xl)를 활용한다
- 콘텐츠 기반 브레이크포인트를 우선 고려한다
- 유연한 레이아웃(flex, grid)으로 다양한 화면 크기에 대응한다

## DO
- Mobile-First로 기본 스타일을 작성하고 미디어 쿼리로 확장한다
- `clamp()` 함수로 유연한 타이포그래피를 구현한다
- 이미지에 `srcset`과 `sizes`를 활용한다
- 터치 대상 크기를 최소 44x44px로 유지한다

## DON'T
- 데스크탑 디자인을 축소하여 모바일에 적용하지 않는다
- 픽셀 단위로 고정 레이아웃을 만들지 않는다
- 모바일에서 호버(hover) 상태에만 의존하지 않는다
- `display: none`으로 모바일에서 콘텐츠를 숨기기만 하지 않는다

## 코드 예시
```tsx
// Tailwind CSS Mobile-First 반응형
export function ProductGrid({ products }: { products: Product[] }) {
  return (
    <div className="
      grid gap-4 p-4
      grid-cols-1        /* 모바일: 1열 */
      sm:grid-cols-2     /* 640px+: 2열 */
      md:grid-cols-3     /* 768px+: 3열 */
      lg:grid-cols-4     /* 1024px+: 4열 */
    ">
      {products.map(product => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}

// 반응형 네비게이션
export function Navigation() {
  return (
    <nav className="flex items-center justify-between p-4">
      <Logo />
      {/* 모바일: 햄버거 메뉴 */}
      <MobileMenu className="md:hidden" />
      {/* 데스크탑: 전체 메뉴 */}
      <DesktopMenu className="hidden md:flex gap-6" />
    </nav>
  );
}

// useMediaQuery 훅
function useMediaQuery(query: string): boolean {
  const [matches, setMatches] = useState(false);
  useEffect(() => {
    const media = window.matchMedia(query);
    setMatches(media.matches);
    const listener = (e: MediaQueryListEvent) => setMatches(e.matches);
    media.addEventListener("change", listener);
    return () => media.removeEventListener("change", listener);
  }, [query]);
  return matches;
}
```
