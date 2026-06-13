---
id: "dev.backend.api.batch-operations"
domain: "development.backend"
type: "pattern"
bloom_level: ""
tags: ["backend", "api", "batch", "bulk", "transaction", "partial-success"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.api.batch-operations

> #104 Idempotency

Batch Operations 패턴 (대량 작업은 개별 API 호출이 아닌 일괄 처리로 한다 -- 100번의 요청을 1번으로 줄여라):

### Batch API 설계 원칙
- 각 항목의 성공/실패를 개별 보고
- 전체 실패(all-or-nothing)와 부분 성공(partial) 모드 지원
- 최대 배치 크기 제한 (기본 100건)

DO:
```typescript
// 1. Batch Create 요청/응답 스키마
const BatchCreateSchema = z.object({
  items: z.array(CreateItemSchema).min(1).max(100),
  mode: z.enum(["atomic", "partial"]).default("partial"),
  // atomic: 하나라도 실패하면 전체 롤백
  // partial: 성공한 것만 저장, 실패는 개별 보고
});

const BatchResponseSchema = z.object({
  succeeded: z.number(),
  failed: z.number(),
  total: z.number(),
  results: z.array(z.object({
    index: z.number(),
    status: z.enum(["success", "error"]),
    data: z.any().optional(),
    error: z.object({
      code: z.string(),
      message: z.string(),
    }).optional(),
  })),
});

// 2. Atomic 모드 (트랜잭션)
app.post("/api/v1/products/batch", authMiddleware, async (c) => {
  const { items, mode } = BatchCreateSchema.parse(await c.req.json());

  if (mode === "atomic") {
    return await handleAtomicBatch(c, items);
  }
  return await handlePartialBatch(c, items);
});

async function handleAtomicBatch(c: Context, items: CreateItemInput[]) {
  const results = await db.transaction(async (tx) => {
    const created: any[] = [];
    for (let i = 0; i < items.length; i++) {
      try {
        const product = await tx.insert(products).values(items[i]).returning();
        created.push({ index: i, status: "success", data: product[0] });
      } catch (err) {
        // 트랜잭션 전체 롤백
        throw new BatchError(`Item ${i} failed: ${err.message}`, i, created);
      }
    }
    return created;
  });

  return c.json({
    succeeded: results.length,
    failed: 0,
    total: items.length,
    results,
  }, 201);
}

// 3. Partial 모드 (개별 처리)
async function handlePartialBatch(c: Context, items: CreateItemInput[]) {
  const results: BatchResult[] = [];
  let succeeded = 0;
  let failed = 0;

  for (let i = 0; i < items.length; i++) {
    try {
      const product = await db.insert(products).values(items[i]).returning();
      results.push({ index: i, status: "success", data: product[0] });
      succeeded++;
    } catch (err) {
      results.push({
        index: i,
        status: "error",
        error: {
          code: mapErrorCode(err),
          message: err instanceof Error ? err.message : "Unknown error",
        },
      });
      failed++;
    }
  }

  const statusCode = failed === 0 ? 201 : failed === items.length ? 400 : 207;
  return c.json({ succeeded, failed, total: items.length, results }, statusCode);
}

// 4. Batch Update (PATCH)
const BatchUpdateSchema = z.object({
  operations: z.array(z.object({
    id: z.string().uuid(),
    data: UpdateItemSchema,
  })).min(1).max(100),
});

app.patch("/api/v1/products/batch", authMiddleware, async (c) => {
  const { operations } = BatchUpdateSchema.parse(await c.req.json());
  const results: BatchResult[] = [];

  await db.transaction(async (tx) => {
    for (let i = 0; i < operations.length; i++) {
      const { id, data } = operations[i];
      const updated = await tx.update(products)
        .set({ ...data, updatedAt: new Date() })
        .where(eq(products.id, id))
        .returning();

      if (updated.length === 0) {
        results.push({
          index: i, status: "error",
          error: { code: "NOT_FOUND", message: `Product ${id} not found` },
        });
      } else {
        results.push({ index: i, status: "success", data: updated[0] });
      }
    }
  });

  return c.json({ succeeded: results.filter(r => r.status === "success").length, failed: results.filter(r => r.status === "error").length, total: operations.length, results });
});

// 5. Batch Delete
app.delete("/api/v1/products/batch", authMiddleware, async (c) => {
  const { ids } = z.object({
    ids: z.array(z.string().uuid()).min(1).max(100),
  }).parse(await c.req.json());

  const deleted = await db.delete(products)
    .where(inArray(products.id, ids))
    .returning({ id: products.id });

  const deletedIds = new Set(deleted.map(d => d.id));
  const results = ids.map((id, i) => ({
    index: i,
    status: deletedIds.has(id) ? "success" as const : "error" as const,
    ...(deletedIds.has(id) ? { data: { id } } : { error: { code: "NOT_FOUND", message: `Product ${id} not found` } }),
  }));

  return c.json({
    succeeded: deleted.length,
    failed: ids.length - deleted.length,
    total: ids.length,
    results,
  });
});
```

### HTTP 상태 코드 기준
| 상태 코드 | 조건 | 설명 |
|-----------|------|------|
| 201 | 전체 성공 | 모든 항목이 성공적으로 생성됨 |
| 207 | 부분 성공 | 일부 성공, 일부 실패 (Multi-Status) |
| 400 | 전체 실패 | 모든 항목이 실패 |
| 413 | 배치 초과 | 최대 배치 크기(100건) 초과 |

DON'T:
```typescript
// ❌ 전체 실패만 반환 -- 어떤 항목이 실패했는지 알 수 없음
app.post("/products/batch", async (c) => {
  try {
    await db.insert(products).values(items);
    return c.json({ success: true });
  } catch {
    return c.json({ success: false }, 400);  // 어떤 항목이 문제인지 모름
  }
});

// ❌ 배치 크기 제한 없음 -- 10만 건 요청으로 서버 과부하
const items = await c.req.json();  // 크기 제한 없음
for (const item of items) { await db.insert(products).values(item); }

// ❌ 진행 상태 피드백 없는 대량 처리 -- 클라이언트 타임아웃
app.post("/products/import", async (c) => {
  const items = await c.req.json();  // 10,000건
  for (const item of items) { await processItem(item); }  // 5분 소요
  return c.json({ done: true });  // 클라이언트는 이미 타임아웃
});
```

### 흔한 실수
- 207 Multi-Status 대신 항상 200/400만 반환 -> 부분 성공 구분 불가
- 배치 내 항목 순서(index)를 응답에 포함하지 않음 -> 어떤 항목이 실패인지 매핑 불가
- 대량 배치(1000건 이상)를 동기 처리 -> 비동기 작업 + 진행 상태 API로 전환 필요
- atomic 모드에서 부분 성공 응답 반환 -> 트랜잭션 전체 롤백과 모순
- DELETE 배치에서 존재하지 않는 ID를 에러 처리하지 않음 -> 클라이언트 혼란
