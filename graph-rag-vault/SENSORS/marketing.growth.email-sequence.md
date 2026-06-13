---
id: "marketing.growth.email-sequence"
domain: "marketing"
type: "pattern"
region: SENSORS
token_estimate: 500
theory: "#61 Hook Model — Trigger (Eyal, 2014)"
tags: [marketing, growth, email, onboarding, sequence, automation, retention]
---

# marketing.growth.email-sequence

> **Region**: 📡 [[SENSORS]]  
> **Domain**: `marketing`  
> **Type**: `pattern`  
> **Theory**: #61 Hook Model — Trigger (Eyal, 2014)  
> **Tokens**: 500

## Content

이메일 시퀀스 — 외부 트리거로 사용자를 제품 핵심 가치(Aha Moment)까지 안내하는 자동화된 커뮤니케이션:

### 온보딩 시퀀스 (가입 후 7일)
| 이메일 | 타이밍 | 목표 | 제목 예시 |
|--------|--------|------|----------|
| Welcome | 즉시 (가입 직후) | 첫 행동 유도 | "환영합니다! 첫 프로젝트를 만들어보세요" |
| Tutorial | Day 1 | 핵심 기능 사용 | "[이름]님, 2분이면 끝나는 빠른 시작 가이드" |
| Value | Day 3 | Aha Moment 도달 | "팀원을 초대하면 생산성이 2배가 됩니다" |
| Upgrade | Day 7 | 전환 유도 | "무료 체험 7일째, 지금까지의 성과를 확인하세요" |

### 너처 시퀀스 (비활성 사용자 재활성화)
| 이메일 | 타이밍 | 목표 | 제목 예시 |
|--------|--------|------|----------|
| Miss You | 비활성 3일 | 재방문 | "작성 중이던 리포트가 있어요" |
| New Feature | 비활성 7일 | 가치 재인식 | "이번 주 새로 추가된 기능 3가지" |
| Win-back | 비활성 14일 | 최후 시도 | "돌아오시면 Pro 30일 무료 드릴게요" |
| Sunset | 비활성 30일 | 정리 | "계정이 곧 비활성화됩니다. 데이터를 보존하시겠어요?" |

### 트랜잭셔널 이메일 패턴
```
결제 확인  → 즉시 발송 → 영수증 + 다음 단계
비밀번호 리셋 → 즉시 발송 → 링크 유효기간: 30분
팀원 초대  → 즉시 발송 → 수락 CTA + 팀 정보
주간 리포트 → 매주 월요일 09:00 → 핵심 수치 3개 + CTA
```

### DO: 효과적인 이메일 설계
```html
<!-- 제목: 30~50자, 개인화, 구체적 -->
Subject: "[이름]님, 이번 주 절약한 시간: 4.5시간"
Preview: "팀 대시보드에서 자세한 리포트를 확인하세요"

<!-- 본문: 단일 CTA, 모바일 퍼스트 -->
<div style="max-width: 600px; padding: 20px;">
  <p>안녕하세요 [이름]님,</p>
  <p>이번 주 [팀명]팀은 AppName으로
     <strong>4.5시간</strong>을 절약했습니다.</p>
  <ul>
    <li>완료한 작업: 47개</li>
    <li>자동화된 리포트: 3개</li>
    <li>팀 협업 시간: 12시간</li>
  </ul>
  <!-- CTA: 하나만, 눈에 띄게 -->
  <a href="https://app.example.com/dashboard"
     style="background: #2563EB; color: white;
            padding: 14px 28px; border-radius: 8px;
            text-decoration: none; display: inline-block;">
    대시보드에서 확인하기
  </a>
  <p style="font-size: 12px; color: #6B7280;">
    이 이메일은 주간 리포트 설정에 의해 발송되었습니다.
    <a href="[unsubscribe_url]">수신 거부</a>
  </p>
</div>
```

DON'T:
```
❌ 과도한 이메일 빈도:
Day 0: Welcome
Day 0: Tutorial 1
Day 1: Tutorial 2
Day 1: Feature highlight
Day 2: Case study
→ 하루 2통 이상 = 스팸 신고 위험, 수신 거부율 급증

❌ 수신 거부 링크 누락:
CAN-SPAM Act / GDPR 위반 → 법적 리스크
모든 마케팅 이메일에 반드시 unsubscribe 링크 포함

❌ 일괄 발송 (개인화 없음):
Subject: "새로운 기능이 출시되었습니다"
Body: "안녕하세요 고객님..."
→ 개인화 이메일 대비 오픈율 26% 낮음 (Campaign Monitor 데이터)

❌ CTA 과다:
"대시보드 보기" + "블로그 읽기" + "팀원 초대" + "업그레이드"
→ 이메일당 CTA 1개. 최대 2개 (primary + secondary)
```

### 핵심 지표
| 지표 | 건강한 수준 | 위험 신호 |
|------|-----------|----------|
| 오픈율 | > 25% | < 15% |
| 클릭률 (CTR) | > 3.5% | < 1% |
| 수신 거부율 | < 0.3% | > 1% |
| 스팸 신고율 | < 0.05% | > 0.1% |
