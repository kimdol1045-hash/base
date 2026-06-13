---
id: "design.ux-psychology.cognitive-load"
domain: "design.ux-psychology"
type: "rule"
bloom_level: ""
tags: ["design", "ux", "cognitive-load", "psychology"]
brain_region: "LIMBIC"
token_estimate: 400
---

# design.ux-psychology.cognitive-load

> #158 Cognitive Load Theory (John Sweller, 1988)

인지 부하 이론 (사용자의 정보 처리 한계를 고려하여 설계한다):

### 3가지 인지 부하
| 유형 | 설명 | UI 예시 |
|------|------|---------|
| Intrinsic | 과제 자체의 복잡성 | 결제 폼의 필수 입력 필드 |
| Extraneous | 불필요한 정보 처리 | 산만한 레이아웃, 불필요한 애니메이션 |
| Germane | 학습/이해에 도움 | 단계 표시, 도움말 툴팁 |

→ 목표: Extraneous ↓, Germane ↑, Intrinsic 은 분할

### 실무 적용 규칙
**정보량 줄이기:**
- 한 화면에 1가지 주요 작업만
- 선택지 5개 이하 (밀러의 법칙 7±2와 연계)
- Progressive Disclosure: 처음엔 핵심만, 필요 시 확장

**구조화하기:**
- 관련 정보 그룹핑 (Chunking)
- 시각적 위계 명확히 (제목 > 부제 > 본문)
- 일관된 패턴 (같은 동작은 같은 위치/스타일)

**기억 부담 줄이기:**
- 입력 대신 선택 (드롭다운, 라디오)
- 자동 완성, 기본값 제공
- 이전 단계 정보 요약 표시

### 체크리스트
- [ ] 한 화면에 주요 CTA가 1개인가?
- [ ] 불필요한 시각 요소(장식, 배경 이미지)가 없는가?
- [ ] 복잡한 작업이 단계별로 분리되었는가?
- [ ] 사용자가 기억해야 할 정보가 3개 이하인가?
