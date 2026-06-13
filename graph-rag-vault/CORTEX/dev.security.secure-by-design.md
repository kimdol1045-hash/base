---
id: "dev.security.secure-by-design"
domain: "development.security"
type: "pattern"
region: CORTEX
token_estimate: 500
theory: "#120 Security by Design (Cavoukian, 2009)"
tags: [security, privacy-by-design, gdpr, secure-design, pattern]
---

# dev.security.secure-by-design

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.security`  
> **Type**: `pattern`  
> **Theory**: #120 Security by Design (Cavoukian, 2009)  
> **Tokens**: 500

## Content

Security by Design + Privacy by Design 7원칙 (Ann Cavoukian, 2009 / GDPR Art.25):

보안과 개인정보 보호는 사후 패치가 아니라 설계 단계부터 시스템에 내장한다.
"보안을 나중에 추가하는 것은 집을 짓고 나서 기초를 보강하는 것과 같다."

### 원칙 1: 사후 대응이 아닌 사전 예방 (Proactive not Reactive)
위협이 발생하기 전에 예방 조치를 설계에 포함한다.
```typescript
// DO: 설계 단계에서 위협 모델링 수행
// 신규 API 설계 시 STRIDE 분석을 먼저 수행하고 코드 작성
interface ThreatModel {
  feature: string;
  threats: Array<{
    type: "S" | "T" | "R" | "I" | "D" | "E";
    scenario: string;
    mitigation: string;
    priority: "high" | "medium" | "low";
  }>;
  reviewedBy: string;
  reviewedAt: string;
}
```

### 원칙 2: 기본값으로 보안 (Privacy as Default)
사용자가 아무 설정도 하지 않아도 최대 보안 상태여야 한다.
```typescript
// DO: 기본값이 가장 안전한 옵션
const DEFAULT_USER_SETTINGS = {
  profileVisibility: "private",     // 기본: 비공개
  dataSharing: false,               // 기본: 공유 안 함
  twoFactorEnabled: true,           // 기본: 2FA 활성화
  sessionTimeout: 15 * 60 * 1000,   // 기본: 15분
  emailNotifications: true,         // 보안 알림: 켜짐
} as const;

// DON'T: 기본값이 열린 상태
const DEFAULT_USER_SETTINGS = {
  profileVisibility: "public",      // 기본: 공개 = 위험
  dataSharing: true,                // 기본: 공유 = 위험
  twoFactorEnabled: false,          // 기본: 2FA 꺼짐 = 위험
};
```

### 원칙 3: 설계에 내장 (Embedded into Design)
보안은 부가 기능이 아니라 핵심 아키텍처의 일부이다.
```typescript
// DO: 엔티티 레벨에서 PII 보호가 내장된 설계
class UserEntity {
  private readonly _email: string;
  private readonly _phone: string;

  constructor(data: { email: string; phone: string }) {
    this._email = encrypt(data.email, ENCRYPTION_KEY);
    this._phone = encrypt(data.phone, ENCRYPTION_KEY);
  }

  // 외부 노출 시 항상 마스킹
  get maskedEmail(): string {
    const email = decrypt(this._email, ENCRYPTION_KEY);
    const [local, domain] = email.split("@");
    return `${local.slice(0, 2)}***@${domain}`;
  }

  // 원본은 명시적 권한이 있을 때만 접근
  getEmail(accessor: { hasPermission: (p: string) => boolean }): string {
    if (!accessor.hasPermission("read:pii")) throw Errors.forbidden();
    return decrypt(this._email, ENCRYPTION_KEY);
  }
}

// DON'T: PII가 그냥 string으로 돌아다니는 설계
interface User { email: string; phone: string; } // 어디서든 평문 접근 가능
```

### 원칙 4: 양립 가능 (Positive-Sum)
보안과 사용성은 상충하지 않는다. 둘 다 달성할 수 있는 설계를 추구한다.
- 비밀번호: 복잡한 규칙 대신 최소 12자 + 실시간 강도 피드백
- 인증: 매번 비밀번호 입력 대신 biometric + 기기 신뢰

### 원칙 5: 전체 수명주기 보안 (End-to-End Lifecycle)
데이터 생성부터 파기까지 보안을 유지한다.
```typescript
// DO: 데이터 보존 정책 + 자동 삭제
const DATA_RETENTION_DAYS = 365 * 2; // 2년 보존

// 매일 실행: 보존 기한 초과 데이터 안전 삭제
async function purgeExpiredData() {
  const cutoff = new Date(Date.now() - DATA_RETENTION_DAYS * 86_400_000);
  const deleted = await db.delete(userActivities)
    .where(lt(userActivities.createdAt, cutoff));
  logger.info({ event: "DATA_PURGE", count: deleted.rowCount, cutoff: cutoff.toISOString() });
}
```

### 원칙 6: 가시성과 투명성 (Visibility and Transparency)
사용자에게 어떤 데이터를 수집하고 어떻게 사용하는지 명확히 알린다.
- 개인정보 수집 시 목적/보존기간/제3자 제공 여부 명시
- 사용자 데이터 다운로드/삭제 기능 제공 (GDPR Art.17 삭제권)

### 원칙 7: 사용자 중심 (User-Centric)
```typescript
// DO: 사용자가 자신의 데이터를 통제할 수 있는 API
app.get("/me/data-export", authMiddleware, async (c) => {
  const data = await userDataService.exportAll(c.get("user").id);
  return c.json({ data }); // GDPR Art.20 데이터 이동권
});

app.delete("/me/account", authMiddleware, mfaRequired, async (c) => {
  await userService.anonymizeAndDelete(c.get("user").id); // 완전 삭제
  return c.json({ message: "계정이 삭제되었습니다" });
});
```

### GDPR Art.25 준수 요약
- Data Minimization: 필요 최소한의 데이터만 수집
- Purpose Limitation: 수집 목적 외 사용 금지
- Storage Limitation: 보존 기간 만료 시 자동 삭제
- Pseudonymization: 가능하면 가명 처리

## Connections

### CO_CREATES (9)

- ← [[dev.security.cia-triad]] `w=0.6`
- → [[dev.security.defense-in-depth]] `w=0.6`
- ← [[dev.security.owasp]] `w=0.6`
- ← [[dev.security.role]] `w=0.6`
- ← [[dev.security.saltzer]] `w=0.6`
- ← [[dev.security.stride]] `w=0.6`
- ← [[dev.security.swiss-cheese]] `w=0.6`
- → [[dev.security.verify]] `w=0.6`
- → [[dev.security.zero-trust]] `w=0.6`
