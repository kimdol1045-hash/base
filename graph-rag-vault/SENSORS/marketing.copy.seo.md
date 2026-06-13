---
id: "marketing.copy.seo"
domain: "marketing"
type: "rule"
region: SENSORS
token_estimate: 420
tags: [marketing, copy, seo, search]
---

# marketing.copy.seo

> **Region**: 📡 [[SENSORS]]  
> **Domain**: `marketing`  
> **Type**: `rule`  
> **Tokens**: 420

## Content

SEO 카피라이팅 (검색 엔진과 사람 모두를 위한 글쓰기):

### 키워드 배치
1. **제목 (H1)**: 핵심 키워드 포함, 60자 이내
2. **메타 디스크립션**: 핵심 키워드 + CTA, 155자 이내
3. **URL**: 짧고 키워드 포함 (/nextjs-deployment-guide)
4. **첫 100단어**: 핵심 키워드 자연스럽게 포함
5. **H2/H3**: 관련 키워드를 소제목에

### Next.js Metadata
```tsx
export const metadata: Metadata = {
  title: 'Next.js 배포 가이드 | 10분 만에 Vercel 배포',
  description: 'Next.js 프로젝트를 Vercel에 배포하는 단계별 가이드. 환경변수 설정부터 도메인 연결까지.',
  openGraph: {
    title: 'Next.js 배포 가이드',
    description: '10분 만에 프로덕션 배포하기',
    images: ['/og-image.png'],
  },
};
```

### 검색 의도 매칭
| 의도 | 키워드 패턴 | 콘텐츠 형식 |
|------|-----------|-----------|
| 정보형 | "~란", "~방법", "~차이" | 블로그, 가이드 |
| 비교형 | "~vs~", "~비교", "~추천" | 비교표, 리뷰 |
| 거래형 | "~가격", "~구매", "~시작" | 랜딩페이지, 가격표 |

### 규칙
- 키워드 밀도: 자연스럽게 (2-3% 이하). 키워드 스터핑 금지.
- 내부 링크: 관련 페이지 2-3개 자연스럽게 연결
- 이미지 alt 태그: 키워드 포함 설명

## Connections

### FEEDS (5)

- → [[dev.frontend.page.seo]] `w=0.5`
- ← [[marketing.seo.content-seo]] `w=0.5`
- ← [[marketing.seo.role]] `w=0.5`
- ← [[marketing.seo.technical-seo]] `w=0.5`
- ← [[marketing.seo.verify]] `w=0.5`
