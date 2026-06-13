---
id: "meta.bias-prevention.planning-fallacy"
domain: "meta"
type: "rule"
region: EGO
token_estimate: 380
theory: "#A9 Planning Fallacy (Buehler, Griffin & Ross, 1994)"
tags: [meta, bias, planning-fallacy, estimation]
---

# meta.bias-prevention.planning-fallacy

> **Region**: 🔵 [[EGO]]  
> **Domain**: `meta`  
> **Type**: `rule`  
> **Theory**: #A9 Planning Fallacy (Buehler, Griffin & Ross, 1994)  
> **Tokens**: 380

## Content

계획 오류 (소요 시간/비용을 체계적으로 과소 추정):

### AI에서 발현
- "이 기능은 2-3일이면 됩니다" (실제 2주)
- MVP 범위를 과소 추정
- 예외 처리, 테스트, 배포 시간 미포함

### 방지 패턴
1. **참조 클래스 예측 (Reference Class Forecasting)**
   과거 유사 프로젝트 데이터 기반 추정:
   "유사한 CRUD API 프로젝트의 실제 소요 시간 분포: 최소 1주, 평균 2주, 최대 4주"

2. **범위 추정 (3점 추정)**
   | 항목 | 낙관 | 기대 | 비관 |
   |------|------|------|------|
   | 인증 API | 3일 | 5일 | 10일 |
   | 결제 연동 | 5일 | 10일 | 20일 |
   - 기대치 = (낙관 + 4×기대 + 비관) / 6

3. **숨겨진 작업 포함 필수**
   개발 외 시간: 설계 리뷰, 코드 리뷰, 테스트 작성, 문서화, 배포, 버그 수정
   경험칙: 순수 코딩 시간 × 2~3 = 실제 소요 시간

4. **절대 하지 말 것**
   - 구체적 일수/시간 추정 제시
   - "금방 됩니다", "간단합니다" 같은 표현

## Connections

### REQUIRES (1)

- ← [[meta.bias-prevention.role]] `w=0.9`

### FEEDS (3)

- ← [[meta.bias-prevention.availability-bias]] `w=0.7`
- → [[meta.bias-prevention.verify]] `w=0.8`
- → [[meta.output-validator]] `w=0.7`
