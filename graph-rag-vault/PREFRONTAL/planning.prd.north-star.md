---
id: "planning.prd.north-star"
domain: "planning"
type: "rule"
region: PREFRONTAL
token_estimate: 400
theory: "#178 North Star Metric (Sean Ellis, Amplitude)"
tags: [planning, north-star, metrics, product]
---

# planning.prd.north-star

> **Region**: 🧠 [[PREFRONTAL]]  
> **Domain**: `planning`  
> **Type**: `rule`  
> **Theory**: #178 North Star Metric (Sean Ellis, Amplitude)  
> **Tokens**: 400

## Content

North Star Metric (제품의 핵심 가치를 하나의 지표로 정렬한다):

### 정의
제품이 고객에게 전달하는 핵심 가치를 가장 잘 반영하는 단일 지표.
모든 팀이 이 지표를 향해 정렬된다.

### 좋은 North Star 기준
- 고객 가치를 반영 (매출 X, 사용 행동 O)
- 선행 지표 (매출보다 앞서 움직임)
- 팀 전체가 기여 가능
- 측정 가능 + 주기적 추적 가능

### 제품 유형별 예시
| 제품 유형 | North Star | 이유 |
|----------|-----------|------|
| SaaS 협업 | 주간 활성 편집자 수 | 협업 가치 반영 |
| 이커머스 | 주간 거래 완료 수 | 구매 가치 반영 |
| 콘텐츠 플랫폼 | 일간 콘텐츠 소비 시간 | 참여 가치 반영 |
| 마켓플레이스 | 주간 성사 매칭 수 | 양면 가치 반영 |
| 핀테크 | 월간 활성 거래 금액 | 금융 가치 반영 |

### Input Metrics (하위 지표)
North Star를 움직이는 레버:
```
North Star: 주간 활성 편집자 수
  ├─ 신규 가입자 중 편집 시작률 (Activation)
  ├─ 기존 사용자 주간 복귀율 (Retention)
  └─ 편집자당 초대한 팀원 수 (Referral)
```

### 주의사항
- 매출은 North Star가 아님 (후행 지표)
- 분기마다 재검토 (제품 단계에 따라 변할 수 있음)
- Vanity metric 배제 (총 가입자 수 등)

## Connections

*Connections will be populated by Graph RAG ingest.*
