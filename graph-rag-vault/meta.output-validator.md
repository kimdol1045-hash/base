---
id: "meta.output-validator"
domain: "meta"
type: "verify"
bloom_level: ""
tags: ["meta", "validation", "hallucination", "consistency", "completeness", "quality-assurance", "output-check"]
brain_region: "PREFRONTAL"
token_estimate: 500
---

# meta.output-validator

> #72 확증 편향 방지 (Wason, 1960) — 자신의 출력을 의심하고 검증한다

AI 출력 검증 패턴 (구조, 완전성, 정합성, 환각을 체계적으로 검증한다):

### 왜 출력 검증이 필요한가?
LLM은 확증 편향(자신의 답이 맞다고 확신)과 환각(그럴듯하지만 사실이 아닌 정보 생성)
경향이 있다. 체계적 검증 없이 출력을 그대로 전달하면 오류가 전파된다.

### 출력 품질 검증 체크리스트 (10항목)

```
┌────┬──────────────────────────────────────────────┬───────────┐
│ #  │ 검증 항목                                     │ 유형      │
├────┼──────────────────────────────────────────────┼───────────┤
│ 1  │ 필수 섹션이 모두 존재하는가?                   │ 구조      │
│ 2  │ 요구사항이 빠짐없이 반영되었는가?              │ 완전성    │
│ 3  │ 앞뒤 문맥에 모순이 없는가?                    │ 정합성    │
│ 4  │ 검증 불가능한 주장이 포함되어 있지 않은가?      │ 환각      │
│ 5  │ 코드가 실제로 컴파일/실행 가능한가?            │ 실행 가능 │
│ 6  │ 네이밍/포맷이 프로젝트 컨벤션과 일치하는가?     │ 일관성    │
│ 7  │ 엣지 케이스가 고려되었는가?                    │ 견고성    │
│ 8  │ 보안 취약점이 포함되어 있지 않은가?            │ 보안      │
│ 9  │ 성능에 문제가 될 수 있는 패턴이 없는가?        │ 성능      │
│ 10 │ 사용자 요구의 의도를 정확히 반영했는가?         │ 의도      │
└────┴──────────────────────────────────────────────┴───────────┘
```

### 1. 구조 검증 (Structural Validation)

DO:
```typescript
// ✅ 출력 구조가 요구 형식과 일치하는지 검증
interface OutputValidation {
  requiredSections: string[];
  actualSections: string[];
  missingSections: string[];
  isValid: boolean;
}

function validateStructure(output: string, template: string[]): OutputValidation {
  const actualSections = extractSections(output); // 헤딩, 키 등 추출
  const missingSections = template.filter(
    (section) => !actualSections.includes(section)
  );
  return {
    requiredSections: template,
    actualSections,
    missingSections,
    isValid: missingSections.length === 0,
  };
}

// 예: PRD 출력 시 필수 섹션 체크
const prdTemplate = [
  "문제 정의", "타겟 사용자", "핵심 기능",
  "성공 지표", "기술 요구사항", "타임라인"
];
```

### 2. 완전성 검증 (Completeness Check)

```typescript
// ✅ 요구사항 추적 매트릭스
interface RequirementTrace {
  requirement: string;
  addressed: boolean;
  location: string; // 출력 내 위치
}

function checkCompleteness(
  requirements: string[],
  output: string
): RequirementTrace[] {
  return requirements.map((req) => ({
    requirement: req,
    addressed: output.toLowerCase().includes(req.toLowerCase()),
    location: findLocation(output, req),
  }));
  // 미반영 요구사항이 있으면 경고
}
```

### 3. 정합성 검증 (Consistency Check)

```typescript
// ✅ 내부 모순 탐지 패턴
// 예: "서버리스 아키텍처를 사용한다" vs "항상 실행 중인 서버에 배포한다"
// 예: API 스펙에서 필드명이 camelCase와 snake_case 혼재

function checkConsistency(output: string): ConsistencyIssue[] {
  const issues: ConsistencyIssue[] = [];

  // 네이밍 일관성 체크
  const camelCaseCount = (output.match(/[a-z][A-Z]/g) || []).length;
  const snakeCaseCount = (output.match(/[a-z]_[a-z]/g) || []).length;
  if (camelCaseCount > 0 && snakeCaseCount > 0) {
    issues.push({
      type: "naming_inconsistency",
      message: `camelCase(${camelCaseCount}회)와 snake_case(${snakeCaseCount}회) 혼재`,
    });
  }

  return issues;
}
```

### 4. 환각 탐지 (Hallucination Detection)

```
환각 위험 신호:
- 구체적인 수치가 출처 없이 등장: "이 방법은 성능이 340% 향상된다"
- 존재하지 않는 API/라이브러리 참조: "react-super-hooks 패키지를 설치한다"
- 과도하게 자신만만한 어조: "이것이 유일한 정답이다"
- 최신 정보 주장: "2025년 발표된 React 22의 새 기능"

대응:
- [UNVERIFIED] 태그 부착: 출처 확인이 필요한 주장 표시
- 코드 예시: 실제 import 경로와 API가 존재하는지 확인
- 수치: 출처(논문, 공식 문서)를 반드시 명시
```

### 5. 코드 실행 가능성 검증

```typescript
// ✅ 최소 검증: 타입 체크 + 임포트 확인
// - import한 패키지가 package.json에 존재하는가?
// - 함수 시그니처와 호출부의 인자가 일치하는가?
// - async 함수에 await가 빠져있지 않은가?
// - 존재하지 않는 메서드를 호출하고 있지 않은가?

// DON'T 예시 — 검증 없이 출력
// import { useServerAction } from "next/server"; ← 존재하지 않는 API
// const data = fetchUsers();  ← await 누락
```

DON'T:
```
❌ 자기 출력을 무비판적으로 신뢰
→ "내가 생성한 코드니까 맞겠지" — 반드시 검증 단계 수행

❌ 검증 없이 구체적 수치 제시
→ "응답 시간이 87% 개선된다" — 출처 없으면 [UNVERIFIED] 태그

❌ 에러 처리 누락 확인 생략
→ try-catch 없는 async 코드, null 체크 없는 접근 등

❌ 보안 검증 스킵
→ SQL injection, XSS, 인증 우회 가능성 미확인
```

## Connections

- [[meta.bias-prevention.role]] — REQUIRES (weight: 0.9)
- [[meta.bias-prevention.verify]] — FEEDS (weight: 0.8)
- [[meta.bias-prevention.planning-fallacy]] — FEEDS (weight: 0.7)
- [[meta.bias-prevention.role]] — FEEDS (weight: 0.5)
- [[meta.bias-prevention.confirmation-bias]] — FEEDS (weight: 0.5)
- [[meta.bias-prevention.survivorship-bias]] — FEEDS (weight: 0.5)
- [[meta.bias-prevention.availability-bias]] — FEEDS (weight: 0.5)
- [[meta.bias-prevention.dunning-kruger]] — FEEDS (weight: 0.5)
- [[meta.bias-prevention.framing-effect]] — FEEDS (weight: 0.5)
- [[meta.bias-prevention.hindsight-bias]] — FEEDS (weight: 0.5)
- [[meta.bias-prevention.sunk-cost]] — FEEDS (weight: 0.5)
