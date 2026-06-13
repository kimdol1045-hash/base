---
id: "dev.backend.testing.fixture-factory"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["testing", "fixture", "factory", "test-data"]
brain_region: "BRAINSTEM"
token_estimate: 400
---

# dev.backend.testing.fixture-factory

> #231 Object Mother / Test Data Builder (Fowler, xUnit Test Patterns 2007)

# 테스트 픽스처 팩토리 가이드

## 핵심 원칙
- 테스트 데이터 생성을 중앙화된 팩토리로 관리한다
- 기본값을 제공하되, 테스트별로 필요한 속성만 오버라이드한다
- 연관 관계가 있는 엔티티를 함께 생성하는 메서드를 제공한다
- 테스트의 의도를 명확히 드러내는 팩토리 메서드명을 사용한다

## DO
- Builder 패턴으로 유연한 데이터 생성을 지원한다
- 시퀀스 카운터로 고유 값(이메일, 이름)을 자동 생성한다
- DB 저장과 인메모리 생성을 분리한다 (build vs create)
- 시나리오별 프리셋을 제공한다 (관리자, 비활성 사용자 등)

## DON'T
- 테스트마다 리터럴 객체를 반복 작성하지 않는다
- 공유 테스트 데이터에 의존하지 않는다 (각 테스트가 자체 데이터 생성)
- 불필요한 필드를 테스트에서 지정하지 않는다 (기본값 활용)
- 팩토리 함수에서 부작용(이메일 발송 등)을 일으키지 않는다

## 코드 예시
```typescript
let seq = 0;
function nextSeq() { return ++seq; }

// 기본 팩토리
function buildUser(overrides: Partial<User> = {}): User {
  const n = nextSeq();
  return {
    id: `user-${n}`,
    email: `user${n}@test.com`,
    displayName: `테스트유저${n}`,
    role: "member",
    status: "active",
    createdAt: new Date(),
    ...overrides,
  };
}

// DB에 저장하는 버전
async function createUser(overrides: Partial<User> = {}): Promise<User> {
  const data = buildUser(overrides);
  return db.users.create({ data });
}

// 시나리오별 프리셋
function buildAdmin(overrides: Partial<User> = {}) {
  return buildUser({ role: "admin", ...overrides });
}

function buildInactiveUser(overrides: Partial<User> = {}) {
  return buildUser({ status: "inactive", ...overrides });
}

// 연관 엔티티 함께 생성
async function createUserWithPosts(postCount = 3) {
  const user = await createUser();
  const posts = await Promise.all(
    Array.from({ length: postCount }, () =>
      createPost({ authorId: user.id })
    ),
  );
  return { user, posts };
}

// 테스트에서 사용
it("관리자만 삭제할 수 있다", async () => {
  const admin = await createUser({ role: "admin" });
  const target = await createUser();
  const result = await deleteUser(admin.id, target.id);
  expect(result.success).toBe(true);
});
```
