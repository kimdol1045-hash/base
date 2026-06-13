---
id: "qa.code-review.priority"
domain: "qa"
type: "rule"
region: EGO
token_estimate: 500
theory: "#121 테스트 피라미드 (Cohn, 2009)"
tags: [qa, code-review, priority, severity, triage]
---

# qa.code-review.priority

> **Region**: 🔵 [[EGO]]  
> **Domain**: `qa`  
> **Type**: `rule`  
> **Theory**: #121 테스트 피라미드 (Cohn, 2009)  
> **Tokens**: 500

## Content

리뷰 우선순위 기준 (가장 위험한 이슈부터 잡아야 한다):

### 심각도 분류

**[Critical] 보안 취약점 — 즉시 수정, 배포 차단**
OWASP Top 10 기준. 데이터 유출/파괴 가능성 있는 이슈.

DO (발견 시 반드시 지적):
```typescript
// ❌ Critical: SQL Injection
const user = await db.query(`SELECT * FROM users WHERE email = '${email}'`);

// ❌ Critical: 하드코딩된 시크릿
const API_KEY = '<hardcoded-api-key>';

// ❌ Critical: 인증 없는 관리자 API
app.delete('/api/admin/users/:id', async (req, res) => {
  await db.query('DELETE FROM users WHERE id = $1', [req.params.id]);
});
```

**[High] 버그/논리 오류 — 반드시 수정**
런타임 크래시, 데이터 손실, 잘못된 비즈니스 로직.

```typescript
// ❌ High: null 체크 누락 → TypeError 크래시
const userName = user.profile.name.toUpperCase();
// ✅ 수정
const userName = user?.profile?.name?.toUpperCase() ?? 'Unknown';

// ❌ High: 비동기 에러 미처리 → 서버 크래시
app.get('/api/users', async (req, res) => {
  const users = await getUsers(); // throw 시 unhandled rejection
  res.json(users);
});
// ✅ 수정: try-catch 또는 에러 핸들링 미들웨어
app.get('/api/users', async (req, res, next) => {
  try {
    const users = await getUsers();
    res.json(users);
  } catch (error) {
    next(error);
  }
});
```

**[Medium] 성능 이슈 — 수정 권장**
N+1 쿼리, 불필요한 리렌더링, 메모리 누수, O(n^2) 알고리즘.

```typescript
// ❌ Medium: 컴포넌트 내 매 렌더마다 새 배열 생성
function UserList({ users }: { users: User[] }) {
  const sorted = users.sort((a, b) => a.name.localeCompare(b.name)); // 원본 mutate + 매번 정렬
  return sorted.map(u => <UserCard key={u.id} user={u} />);
}
// ✅ useMemo로 메모이제이션
function UserList({ users }: { users: User[] }) {
  const sorted = useMemo(
    () => [...users].sort((a, b) => a.name.localeCompare(b.name)),
    [users]
  );
  return sorted.map(u => <UserCard key={u.id} user={u} />);
}
```

**[Low] 코드 스타일/가독성 — 선택적 수정**
네이밍 개선, 불필요한 코드, 더 나은 패턴 존재.

```typescript
// ❌ Low: 의미 불명확한 변수명
const d = new Date();
const x = users.filter(u => u.a);
// ✅ 명확한 이름
const currentDate = new Date();
const activeUsers = users.filter(user => user.isActive);
```

**[Info] 개선 제안 — 참고 사항**
리팩토링 기회, 새로운 API/패턴 안내, 문서화 제안.

### 심각도별 행동 기준
| 심각도 | 행동 | PR 머지 |
|--------|------|---------|
| Critical | 즉시 수정 필수 | 차단 |
| High | 반드시 수정 | 차단 |
| Medium | 수정 권장 (이번 또는 다음 PR) | 허용 (조건부) |
| Low | 선택적 수정 | 허용 |
| Info | 참고만 | 허용 |

### 흔한 실수
- 스타일 이슈를 Critical로 분류 → 리뷰어 신뢰 하락
- 보안 이슈를 Low로 분류 → 심각한 사고 위험
- 모든 이슈를 Medium으로 분류 → 우선순위 무의미화

## Connections

### REQUIRES (2)

- ← [[qa.code-review.role]] `w=0.9`
- ← [[qa.test-gen.role]] `w=0.9`

### FEEDS (7)

- → [[qa.code-review.readability]] `w=0.7`
- → [[qa.code-review.verify]] `w=0.8`
- → [[qa.test-gen.component-test]] `w=0.5`
- → [[qa.test-gen.integration]] `w=0.5`
- → [[qa.test-gen.role]] `w=0.5`
- → [[qa.test-gen.unit]] `w=0.5`
- → [[qa.test-gen.verify]] `w=0.8`

### CO_CREATES (2)

- → [[qa.code-review.performance]] `w=0.6`
- ← [[qa.code-review.role]] `w=0.6`
