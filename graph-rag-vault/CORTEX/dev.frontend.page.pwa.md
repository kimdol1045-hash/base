---
id: "dev.frontend.page.pwa"
domain: "development.frontend"
type: "pattern"
region: CORTEX
token_estimate: 500
theory: "#35 Doherty Threshold (Doherty & Kelisky, 1979) — 400ms 이내 응답"
tags: [frontend, pwa, service-worker, offline, caching, install-prompt, manifest]
---

# dev.frontend.page.pwa

> **Region**: ⚡ [[CORTEX]]  
> **Domain**: `development.frontend`  
> **Type**: `pattern`  
> **Theory**: #35 Doherty Threshold (Doherty & Kelisky, 1979) — 400ms 이내 응답  
> **Tokens**: 500

## Content

PWA 패턴 (오프라인 대응, 설치 가능한 웹 앱을 구축한다):

### PWA 핵심 요소
1. **Service Worker**: 네트워크 프록시, 캐싱, 백그라운드 동기화
2. **Web App Manifest**: 설치, 아이콘, 시작 URL, 디스플레이 모드
3. **HTTPS**: Service Worker는 HTTPS 필수 (localhost 제외)

### 1. next-pwa 설정

DO:
```typescript
// ✅ next.config.ts — next-pwa 설정
import withPWA from "next-pwa";

const config = withPWA({
  dest: "public",
  register: true,
  skipWaiting: true,
  disable: process.env.NODE_ENV === "development", // 개발 시 비활성화
  runtimeCaching: [
    {
      // 정적 에셋 — Cache First (변경 거의 없음)
      urlPattern: /\.(?:js|css|woff2|png|jpg|svg)$/i,
      handler: "CacheFirst",
      options: {
        cacheName: "static-assets",
        expiration: {
          maxEntries: 200,
          maxAgeSeconds: 30 * 24 * 60 * 60, // 30일
        },
      },
    },
    {
      // API 요청 — Network First (최신 데이터 우선)
      urlPattern: /\/api\/.*$/i,
      handler: "NetworkFirst",
      options: {
        cacheName: "api-cache",
        networkTimeoutSeconds: 5,   // 5초 타임아웃 후 캐시
        expiration: {
          maxEntries: 100,
          maxAgeSeconds: 5 * 60,    // 5분
        },
      },
    },
    {
      // 페이지 네비게이션 — Stale While Revalidate
      urlPattern: /^https:\/\/.*\.html$/i,
      handler: "StaleWhileRevalidate",
      options: {
        cacheName: "pages-cache",
        expiration: {
          maxEntries: 50,
          maxAgeSeconds: 24 * 60 * 60, // 24시간
        },
      },
    },
  ],
});
```

### 2. Web App Manifest

```typescript
// ✅ public/manifest.json
// {
//   "name": "My App",
//   "short_name": "App",
//   "start_url": "/",
//   "display": "standalone",
//   "background_color": "#ffffff",
//   "theme_color": "#000000",
//   "icons": [
//     { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
//     { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" },
//     { "src": "/icons/icon-maskable.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
//   ]
// }
```

### 3. 오프라인 폴백 페이지

```tsx
// ✅ app/offline/page.tsx — 오프라인 시 표시
export default function OfflinePage() {
  return (
    <div className="flex min-h-screen items-center justify-center p-4">
      <div className="text-center space-y-4">
        <WifiOffIcon className="mx-auto h-16 w-16 text-muted-foreground" />
        <h1 className="text-2xl font-bold">오프라인 상태</h1>
        <p className="text-muted-foreground">
          인터넷 연결을 확인하고 다시 시도해주세요.
        </p>
        <Button onClick={() => window.location.reload()}>
          다시 시도
        </Button>
      </div>
    </div>
  );
}
```

### 4. 설치 프롬프트 (A2HS)

```typescript
// ✅ 커스텀 설치 배너 (기본 브라우저 프롬프트 대체)
function useInstallPrompt() {
  const [deferredPrompt, setDeferredPrompt] = useState<BeforeInstallPromptEvent | null>(null);

  useEffect(() => {
    const handler = (e: Event) => {
      e.preventDefault();
      setDeferredPrompt(e as BeforeInstallPromptEvent);
    };
    window.addEventListener("beforeinstallprompt", handler);
    return () => window.removeEventListener("beforeinstallprompt", handler);
  }, []);

  const install = async () => {
    if (!deferredPrompt) return;
    await deferredPrompt.prompt();
    const result = await deferredPrompt.userChoice;
    if (result.outcome === "accepted") {
      setDeferredPrompt(null); // 설치 완료
    }
  };

  return { canInstall: !!deferredPrompt, install };
}
```

### 5. 캐싱 전략 요약

| 전략 | 패턴 | 적합 대상 |
|------|------|-----------|
| Cache First | 캐시 → 없으면 네트워크 | 정적 에셋, 폰트, 이미지 |
| Network First | 네트워크 → 실패 시 캐시 | API, 동적 데이터 |
| Stale While Revalidate | 캐시 반환 + 백그라운드 갱신 | 페이지, 자주 변경되는 콘텐츠 |
| Network Only | 항상 네트워크 | 인증, 결제 등 실시간 필수 |
| Cache Only | 캐시에서만 | 오프라인 전용 콘텐츠 |

DON'T:
```typescript
// ❌ 모든 응답을 무조건 캐싱 — 인증 토큰, 개인정보 노출 위험
// handler: "CacheFirst" // 인증 API에 적용? → 다른 사용자 데이터 노출

// ❌ 캐시 무효화 없음 — 오래된 데이터 계속 표시
// maxAgeSeconds 미설정 → 영구 캐시

// ❌ 오프라인 UX 미고려 — 네트워크 에러만 표시
// 오프라인 폴백 페이지 없이 빈 화면 또는 에러 표시
```
