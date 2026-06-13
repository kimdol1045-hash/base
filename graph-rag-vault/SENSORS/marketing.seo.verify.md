---
id: "marketing.seo.verify"
domain: "marketing"
type: "verify"
region: SENSORS
token_estimate: 480
tags: [marketing, seo, verify, checklist, technical-seo, core-web-vitals]
---

# marketing.seo.verify

> **Region**: 📡 [[SENSORS]]  
> **Domain**: `marketing`  
> **Type**: `verify`  
> **Tokens**: 480

## Content

SEO 검증 체크리스트 — 페이지 또는 사이트 단위로 SEO 기본 요소를 점검:

### Technical SEO 체크리스트
- [ ] meta title이 30~60자 이내이고 키워드를 포함하는가?
- [ ] meta description이 80~160자 이내이고 CTA를 포함하는가?
- [ ] 각 페이지가 고유한 title과 description을 가지는가? (중복 금지)
- [ ] 페이지당 H1 태그가 정확히 1개만 존재하는가?
- [ ] H1 → H2 → H3 헤딩 계층이 논리적으로 구성되었는가?
- [ ] canonical URL이 모든 페이지에 올바르게 설정되었는가?
- [ ] sitemap.xml이 존재하고 모든 주요 페이지를 포함하는가?
- [ ] robots.txt가 적절히 설정되었는가? (중요 페이지 차단 없음)
- [ ] 구조화 데이터(JSON-LD)가 Google Rich Results Test를 통과하는가?
- [ ] Open Graph 태그가 설정되어 SNS 공유 시 적절히 표시되는가?

### Content SEO 체크리스트
- [ ] 타겟 키워드가 title, H1, 첫 100단어에 자연스럽게 포함되었는가?
- [ ] 키워드 밀도가 1~2% 범위이고 스터핑이 아닌가?
- [ ] 모든 이미지에 설명적 alt text가 있는가?
- [ ] 내부 링크가 설명적 앵커 텍스트로 연결되었는가? ("여기 클릭" 금지)
- [ ] 고아 페이지(내부 링크 없는 페이지)가 없는가?
- [ ] 주요 페이지가 홈에서 3클릭 이내 도달 가능한가?
- [ ] 콘텐츠 최종 업데이트가 6개월 이내인가?

### 성능 (Core Web Vitals) 체크리스트
- [ ] LCP (Largest Contentful Paint) < 2.5초인가?
- [ ] INP (Interaction to Next Paint) < 200ms인가?
- [ ] CLS (Cumulative Layout Shift) < 0.1인가?
- [ ] 이미지가 적절한 포맷(WebP/AVIF)과 크기로 최적화되었는가?
- [ ] 폰트가 font-display: swap으로 설정되었는가?

### 인덱싱 체크리스트
- [ ] Google Search Console에 사이트가 등록되었는가?
- [ ] 인덱싱 오류(404, 5xx, redirect loop)가 없는가?
- [ ] 모바일 친화성 테스트를 통과하는가?
- [ ] HTTPS가 강제되고 HTTP → HTTPS 리다이렉트가 작동하는가?
- [ ] URL 구조가 짧고 읽기 쉬운가? (한글 인코딩 대신 영문 slug)

### 검증 도구
| 도구 | 점검 항목 |
|------|----------|
| Google Search Console | 인덱싱, 검색 성과, Core Web Vitals |
| Google Rich Results Test | 구조화 데이터 유효성 |
| PageSpeed Insights | LCP, INP, CLS 측정 |
| Screaming Frog | 사이트 전체 크롤링, 누락 메타태그 |
| Ahrefs / SEMrush | 키워드 순위, 백링크, 경쟁 분석 |

## Connections

### FEEDS (2)

- → [[dev.frontend.page.seo]] `w=0.5`
- → [[marketing.copy.seo]] `w=0.5`

### CO_CREATES (3)

- ← [[marketing.seo.content-seo]] `w=0.6`
- ← [[marketing.seo.role]] `w=0.6`
- ← [[marketing.seo.technical-seo]] `w=0.6`
