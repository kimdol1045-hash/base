---
id: "dev.backend.auth.jwt-auth"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "auth", "jwt", "token"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.auth.jwt-auth

> #115 Saltzer Least Privilege

JWT 인증 심화 (Access/Refresh 토큰 이중 구조로 보안과 UX를 동시에 확보한다):

### 토큰 설계
| 토큰 | 만료 | 저장 위치 | 용도 |
|------|------|-----------|------|
| Access Token | 15분 | 메모리 (JS 변수) | API 인가 |
| Refresh Token | 7일 | httpOnly secure cookie | Access 재발급 |

### Access + Refresh 흐름
```typescript
// DO: verify()로 검증, httpOnly cookie에 refresh 저장
import jwt from 'jsonwebtoken';

function generateTokenPair(userId: string, role: string) {
  const accessToken = jwt.sign(
    { sub: userId, role },
    process.env.JWT_ACCESS_SECRET!,
    { expiresIn: '15m', algorithm: 'RS256' }
  );
  const refreshToken = jwt.sign(
    { sub: userId, tokenVersion: 1 },
    process.env.JWT_REFRESH_SECRET!,
    { expiresIn: '7d', algorithm: 'RS256' }
  );
  return { accessToken, refreshToken };
}

// Refresh 엔드포인트: 토큰 회전(rotation) 적용
async function refresh(req: Request, res: Response) {
  const token = req.cookies.refreshToken;
  const payload = jwt.verify(token, process.env.JWT_REFRESH_SECRET!);
  // 블랙리스트 확인 (로그아웃된 토큰 차단)
  if (await redis.get(`blacklist:${token}`)) throw new Error('Revoked');
  // 이전 refresh token 블랙리스트 등록 (rotation)
  await redis.set(`blacklist:${token}`, '1', 'EX', 7 * 86400);
  const pair = generateTokenPair(payload.sub, payload.role);
  res.cookie('refreshToken', pair.refreshToken, {
    httpOnly: true, secure: true, sameSite: 'strict', maxAge: 7 * 86400 * 1000
  });
  return res.json({ accessToken: pair.accessToken });
}
```

DON'T:
```typescript
// ❌ localStorage에 토큰 저장 (XSS 취약)
localStorage.setItem('token', accessToken);

// ❌ decode()만 사용 — 서명 검증 없음
const payload = jwt.decode(token); // 누구나 조작 가능!

// ❌ Refresh rotation 없음 — 탈취 시 7일간 무제한 사용
// ❌ 로그아웃 시 블랙리스트 미등록 — 토큰 여전히 유효
```

### 로그아웃 처리
- Access Token: 짧은 만료로 자연 소멸 (15분)
- Refresh Token: Redis 블랙리스트에 등록 (TTL = 남은 만료 시간)
- Cookie 삭제: `res.clearCookie('refreshToken')`

### 흔한 실수
- HS256 사용 시 secret이 약하면 brute force 가능 → RS256 권장
- JWT payload에 민감 정보(비밀번호, 카드번호) 포함
- Access Token을 30일로 설정 — 탈취 시 피해 기간 과도

## Connections

- [[dev.backend.auth.role]] — CO_CREATES (weight: 0.6)
- [[dev.backend.auth.rbac]] — CO_CREATES (weight: 0.6)
- [[dev.backend.auth.verify]] — CO_CREATES (weight: 0.6)
- [[dev.backend.auth.password]] — CO_CREATES (weight: 0.6)
- [[dev.backend.api.security]] — CO_CREATES (weight: 0.6)
- [[dev.backend.api.payment]] — CO_CREATES (weight: 0.6)
- [[dev.backend.patterns.idempotency]] — CO_CREATES (weight: 0.6)
