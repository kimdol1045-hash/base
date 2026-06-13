---
id: "content.changelog"
domain: "content"
type: "pattern"
region: HIPPOCAMPUS
token_estimate: 420
theory: "#145 Keep a Changelog (Oliveira) + Semantic Versioning (Preston-Werner)"
tags: [content, changelog, release-notes, semver]
---

# content.changelog

> **Region**: 🌿 [[HIPPOCAMPUS]]  
> **Domain**: `content`  
> **Type**: `pattern`  
> **Theory**: #145 Keep a Changelog (Oliveira) + Semantic Versioning (Preston-Werner)  
> **Tokens**: 420

## Content

체인지로그 & 릴리즈 노트 (변경사항을 명확히 전달한다):

### Keep a Changelog 형식
```markdown
## [1.2.0] - 2024-03-15

### Added
- 소셜 로그인 (Google, GitHub) 지원
- 다크 모드 토글

### Changed
- 비밀번호 최소 길이 6자 → 8자

### Fixed
- 모바일에서 드롭다운 메뉴 잘림 현상 수정

### Deprecated
- v1 API 엔드포인트 (v2 마이그레이션 가이드 참조)

### Removed
- IE11 지원 중단

### Security
- XSS 취약점 패치 (CVE-2024-XXXX)
```

### Semantic Versioning (SemVer)
- MAJOR: 하위 호환 불가 변경 (2.0.0)
- MINOR: 하위 호환 기능 추가 (1.1.0)
- PATCH: 하위 호환 버그 수정 (1.0.1)
- 판단 기준: "기존 사용자 코드가 깨지는가?"

### 릴리즈 노트 vs 체인지로그
| 구분 | 체인지로그 | 릴리즈 노트 |
|------|----------|-----------|
| 독자 | 개발자 | 사용자/이해관계자 |
| 내용 | 기술적 변경 | 사용자 관점 혜택 |
| 톤 | 간결/목록형 | 설명적/스크린샷 포함 |

### 금지사항
- "각종 버그 수정" 같은 뭉뚱그린 설명
- 이슈 번호 없는 변경사항
- Breaking Change 미고지

## Connections

*Connections will be populated by Graph RAG ingest.*
