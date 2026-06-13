---
id: "dev.backend.auth.verify"
domain: "development.backend"
type: "verify"
region: BRAINSTEM
token_estimate: 500
tags: [backend, auth, security, verify, checklist]
---

# dev.backend.auth.verify

> **Region**: 🔴 [[BRAINSTEM]]  
> **Domain**: `development.backend`  
> **Type**: `verify`  
> **Tokens**: 500

## Content

Auth 구현 자기 검증 체크리스트 (배포 전 반드시 확인):

### A. 토큰/세션 관리
- [ ] Access Token 만료가 15분 이하인가?
- [ ] Refresh Token rotation이 적용되어 있는가? (재사용 시 전체 무효화)
- [ ] 로그아웃 시 서버 측 토큰/세션이 무효화되는가? (블랙리스트 or 세션 삭제)
- [ ] 토큰이 httpOnly, secure, sameSite 쿠키에 저장되는가? (localStorage 사용 금지)

### B. 비밀번호 보안
- [ ] argon2id 또는 bcrypt(cost 12+)로 해싱하는가?
- [ ] 비밀번호 리셋 토큰이 crypto.randomBytes(32)로 생성되는가?
- [ ] 리셋 토큰 만료(1시간)와 일회용 처리가 되어 있는가?
- [ ] 비밀번호 변경 시 기존 세션이 모두 무효화되는가?

### C. CORS / CSRF / XSS 방어
- [ ] CORS origin이 와일드카드(*)가 아닌 명시적 도메인인가?
- [ ] 쿠키 기반 인증 시 CSRF 토큰 또는 sameSite=strict가 적용되어 있는가?
- [ ] 사용자 입력이 적절히 sanitize/escape 되는가?

### D. Rate Limiting
- [ ] 로그인 엔드포인트: IP당 5회/분, 계정당 10회/시간 제한이 있는가?
- [ ] 비밀번호 리셋 요청: IP당 3회/시간 제한이 있는가?
- [ ] MFA 코드 검증: 5회 실패 시 15분 잠금이 적용되는가?

### E. 인가 (Authorization)
- [ ] 모든 API에 인증 미들웨어가 적용되어 있는가? (화이트리스트 방식)
- [ ] 역할(role) 체크가 백엔드에서 수행되는가? (프론트 의존 금지)
- [ ] 리소스 소유권 검증이 적용되어 있는가? (본인 데이터만 접근)
- [ ] 관리자 기능이 별도 라우터/미들웨어로 분리되어 있는가?

### F. MFA (다중 인증)
- [ ] MFA 등록 시 검증 코드 확인 후 활성화하는가?
- [ ] 백업 코드가 해싱되어 저장되는가? (평문 금지)
- [ ] MFA 비활성화 시 비밀번호 재확인을 요구하는가?

### G. 로깅 및 감사
- [ ] 로그인 성공/실패가 기록되는가? (IP, User-Agent 포함)
- [ ] 비밀번호 변경, MFA 변경, 역할 변경이 감사 로그에 남는가?
- [ ] 로그에 비밀번호, 토큰, 비밀키가 절대 포함되지 않는가?

### 검증 방법
```typescript
// 자동화된 보안 테스트 예시
describe('Auth Security', () => {
  it('만료된 access token은 거부', async () => {
    const expired = jwt.sign({ sub: 'user1' }, secret, { expiresIn: '0s' });
    const res = await request(app).get('/api/me').set('Authorization', `Bearer ${expired}`);
    expect(res.status).toBe(401);
  });

  it('타인의 리소스 접근 시 403', async () => {
    const userToken = getTokenFor('user2');
    const res = await request(app).get('/api/posts/user1-post-id').set('Authorization', `Bearer ${userToken}`);
    expect(res.status).toBe(403);
  });

  it('Rate limit 초과 시 429', async () => {
    for (let i = 0; i < 6; i++) {
      await request(app).post('/api/login').send({ email: 'a@b.com', password: 'wrong' });
    }
    const res = await request(app).post('/api/login').send({ email: 'a@b.com', password: 'wrong' });
    expect(res.status).toBe(429);
  });
});
```

## Connections

### CO_CREATES (3)

- ← [[dev.backend.auth.jwt-auth]] `w=0.6`
- ← [[dev.backend.auth.rbac]] `w=0.6`
- ← [[dev.backend.auth.role]] `w=0.6`
