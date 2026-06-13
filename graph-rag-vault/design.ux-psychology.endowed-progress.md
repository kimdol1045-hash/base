---
id: "design.ux-psychology.endowed-progress"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ux", "endowed-progress", "onboarding"]
brain_region: "CORTEX"
token_estimate: 380
---

# design.ux-psychology.endowed-progress

> #51 Endowed Progress Effect (Nunes & Drèze, 2006)

진행 기부 효과 (이미 시작된 것처럼 보여주면 완료 동기가 높아진다):

### 실험 결과
- A: 빈 카드 8칸 스탬프 → 완료율 19%
- B: 10칸 카드 중 2칸 이미 찍힘 → 완료율 34%
- 실제 필요 스탬프 수는 같지만 B가 80% 더 높은 완료율

### UX 적용
1. **온보딩**: "1/5 완료" 대신 "3/7 완료" (계정 생성+이메일 인증 이미 카운트)
2. **프로필**: "프로필 20% 완성됨!" (이름/이메일 자동 포함)
3. **로열티**: "첫 구매 보너스 포인트 포함! 3/10 적립 완료"
4. **코스**: "기초 레벨 통과! 중급 2/8 진행 중"

### 구현 패턴
```tsx
const totalSteps = 7;
const preFilledSteps = 2; // 자동 완료 단계
const userSteps = 1; // 사용자가 완료한 단계
const progress = ((preFilledSteps + userSteps) / totalSteps) * 100;

<div>
  <p className="text-sm font-medium">{preFilledSteps + userSteps}/{totalSteps} 완료</p>
  <Progress value={progress} />
</div>
```

### 주의
- 과도한 부풀리기는 역효과 (신뢰 상실)
- 기부된 진행이 합리적으로 설명 가능해야 함

## Connections

- [[design.ux-psychology.zeigarnik]] — CO_CREATES (weight: 0.6)
- [[marketing.persuasion.hook-model]] — FEEDS (weight: 0.5)
