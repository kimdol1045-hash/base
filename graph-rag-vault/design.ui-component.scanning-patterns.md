---
id: "design.ui-component.scanning-patterns"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ui", "f-pattern", "z-pattern", "scanning"]
brain_region: "CORTEX"
token_estimate: 400
---

# design.ui-component.scanning-patterns

> #159 F-Pattern & Z-Pattern (Nielsen Norman Group, 2006)

시선 스캔 패턴 (사용자의 자연스러운 시선 흐름에 맞춰 배치한다):

### F-Pattern (텍스트 중심 페이지)
```
████████████████     ← 상단 수평 스캔
████████████████
██████████           ← 두 번째 수평 (더 짧음)
██████████
████                 ← 좌측 수직 스캔
████
████
```
**적용:** 블로그, 검색 결과, 기사 목록
- 핵심 정보를 좌측 상단에 배치
- 중요 키워드를 각 문단 첫 2단어에
- 소제목으로 스캔 포인트 제공

### Z-Pattern (비주얼 중심 페이지)
```
① ─────────── ②
              ╱
            ╱
③ ─────────── ④
```
**적용:** 랜딩페이지, 히어로 섹션, 대시보드
- ① 로고/네비게이션
- ② CTA 또는 핵심 메시지
- ③ 부가 정보/이미지
- ④ 최종 CTA (가입, 구매)

### 구텐베르크 다이어그램 (균일 콘텐츠)
```
[Primary]  [Strong]
[Weak]     [Terminal]
```
- CTA는 Terminal Area (우하단)에 배치
- 적용: 폼, 다이얼로그, 카드

### 실무 규칙
- Above the fold: 핵심 가치 제안 + CTA
- 좌측 정렬 텍스트 (우측 정렬은 스캔 방해)
- 시선 흐름을 끊는 요소 제거 (자동 재생 영상, 팝업)
- 시각적 앵커 (이미지, 아이콘)로 시선 유도
