---
id: "qa.test-gen.component-test"
domain: "qa"
type: "pattern"
region: EGO
token_estimate: 490
theory: "#126 Testing Trophy (Dodds, 2019)"
tags: [qa, test, component-test, testing-library, storybook, msw]
---

# qa.test-gen.component-test

> **Region**: 🔵 [[EGO]]  
> **Domain**: `qa`  
> **Type**: `pattern`  
> **Theory**: #126 Testing Trophy (Dodds, 2019)  
> **Tokens**: 490

## Content

컴포넌트 테스트 (사용자 관점에서 UI 컴포넌트의 동작을 검증한다):

### Testing Library 철학
"테스트가 소프트웨어 사용 방식과 닮을수록, 더 큰 신뢰를 준다."
— 구현이 아닌 **행동(behavior)**을 테스트한다.

### 접근 가능한 쿼리 우선순위
1. `getByRole` — 가장 권장 (접근성 트리 기반)
2. `getByLabelText` — 폼 요소
3. `getByPlaceholderText` — 라벨 없을 때
4. `getByText` — 비상호작용 요소
5. `getByTestId` — 최후 수단

### DO: 행동 기반 테스트
```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SearchForm } from './SearchForm';

describe('SearchForm', () => {
  it('검색어 입력 후 결과를 표시한다', async () => {
    const user = userEvent.setup();
    render(<SearchForm />);

    // 사용자처럼 상호작용
    const input = screen.getByRole('searchbox', { name: '상품 검색' });
    await user.type(input, '노트북');
    await user.click(screen.getByRole('button', { name: '검색' }));

    // 결과 확인
    await waitFor(() => {
      expect(screen.getByRole('list')).toBeInTheDocument();
      expect(screen.getAllByRole('listitem')).toHaveLength(5);
    });
  });

  it('빈 검색어 시 에러 메시지 표시', async () => {
    const user = userEvent.setup();
    render(<SearchForm />);

    await user.click(screen.getByRole('button', { name: '검색' }));

    expect(screen.getByRole('alert')).toHaveTextContent(
      '검색어를 입력해주세요'
    );
  });
});
```

### MSW로 API Mocking
```typescript
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';

const server = setupServer(
  http.get('/api/products', ({ request }) => {
    const url = new URL(request.url);
    const q = url.searchParams.get('q');
    return HttpResponse.json({
      items: [{ id: 1, name: `${q} Pro` }],
    });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
```

DON'T:
```typescript
// ❌ 구현 상세 테스트 (내부 상태 직접 접근)
const { result } = renderHook(() => useSearch());
expect(result.current.internalState).toBe('loading');

// ❌ fireEvent 대신 userEvent 사용 (실제 사용자 동작 시뮬레이션)
fireEvent.change(input, { target: { value: '노트북' } });

// ❌ 스냅샷 테스트로 로직 검증 (변경 시마다 깨짐)
expect(container).toMatchSnapshot();

// ❌ getByTestId를 첫 번째 선택지로
screen.getByTestId('search-btn'); // role이나 text가 있으면 그걸 사용
```

### Storybook Interaction Test
```typescript
// *.stories.tsx 안에서 play 함수로 상호작용 테스트
export const WithSearch: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    await userEvent.type(canvas.getByRole('searchbox'), '노트북');
    await userEvent.click(canvas.getByRole('button', { name: '검색' }));
    await expect(canvas.getByRole('list')).toBeInTheDocument();
  },
};
```

### 비동기 패턴
- `waitFor`: 상태 변경 대기 (폴링 방식, 기본 1000ms 타임아웃)
- `findByRole`: `waitFor` + `getByRole` 조합 (가장 간결)
- `act()` 직접 사용 금지 — Testing Library가 내부적으로 처리

## Connections

### FEEDS (3)

- ← [[qa.code-review.performance]] `w=0.5`
- ← [[qa.code-review.priority]] `w=0.5`
- ← [[qa.code-review.role]] `w=0.5`

### CO_CREATES (4)

- ← [[qa.test-gen.integration]] `w=0.6`
- ← [[qa.test-gen.role]] `w=0.6`
- ← [[qa.test-gen.unit]] `w=0.6`
- → [[qa.test-gen.verify]] `w=0.6`
