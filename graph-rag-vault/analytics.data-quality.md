---
id: "analytics.data-quality"
domain: "analytics"
type: "rule"
bloom_level: ""
tags: ["analytics", "data-quality", "validation", "dama"]
brain_region: "THALAMUS"
token_estimate: 390
---

# analytics.data-quality

> #182 Data Quality Dimensions (DAMA International)

데이터 품질 (분석 결과의 신뢰성을 보장한다):

### 6가지 품질 차원
| 차원 | 설명 | 검증 방법 |
|------|------|----------|
| Completeness | 필수 필드가 채워져 있는가 | NULL 비율 체크 |
| Accuracy | 실제 값과 일치하는가 | 외부 소스와 교차 검증 |
| Consistency | 시스템 간 데이터가 일치하는가 | 소스 간 비교 쿼리 |
| Timeliness | 적시에 사용 가능한가 | 파이프라인 지연 모니터링 |
| Uniqueness | 중복이 없는가 | DISTINCT 비율 체크 |
| Validity | 허용 범위 내인가 | 스키마/규칙 검증 |

### 자동 검증 규칙
```sql
-- Completeness
SELECT COUNT(*) FILTER (WHERE email IS NULL) * 100.0 / COUNT(*)
FROM users; -- 임계치: < 1%

-- Freshness
SELECT MAX(created_at) FROM events;
-- 마지막 이벤트가 1시간 이전이면 알림

-- Volume
SELECT COUNT(*) FROM events
WHERE created_at > NOW() - INTERVAL '1 hour';
-- 시간당 이벤트 수가 평소의 50% 미만이면 알림
```

### 데이터 계약 (Data Contract)
- 소스 팀과 분석 팀 간 스키마 합의
- 필수/선택 필드, 데이터 타입, 허용 값 명시
- Breaking change 시 사전 통지 + 마이그레이션 기간

## Connections

- [[analytics.role]] — FEEDS (weight: 0.5)
