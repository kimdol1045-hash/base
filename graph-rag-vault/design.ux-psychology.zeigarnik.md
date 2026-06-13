---
id: "design.ux-psychology.zeigarnik"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ux", "zeigarnik", "engagement"]
brain_region: "CORTEX"
token_estimate: 380
---

# design.ux-psychology.zeigarnik

> #48 Zeigarnik Effect (Zeigarnik, 1927)

자이가르닉 효과 (미완료 작업이 완료된 작업보다 더 기억에 남는다):

### UX 적용
1. **프로그레스 바**: 완료까지 남은 정도를 시각화
   ```tsx
   <div className="space-y-2">
     <div className="flex justify-between text-sm">
       <span>프로필 완성도</span>
       <span className="text-muted-foreground">3/5 완료</span>
     </div>
     <Progress value={60} className="h-2" />
     <p className="text-xs text-muted-foreground">
       사진을 추가하면 매칭률이 40% 올라갑니다
     </p>
   </div>
   ```

2. **온보딩 체크리스트**: 완료한 것 + 남은 것 동시 표시
   ```tsx
   <ul className="space-y-2">
     <li className="flex items-center gap-2 text-muted-foreground line-through">
       <CheckCircle className="h-4 w-4" /> 계정 생성
     </li>
     <li className="flex items-center gap-2 font-medium">
       <Circle className="h-4 w-4" /> 프로필 사진 추가
     </li>
     <li className="flex items-center gap-2 text-muted-foreground">
       <Circle className="h-4 w-4" /> 첫 프로젝트 생성
     </li>
   </ul>
   ```

3. **스트릭(Streak)**: 연속 일수 표시로 중단 저항
4. **저장 알림**: "작성 중인 글이 있습니다" 리마인더

### 주의: 과도한 활용 금지
- 의무적 느낌 → 스트레스 → 이탈
- 달성 불가능한 목표 → 포기

## Connections

- [[design.ux-psychology.endowed-progress]] — CO_CREATES (weight: 0.6)
- [[marketing.persuasion.hook-model]] — FEEDS (weight: 0.5)
