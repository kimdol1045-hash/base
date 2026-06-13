---
id: "planning.prd.rice"
domain: "planning"
type: "pattern"
region: PREFRONTAL
token_estimate: 430
theory: "#157 RICE Scoring (Intercom, 2016)"
tags: [planning, rice, prioritization, product]
---

# planning.prd.rice

> **Region**: 🧠 [[PREFRONTAL]]  
> **Domain**: `planning`  
> **Type**: `pattern`  
> **Theory**: #157 RICE Scoring (Intercom, 2016)  
> **Tokens**: 430

## Content

RICE 스코어링 (기능 우선순위를 정량적으로 결정한다):

### 공식
```
RICE Score = (Reach × Impact × Confidence) / Effort
```

### 각 요소 정의
| 요소 | 설명 | 측정 단위 |
|------|------|----------|
| Reach | 분기 내 영향받는 사용자 수 | 명 (예: 10,000명/분기) |
| Impact | 개인당 기여도 | 3=대, 2=고, 1=중, 0.5=저, 0.25=최소 |
| Confidence | 추정치 확신도 | 100%=높음, 80%=중, 50%=낮음 |
| Effort | 개발 공수 | 인-월 (person-months) |

### 예시 비교
| 기능 | Reach | Impact | Confidence | Effort | Score |
|------|-------|--------|------------|--------|-------|
| 소셜 로그인 | 5000 | 2 | 80% | 1 | 8000 |
| AI 추천 | 2000 | 3 | 50% | 3 | 1000 |
| 다크 모드 | 8000 | 0.5 | 100% | 0.5 | 8000 |
→ 소셜 로그인과 다크 모드 먼저 (같은 점수면 Effort 낮은 것 우선)

### 주의사항
- Confidence 50% 미만이면 리서치부터 (구현 X)
- Effort 과소평가 주의: 개발자 추정치에 1.5x 버퍼
- 전략적 중요도는 RICE에 안 잡힘 → 별도 가중치 필요
- 팀 전체가 합의한 기준으로 점수 매기기 (개인 편향 방지)

### vs 다른 프레임워크
| 프레임워크 | 장점 | 단점 |
|-----------|------|------|
| RICE | 정량적, 비교 쉬움 | Impact 주관적 |
| MoSCoW | 간단, 빠름 | 비정량적 |
| Kano | 고객 관점 | 설문 필요 |
| ICE | 빠른 판단 | Confidence 생략 가능 |

## Connections

*Connections will be populated by Graph RAG ingest.*
