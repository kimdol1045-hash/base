---
id: "dev.backend.auth.rbac"
domain: "development.backend"
type: "rule"
bloom_level: ""
tags: ["backend", "auth", "rbac", "abac", "authorization"]
brain_region: "BRAINSTEM"
token_estimate: 500
---

# dev.backend.auth.rbac

> #115 Saltzer Least Privilege

RBAC + ABAC + 리소스 소유권 (최소 권한 원칙에 기반한 다층 접근 제어):

### 역할별 권한 매트릭스
| 권한 | admin | editor | viewer |
|------|-------|--------|--------|
| user.list | ✅ | ❌ | ❌ |
| post.create | ✅ | ✅ | ❌ |
| post.edit | ✅ | own | ❌ |
| post.delete | ✅ | own | ❌ |
| post.read | ✅ | ✅ | ✅ |
| settings.manage | ✅ | ❌ | ❌ |

### 미들웨어 체인 구현
```typescript
// DO: auth → role → ownership 순서로 미들웨어 체인
enum Permission {
  POST_CREATE = 'post.create',
  POST_EDIT = 'post.edit',
  POST_DELETE = 'post.delete',
  USER_LIST = 'user.list',
}

const ROLE_PERMISSIONS: Record<string, Permission[]> = {
  admin: [Permission.POST_CREATE, Permission.POST_EDIT, Permission.POST_DELETE, Permission.USER_LIST],
  editor: [Permission.POST_CREATE, Permission.POST_EDIT, Permission.POST_DELETE],
  viewer: [],
};

// 1단계: 역할 기반 권한 확인
function requirePermission(...perms: Permission[]) {
  return (req: Request, res: Response, next: NextFunction) => {
    const userPerms = ROLE_PERMISSIONS[req.user.role] ?? [];
    const hasAll = perms.every(p => userPerms.includes(p));
    if (!hasAll) return res.status(403).json({ error: 'Insufficient permissions' });
    next();
  };
}

// 2단계: 리소스 소유권 확인 (admin은 bypass)
function requireOwnership(resourceFn: (req: Request) => Promise<{ ownerId: string } | null>) {
  return async (req: Request, res: Response, next: NextFunction) => {
    if (req.user.role === 'admin') return next();
    const resource = await resourceFn(req);
    if (!resource) return res.status(404).json({ error: 'Not found' });
    if (resource.ownerId !== req.user.id) return res.status(403).json({ error: 'Not owner' });
    next();
  };
}

// 라우터 적용
router.put('/posts/:id',
  authenticate,
  requirePermission(Permission.POST_EDIT),
  requireOwnership(req => postRepo.findById(req.params.id)),
  updatePostHandler,
);
```

DON'T:
```typescript
// ❌ 핸들러 내부에 하드코딩된 역할 체크
async function updatePost(req: Request, res: Response) {
  if (req.user.role !== 'admin' && req.user.role !== 'editor') {
    return res.status(403).send('Forbidden');
  }
  // 소유권 확인 누락! editor가 남의 글 수정 가능
  await postRepo.update(req.params.id, req.body);
}
```

### ABAC 확장 예시
- 근무시간(09-18시)에만 관리자 기능 허용
- IP 화이트리스트 기반 접근 제한
- 조건: `if (user.department === resource.department)`

### 흔한 실수
- 프론트엔드에서만 권한 체크 (백엔드 미적용)
- admin 역할의 범위가 너무 넓음 — super_admin / admin 분리 필요
- 역할 변경 후 기존 세션/토큰의 권한이 갱신되지 않음

## Connections

- [[dev.backend.auth.role]] — CO_CREATES (weight: 0.6)
- [[dev.backend.auth.jwt-auth]] — CO_CREATES (weight: 0.6)
- [[dev.backend.auth.verify]] — CO_CREATES (weight: 0.6)
- [[dev.backend.api.auth]] — CO_CREATES (weight: 0.6)
- [[dev.backend.api.middleware]] — CO_CREATES (weight: 0.6)
