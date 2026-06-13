---
id: "dev.backend.auth.session-auth"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "auth", "session", "cookie", "redis"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.auth.session-auth

> #115 Saltzer Least Privilege

세션 기반 인증 (서버 측 상태 관리로 즉시 무효화가 가능한 인증 방식):

### Session vs JWT 비교
| 항목 | Session | JWT |
|------|---------|-----|
| 상태 관리 | 서버 (Redis/DB) | 클라이언트 (stateless) |
| 즉시 무효화 | ✅ 세션 삭제 | ❌ 만료까지 대기 (블랙리스트 필요) |
| 확장성 | Redis 클러스터 필요 | ✅ 서버 무상태 |
| 저장 크기 | 쿠키: session ID만 (~32B) | 쿠키/헤더: 전체 payload (~500B+) |
| CSRF | ⚠️ 쿠키 기반이므로 방어 필요 | ✅ Authorization 헤더 시 불필요 |
| 적합 사례 | SSR, 관리자 패널, 은행 | SPA, 모바일 API, MSA |

### Redis 세션 스토어 구현
```typescript
// DO: Redis 세션 스토어 + 안전한 쿠키 설정
import session from 'express-session';
import RedisStore from 'connect-redis';
import Redis from 'ioredis';

const redis = new Redis({ host: 'localhost', port: 6379 });

app.use(session({
  store: new RedisStore({ client: redis, prefix: 'sess:' }),
  secret: process.env.SESSION_SECRET!,       // 최소 32자 랜덤
  name: '__Host-sid',                         // __Host- 접두사: secure + path=/ 강제
  resave: false,
  saveUninitialized: false,
  rolling: true,                              // 활동 시 만료 갱신
  cookie: {
    httpOnly: true,
    secure: true,                             // HTTPS만
    sameSite: 'strict',
    maxAge: 30 * 60 * 1000,                   // 30분 (비활동 시 만료)
  },
}));

// 로그인 시 세션 재생성 (session fixation 방지)
async function login(req: Request, res: Response) {
  const user = await authenticate(req.body.email, req.body.password);
  req.session.regenerate((err) => {           // 새 session ID 발급!
    req.session.userId = user.id;
    req.session.role = user.role;
    req.session.createdAt = Date.now();
    req.session.save(() => res.json({ success: true }));
  });
}

// 로그아웃: 세션 즉시 파괴
async function logout(req: Request, res: Response) {
  req.session.destroy((err) => {
    res.clearCookie('__Host-sid');
    res.json({ success: true });
  });
}
```

DON'T:
```typescript
// ❌ 메모리 세션 스토어 (프로덕션) — 서버 재시작 시 전체 로그아웃, 메모리 누수
app.use(session({ secret: 'keyboard cat' })); // MemoryStore가 기본값!

// ❌ 로그인 후 세션 재생성 없음 — session fixation 공격 가능
async function login(req: Request, res: Response) {
  req.session.userId = user.id; // 기존 session ID 유지 → 위험
}

// ❌ cookie 이름이 기본값 'connect.sid' — 프레임워크 식별 가능
// ❌ sameSite 미설정 — CSRF 공격에 노출
```

### 세션 보안 강화
- 절대 만료: 로그인 후 24시간이면 활동 여부와 무관하게 재인증
- 동시 세션 제한: 사용자당 최대 5개 세션 허용
- 의심 활동 시 전체 세션 무효화: `redis.del('sess:*:userId')`

### 흔한 실수
- 세션 데이터에 민감 정보(비밀번호) 저장
- Redis 연결 실패 시 fallback으로 MemoryStore 사용
- 세션 만료 후에도 쿠키가 남아있어 혼란 유발

## Connections

- [[dev.backend.auth.role]] — CO_CREATES (weight: 0.6)
