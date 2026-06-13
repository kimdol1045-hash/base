---
id: "qa.code-review.security"
domain: "qa"
type: "rule"
bloom_level: ""
tags: ["qa", "code-review", "security", "owasp", "xss", "injection", "idor"]
brain_region: "CEREBELLUM"
token_estimate: 500
---

# qa.code-review.security

> #116 OWASP Top 10 (OWASP Foundation, 2021)

보안 관점 리뷰 체크포인트 (하나의 취약점이 전체 시스템을 무너뜨린다):

### 1. 입력 검증 (Injection Prevention)
모든 외부 입력은 신뢰하지 않는다. 반드시 검증 후 사용한다.

DO:
```typescript
import { z } from 'zod';

// ✅ Zod 스키마로 입력 검증
const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100).trim(),
  age: z.number().int().min(0).max(150),
});

app.post('/api/users', async (req, res) => {
  const parsed = CreateUserSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ errors: parsed.error.flatten() });
  }
  // parsed.data는 안전하게 타입 검증됨
  await createUser(parsed.data);
});
```

DON'T:
```typescript
// ❌ 입력 검증 없이 직접 사용
app.post('/api/users', async (req, res) => {
  await db.query('INSERT INTO users (email, name) VALUES ($1, $2)', [
    req.body.email, // 검증 안 됨 → 빈 문자열, 초장문, 악성 코드 가능
    req.body.name,
  ]);
});
```

### 2. SQL Injection
문자열 연결로 쿼리를 만들지 않는다.

```typescript
// ❌ 문자열 연결 → Injection
const query = `SELECT * FROM users WHERE name = '${name}'`;

// ✅ Parameterized query
const query = 'SELECT * FROM users WHERE name = $1';
await db.query(query, [name]);

// ✅ ORM 사용 (Prisma)
const user = await prisma.user.findFirst({ where: { name } });
```

### 3. XSS (Cross-Site Scripting)
사용자 입력을 렌더링할 때 반드시 이스케이핑한다.

```typescript
// ❌ dangerouslySetInnerHTML → XSS 취약
<div dangerouslySetInnerHTML={{ __html: userComment }} />

// ✅ React는 기본적으로 이스케이핑 (JSX 사용 시 안전)
<div>{userComment}</div>

// ✅ HTML이 필요하면 sanitizer 적용
import DOMPurify from 'dompurify';
<div dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(userComment) }} />
```

### 4. 인증/인가 (Authentication/Authorization)
모든 비공개 엔드포인트에 인증 미들웨어를 적용한다.

```typescript
// ❌ 인증 없는 API → 누구나 접근 가능
app.get('/api/admin/users', async (req, res) => { ... });

// ✅ 인증 + 인가 미들웨어
app.get('/api/admin/users',
  requireAuth,          // 로그인 확인
  requireRole('admin'), // 관리자 권한 확인
  async (req, res) => { ... }
);
```

### 5. IDOR (Insecure Direct Object Reference)
다른 사용자의 데이터에 접근할 수 없도록 소유자 검증을 한다.

```typescript
// ❌ IDOR: URL의 id만으로 조회 → 다른 사용자 데이터 접근 가능
app.get('/api/orders/:id', async (req, res) => {
  const order = await db.query('SELECT * FROM orders WHERE id = $1', [req.params.id]);
  res.json(order);
});

// ✅ 소유자 검증 추가
app.get('/api/orders/:id', requireAuth, async (req, res) => {
  const order = await db.query(
    'SELECT * FROM orders WHERE id = $1 AND user_id = $2',
    [req.params.id, req.user.id]
  );
  if (!order) return res.status(404).json({ error: 'Not found' });
  res.json(order);
});
```

### 6. 민감 정보 노출
```typescript
// ❌ 로그에 비밀번호/토큰 노출
console.log('Login attempt:', { email, password });
console.log('API response:', { token: user.accessToken });

// ✅ 민감 정보 마스킹
console.log('Login attempt:', { email, password: '***' });

// ❌ API 응답에 불필요한 내부 정보
res.json({ user, passwordHash: user.password_hash, internalId: user._id });

// ✅ 필요한 필드만 응답
const { id, email, name } = user;
res.json({ id, email, name });
```

### 7. 의존성 보안
```bash
# 정기적으로 취약점 검사
npm audit
npx audit-ci --critical

# GitHub Dependabot 활성화 필수
```

### 흔한 실수
- "내부 API니까 인증 필요 없다" → 내부 네트워크도 침해 가능
- JWT를 localStorage에 저장 → XSS 시 토큰 탈취 (httpOnly 쿠키 사용)
- CORS에 `origin: '*'` → 모든 도메인에서 API 호출 가능
- 에러 메시지에 스택 트레이스 노출 → 프로덕션에서는 일반적 메시지만

## Connections

- [[qa.code-review.role]] — REQUIRES (weight: 0.9)
- [[qa.test-gen.role]] — REQUIRES (weight: 0.9)
- [[qa.code-review.verify]] — FEEDS (weight: 0.8)
- [[qa.test-gen.verify]] — FEEDS (weight: 0.8)
- [[qa.code-review.readability]] — FEEDS (weight: 0.7)
- [[qa.test-gen.integration]] — FEEDS (weight: 0.7)
- [[qa.code-review.bug-analysis]] — FEEDS (weight: 0.7)
