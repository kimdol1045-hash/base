---
id: "dev.frontend.testing.component-testing"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "testing", "component", "testing-library"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.testing.component-testing

> #256 Component Testing (Testing Library, Kent C. Dodds 2018)

# 컴포넌트 테스트 가이드

## 핵심 원칙
- 사용자 관점에서 컴포넌트의 동작을 테스트한다
- 구현 세부사항(state, 내부 메서드)이 아닌 DOM 출력과 인터랙션을 검증한다
- Testing Library의 쿼리 우선순위를 따른다 (getByRole > getByText > getByTestId)
- 테스트가 실제 사용자의 사용 방식을 반영해야 한다

## DO
- `@testing-library/react`를 사용한다
- `userEvent`로 실제 사용자 인터랙션을 시뮬레이션한다
- 접근성 역할(role)로 요소를 쿼리한다
- 비동기 동작은 `waitFor` 또는 `findBy`로 처리한다

## DON'T
- `container.querySelector`로 DOM을 직접 조회하지 않는다
- `fireEvent` 대신 `userEvent`를 사용한다 (더 현실적)
- 스타일, className을 테스트하지 않는다 (동작을 테스트)
- 스냅샷 테스트만으로 컴포넌트를 검증하지 않는다

## 코드 예시
```tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { LoginForm } from "./LoginForm";

describe("LoginForm", () => {
  it("이메일과 비밀번호를 입력하고 로그인할 수 있다", async () => {
    const handleSubmit = vi.fn();
    render(<LoginForm onSubmit={handleSubmit} />);

    const user = userEvent.setup();

    await user.type(screen.getByRole("textbox", { name: /이메일/i }), "test@test.com");
    await user.type(screen.getByLabelText(/비밀번호/i), "password123");
    await user.click(screen.getByRole("button", { name: /로그인/i }));

    expect(handleSubmit).toHaveBeenCalledWith({
      email: "test@test.com",
      password: "password123",
    });
  });

  it("이메일 형식이 잘못되면 에러를 표시한다", async () => {
    render(<LoginForm onSubmit={vi.fn()} />);
    const user = userEvent.setup();

    await user.type(screen.getByRole("textbox", { name: /이메일/i }), "invalid");
    await user.click(screen.getByRole("button", { name: /로그인/i }));

    expect(screen.getByRole("alert")).toHaveTextContent("올바른 이메일을 입력하세요");
  });

  it("로딩 중에는 버튼이 비활성화된다", async () => {
    render(<LoginForm onSubmit={vi.fn()} isLoading />);
    expect(screen.getByRole("button", { name: /로그인/i })).toBeDisabled();
  });
});
```
