---
id: "dev.frontend.testing.storybook"
domain: "development.frontend"
type: "pattern"
bloom_level: ""
tags: ["frontend", "testing", "storybook", "documentation"]
brain_region: "CORTEX"
token_estimate: 420
---

# dev.frontend.testing.storybook

> #258 Component-Driven Development (Storybook, Chromatic 2016)

# Storybook 활용 가이드

## 핵심 원칙
- 컴포넌트를 독립적으로 개발하고 문서화하는 도구이다
- 다양한 props 조합을 스토리로 정의하여 시각적으로 확인한다
- 디자이너, QA, 개발자 간 커뮤니케이션 도구로 활용한다
- 인터랙션 테스트와 비주얼 테스트의 기반이 된다

## DO
- 공유 컴포넌트(디자인 시스템)에 스토리를 필수로 작성한다
- args와 argTypes로 컨트롤 패널을 구성한다
- play 함수로 인터랙션 시나리오를 정의한다
- autodocs로 자동 문서를 생성한다

## DON'T
- 페이지 전체를 하나의 스토리로 작성하지 않는다 (컴포넌트 단위)
- 스토리 없이 컴포넌트를 PR에 올리지 않는다
- 외부 API에 의존하는 스토리를 만들지 않는다 (MSW로 Mock)
- 스토리를 최신 상태로 유지하지 않고 방치하지 않는다

## 코드 예시
```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react";
import { within, userEvent, expect } from "@storybook/test";
import { Button } from "./Button";

const meta: Meta<typeof Button> = {
  title: "UI/Button",
  component: Button,
  tags: ["autodocs"],
  argTypes: {
    variant: { control: "select", options: ["primary", "secondary", "ghost"] },
    size: { control: "select", options: ["sm", "md", "lg"] },
    disabled: { control: "boolean" },
  },
};
export default meta;

type Story = StoryObj<typeof Button>;

export const Primary: Story = {
  args: { children: "버튼", variant: "primary" },
};

export const Secondary: Story = {
  args: { children: "버튼", variant: "secondary" },
};

export const AllVariants: Story = {
  render: () => (
    <div className="flex gap-4">
      <Button variant="primary">Primary</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="ghost">Ghost</Button>
    </div>
  ),
};

// 인터랙션 테스트
export const ClickTest: Story = {
  args: { children: "클릭하세요" },
  play: async ({ canvasElement, args }) => {
    const canvas = within(canvasElement);
    const button = canvas.getByRole("button");
    await userEvent.click(button);
    await expect(args.onClick).toHaveBeenCalled();
  },
};
```
