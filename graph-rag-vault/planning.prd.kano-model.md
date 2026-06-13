---
id: "planning.prd.kano-model"
domain: "planning"
type: "pattern"
bloom_level: ""
tags: ["planning", "kano", "prioritization", "product"]
brain_region: "PREFRONTAL"
token_estimate: 420
---

# planning.prd.kano-model

> #156 Kano Model (Noriaki Kano, 1984)

카노 모델 (기능별 고객 만족 기여도를 분류한다):

### 5가지 분류
| 유형 | 없을 때 | 있을 때 | 예시 |
|------|--------|--------|------|
| Must-be (기본) | 매우 불만 | 당연 | 로그인, 결제 정상 동작 |
| One-dimensional (성능) | 불만 | 만족 비례 | 로딩 속도, 검색 정확도 |
| Attractive (매력) | 무관 | 높은 만족 | AI 추천, 다크 모드 |
| Indifferent (무관) | 무관 | 무관 | 내부 리팩토링 |
| Reverse (역효과) | 만족 | 불만 | 과도한 알림, 강제 튜토리얼 |

### MVP 우선순위 적용
```
1순위: Must-be (없으면 사용 불가)
2순위: One-dimensional (경쟁 차별화)
3순위: Attractive (WOW 요소 1~2개)
제외: Indifferent + Reverse
```

### 기능 분류 질문법 (기능적/역기능적 질문)
- 기능적: "이 기능이 있다면 어떻게 느끼시겠습니까?"
- 역기능적: "이 기능이 없다면 어떻게 느끼시겠습니까?"
- 답변 조합으로 5가지 분류 결정

### 시간에 따른 변화
Attractive → One-dimensional → Must-be 로 시간이 지남에 따라 기대치 상승.
예: 스마트폰 터치스크린은 한때 Attractive, 지금은 Must-be.

### 적용 시 주의
- 문화/시장에 따라 분류가 다를 수 있음
- 정기적 재평가 필요 (분기별)
- 경쟁사의 Attractive가 우리의 Must-be가 될 수 있음

## Connections

- [[planning.prd.feature-prioritization]] — CO_CREATES (weight: 0.6)
- [[planning.prd.rice]] — CO_CREATES (weight: 0.6)
- [[planning.prd.metrics]] — CO_CREATES (weight: 0.6)
