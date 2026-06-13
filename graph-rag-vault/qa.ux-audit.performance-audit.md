---
id: "qa.ux-audit.performance-audit"
domain: "qa"
type: "pattern"
bloom_level: "성능 감사는 Core Web Vitals(LCP, FID, CLS)을 중심으로 웹 애플리케이션의 로딩 속도, 인터랙티브 반응성, 시각적 안정성을 평가하는 프로세스이다. Google의 검색 랭킹 요소이자 사용자 경험의 핵심이다."
tags: ["performance", "core-web-vitals", "lighthouse", "audit"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# qa.ux-audit.performance-audit

> 성능 감사는 Core Web Vitals(LCP, FID, CLS)을 중심으로 웹 애플리케이션의 로딩 속도, 인터랙티브 반응성, 시각적 안정성을 평가하는 프로세스이다. Google의 검색 랭킹 요소이자 사용자 경험의 핵심이다.

# 성능 감사 가이드

## 핵심 원칙
- Core Web Vitals 기준으로 측정
- 실험실 데이터(Lab)와 필드 데이터(RUM) 모두 분석
- 성능 예산(Performance Budget) 설정
- 가장 느린 사용자 기준 (p75 이상)

## Core Web Vitals
| 지표 | 의미 | 목표 |
|------|------|------|
| LCP | 최대 콘텐츠 렌더링 | 2.5초 이하 |
| FID/INP | 첫 입력 반응 시간 | 200ms 이하 |
| CLS | 레이아웃 이동 정도 | 0.1 이하 |

## 감사 체크리스트
### 로딩 성능
- [ ] 중요 리소스 프리로드(preload)
- [ ] 이미지 최적화 (WebP, lazy loading)
- [ ] 코드 스플리팅 적용
- [ ] 서드파티 스크립트 영향 분석

### 런타임 성능
- [ ] 불필요한 리렌더링 제거
- [ ] 메인 스레드 블로킹 작업 분리
- [ ] 메모리 누수 확인

### 네트워크 성능
- [ ] CDN 적용
- [ ] HTTP/2 또는 HTTP/3 사용
- [ ] gzip/brotli 압축 적용

## 도구
- Lighthouse, WebPageTest, Chrome DevTools
- RUM: web-vitals 라이브러리, Datadog RUM

## DO
- 성능 예산을 CI에서 자동 검증
- 실제 사용자 성능 데이터(RUM) 수집
- 주요 사용자 경로의 성능을 우선 최적화

## DON'T
- 개발자 머신 기준으로만 성능 판단하지 않기
- 전체 페이지를 한 번에 최적화하려 하지 않기
- 성능 개선 없이 번들 크기만 줄이지 않기
