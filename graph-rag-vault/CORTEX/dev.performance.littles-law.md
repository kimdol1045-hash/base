---
id: "dev.performance.littles-law"
domain: "development.performance"
type: "rule"
region: CORTEX
token_estimate: 380
theory: "#136 Little's Law (Little, 1961)"
tags: [performance, capacity, scaling]
---

# dev.performance.littles-law

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.performance`  
> **Type**: `rule`  
> **Theory**: #136 Little's Law (Little, 1961)  
> **Tokens**: 380

## Content

리틀의 법칙 (시스템 용량을 수학적으로 계산한다):

### 공식
L = λ × W
- L = 시스템 내 평균 요청 수 (동시접속)
- λ = 초당 도착률 (요청/초, RPS)
- W = 평균 처리 시간 (초)

### 용량 계획 예시
요구사항: 초당 100 요청, 평균 응답시간 200ms
- L = 100 × 0.2 = 20 (동시 처리 필요)
- 서버 1대가 10 동시 처리 → 최소 2대 + 여유 1대 = 3대

### DB 커넥션 풀 크기 결정
```
풀 크기 = (초당 쿼리 수) × (쿼리 평균 시간)

예: 500 QPS × 10ms = 5 커넥션
여유 50% → pool_size = 8
```

### 실무 활용
1. 로드 테스트로 W(평균 처리 시간) 측정
2. 예상 트래픽에서 λ(RPS) 산출
3. L 계산 → 서버/커넥션/워커 수 결정
4. 피크 트래픽은 평균의 3-5배로 가정

### 경고 신호
- L이 처리 능력 초과 → 큐잉 시작 → W 급증 → 장애
- 모니터링: 동시접속수가 설계치의 80% 넘으면 알림

## Connections

### FEEDS (1)

- → [[dev.frontend.component.performance]] `w=0.5`

### CO_CREATES (5)

- ← [[dev.performance.amdahl]] `w=0.6`
- ← [[dev.performance.budget]] `w=0.6`
- ← [[dev.performance.caching]] `w=0.6`
- ← [[dev.performance.role]] `w=0.6`
- ← [[dev.performance.web-vitals]] `w=0.6`
