---
id: "analytics.funnel-analysis"
domain: "analytics"
type: "pattern"
region: HIPPOCAMPUS
token_estimate: 400
theory: "#140 Funnel Analysis + AARRR (McClure, 2007)"
tags: [analytics, funnel, conversion, aarrr]
---

# analytics.funnel-analysis

> **Region**: 🌿 [[HIPPOCAMPUS]]  
> **Domain**: `analytics`  
> **Type**: `pattern`  
> **Theory**: #140 Funnel Analysis + AARRR (McClure, 2007)  
> **Tokens**: 400

## Content

퍼널 분석 (전환 과정의 병목을 찾아 개선한다):

### 퍼널 구성 원칙
- 단계 정의: 사용자 여정의 핵심 전환점만 포함 (5~8단계)
- 각 단계는 명확한 이벤트로 측정 가능해야 함
- 시간 윈도우 설정: "7일 내 전환"처럼 기간 제한

### 분석 프레임워크
| 단계 | 지표 | 이탈률 기준 |
|------|------|-----------|
| 랜딩 → 가입 | 가입 전환율 | > 70% 이탈 시 개선 |
| 가입 → 활성화 | 핵심 기능 도달률 | > 50% 이탈 시 개선 |
| 활성화 → 결제 | 결제 전환율 | > 90% 이탈 시 개선 |
| 결제 → 재구매 | 재구매율 | > 80% 이탈 시 개선 |

### 세그먼트별 퍼널
전체 평균만 보면 심슨의 역설 위험:
- 유입 채널별 (광고 vs 자연 vs 추천)
- 디바이스별 (모바일 vs 데스크톱)
- 사용자 유형별 (신규 vs 복귀)

### 개선 우선순위
1. 이탈률이 가장 높은 단계부터
2. 트래픽이 가장 많은 단계 우선
3. 개선 난이도 낮은 것부터 (Quick Win)

### 흔한 실수
- 퍼널 단계가 너무 많아 분석 불가능
- 시간 윈도우 미설정 (무한 퍼널)
- 이탈 사유 분석 없이 수치만 보기

## Connections

*Connections will be populated by Graph RAG ingest.*
