---
id: "dev.backend.auth.mfa"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "auth", "mfa", "totp", "webauthn", "security"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.auth.mfa

> #114 Swiss Cheese Model (Defense in Depth)

다중 인증 MFA (비밀번호 탈취만으로 계정 침해를 막는 추가 인증 계층):

### MFA 방식 비교
| 방식 | 보안 수준 | UX | 권장 |
|------|-----------|-----|------|
| TOTP (앱) | ★★★★ | 보통 | ✅ 기본 |
| WebAuthn/Passkey | ★★★★★ | 좋음 | ✅ 최우선 |
| SMS OTP | ★★ | 좋음 | ⚠️ SIM swap 위험 |
| 이메일 OTP | ★★ | 보통 | ⚠️ 이메일 탈취 시 무력화 |
| 백업 코드 | ★★★ | — | ✅ 복구용 필수 |

### TOTP 설정 및 검증
```typescript
// DO: TOTP 비밀키 생성, QR 코드, 검증
import speakeasy from 'speakeasy';
import QRCode from 'qrcode';

// 1. TOTP 설정 (사용자가 MFA 활성화 시)
async function setupTOTP(userId: string) {
  const secret = speakeasy.generateSecret({
    name: `MyApp:${userId}`,
    issuer: 'MyApp',
    length: 32,
  });
  // 임시 저장 (사용자 확인 전까지 pending 상태)
  await db.savePendingMFA(userId, {
    secret: encrypt(secret.base32),  // 암호화 저장!
    type: 'totp',
  });
  const qrUrl = await QRCode.toDataURL(secret.otpauth_url!);
  return { qrUrl, manualKey: secret.base32 };
}

// 2. TOTP 검증 (로그인 2단계)
async function verifyTOTP(userId: string, code: string): Promise<boolean> {
  const mfa = await db.getMFA(userId);
  const secret = decrypt(mfa.secret);
  return speakeasy.totp.verify({
    secret, encoding: 'base32', token: code,
    window: 1,  // ±30초 허용 (총 90초 창)
  });
}
```

### 백업 코드 관리
```typescript
// DO: 10개 백업 코드 생성, 해싱 저장
import crypto from 'crypto';
import argon2 from 'argon2';

async function generateBackupCodes(userId: string): Promise<string[]> {
  const codes: string[] = [];
  const hashedCodes: string[] = [];
  for (let i = 0; i < 10; i++) {
    const code = crypto.randomBytes(4).toString('hex'); // 8자 hex
    codes.push(code);
    hashedCodes.push(await argon2.hash(code));
  }
  await db.saveBackupCodes(userId, hashedCodes);
  return codes; // 평문은 이때 한 번만 사용자에게 표시!
}

async function useBackupCode(userId: string, code: string): Promise<boolean> {
  const stored = await db.getBackupCodes(userId);
  for (let i = 0; i < stored.length; i++) {
    if (await argon2.verify(stored[i], code)) {
      stored.splice(i, 1); // 사용한 코드 삭제 (일회용)
      await db.saveBackupCodes(userId, stored);
      return true;
    }
  }
  return false;
}
```

DON'T:
```typescript
// ❌ SMS만 사용 — SIM swap 공격에 취약
await sendSMS(user.phone, `Your code is ${otp}`); // 유일한 MFA 수단

// ❌ 백업 코드 평문 저장
await db.saveBackupCodes(userId, plainCodes); // DB 유출 시 즉시 악용

// ❌ TOTP 시도 횟수 제한 없음 — brute force (6자리 = 100만 가지)
// ❌ MFA 비밀키 암호화 없이 DB 저장
```

### Rate Limiting 기준
- TOTP 검증: 5회 실패 시 15분 잠금
- 백업 코드: 3회 실패 시 30분 잠금
- MFA 설정 변경: 비밀번호 재확인 필수

### 흔한 실수
- MFA 설정 활성화 시 검증 코드 확인 없이 바로 적용
- 백업 코드 소진 시 복구 방법 미제공
- TOTP secret을 로그에 기록

## Connections

- [[dev.backend.auth.role]] — CO_CREATES (weight: 0.6)
