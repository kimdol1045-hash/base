---
id: "content.readability"
domain: "content"
type: "rule"
bloom_level: ""
tags: ["content", "writing", "readability"]
brain_region: "WERNICKE"
token_estimate: 380
---

# content.readability

> #150 Readability (Flesch, 1948)

가독성 (읽기 쉬운 글이 이해하기 쉬운 글이다):

### 한국어 가독성 규칙
1. 문장 길이: 30자 이내 권장 (최대 50자)
2. 문단 길이: 3-4문장. 5문장 넘으면 분리.
3. 한 문장 = 한 가지 정보.

### 문체 규칙
- 능동태 > 수동태: "서버가 요청을 처리합니다" > "요청이 서버에 의해 처리됩니다"
- 긍정문 > 부정문: "인증이 필요합니다" > "인증 없이는 불가합니다"
- 구체적 > 추상적: "3초 내 응답" > "빠르게 응답"
- 명사형 종결 지양: "~하는 것이 중요함" → "~해야 합니다"

### 기술 문서 특화
- 전문용어 첫 등장 시 설명: "SSR(서버 사이드 렌더링)"
- 코드와 설명 교대 배치 (코드 블록 앞에 한 줄 설명)
- 단계별 설명은 번호 매기기 (1, 2, 3)
- 주의사항은 별도 블록으로 강조

### DO:
"API 키를 환경변수에 저장하세요. `.env` 파일에 추가합니다."

### DON'T:
"API 키의 경우, 보안상의 이유로 인해 하드코딩하지 않는 것이 권장되며, 대신 환경변수를 활용하는 방식으로 관리하는 것이 바람직하다고 할 수 있겠습니다."

## Connections

- [[content.role]] — REQUIRES (weight: 0.9)
- [[content.verify]] — FEEDS (weight: 0.8)
- [[content.inverted-pyramid]] — FEEDS (weight: 0.7)
- [[content.structure]] — FEEDS (weight: 0.7)
- [[content.role]] — FEEDS (weight: 0.5)
- [[content.structure]] — FEEDS (weight: 0.5)
- [[content.technical-docs]] — FEEDS (weight: 0.5)
