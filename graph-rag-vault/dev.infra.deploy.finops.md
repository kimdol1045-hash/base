---
id: "dev.infra.deploy.finops"
domain: "development.infra"
type: "rule"
bloom_level: ""
tags: ["infra", "finops", "cost-optimization", "cloud"]
brain_region: "CEREBELLUM"
token_estimate: 400
---

# dev.infra.deploy.finops

> #190 FinOps (Cloud Financial Management, FinOps Foundation)

FinOps (클라우드 비용을 엔지니어링 관점에서 최적화한다):

### 3단계 순환
1. **Inform**: 비용 가시성 확보 (누가, 무엇에, 얼마나)
2. **Optimize**: 불필요한 지출 제거 + 할인 활용
3. **Operate**: 비용 의식 문화 + 자동화

### 즉시 절약 체크리스트
- [ ] 미사용 리소스 정리 (유휴 EC2, 빈 EBS, 오래된 스냅샷)
- [ ] 적정 사이즈: 과다 프로비저닝된 인스턴스 다운사이징
- [ ] Reserved/Savings Plan: 예측 가능한 워크로드에 1~3년 약정
- [ ] Spot Instance: 내결함성 있는 워크로드에 활용 (70% 절약)
- [ ] 스토리지 계층화: S3 Glacier로 오래된 데이터 이동
- [ ] 개발/스테이징 환경 야간/주말 자동 종료

### 비용 태깅
```
태그 필수: team, service, environment, cost-center
```
팀별/서비스별 비용 추적이 태깅 없으면 불가능

### 알림 설정
- 일별 비용이 전월 평균의 150% 초과 시 알림
- 월 예산 80% 도달 시 경고
- 신규 리소스 생성 시 태그 누락 알림

### 핵심 지표
- Unit Economics: 사용자당/거래당 인프라 비용
- Coverage: RI/SP 커버리지 비율 (목표 70%+)
- Waste: 유휴 리소스 비율 (목표 5% 미만)
