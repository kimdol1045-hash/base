---
id: "dev.frontend.component.i18n"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "i18n", "internationalization", "next-intl", "rtl", "icu", "intl-api", "locale"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.frontend.component.i18n

> #7 Jakob's Law — 사용자는 자신의 언어와 문화 관습을 기대한다 (Nielsen, 2000)

국제화(i18n) 패턴 (다국어, 날짜/숫자 포맷, RTL을 체계적으로 지원한다):

### 1. next-intl 기본 설정 (Next.js App Router)

DO:
```typescript
// ✅ 메시지 파일 구조 — messages/ko.json
{
  "common": {
    "save": "저장",
    "cancel": "취소",
    "delete": "삭제",
    "loading": "로딩 중..."
  },
  "auth": {
    "login": {
      "title": "로그인",
      "email": "이메일",
      "password": "비밀번호",
      "submit": "로그인",
      "noAccount": "계정이 없으신가요? {signupLink}",
      "error": "이메일 또는 비밀번호가 올바르지 않습니다."
    }
  },
  "dashboard": {
    "welcome": "{name}님, 환영합니다!",
    "projects": {
      "count": "{count, plural, =0 {프로젝트 없음} one {프로젝트 1개} other {프로젝트 {count}개}}"
    }
  }
}

// ✅ 컴포넌트에서 사용
import { useTranslations } from "next-intl";

function LoginForm() {
  const t = useTranslations("auth.login");
  return (
    <form>
      <h1>{t("title")}</h1>
      <Input placeholder={t("email")} />
      <Input type="password" placeholder={t("password")} />
      <Button>{t("submit")}</Button>
    </form>
  );
}
```

### 2. 키 네이밍 컨벤션

| 패턴 | 예시 | 설명 |
|------|------|------|
| `page.section.element` | `dashboard.header.title` | 위치 기반 (권장) |
| `feature.action` | `auth.login` | 기능 기반 |
| `common.*` | `common.save` | 공통 (재사용) |

네임스페이스 깊이 최대 3단계. 4단계 이상은 인지 부하 증가.

### 3. 복수형 처리 (ICU MessageFormat)

```typescript
// ✅ ICU 복수형 — 언어별 규칙 자동 적용
// ko.json: "items": "{count, plural, =0 {항목 없음} other {{count}개 항목}}"
// en.json: "items": "{count, plural, =0 {No items} one {{count} item} other {{count} items}}"
// ar.json: 아랍어는 6가지 복수형 (zero, one, two, few, many, other)

t("dashboard.projects.count", { count: projects.length });
```

### 4. 날짜/숫자 포맷 — Intl API

DO:
```typescript
// ✅ Intl.DateTimeFormat — 로케일 자동 포맷
import { useFormatter } from "next-intl";

function DateDisplay({ date }: { date: Date }) {
  const format = useFormatter();
  return (
    <time dateTime={date.toISOString()}>
      {format.dateTime(date, {
        year: "numeric",
        month: "long",
        day: "numeric",
      })}
      {/* ko: "2024년 3월 15일", en: "March 15, 2024" */}
    </time>
  );
}

// ✅ 숫자/통화 포맷
format.number(1234567.89, { style: "currency", currency: "KRW" });
// → "₩1,234,568"
format.number(0.156, { style: "percent" });
// → "16%" (ko), "16%" (en)

// ✅ 상대 시간
format.relativeTime(new Date("2024-03-10"), new Date("2024-03-15"));
// → "5일 전" (ko), "5 days ago" (en)
```

### 5. RTL 지원 (아랍어, 히브리어)

```tsx
// ✅ CSS logical properties — LTR/RTL 자동 전환
// margin-inline-start 대신 Tailwind: ms-4
<div className="ms-4 ps-2 text-start">
  {/* ms = margin-start, ps = padding-start, text-start */}
  {/* LTR: margin-left, RTL: margin-right 자동 전환 */}
</div>

// ✅ html dir 속성 설정
// <html lang={locale} dir={locale === "ar" ? "rtl" : "ltr"}>
```

DON'T:
```typescript
// ❌ 하드코딩 문자열 — 번역 불가
<h1>환영합니다!</h1>

// ❌ 문자열 연결로 번역 문장 조합 — 어순이 언어마다 다름
t("hello") + " " + name + t("welcome") // 어순 깨짐

// ❌ 수동 날짜 포맷 — 로케일 규칙 무시
`${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`
// 미국: MM/DD/YYYY, 한국: YYYY.MM.DD → Intl API 사용

// ❌ margin-left/right 고정 — RTL에서 깨짐
<div className="ml-4" /> // → ms-4 사용
```
