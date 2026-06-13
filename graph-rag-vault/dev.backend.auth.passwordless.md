---
id: "dev.backend.auth.passwordless"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["auth", "passwordless", "webauthn", "magic-link"]
brain_region: "BRAINSTEM"
token_estimate: 420
---

# dev.backend.auth.passwordless

> #227 Passwordless Authentication (WebAuthn W3C Spec, 2021; FIDO2)

# Passwordless 인증 가이드

## 핵심 원칙
- 비밀번호 없이 인증하여 피싱, 재사용 공격 위험을 제거한다
- Magic Link, OTP, WebAuthn(FIDO2) 방식 중 적합한 것을 선택한다
- 인증 수단의 보안 강도와 사용자 경험을 균형 있게 고려한다
- 복구 수단(Recovery)을 반드시 제공한다

## 주요 방식
| 방식 | 보안 강도 | UX | 적합한 경우 |
|------|-----------|-----|-------------|
| Magic Link | 중 | 좋음 | 이메일 기반 서비스 |
| SMS/Email OTP | 중 | 보통 | 간단한 인증 |
| WebAuthn/Passkey | 높음 | 좋음 | 높은 보안 요구 |

## DO
- Magic Link에 짧은 만료시간(15분)을 설정한다
- 일회용 토큰을 사용하고, 사용 후 즉시 무효화한다
- WebAuthn에서 챌린지를 서버에서 생성하고 검증한다
- Rate Limiting을 적용하여 OTP 브루트포스를 방지한다

## DON'T
- Magic Link 토큰을 예측 가능하게 생성하지 않는다
- 인증 토큰을 URL에 포함할 때 로그에 기록되지 않도록 한다
- OTP 길이를 4자리 미만으로 하지 않는다 (최소 6자리)
- 복구 수단 없이 Passwordless만 제공하지 않는다

## 코드 예시
```typescript
import { randomBytes } from "crypto";

// Magic Link 생성 및 전송
async function sendMagicLink(email: string) {
  const token = randomBytes(32).toString("base64url");
  const expiresAt = new Date(Date.now() + 15 * 60_000); // 15분

  await db.magicLinks.create({
    email,
    tokenHash: hashToken(token),
    expiresAt,
    usedAt: null,
  });

  const link = `${APP_URL}/auth/verify?token=${token}&email=${email}`;
  await emailService.send({
    to: email,
    subject: "로그인 링크",
    html: `<a href="${link}">로그인하기</a> (15분 이내 유효)`,
  });
}

// Magic Link 검증
app.get("/auth/verify", async (req, res) => {
  const { token, email } = req.query;
  const tokenHash = hashToken(token as string);

  const record = await db.magicLinks.findFirst({
    where: {
      email: email as string,
      tokenHash,
      usedAt: null,
      expiresAt: { gt: new Date() },
    },
  });

  if (!record) {
    return res.status(401).json({ error: "링크가 만료되었거나 유효하지 않습니다" });
  }

  await db.magicLinks.update({
    where: { id: record.id },
    data: { usedAt: new Date() },
  });

  const user = await findOrCreateUser(email as string);
  const session = await createSession(user.id);
  res.cookie("session", session.token, { httpOnly: true, secure: true });
  res.redirect("/dashboard");
});
```
