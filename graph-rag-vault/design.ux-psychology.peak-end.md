---
id: "design.ux-psychology.peak-end"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ux", "peak-end", "experience"]
brain_region: "CORTEX"
token_estimate: 380
---

# design.ux-psychology.peak-end

> #49 Peak-End Rule (Kahneman et al., 1993)

피크엔드 규칙 (경험의 최고점과 마지막 순간이 전체 평가를 결정한다):

### UX 적용

**피크 순간 강화:**
- 핵심 성공 인터랙션에 마이크로 애니메이션:
  결제 완료 → confetti, 목표 달성 → 축하 모션
- 예상치 못한 즐거움(Delight): 이스터에그, 유머러스한 에러 메시지
- "와!" 순간 설계: 첫 데이터 로딩 완료, 첫 수익 발생

**마지막 순간 강화:**
```tsx
// 결제 완료 페이지 — 마지막 인상이 전체 경험을 좌우
<div className="flex flex-col items-center gap-6 py-12">
  <CheckCircle className="h-16 w-16 text-green-500 animate-bounce" />
  <h1 className="text-2xl font-bold">주문 완료!</h1>
  <p className="text-muted-foreground">3일 내 배송됩니다</p>
  <div className="rounded-lg bg-muted p-4 text-center">
    <p className="text-sm">주문번호: #A12345</p>
  </div>
  <Button variant="outline">주문 상세 보기</Button>
</div>
```

**나쁜 끝 방지:**
- 에러 메시지를 친절하게 (기술 코드 ❌ → 안내 메시지 ✅)
- 로그아웃 시 따뜻한 인사 "다음에 또 만나요"
- 구독 해지 시 협박 금지, 깔끔한 프로세스

## Connections

- [[design.ux-psychology.role]] — REQUIRES (weight: 0.9)
- [[design.ux-psychology.verify]] — FEEDS (weight: 0.8)
- [[design.ux-psychology.jakobs-law]] — FEEDS (weight: 0.7)
- [[design.ux-psychology.von-restorff]] — FEEDS (weight: 0.7)
