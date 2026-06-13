---
id: "planning.competitive-analysis.swot"
domain: "planning"
type: "pattern"
region: PREFRONTAL
token_estimate: 500
theory: "#82 SWOT (Humphrey, 1960s)"
tags: [planning, competitive-analysis, swot, tows, pattern]
---

# planning.competitive-analysis.swot

> **Region**: 🧠 [[PREFRONTAL]]  
> **Domain**: `planning`  
> **Type**: `pattern`  
> **Theory**: #82 SWOT (Humphrey, 1960s)  
> **Tokens**: 500

## Content

SWOT Analysis (내부 역량과 외부 환경을 체계적으로 분석한다):

### 왜 SWOT인가?
SWOT은 가장 널리 쓰이는 전략 분석 도구이지만, 제대로 활용하는 경우는 드물다.
단순히 4칸을 채우는 것이 아니라, 내부 요인(통제 가능)과 외부 요인(통제 불가)을
구분하고, 이를 TOWS 매트릭스로 전환하여 구체적 전략을 도출해야 한다.

### SWOT 4사분면 정의

|  | 긍정적 | 부정적 |
|--|--------|--------|
| **내부** (통제 가능) | **Strengths** | **Weaknesses** |
| **외부** (통제 불가) | **Opportunities** | **Threats** |

**핵심 구분 기준:**
- 내부 요인: 우리 팀/제품/조직이 직접 변경할 수 있는 것
- 외부 요인: 시장, 경쟁, 기술 트렌드, 규제 등 우리가 통제할 수 없는 것

### 각 사분면 작성 가이드

**Strengths (내부 강점)** — 3-5개
질문: "경쟁사 대비 우리가 확실히 나은 점은?"
- 기술적 역량, 팀 전문성, 독점 데이터, 기존 사용자 기반
- DO: "팀에 추천 알고리즘 전문 ML 엔지니어가 있어 개인화 기능에 강점"
- DON'T: "열정적인 팀" → 측정/검증 불가능한 것은 강점이 아니다
- 검증 질문: "이것이 정말 경쟁 우위인가, 아니면 희망사항인가?"

**Weaknesses (내부 약점)** — 3-5개
질문: "솔직하게, 우리의 약한 점은?"
- 부족한 리소스, 기술 부채, 브랜드 인지도 부재, 경험 부족
- DO: "디자인 전문 인력 부재로 UI/UX 품질에 한계.
       MVP 단계에서는 템플릿 기반으로 진행하고 Series A 이후 채용 계획"
- DON'T: 약점을 숨기거나 최소화 → 솔직한 인정이 전략 수립의 기초

**Opportunities (외부 기회)** — 3-5개
질문: "시장에서 우리에게 유리하게 작용하는 변화는?"
- 시장 성장, 기술 트렌드, 규제 변화, 경쟁사 약화, 소비자 행동 변화
- DO: "생성형 AI 기술의 보편화로 소규모 팀도 AI 기능 구현이 가능해짐.
       OpenAI API 비용이 전년 대비 80% 하락 [출처: OpenAI 공식 블로그]"
- DON'T: "AI 시장이 크다" → 구체적 트렌드와 우리에게 미치는 영향 서술

**Threats (외부 위협)** — 3-5개
질문: "시장에서 우리에게 불리하게 작용하는 변화는?"
- 경쟁 심화, 기술 변화, 규제 리스크, 경기 침체, 대기업 진입
- DO: "Google이 유사 기능을 기본 탑재할 가능성. Gmail에 AI 요약 기능이
       추가되면 우리 제품의 핵심 가치 제안이 약화될 수 있다"
- DON'T: "경쟁이 심해질 수 있다" → 구체적 시나리오 제시

### TOWS 매트릭스 (SWOT → 전략 전환)
SWOT을 채우는 것에 그치지 않고, 교차 분석으로 전략을 도출한다:

| | Strengths | Weaknesses |
|--|-----------|------------|
| **Opportunities** | **SO 전략** (강점으로 기회 활용) | **WO 전략** (약점 보완하여 기회 활용) |
| **Threats** | **ST 전략** (강점으로 위협 대응) | **WT 전략** (약점+위협 최소화) |

**SO 전략 예시:** "ML 전문성(S)을 활용하여 AI 트렌드(O)에 맞는
개인화 추천 기능을 차별화 포인트로 내세운다"

**WO 전략 예시:** "디자인 역량 부족(W)을 보완하기 위해
no-code UI 빌더 트렌드(O)를 활용하여 템플릿 기반 접근"

**ST 전략 예시:** "기존 사용자 기반(S)을 활용하여 대기업 진입(T) 전에
네트워크 효과를 구축하여 전환 비용 높이기"

**WT 전략 예시:** "브랜드 인지도 부족(W) + 경쟁 심화(T) 상황에서
니치 시장에 집중하여 특정 세그먼트 1위 달성"

### TOWS 전략 템플릿
```
전략 유형: SO / WO / ST / WT
전략명: [1줄 요약]
근거 S/W: [연결된 내부 요인]
근거 O/T: [연결된 외부 요인]
구체적 액션: [실행 가능한 행동]
시기: MVP / v2 / 장기
```

### 주의사항
- S/W/O/T 각각 3-5개씩. 1-2개는 분석 부족, 7개 이상은 초점 분산
- Strength에 "열정", "팀워크" 같은 검증 불가능한 항목 금지
- 외부 요인에 출처/근거 제시: "AI 시장 성장 [Gartner 2024 추정치]"
- TOWS까지 완성해야 SWOT의 가치가 있다 (4칸 채우기만으로는 부족)

## Connections

### CO_CREATES (4)

- ← [[planning.competitive-analysis.porter]] `w=0.6`
- ← [[planning.competitive-analysis.role]] `w=0.6`
- → [[planning.competitive-analysis.value-curve]] `w=0.6`
- → [[planning.competitive-analysis.verify]] `w=0.6`
