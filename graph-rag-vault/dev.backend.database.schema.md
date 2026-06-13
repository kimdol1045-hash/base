---
id: "dev.backend.database.schema"
domain: "development.database"
type: "rule"
bloom_level: ""
tags: ["database", "schema", "normalization", "postgresql", "rls"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.database.schema

> #107 Codd 정규화 이론 (Codd, 1970)

스키마 설계 규칙 (데이터 무결성과 일관성을 보장한다):

### 정규화 원칙
- 3NF 이상 정규화가 기본. 의도적 비정규화는 주석에 근거 필수
- 비정규화 허용 조건: 읽기 비율 90%+ 이고 JOIN이 3개 이상 필요한 경우

### PK 전략
DO:
```sql
-- ✅ UUID v4: 예측 불가, 분산 시스템 안전
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  display_name VARCHAR(100) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_at TIMESTAMPTZ  -- soft delete
);
```

DON'T:
```sql
-- ❌ auto-increment: ID 추측 가능 → IDOR 취약점
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT  -- ❌ 길이 제한 없음, UNIQUE 누락
);
```

### 타임스탬프 필수 컬럼
모든 테이블에 아래 3개 컬럼을 포함한다:
- `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- `updated_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- `deleted_at TIMESTAMPTZ` (soft delete가 필요한 경우)

`updated_at` 자동 갱신 트리거:
```sql
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_updated_at
  BEFORE UPDATE ON users
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
```

### 외래키 규칙
DO:
```sql
-- ✅ CASCADE/SET NULL 명시적 선언
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  author_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  category_id UUID REFERENCES categories(id) ON DELETE SET NULL,
  title VARCHAR(200) NOT NULL,
  content TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

DON'T:
```sql
-- ❌ ON DELETE 미명시 → 기본값 NO ACTION으로 삭제 시 에러
CREATE TABLE posts (
  author_id UUID REFERENCES users(id)
);
```

### 네이밍 컨벤션
- 테이블명: `snake_case`, 복수형 (`users`, `order_items`)
- 컬럼명: `snake_case` (`created_at`, `author_id`)
- 인덱스명: `idx_{table}_{columns}` (`idx_posts_author_id`)
- 외래키명: `fk_{table}_{ref_table}` (`fk_posts_users`)

### ENUM 처리
```sql
-- ✅ PostgreSQL ENUM 타입 (값이 고정적일 때)
CREATE TYPE order_status AS ENUM ('pending', 'confirmed', 'shipped', 'delivered', 'cancelled');

-- ✅ 참조 테이블 (값이 자주 변경될 때)
CREATE TABLE order_statuses (
  id VARCHAR(20) PRIMARY KEY,
  label VARCHAR(50) NOT NULL,
  sort_order INT NOT NULL DEFAULT 0
);
```

### RLS 정책 (Supabase)
```sql
-- 사용자는 자신의 데이터만 CRUD 가능
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can read own posts"
  ON posts FOR SELECT
  USING (author_id = auth.uid());

CREATE POLICY "Users can insert own posts"
  ON posts FOR INSERT
  WITH CHECK (author_id = auth.uid());
```

### 흔한 실수
- VARCHAR 길이 미지정 → TEXT와 동일하지만 의도가 불명확
- NOT NULL 누락 → 의도치 않은 NULL 데이터 유입
- 인덱스 없는 외래키 → JOIN 성능 저하
- TIMESTAMPTZ 대신 TIMESTAMP → 타임존 이슈 발생

## Connections

- [[dev.backend.database.role]] — REQUIRES (weight: 0.9)
- [[dev.backend.database.verify]] — FEEDS (weight: 0.8)
- [[dev.backend.database.query]] — FEEDS (weight: 0.7)
- [[dev.backend.database.query]] — CO_CREATES (weight: 0.6)
- [[dev.backend.database.index]] — CO_CREATES (weight: 0.6)
- [[dev.backend.database.transaction]] — CO_CREATES (weight: 0.6)
- [[dev.backend.database.migration]] — CO_CREATES (weight: 0.6)
