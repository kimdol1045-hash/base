---
id: "design.ux-psychology.doherty-threshold"
domain: "design"
type: "rule"
bloom_level: ""
tags: ["design", "ux", "doherty", "performance"]
brain_region: "CORTEX"
token_estimate: 420
---

# design.ux-psychology.doherty-threshold

> #52 Doherty Threshold (Doherty & Thadhani, 1982)

도허티 임계값 (시스템 응답이 400ms 이내면 사용자 생산성이 급증한다):

### 응답 시간 기준
| 시간 | 사용자 인지 | 대응 |
|------|-----------|------|
| < 100ms | 즉각 반응으로 느낌 | 최적 |
| 100-400ms | 약간 지연 인지 | 수용 가능 |
| 400ms-1s | 명확한 지연 | 로딩 인디케이터 필요 |
| 1-5s | 집중력 이탈 시작 | 프로그레스 바 + 스켈레톤 |
| > 5s | 작업 포기 가능 | 비동기 처리 + 알림 |

### 400ms 이내 달성 전략
1. **낙관적 업데이트 (Optimistic Update)**
   ```tsx
   const handleLike = async () => {
     setLiked(true); // 즉시 UI 반영
     setCount(prev => prev + 1);
     try {
       await api.like(postId);
     } catch {
       setLiked(false); // 실패 시 롤백
       setCount(prev => prev - 1);
       toast.error("다시 시도해주세요");
     }
   };
   ```

2. **스켈레톤 UI**: 콘텐츠 로딩 중 레이아웃 미리 표시
3. **프리페치**: 사용자가 클릭하기 전에 데이터 미리 로드
   ```tsx
   <Link href="/dashboard" prefetch={true}>대시보드</Link>
   ```
4. **스피너 대신 스켈레톤**: 스피너는 시간을 인지하게 함

## Connections

- [[design.ux-psychology.role]] — REQUIRES (weight: 0.9)
- [[design.ux-psychology.verify]] — FEEDS (weight: 0.8)
- [[design.ux-psychology.aesthetic-usability]] — FEEDS (weight: 0.7)
- [[design.ux-psychology.recognition-over-recall]] — FEEDS (weight: 0.7)
