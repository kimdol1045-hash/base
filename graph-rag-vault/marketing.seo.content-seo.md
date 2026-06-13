---
id: "marketing.seo.content-seo"
domain: "marketing"
type: "pattern"
bloom_level: "콘텐츠 SEO는 검색 엔진 최적화를 위한 콘텐츠 기획·작성·최적화 전략이다. 검색 의도(Search Intent) 매칭, 토픽 클러스터, E-E-A-T 신호가 Google 알고리즘의 핵심 랭킹 요소이다."
tags: ["content-seo", "search-intent", "topic-cluster"]
brain_region: "SENSORS"
token_estimate: 400
---

# marketing.seo.content-seo

> 콘텐츠 SEO는 검색 엔진 최적화를 위한 콘텐츠 기획·작성·최적화 전략이다. 검색 의도(Search Intent) 매칭, 토픽 클러스터, E-E-A-T 신호가 Google 알고리즘의 핵심 랭킹 요소이다.

# 콘텐츠 SEO 가이드

## 핵심 원칙
- 검색 의도(Intent)에 정확히 매칭하는 콘텐츠
- 토픽 클러스터로 주제 권위(Authority) 구축
- E-E-A-T: 경험, 전문성, 권위, 신뢰 신호 강화
- 기술적 SEO와 콘텐츠 SEO 동시 최적화

## 토픽 클러스터 전략
1. **필러 페이지**: 핵심 주제의 종합 가이드 (3000자+)
2. **클러스터 콘텐츠**: 하위 주제별 상세 글 (1500자+)
3. **내부 링크**: 필러 ↔ 클러스터 양방향 링크

## 검색 의도 매핑
| 의도 | 키워드 패턴 | 콘텐츠 유형 |
|------|-----------|-----------|
| 정보형 | "방법", "가이드", "뜻" | 블로그, 가이드 |
| 탐색형 | "비교", "추천", "리뷰" | 비교표, 리스트 |
| 거래형 | "가격", "구매", "할인" | 제품 페이지 |
| 브랜드 | 브랜드명 + 기능 | 기능 페이지 |

## 온페이지 최적화 체크리스트
- 타이틀 태그: 주요 키워드 앞쪽 배치 (60자)
- 메타 디스크립션: CTA 포함 (155자)
- H1: 페이지당 1개, 키워드 포함
- H2/H3: 롱테일 키워드 자연 배치
- 내부 링크: 3-5개 관련 페이지 연결

## DO
- 분기별 기존 콘텐츠 업데이트 (콘텐츠 프레시니스)
- 구조화된 데이터(Schema) 마크업 적용
- 핵심 웹 바이탈(CWV) 성능 유지

## DON'T
- 키워드 스터핑 (과도한 반복) 하지 않기
- 동일 키워드로 여러 페이지 타겟팅하지 않기 (카니발라이제이션)
- AI 생성 콘텐츠를 검수 없이 발행하지 않기

## Connections

- [[marketing.seo.role]] — REQUIRES (weight: 0.9)
- [[marketing.seo.verify]] — FEEDS (weight: 0.8)
- [[marketing.seo.technical-seo]] — FEEDS (weight: 0.7)
- [[marketing.seo.role]] — CO_CREATES (weight: 0.6)
- [[marketing.seo.technical-seo]] — CO_CREATES (weight: 0.6)
- [[marketing.seo.verify]] — CO_CREATES (weight: 0.6)
- [[marketing.copy.seo]] — FEEDS (weight: 0.5)
- [[dev.frontend.page.seo]] — FEEDS (weight: 0.5)
