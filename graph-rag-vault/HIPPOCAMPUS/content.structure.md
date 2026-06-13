---
id: "content.structure"
domain: "content"
type: "pattern"
region: HIPPOCAMPUS
token_estimate: 400
tags: [content, writing, structure, template]
---

# content.structure

> **Region**: 🌿 [[HIPPOCAMPUS]]  
> **Domain**: `content`  
> **Type**: `pattern`  
> **Tokens**: 400

## Content

글 구조 패턴 (목적에 맞는 구조를 선택한다):

### 1. 문제-해결 (Problem-Solution)
적합: 기술 블로그, 제품 소개, 에러 가이드
```
❌ 문제: Next.js에서 번들 크기가 500KB를 초과합니다.
💡 원인: barrel export로 불필요한 코드가 포함됩니다.
✅ 해결: 개별 파일에서 직접 임포트하세요.
📝 코드 예시: ...
```

### 2. 단계별 (Step-by-Step)
적합: 튜토리얼, 설정 가이드, 온보딩
```
1. 프로젝트 생성: npx create-next-app@latest
2. 의존성 설치: npm install @supabase/supabase-js
3. 환경변수 설정: .env.local에 SUPABASE_URL 추가
4. 클라이언트 초기화: lib/supabase.ts 작성
```

### 3. 비교 대조 (Comparison)
적합: 기술 선택, 가격 비교, 마이그레이션 가이드
```
| 기준 | REST | GraphQL | tRPC |
|------|------|---------|------|
| 학습 곡선 | 낮음 | 중간 | 중간 |
| 타입 안전 | 수동 | codegen | 자동 |
| 적합한 경우 | 공개 API | 복잡 데이터 | 풀스택 TS |
```

### 4. 원인-결과 (Cause-Effect)
적합: 장애 보고서, 버그 분석, 성능 리포트
```
◆ 현상: 결제 API 응답시간 5초 → 타임아웃
◆ 원인: N+1 쿼리로 주문 건당 상품 조회
◆ 영향: 결제 실패율 15% 증가
◆ 해결: JOIN 쿼리로 변경 → 응답시간 200ms
```

## Connections

### REQUIRES (1)

- ← [[content.role]] `w=0.9`

### FEEDS (4)

- ← [[content.readability]] `w=0.7`
- → [[content.readability]] `w=0.5`
- ← [[content.role]] `w=0.5`
- → [[content.verify]] `w=0.8`
