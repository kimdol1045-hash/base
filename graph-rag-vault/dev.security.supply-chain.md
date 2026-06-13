---
id: "dev.security.supply-chain"
domain: "development.security"
type: "rule"
bloom_level: ""
tags: ["security", "supply-chain", "dependency", "slsa"]
brain_region: "CORTEX"
token_estimate: 400
---

# dev.security.supply-chain

> #175 Supply Chain Security (SLSA Framework, Google)

공급망 보안 (의존성과 빌드 파이프라인의 무결성을 보장한다):

### 주요 위협
| 공격 | 설명 | 사례 |
|------|------|------|
| 의존성 혼동 | 공개 패키지가 내부 패키지명 탈취 | ua-parser-js (2021) |
| 타이포스쿼팅 | 유사 패키지명으로 악성 코드 배포 | crossenv → cross-env |
| 유지보수자 탈취 | 패키지 유지보수자 계정 해킹 | event-stream (2018) |
| 빌드 파이프라인 | CI/CD에 악성 코드 주입 | SolarWinds (2020) |

### 방어 체크리스트
- [ ] `npm audit` / `pip audit` 정기 실행
- [ ] 의존성 lockfile(package-lock.json) 커밋 필수
- [ ] Dependabot/Renovate로 자동 업데이트 PR
- [ ] 신규 의존성 추가 시 다운로드 수, 유지보수 상태, 라이선스 확인
- [ ] 최소 의존성 원칙 (기능 1개를 위해 패키지 추가 금지)
- [ ] CI에서 npm ci (clean install) 사용
- [ ] Private registry (Artifactory, Verdaccio) 고려

### SLSA 레벨
| 레벨 | 요구사항 |
|------|---------|
| 1 | 빌드 프로세스 문서화 |
| 2 | 호스팅된 빌드 서비스 사용 |
| 3 | 소스/빌드 무결성 검증 |
| 4 | 2인 리뷰 + 재현 가능한 빌드 |
