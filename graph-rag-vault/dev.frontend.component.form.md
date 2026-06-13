---
id: "dev.frontend.component.form"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "component", "form", "react-hook-form", "zod", "accessibility"]
brain_region: "CORTEX"
token_estimate: 500
---

# dev.frontend.component.form

React 폼 패턴 (일관된 유효성 검증과 접근성을 확보한다):

### 1. React Hook Form + Zod 통합
react-hook-form은 비제어 컴포넌트 기반으로 리렌더링을 최소화한다.
zod로 스키마를 정의하면 타입과 유효성 규칙을 한 곳에서 관리할 수 있다.

DO:
```tsx
// ✅ 스키마 정의 (types.ts 또는 schemas.ts)
import { z } from "zod";

export const createUserSchema = z.object({
  name: z.string()
    .min(2, "이름은 2자 이상이어야 합니다")
    .max(50, "이름은 50자 이하여야 합니다"),
  email: z.string()
    .email("올바른 이메일 형식이 아닙니다"),
  role: z.enum(["admin", "user", "viewer"], {
    errorMap: () => ({ message: "역할을 선택해주세요" }),
  }),
  bio: z.string().max(500).optional(),
});

export type CreateUserInput = z.infer<typeof createUserSchema>;
```

```tsx
// ✅ 폼 컴포넌트 (CreateUserForm.tsx)
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { createUserSchema, type CreateUserInput } from "./schemas";

export function CreateUserForm({ onSubmit }: { onSubmit: (data: CreateUserInput) => Promise<void> }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    reset,
  } = useForm<CreateUserInput>({
    resolver: zodResolver(createUserSchema),
    defaultValues: { name: "", email: "", role: "user", bio: "" },
  });

  const handleFormSubmit = async (data: CreateUserInput) => {
    await onSubmit(data);
    reset();
  };

  return (
    <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4" noValidate>
      {/* Name 필드 */}
      <div className="space-y-1">
        <label htmlFor="name" className="text-sm font-medium">
          이름 <span className="text-destructive">*</span>
        </label>
        <input
          id="name"
          {...register("name")}
          className="w-full rounded border px-3 py-2"
          aria-invalid={!!errors.name}
          aria-describedby={errors.name ? "name-error" : undefined}
        />
        {errors.name && (
          <p id="name-error" role="alert" className="text-sm text-destructive">
            {errors.name.message}
          </p>
        )}
      </div>

      {/* Email 필드 */}
      <div className="space-y-1">
        <label htmlFor="email" className="text-sm font-medium">
          이메일 <span className="text-destructive">*</span>
        </label>
        <input
          id="email"
          type="email"
          {...register("email")}
          className="w-full rounded border px-3 py-2"
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? "email-error" : undefined}
        />
        {errors.email && (
          <p id="email-error" role="alert" className="text-sm text-destructive">
            {errors.email.message}
          </p>
        )}
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="rounded bg-primary px-4 py-2 text-white disabled:opacity-50"
      >
        {isSubmitting ? "저장 중..." : "저장"}
      </button>
    </form>
  );
}
```

### 2. 유효성 검증 UX 규칙
- **제출 시** 전체 검증 (첫 번째 에러 필드로 포커스 이동).
- **에러 발생 후** 실시간 검증 (onChange/onBlur).
- 에러 메시지는 **해결 방법**을 포함한다 ("이름을 입력하세요" > "필수 항목입니다").
- 서버 에러는 `setError`로 폼에 표시한다.

DO:
```tsx
// ✅ 서버 에러를 폼 필드에 매핑
const onSubmit = async (data: CreateUserInput) => {
  try {
    await createUser(data);
  } catch (err) {
    if (err instanceof ApiError && err.field) {
      setError(err.field as keyof CreateUserInput, {
        message: err.message,
      });
    } else {
      setError("root", { message: "서버 오류가 발생했습니다" });
    }
  }
};

// 루트 에러 표시
{errors.root && (
  <div role="alert" className="rounded bg-destructive/10 p-3 text-destructive">
    {errors.root.message}
  </div>
)}
```

### 3. shadcn/ui Form 통합
shadcn/ui의 Form 컴포넌트를 활용하면 접근성이 자동 처리된다.

```tsx
// ✅ shadcn/ui Form 사용
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";

<Form {...form}>
  <form onSubmit={form.handleSubmit(onSubmit)}>
    <FormField
      control={form.control}
      name="name"
      render={({ field }) => (
        <FormItem>
          <FormLabel>이름</FormLabel>
          <FormControl>
            <Input placeholder="홍길동" {...field} />
          </FormControl>
          <FormMessage />
        </FormItem>
      )}
    />
  </form>
</Form>
```

### 4. 접근성 필수 규칙
- 모든 input에 `label`을 연결한다 (`htmlFor` + `id` 매칭).
- 에러 메시지에 `role="alert"`과 `aria-describedby`를 사용한다.
- 에러 상태에 `aria-invalid={true}`를 설정한다.
- 제출 버튼에 `disabled` + 로딩 텍스트를 표시한다.
- `noValidate`로 브라우저 기본 유효성 검사를 비활성화한다.

DON'T:
```tsx
// ❌ label 없는 input
<input placeholder="이름" />
// ❌ 에러 메시지에 접근성 속성 없음
<span className="text-red-500">{error}</span>
// ❌ 제출 중 중복 클릭 방지 없음
<button type="submit">저장</button>
```

### Edge Cases
- 파일 업로드는 `register`가 아닌 `Controller`로 처리한다.
- 동적 필드(배열)는 `useFieldArray`를 사용한다.
- 멀티 스텝 폼은 각 스텝을 별도 스키마로 정의하고 합성한다.
- 폼 상태가 리셋되지 않는 경우 `reset()` 호출 시점을 확인한다.

## Connections

- [[dev.backend.api.validation]] — FEEDS (weight: 0.5)
