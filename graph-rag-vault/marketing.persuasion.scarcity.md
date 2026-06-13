---
id: "marketing.persuasion.scarcity"
domain: "marketing"
type: "pattern"
bloom_level: ""
tags: ["marketing", "persuasion", "scarcity", "urgency", "countdown", "conversion"]
brain_region: "SENSORS"
token_estimate: 480
---

# marketing.persuasion.scarcity

> #63 희소성 (Cialdini, 1984 Ch.7)

희소성 — 제한된 것은 더 가치 있게 느껴진다 (구할 수 없는 것을 더 원한다):

### 희소성 3가지 유형

**1. 수량 한정 (Limited Quantity)**
- "선착순 100명 한정"
- "남은 좌석: 7석"
- "재고 3개 남음"
- 실시간 재고 카운터로 긴급감 극대화

**2. 시간 한정 (Limited Time)**
- "오늘 자정까지만"
- "얼리버드 할인 D-3"
- 카운트다운 타이머 표시
```
┌─────────────────────────────────┐
│  얼리버드 할인 종료까지           │
│  02일 14시간 37분 22초           │
│  [지금 등록하기 — ₩990,000]     │
└─────────────────────────────────┘
```

**3. 접근 한정 (Limited Access)**
- "초대 코드가 있는 분만"
- "프리미엄 회원 전용"
- "베타 테스터 500명 모집"
- 대기 리스트: "현재 3,421명 대기 중. 지금 등록하면 3,422번째"

### 카피 예시
- "이번 기수 마감까지 남은 자리: 12석 / 50석"
- "이 할인가는 오늘 가입하는 분에게만 적용됩니다"
- "지난 프로모션은 2시간 만에 마감되었습니다"
- "현재 487명이 이 상품을 보고 있습니다"
- "오늘 구매하면 한정판 보너스 키트 증정"
- "무료 체험은 이번 달까지만 제공됩니다"

### 카운트다운 타이머 구현 (React)
```tsx
function CountdownTimer({ deadline }: { deadline: Date }) {
  const [timeLeft, setTimeLeft] = useState(getTimeLeft(deadline));

  useEffect(() => {
    const timer = setInterval(() => {
      const remaining = getTimeLeft(deadline);
      if (remaining.total <= 0) {
        clearInterval(timer);
        setTimeLeft({ days: 0, hours: 0, minutes: 0, seconds: 0, total: 0 });
        return;
      }
      setTimeLeft(remaining);
    }, 1000);
    return () => clearInterval(timer);
  }, [deadline]);

  return (
    <div className="flex gap-2 text-center">
      <TimeBlock value={timeLeft.days} label="일" />
      <TimeBlock value={timeLeft.hours} label="시간" />
      <TimeBlock value={timeLeft.minutes} label="분" />
      <TimeBlock value={timeLeft.seconds} label="초" />
    </div>
  );
}
```

### 윤리적 주의점
| 허용 | 금지 |
|------|------|
| 실제 한정 수량 표시 | 가짜 재고 카운터 (항상 "3개 남음") |
| 실제 마감 기한 카운트다운 | 리셋되는 가짜 타이머 |
| 시즌 한정 프로모션 | "마지막 기회"를 반복 사용 |
| 대기 리스트 실제 순번 | 조작된 대기자 수 |
| 재고 연동 실시간 표시 | 인위적으로 재고를 줄여 표시 |

### 효과 극대화 조건
- 희소성 + 사회적 증거: "487명이 보고 있고 재고 3개" (경쟁 심리)
- 희소성 + 손실 회피: "오늘 놓치면 ₩50,000 할인이 사라집니다"
- 구체적 숫자일수록 신뢰도 상승: "한정" < "100명 한정" < "남은 7자리"

## Connections

- [[marketing.persuasion.role]] — REQUIRES (weight: 0.9)
- [[marketing.persuasion.verify]] — FEEDS (weight: 0.8)
- [[marketing.persuasion.authority]] — FEEDS (weight: 0.7)
- [[marketing.persuasion.fogg-model]] — CO_CREATES (weight: 0.6)
- [[marketing.persuasion.anchoring]] — CO_CREATES (weight: 0.6)
- [[marketing.persuasion.endowment]] — CO_CREATES (weight: 0.6)
- [[marketing.persuasion.prospect-theory]] — CO_CREATES (weight: 0.6)
- [[marketing.copy.cta]] — FEEDS (weight: 0.5)
