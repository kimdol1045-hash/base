---
id: "content.technical-docs"
domain: "content"
type: "pattern"
region: HIPPOCAMPUS
token_estimate: 420
theory: "#143 Divio Documentation System (4-type model)"
tags: [content, documentation, api-docs, readme]
---

# content.technical-docs

> **Region**: 🌿 [[HIPPOCAMPUS]]  
> **Domain**: `content`  
> **Type**: `pattern`  
> **Theory**: #143 Divio Documentation System (4-type model)  
> **Tokens**: 420

## Content

기술 문서 작성 (사용자가 원하는 정보를 빠르게 찾게 한다):

### Divio 4분류 모델
| 유형 | 목적 | 예시 |
|------|------|------|
| Tutorial | 학습 (따라하기) | "첫 API 호출하기" |
| How-to Guide | 문제 해결 | "인증 토큰 갱신하는 법" |
| Reference | 정보 조회 | API 엔드포인트 명세 |
| Explanation | 이해 | "인증 방식 비교 (JWT vs Session)" |

### API 문서 필수 항목
```markdown
## POST /api/users

사용자를 생성합니다.

### Request
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| email | string | Yes | 유효한 이메일 |
| name | string | Yes | 2~50자 |

### Response (201)
{ "id": "uuid", "email": "...", "createdAt": "ISO8601" }

### Error
- 400: 유효성 검증 실패
- 409: 이미 존재하는 이메일
```

### README 구조
1. 프로젝트 한 줄 설명
2. Quick Start (3단계 이내)
3. 설치 방법
4. 사용 예제 (복사-붙여넣기 가능)
5. 설정 옵션
6. 라이선스

### 품질 기준
- 코드 예제는 실제 실행 가능해야 함
- 버전별 차이 명시 (v1 → v2 마이그레이션 가이드)
- 마지막 업데이트 날짜 표기

## Connections

*Connections will be populated by Graph RAG ingest.*
