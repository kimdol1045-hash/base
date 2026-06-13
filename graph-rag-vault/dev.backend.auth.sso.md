---
id: "dev.backend.auth.sso"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["auth", "sso", "oidc", "saml", "enterprise"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.auth.sso

> #226 SSO/SAML/OIDC (OASIS SAML 2.0, 2005; OpenID Connect Core 1.0, 2014)

# SSO (Single Sign-On) 구현 가이드

## 핵심 원칙
- 사용자가 한 번의 인증으로 여러 서비스에 접근할 수 있도록 한다
- OIDC(OpenID Connect)를 기본 프로토콜로 사용한다
- 엔터프라이즈 고객은 SAML 2.0 지원이 필요할 수 있다
- IdP(Identity Provider)에서 인증을 처리하고, SP(Service Provider)에서 인가를 처리한다

## DO
- OIDC Authorization Code Flow + PKCE를 사용한다
- state 파라미터로 CSRF를 방지한다
- nonce 파라미터로 ID 토큰 재사용 공격을 방지한다
- 사용자 프로비저닝(SCIM)을 지원한다
- IdP 메타데이터를 자동 갱신한다

## DON'T
- Implicit Flow를 사용하지 않는다 (Authorization Code Flow + PKCE 사용)
- IdP에서 받은 클레임을 검증 없이 신뢰하지 않는다
- SSO 로그아웃(Single Logout)을 구현하지 않고 방치하지 않는다
- 모든 사용자 정보를 토큰에 넣지 않는다 (필요시 UserInfo 엔드포인트 조회)

## 코드 예시
```typescript
import { Issuer, generators } from "openid-client";

// OIDC 클라이언트 설정
async function createOidcClient(issuerUrl: string) {
  const issuer = await Issuer.discover(issuerUrl);
  return new issuer.Client({
    client_id: process.env.OIDC_CLIENT_ID!,
    client_secret: process.env.OIDC_CLIENT_SECRET!,
    redirect_uris: [`${APP_URL}/auth/callback`],
    response_types: ["code"],
  });
}

// 로그인 시작
app.get("/auth/login", async (req, res) => {
  const codeVerifier = generators.codeVerifier();
  const codeChallenge = generators.codeChallenge(codeVerifier);
  const state = generators.state();
  const nonce = generators.nonce();

  // 세션에 저장 (콜백에서 검증용)
  req.session.oidc = { codeVerifier, state, nonce };

  const authUrl = client.authorizationUrl({
    scope: "openid email profile",
    state,
    nonce,
    code_challenge: codeChallenge,
    code_challenge_method: "S256",
  });

  res.redirect(authUrl);
});

// 콜백 처리
app.get("/auth/callback", async (req, res) => {
  const { codeVerifier, state, nonce } = req.session.oidc!;
  const params = client.callbackParams(req);

  const tokenSet = await client.callback(
    `${APP_URL}/auth/callback`,
    params,
    { code_verifier: codeVerifier, state, nonce },
  );

  const userInfo = await client.userinfo(tokenSet.access_token!);
  const user = await findOrCreateUser(userInfo);
  req.session.userId = user.id;
  res.redirect("/dashboard");
});
```
