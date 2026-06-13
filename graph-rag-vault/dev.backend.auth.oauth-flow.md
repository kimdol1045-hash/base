---
id: "dev.backend.auth.oauth-flow"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "auth", "oauth", "social-login"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.auth.oauth-flow

> #116 OWASP A07

OAuth2 Authorization Code + PKCE Flow (소셜 로그인의 보안 표준):

### 흐름 단계
1. 클라이언트 → Authorization URL (state + code_challenge)
2. 사용자 → Provider 로그인 및 동의
3. Provider → Redirect URI (authorization code + state)
4. 서버 → Provider token endpoint (code + code_verifier)
5. Provider → Access Token + ID Token
6. 서버 → 사용자 생성/연동 + 세션 발급

### PKCE + State 구현
```typescript
// DO: PKCE로 code interception 공격 방지, state로 CSRF 방지
import crypto from 'crypto';

function startOAuthFlow(provider: 'google' | 'github') {
  const state = crypto.randomBytes(32).toString('hex');
  const codeVerifier = crypto.randomBytes(32).toString('base64url');
  const codeChallenge = crypto
    .createHash('sha256').update(codeVerifier).digest('base64url');

  // 세션에 state, codeVerifier 저장
  session.set({ state, codeVerifier });

  const params = new URLSearchParams({
    client_id: config[provider].clientId,
    redirect_uri: config[provider].redirectUri,
    response_type: 'code',
    scope: provider === 'google' ? 'openid email profile' : 'user:email',
    state,
    code_challenge: codeChallenge,
    code_challenge_method: 'S256',
  });
  return `${config[provider].authUrl}?${params}`;
}

// 콜백 처리: 기존 계정 연동 포함
async function handleOAuthCallback(code: string, state: string) {
  if (state !== session.get('state')) throw new Error('CSRF detected');
  const tokens = await exchangeCode(code, session.get('codeVerifier'));
  const profile = await fetchUserProfile(tokens.access_token);

  // 이메일로 기존 사용자 검색 → 연동 or 생성
  let user = await db.findByEmail(profile.email);
  if (user) {
    await db.linkProvider(user.id, provider, profile.providerId);
  } else {
    if (!profile.email_verified) throw new Error('Email not verified');
    user = await db.createUser({ email: profile.email, name: profile.name });
    await db.linkProvider(user.id, provider, profile.providerId);
  }
  return generateSession(user);
}
```

DON'T:
```typescript
// ❌ Implicit Flow — 토큰이 URL fragment에 노출
response_type: 'token'  // 절대 사용 금지

// ❌ state 파라미터 없음 — CSRF 공격 가능
// ❌ Provider 이메일을 검증 없이 신뢰
const user = await db.findOrCreate({ email: profile.email }); // email_verified 미확인!

// ❌ PKCE 없이 public client에서 사용 — code interception 가능
```

### Provider 설정 체크리스트
| Provider | Scope | Token URL |
|----------|-------|-----------|
| Google | openid email profile | oauth2.googleapis.com/token |
| GitHub | user:email | github.com/login/oauth/access_token |
| Kakao | account_email profile | kauth.kakao.com/oauth/token |

### 흔한 실수
- redirect_uri를 와일드카드로 설정 (open redirect 취약점)
- 소셜 계정 연동 해제 시 로컬 비밀번호 미설정 확인 누락
- Provider 토큰을 DB에 평문 저장 — 암호화 필수

## Connections

- [[dev.backend.auth.role]] — CO_CREATES (weight: 0.6)
