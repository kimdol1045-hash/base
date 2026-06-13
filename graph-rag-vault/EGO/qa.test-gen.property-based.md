---
id: "qa.test-gen.property-based"
domain: "qa"
type: "pattern"
region: EGO
token_estimate: 430
theory: "#155 Property-Based Testing (QuickCheck, Claessen & Hughes, 2000)"
tags: [qa, property-based-testing, fast-check, quickcheck]
---

# qa.test-gen.property-based

> **Region**: 🔵 [[EGO]]  
> **Domain**: `qa`  
> **Type**: `pattern`  
> **Theory**: #155 Property-Based Testing (QuickCheck, Claessen & Hughes, 2000)  
> **Tokens**: 430

## Content

Property-Based Testing (속성을 정의하고 랜덤 입력으로 검증한다):

### 핵심 개념
- 예시 기반: "입력 A → 출력 B" (특정 케이스)
- 속성 기반: "모든 입력에 대해 속성 P가 성립" (일반화)

### 자주 쓰는 속성 유형
| 속성 | 설명 | 예시 |
|------|------|------|
| 왕복(Roundtrip) | 변환→역변환 = 원본 | encode(decode(x)) === x |
| 멱등성 | 두 번 적용해도 같음 | sort(sort(x)) === sort(x) |
| 불변식 | 항상 참인 조건 | sort(x).length === x.length |
| 모델 비교 | 단순 구현과 결과 비교 | fastSort(x) === simpleSort(x) |
| 에러 없음 | 어떤 입력이든 크래시 안 남 | parse(randomString) doesn't throw |

### fast-check 예시 (TypeScript)
```typescript
import fc from 'fast-check';

// 정렬 결과 길이가 입력과 같다 (불변식)
test('sort 결과 길이 보존', () => {
  fc.assert(
    fc.property(fc.array(fc.integer()), (arr) => {
      const sorted = mySort(arr);
      return sorted.length === arr.length;
    })
  );
});

// JSON 직렬화 왕복
test('JSON roundtrip', () => {
  fc.assert(
    fc.property(fc.jsonValue(), (value) => {
      expect(JSON.parse(JSON.stringify(value))).toEqual(value);
    })
  );
});
```

### 적용 대상
- ✅ 적용: 파서, 직렬화, 정렬, 수학 연산, 데이터 변환
- ❌ 부적합: UI 테스트, 외부 API 의존 테스트

### Shrinking
실패 케이스 발견 시 자동으로 최소 반례를 찾아줌.
예: [3, -1, 99, 0, -5] 실패 → [-1] 최소 반례

## Connections

*Connections will be populated by Graph RAG ingest.*
