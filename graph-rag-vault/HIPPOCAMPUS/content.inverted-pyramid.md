---
id: "content.inverted-pyramid"
domain: "content"
type: "rule"
region: HIPPOCAMPUS
token_estimate: 380
theory: "#149 Inverted Pyramid (Pöttker, 2003)"
tags: [content, writing, structure]
---

# content.inverted-pyramid

> **Region**: 🌿 [[HIPPOCAMPUS]]  
> **Domain**: `content`  
> **Type**: `rule`  
> **Theory**: #149 Inverted Pyramid (Pöttker, 2003)  
> **Tokens**: 380

## Content

역피라미드 (가장 중요한 정보를 먼저 전달한다):

### 구조
1. **리드 (첫 1-2문장)**: 핵심 결론/가치. 이것만 읽어도 핵심 파악.
2. **핵심 정보 (2-3단락)**: Why, How, What 상세.
3. **배경/세부 (나머지)**: 추가 맥락, 기술 상세, 참고자료.

### DO:
리드 예시 (기술 블로그):
"Next.js 15의 Partial Prerendering은 정적+동적 렌더링을 한 페이지에서 결합하여 TTFB를 50% 단축합니다."

리드 예시 (제품 업데이트):
"이제 대시보드에서 실시간 협업이 가능합니다. 팀원이 수정 중인 셀이 실시간으로 표시됩니다."

### DON'T:
"안녕하세요, 오늘은 Next.js 15에 대해 이야기해보려고 합니다.
Next.js는 Vercel에서 만든 React 프레임워크로..." (핵심이 3번째 단락에)

### 적용 상황별
- 기술 문서: 결론(이렇게 하세요) → 이유 → 상세 구현
- 이메일: 용건(요청/공유) → 맥락 → 상세
- PR 설명: 변경사항 요약 → 왜 → 기술적 세부
- 에러 메시지: 무엇이 잘못됐는지 → 어떻게 해결하는지

## Connections

### REQUIRES (1)

- ← [[content.role]] `w=0.9`

### FEEDS (2)

- → [[content.readability]] `w=0.7`
- → [[content.verify]] `w=0.8`
