---
id: "design.ux-psychology.teslers-law"
domain: "design"
type: "rule"
region: LIMBIC
token_estimate: 400
theory: "#53 Tesler's Law (Tesler, 2007)"
tags: [design, ux, tesler, simplicity]
---

# design.ux-psychology.teslers-law

> **Region**: 💜 [[LIMBIC]]  
> **Domain**: `design`  
> **Type**: `rule`  
> **Theory**: #53 Tesler's Law (Tesler, 2007)  
> **Tokens**: 400

## Content

테슬러 법칙 (모든 시스템에는 줄일 수 없는 본질적 복잡성이 있다):

### 핵심 원리
복잡성은 사라지지 않고 이동한다: 사용자 → 시스템, 또는 시스템 → 사용자.
좋은 설계 = 시스템이 복잡성을 흡수하여 사용자 부담 최소화.

### 적용 패턴
1. **스마트 기본값**: 사용자가 선택하지 않아도 합리적으로 동작
   - 배송지: 최근 사용 주소 자동 선택
   - 알림: 합리적 기본값 ON, 세부 설정은 옵션
   - 날짜: 오늘 날짜 기본값

2. **점진적 공개 (Progressive Disclosure)**: 고급 옵션은 숨김
   ```tsx
   <div>
     <Input placeholder="검색어 입력" />
     <Collapsible>
       <CollapsibleTrigger className="text-sm text-muted-foreground">
         고급 검색 옵션 ▾
       </CollapsibleTrigger>
       <CollapsibleContent>
         <Select>날짜 범위</Select>
         <Select>카테고리</Select>
         <Checkbox>정확히 일치</Checkbox>
       </CollapsibleContent>
     </Collapsible>
   </div>
   ```

3. **자동 완성/추론**: 시스템이 추론 가능한 건 묻지 않기
   - 우편번호 → 주소 자동 완성
   - 카드 번호 앞 자리 → 카드사 자동 인식
   - 위치 기반 → 언어/통화 자동 설정

### 경고
- 과도한 자동화: 사용자가 통제감을 잃으면 불안 (자율성 침해)
- 마법 같은 동작: 왜 이렇게 되었는지 설명 가능해야

## Connections

### REQUIRES (1)

- ← [[design.ux-psychology.role]] `w=0.9`

### FEEDS (2)

- ← [[design.ux-psychology.recognition-over-recall]] `w=0.7`
- → [[design.ux-psychology.verify]] `w=0.8`
