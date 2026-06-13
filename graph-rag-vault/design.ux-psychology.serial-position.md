---
id: "design.ux-psychology.serial-position"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ux", "serial-position", "primacy", "recency", "navigation", "tab-bar", "menu"]
brain_region: "CORTEX"
token_estimate: 500
---

# design.ux-psychology.serial-position

> #47 직렬 위치 효과 (Murdock, 1962)

직렬 위치 효과 — 목록에서 첫 번째(초두 효과)와 마지막(최신 효과) 항목이 가장 잘 기억된다.
중간 항목은 기억 확률이 가장 낮다.

### 핵심 원칙
- **핵심 기능/메뉴**를 첫 번째와 마지막에 배치
- 덜 중요한 항목은 중간에 배치
- 탭바: 홈(첫째) + 프로필/CTA(마지막)
- 리스트/카드: 가장 중요한 정보를 상단과 하단에

### 1. 모바일 탭바 — 핵심 기능을 양 끝에

```tsx
{/* 홈(초두) ... 프로필(최신) — 가장 많이 쓰는 기능이 양 끝 */}
<nav className="fixed bottom-0 inset-x-0 bg-background border-t
                flex justify-around h-16 pb-safe">
  {/* 1st: 홈 — 초두 효과 (Primacy) */}
  <TabBarItem icon={Home} label="홈" href="/" active />
  {/* 2nd~4th: 중간 — 기억률 낮은 위치 */}
  <TabBarItem icon={Search} label="탐색" href="/explore" />
  <TabBarItem icon={PlusCircle} label="작성" href="/create" />
  <TabBarItem icon={Bell} label="알림" href="/notifications" />
  {/* 5th: 프로필 — 최신 효과 (Recency) */}
  <TabBarItem icon={User} label="내 정보" href="/profile" />
</nav>
```

### 2. 기능 소개 리스트 — 핵심 가치를 처음/마지막

```tsx
{/* 랜딩 페이지: 첫/마지막 feature가 가장 기억에 남는다 */}
<div className="space-y-12">
  {/* 1st — 초두: 가장 강력한 USP */}
  <FeatureSection
    icon={<Zap className="h-8 w-8 text-primary" />}
    title="10배 빠른 배포"
    description="원클릭 배포로 개발 시간을 90% 단축합니다."
  />
  {/* 중간: 보조 기능들 */}
  <FeatureSection
    icon={<Shield className="h-8 w-8 text-muted-foreground" />}
    title="엔터프라이즈 보안"
    description="SOC2, GDPR 인증 완료."
  />
  <FeatureSection
    icon={<Users className="h-8 w-8 text-muted-foreground" />}
    title="실시간 협업"
    description="팀원과 동시 편집 가능."
  />
  {/* Last — 최신: 행동 유도 메시지 */}
  <FeatureSection
    icon={<Sparkles className="h-8 w-8 text-primary" />}
    title="지금 무료로 시작하세요"
    description="신용카드 없이 14일 무료 체험."
    cta={<Button size="lg">무료 시작</Button>}
  />
</div>
```

### 3. 드롭다운 메뉴 — 자주 쓰는 액션을 위/아래

```tsx
<DropdownMenuContent>
  {/* 첫 번째: 가장 자주 쓰는 액션 */}
  <DropdownMenuItem><Edit className="mr-2 h-4 w-4" />편집</DropdownMenuItem>
  <DropdownMenuItem><Copy className="mr-2 h-4 w-4" />복제</DropdownMenuItem>
  <DropdownMenuSeparator />
  {/* 중간: 덜 빈번한 액션 */}
  <DropdownMenuItem><Archive className="mr-2 h-4 w-4" />보관</DropdownMenuItem>
  <DropdownMenuItem><Download className="mr-2 h-4 w-4" />내보내기</DropdownMenuItem>
  <DropdownMenuSeparator />
  {/* 마지막: 명확한 구분이 필요한 위험 액션 */}
  <DropdownMenuItem className="text-destructive">
    <Trash className="mr-2 h-4 w-4" />삭제
  </DropdownMenuItem>
</DropdownMenuContent>
```

### 적용 가이드
| UI 요소 | 첫 번째 (초두) | 마지막 (최신) |
|---------|---------------|--------------|
| 탭바 | 홈 / 핵심 기능 | 프로필 / 설정 |
| 랜딩 feature | 최대 USP | CTA / 전환 유도 |
| 메뉴 | 가장 빈번한 액션 | 위험/구분 액션 |
| 카드 리스트 | 추천/인기 항목 | 최신 항목 |

## Connections

- [[design.ux-psychology.role]] — REQUIRES (weight: 0.9)
- [[design.ux-psychology.verify]] — FEEDS (weight: 0.8)
- [[design.ux-psychology.von-restorff]] — FEEDS (weight: 0.7)
- [[design.ux-psychology.aesthetic-usability]] — FEEDS (weight: 0.7)
