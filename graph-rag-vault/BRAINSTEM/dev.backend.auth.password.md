---
id: "dev.backend.auth.password"
domain: "development.backend"
type: "rule"
region: BRAINSTEM
token_estimate: 500
theory: "#115 Saltzer, #116 OWASP A02"
tags: [backend, auth, password, hashing, security]
---

# dev.backend.auth.password

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `rule`  
> **Theory**: #115 Saltzer, #116 OWASP A02  
> **Tokens**: 500

## Content

비밀번호 해싱, 정책, 리셋 플로우 (안전한 자격증명 관리의 모든 것):

### 해싱 알고리즘 비교
| 알고리즘 | 권장 | 파라미터 | 비고 |
|----------|------|----------|------|
| argon2id | ✅ 최우선 | memory:64MB, iterations:3, parallelism:1 | GPU 공격 저항 |
| bcrypt | ✅ 대안 | cost:12 (최소 10) | 72바이트 제한 |
| scrypt | ⚠️ 가능 | N:2^14, r:8, p:1 | 설정 복잡 |
| SHA256/MD5 | ❌ 금지 | — | 무차별 대입에 취약 |

### 비밀번호 해싱 구현
```typescript
// DO: argon2id 해싱 + timing-safe 비교
import argon2 from 'argon2';
import crypto from 'crypto';

async function hashPassword(password: string): Promise<string> {
  return argon2.hash(password, {
    type: argon2.argon2id,
    memoryCost: 65536,    // 64MB
    timeCost: 3,
    parallelism: 1,
  });
}

async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return argon2.verify(hash, password); // 내부적으로 timing-safe
}
```

### 비밀번호 정책
- 최소 8자, 최대 72자 (bcrypt 제한 고려)
- 복잡성: 대/소문자 + 숫자 + 특수문자 중 3종 이상
- Have I Been Pwned API로 유출 비밀번호 차단 (k-anonymity)
- 이전 5개 비밀번호 재사용 금지

### 비밀번호 리셋 플로우
```typescript
// DO: 암호학적 안전 토큰, 1시간 만료, 일회용
async function requestReset(email: string) {
  const user = await db.findByEmail(email);
  // 사용자 존재 여부와 무관하게 동일 응답 (enumeration 방지)
  if (!user) return { message: 'If the email exists, a reset link was sent.' };

  const token = crypto.randomBytes(32).toString('hex');
  const hashedToken = crypto.createHash('sha256').update(token).digest('hex');
  await db.saveResetToken({
    userId: user.id,
    token: hashedToken,
    expiresAt: new Date(Date.now() + 3600_000), // 1시간
  });
  await email.send(user.email, `https://app.com/reset?token=${token}`);
  return { message: 'If the email exists, a reset link was sent.' };
}

async function executeReset(token: string, newPassword: string) {
  const hashedToken = crypto.createHash('sha256').update(token).digest('hex');
  const record = await db.findResetToken(hashedToken);
  if (!record || record.expiresAt < new Date()) throw new Error('Invalid or expired');
  await db.updatePassword(record.userId, await hashPassword(newPassword));
  await db.deleteResetToken(hashedToken);  // 일회용: 즉시 삭제
  await db.invalidateAllSessions(record.userId); // 기존 세션 모두 만료
}
```

DON'T:
```typescript
// ❌ MD5/SHA1 해싱 — 초당 수십억 회 시도 가능
const hash = crypto.createHash('md5').update(password).digest('hex');

// ❌ 예측 가능한 리셋 토큰
const token = `reset-${userId}-${Date.now()}`; // 추측 가능!

// ❌ 리셋 토큰 만료 없음, 재사용 가능
// ❌ Rate limit 없음 — 무차별 리셋 요청 가능
```

### 흔한 실수
- 비밀번호 변경 후 기존 세션 유지 (탈취된 세션 계속 유효)
- 리셋 이메일에서 사용자 존재 여부 노출 ("해당 이메일 없음")
- 로그에 비밀번호 평문 기록 (req.body 전체 로깅)

## Connections

### CO_CREATES (3)

- → [[dev.backend.api.security]] `w=0.6`
- ← [[dev.backend.auth.jwt-auth]] `w=0.6`
- → [[dev.backend.auth.role]] `w=0.6`
