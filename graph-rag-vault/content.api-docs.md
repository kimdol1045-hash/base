---
id: "content.api-docs"
domain: "content"
type: "pattern"
bloom_level: "API 문서는 개발자 경험(DX)의 핵심 요소로, 잘 작성된 문서는 지원 문의를 60% 이상 감소시킨다. OpenAPI/Swagger 명세를 기반으로 하되, 실행 가능한 예제가 핵심이다."
tags: ["api-docs", "technical-writing", "dx"]
brain_region: "WERNICKE"
token_estimate: 420
---

# content.api-docs

> API 문서는 개발자 경험(DX)의 핵심 요소로, 잘 작성된 문서는 지원 문의를 60% 이상 감소시킨다. OpenAPI/Swagger 명세를 기반으로 하되, 실행 가능한 예제가 핵심이다.

# API 문서 작성 가이드

## 핵심 원칙
- 모든 엔드포인트에 실행 가능한 예제 포함
- 에러 응답 코드별 상세 설명
- 인증 방식을 문서 최상단에 명시
- 변경 이력(Changelog) 관리 필수

## 문서 구조
1. **개요**: API 목적, 기본 URL, 인증 방식
2. **퀵스타트**: 5분 내 첫 API 호출 성공 가이드
3. **엔드포인트 목록**: HTTP 메서드 + 경로 + 설명
4. **요청/응답 스키마**: 필드별 타입, 필수 여부, 설명
5. **에러 코드**: 코드별 원인 + 해결 방법
6. **SDK 예제**: 주요 언어별 코드 스니펫

## DO
- curl 예제를 복사-붙여넣기로 바로 실행 가능하게 작성
- Rate Limit 정책을 명확히 기술
- 페이지네이션 방식을 예제와 함께 설명
- 필드 변경 시 deprecated 표시 후 2버전 유지

## DON'T
- 인증 토큰을 예제에 하드코딩하지 않기
- 선택적 파라미터를 필수처럼 기술하지 않기
- 실제 동작과 다른 응답 예시 사용하지 않기
- 버전 없이 API 변경 사항 배포하지 않기
