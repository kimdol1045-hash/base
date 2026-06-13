---
id: "analytics.data-pipeline"
domain: "analytics"
type: "pattern"
region: HIPPOCAMPUS
token_estimate: 380
theory: "#181 Data Pipeline / ETL Best Practices"
tags: [analytics, data-pipeline, etl, event-tracking]
---

# analytics.data-pipeline

> **Region**: 🌿 [[HIPPOCAMPUS]]  
> **Domain**: `analytics`  
> **Type**: `pattern`  
> **Theory**: #181 Data Pipeline / ETL Best Practices  
> **Tokens**: 380

## Content

데이터 파이프라인 (원시 데이터를 분석 가능한 형태로 변환한다):

### ETL vs ELT
| 구분 | ETL | ELT |
|------|-----|-----|
| 순서 | Extract→Transform→Load | Extract→Load→Transform |
| 변환 위치 | 중간 서버 | 데이터 웨어하우스 내부 |
| 적합 | 정형 데이터, 소규모 | 빅데이터, 클라우드 DW |

### 파이프라인 설계 원칙
- 멱등성: 같은 데이터 재처리해도 결과 동일
- 재처리 가능: 실패 시 특정 시점부터 재실행
- 모니터링: 처리량, 지연시간, 에러율 추적
- 스키마 진화: 소스 스키마 변경에 graceful 대응

### 이벤트 트래킹 설계
```json
{
  "event": "button_clicked",
  "properties": {
    "button_name": "signup_cta",
    "page": "/landing",
    "variant": "A"
  },
  "user_id": "u-123",
  "timestamp": "2024-03-15T10:30:00Z",
  "session_id": "s-456"
}
```

### 이벤트 네이밍 컨벤션
- `object_action` 형식: `page_viewed`, `button_clicked`, `order_completed`
- 과거형 사용 (이벤트는 이미 발생한 것)
- 일관된 property 네이밍 (camelCase 또는 snake_case 통일)

## Connections

*Connections will be populated by Graph RAG ingest.*
