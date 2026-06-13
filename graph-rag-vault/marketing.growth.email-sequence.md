---
id: "marketing.growth.email-sequence"
domain: "marketing"
type: "pattern"
bloom_level: "이메일 시퀀스는 사전에 설계된 자동화 이메일 시리즈로, 사용자 행동과 생애주기 단계에 맞춰 발송된다. 온보딩, 너처링, 재활성화, 업셀링 등 목적별 시퀀스가 핵심이다."
tags: ["email", "automation", "drip-campaign", "sequence"]
brain_region: "SENSORS"
token_estimate: 400
---

# marketing.growth.email-sequence

> 이메일 시퀀스는 사전에 설계된 자동화 이메일 시리즈로, 사용자 행동과 생애주기 단계에 맞춰 발송된다. 온보딩, 너처링, 재활성화, 업셀링 등 목적별 시퀀스가 핵심이다.

# 이메일 시퀀스 가이드

## 핵심 원칙
- 사용자 행동/단계에 맞는 맥락적 발송
- 가치 제공 이메일 : 홍보 이메일 = 4:1
- 개인화: 이름, 행동, 세그먼트 기반
- 빈도 제한: 피로 방지 (일 1회, 주 3회 상한)

## 시퀀스 유형
### 온보딩 시퀀스 (7일)
- Day 0: 환영 + 핵심 가치 제안
- Day 1: 첫 단계 가이드 (Aha Moment 유도)
- Day 3: 팁 + 성공 사례
- Day 5: 고급 기능 소개
- Day 7: 피드백 요청

### 너처링 시퀀스
- 주 1-2회, 교육적 콘텐츠 중심
- 리드 스코어에 따라 영업 전달

### 재활성화 시퀀스
- 30일 미접속 시 트리거
- 변경 사항 + 인센티브 제공

## 이메일 최적화 지표
| 지표 | 벤치마크 |
|------|---------|
| 오픈율 | 20-30% |
| 클릭률 | 2-5% |
| 구독 해지율 | 0.5% 이하 |
| 전환율 | 시퀀스 목적별 상이 |

## DO
- 제목에 개인화 요소 포함
- 하나의 이메일에 하나의 CTA만 포함
- 발송 시간 A/B 테스트

## DON'T
- 구독 해지 링크를 숨기거나 어렵게 하지 않기
- 모든 세그먼트에 동일한 시퀀스 보내지 않기
- 이미지만으로 핵심 메시지 전달하지 않기

## Connections

- [[marketing.growth.role]] — REQUIRES (weight: 0.9)
- [[marketing.growth.verify]] — FEEDS (weight: 0.8)
- [[marketing.growth.social-media]] — FEEDS (weight: 0.7)
- [[marketing.growth.role]] — CO_CREATES (weight: 0.6)
