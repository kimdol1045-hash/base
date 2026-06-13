---
id: "qa.test-gen.fuzz"
domain: "qa"
type: "pattern"
bloom_level: ""
tags: ["qa", "fuzz-testing", "security", "crash"]
brain_region: "CEREBELLUM"
token_estimate: 370
---

# qa.test-gen.fuzz

> #184 Fuzz Testing (Barton Miller, 1988)

퍼즈 테스트 (랜덤/비정상 입력으로 크래시와 취약점을 발견한다):

### 핵심 개념
프로그램에 무작위/비정상 데이터를 대량 입력 → 크래시, 메모리 누수, 보안 취약점 발견

### 퍼징 유형
| 유형 | 설명 | 도구 |
|------|------|------|
| Dumb Fuzzing | 완전 랜덤 입력 | 간단하지만 커버리지 낮음 |
| Smart Fuzzing | 입력 형식 인지 | AFL, libFuzzer |
| Coverage-guided | 코드 커버리지 피드백 활용 | AFL++, Jazzer |

### 웹 API 퍼징
```bash
# OpenAPI 스펙 기반 퍼징
restler-fuzzer --api_spec openapi.json --time_budget 3600
```

### 퍼징 대상
- ✅ 효과적: 파서(JSON, XML, CSV), 이미지 처리, 파일 업로드, 인증 로직
- ❌ 비효율: UI 테스트, 외부 API 의존 코드

### 입력 생성 전략
- 경계값: 0, -1, MAX_INT, 빈 문자열, 매우 긴 문자열
- 특수문자: `<script>`, `'; DROP TABLE`, `../../../etc/passwd`
- 타입 혼동: 숫자 필드에 문자열, 배열 필드에 객체
- 유니코드: 이모지, RTL 문자, NULL 바이트

## Connections

- [[qa.test-gen.role]] — CO_CREATES (weight: 0.6)
