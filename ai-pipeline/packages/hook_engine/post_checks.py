"""Phase 3: POST 검증 체크리스트 생성."""

from __future__ import annotations

# ─── 도메인별 POST 체크리스트 ───

DOMAIN_POST_CHECKS: dict[str, list[str]] = {
    # ─── Development ───
    "development.backend": [
        "모든 입력이 Zod로 검증되는가?",
        "SQL 인젝션 가능 경로가 없는가?",
        "인증 없는 엔드포인트가 의도적인가?",
        "에러 응답이 일관된 형식인가?",
        "환경변수가 하드코딩되지 않았는가?",
        "적절한 HTTP 상태코드를 사용하는가?",
    ],
    "development.frontend": [
        "TypeScript strict 에러가 없는가?",
        "불필요한 리렌더링이 없는가?",
        "로딩/에러/빈 상태를 모두 처리하는가?",
        "모바일 320px에서 깨지지 않는가?",
        "any 타입을 사용하지 않았는가?",
    ],
    "development.database": [
        "3NF 이상 정규화가 적용되었는가?",
        "인덱스가 적절히 설정되었는가?",
        "마이그레이션이 롤백 가능한가?",
        "created_at/updated_at이 모든 테이블에 있는가?",
    ],
    "development.infra": [
        "환경변수가 하드코딩되지 않았는가?",
        ".env 파일이 .gitignore에 포함되었는가?",
        "헬스체크 엔드포인트가 있는가?",
        "Dockerfile에 non-root 유저가 설정되었는가?",
    ],
    "development.security": [
        "OWASP Top 10 취약점이 없는가?",
        "민감 정보가 로그에 노출되지 않는가?",
        "인증/인가가 모든 보호 경로에 적용되었는가?",
        "입력 검증이 서버 측에서 수행되는가?",
        "CORS 설정이 와일드카드가 아닌가?",
    ],
    "development.ai": [
        "LLM 출력 검증 로직이 있는가?",
        "토큰 예산이 설정되었는가?",
        "Rate limit 429 재시도가 구현되었는가?",
        "프롬프트 인젝션 방어가 적용되었는가?",
        "API 키가 환경변수로 관리되는가?",
    ],
    "development.performance": [
        "LCP 2.5초 이내 목표가 충족되는가?",
        "불필요한 번들 사이즈 증가가 없는가?",
        "N+1 쿼리 문제가 없는가?",
        "캐싱 전략이 적절한가?",
    ],
    # ─── Planning ───
    "planning": [
        "각 기능이 문제 정의와 직접 연결되는가?",
        "검증 불가능한 주장에 '[검증 필요]' 태그가 있는가?",
        "MVP 기능이 5개를 초과하지 않는가?",
        "추론과 사실이 명확히 구분되는가?",
    ],
    "planning.business": [
        "TAM/SAM/SOM이 구체적 수치로 제시되는가?",
        "가설-검증 구조로 작성되었는가?",
        "경쟁사 분석이 포함되었는가?",
        "수익 모델이 명시되었는가?",
    ],
    "planning.project-mgmt": [
        "작업이 2주 이내 단위로 분해되었는가?",
        "의존성이 명확히 표시되었는가?",
        "기술부채 항목이 식별되었는가?",
    ],
    # ─── Design ───
    "design": [
        "CTA가 44px 이상인가?",
        "색상 대비 4.5:1 이상인가?",
        "모바일 퍼스트로 설계되었는가?",
        "게슈탈트 원리(근접/유사/폐쇄)가 적용되었는가?",
    ],
    "design.wireframe": [
        "정보 계층이 명확한가?",
        "네비게이션 흐름이 자연스러운가?",
        "핵심 CTA가 눈에 띄는 위치에 있는가?",
    ],
    "design.design-system": [
        "디자인 토큰이 일관되게 사용되는가?",
        "컴포넌트 네이밍 컨벤션이 통일되었는가?",
        "테마 전환(다크모드)이 올바르게 동작하는가?",
    ],
    "design.ux-psychology": [
        "선택지가 7±2 이내인가? (힉스 법칙)",
        "주요 CTA가 엄지 도달 범위 내인가? (피츠 법칙)",
        "기존 멘탈 모델을 따르는가? (제이콥스 법칙)",
        "진행률 표시가 포함되었는가? (자이가르닉 효과)",
    ],
    # ─── Marketing ───
    "marketing": [
        "3초 내 핵심을 파악할 수 있는가?",
        "CTA가 명확하고 구체적인가?",
        "과장/검증불가 주장이 없는가?",
        "AIDA 순서를 따르는가?",
    ],
    "marketing.persuasion": [
        "사회적 증거가 구체적 수치로 제시되는가?",
        "희소성 표현이 진실한가?",
        "행동 유도가 윤리적인가?",
        "사용자의 자율적 선택이 보장되는가?",
    ],
    "marketing.seo": [
        "메타 태그(title, description)가 페이지별 설정되었는가?",
        "canonical URL이 설정되었는가?",
        "구조화 데이터(JSON-LD)가 포함되었는가?",
        "모바일 친화적인가?",
    ],
    "marketing.growth": [
        "CTA가 명확하고 측정 가능한가?",
        "UTM 파라미터가 설정되었는가?",
        "A/B 테스트 가능한 구조인가?",
    ],
    "qa.code-review": [
        "수정 제안이 실제로 컴파일 가능한가?",
        "우선순위가 적절한가?",
        "잘된 점도 언급했는가?",
    ],
    "qa.testing": [
        "테스트 피라미드 비율이 적절한가?",
        "테스트 커버리지 목표가 명시되었는가?",
        "모킹이 과도하지 않은가?",
        "테스트가 독립적이고 반복 가능한가?",
    ],
    # ─── Analytics / Content / QA / Meta ───
    "analytics": [
        "지표 정의가 명확하고 측정 가능한가?",
        "통계적 유의성 기준이 명시되었는가?",
        "심슨의 역설 등 데이터 함정이 고려되었는가?",
    ],
    "content": [
        "핵심 메시지가 첫 문단에 나오는가? (역피라미드)",
        "문장 길이가 25단어 이내인가?",
        "전문 용어에 설명이 달려있는가?",
    ],
    "qa": [
        "수정 제안이 실제로 컴파일 가능한가?",
        "우선순위가 적절한가?",
        "잘된 점도 언급했는가?",
        "테스트 커버리지 목표가 명시되었는가?",
    ],
    "qa.ux-audit": [
        "Nielsen 10가지 휴리스틱이 모두 평가되었는가?",
        "심각도 등급(critical/major/minor)이 매겨졌는가?",
        "개선 권고안이 포함되었는가?",
    ],
    "meta": [
        "확증 편향이 개입되지 않았는가?",
        "생존자 편향 없이 실패 사례도 고려했는가?",
        "계획 오류 없이 현실적 일정인가?",
    ],
}

# ─── 의미 키워드별 추가 체크 ───

KEYWORD_POST_CHECKS: dict[str, list[str]] = {
    "auth": [
        "OWASP Top 10 취약점이 없는가?",
        "민감 정보가 로그에 노출되지 않는가?",
        "토큰 만료 정책이 적용되었는가?",
    ],
    "login": [
        "비밀번호가 해싱 처리되는가?",
        "Rate limiting이 적용되었는가?",
    ],
    "payment": [
        "ACID 트랜잭션이 보장되는가?",
        "멱등성 키가 적용되었는가?",
        "PCI DSS 관련 데이터가 평문 저장되지 않는가?",
    ],
    "file-upload": [
        "파일 타입 검증이 있는가? (magic bytes)",
        "파일 크기 제한이 있는가?",
    ],
    "database": [
        "SELECT *를 사용하지 않았는가?",
        "N+1 쿼리 문제가 없는가?",
    ],
    "security": [
        "CORS 설정이 와일드카드가 아닌가?",
        "HTTPS가 강제되는가?",
        "보안 헤더(CSP, HSTS, Permissions-Policy)가 설정되었는가?",
        "에러 응답에 스택 트레이스/내부 경로가 노출되지 않는가?",
        "API 키가 서버 사이드에서만 사용되는가?",
    ],
    "xss": [
        "dangerouslySetInnerHTML 사용 시 DOMPurify/react-markdown 대체를 검토했는가?",
        "사용자 입력에 HTML 태그 제거(sanitize)가 적용되었는가?",
        "CSP 헤더가 설정되어 있는가?",
        "href/src에 사용자 입력 시 프로토콜 화이트리스트가 적용되었는가?",
    ],
    "sanitize": [
        "Zod transform에서 HTML 태그 제거가 적용되었는가?",
        "이중 인코딩 공격(double encoding)에 대응하는가?",
    ],
    "prompt-injection": [
        "system/user 메시지가 명확히 분리되었는가?",
        "사용자 입력에 인젝션 패턴 새니타이징이 적용되었는가?",
        "LLM 출력에 검증 로직이 있는가?",
        "시스템 프롬프트에 보안 지시사항이 포함되었는가?",
    ],
    "rls": [
        "모든 사용자 데이터 테이블에 RLS가 활성화되었는가?",
        "anonymous 역할에 INSERT/UPDATE/DELETE 정책이 없는가?",
        "service_role 키가 서버 환경변수에만 존재하는가?",
    ],
    "secrets": [
        "API 키가 NEXT_PUBLIC_ 접두사 없이 서버 전용으로 사용되는가?",
        ".env.local이 .gitignore에 포함되어 있는가?",
        "로그에 API 키/토큰이 마스킹되는가?",
    ],
    "ddd": [
        "Bounded Context 경계가 명확한가?",
        "Aggregate Root가 올바르게 설계되었는가?",
    ],
    "microservice": [
        "서비스 간 통신 방식이 명시되었는가?",
        "장애 전파 방지 (Circuit Breaker)가 고려되었는가?",
    ],
    "docker": [
        "멀티스테이지 빌드를 사용하는가?",
        "불필요한 레이어가 없는가?",
    ],
    "monitoring": [
        "Four Golden Signals가 모니터링되는가?",
        "알림 임계값이 설정되었는가?",
    ],
    "ab-testing": [
        "표본 크기가 통계적으로 충분한가?",
        "p-value 기준이 사전에 정의되었는가?",
    ],
    "onboarding": [
        "첫 가치 도달까지 3단계 이내인가?",
        "진행률 표시가 있는가?",
    ],
    "accessibility": [
        "WCAG 2.1 AA 기준을 충족하는가?",
        "키보드 네비게이션이 가능한가?",
        "스크린 리더 호환성이 확인되었는가?",
    ],
    "performance": [
        "Core Web Vitals 기준을 충족하는가?",
        "번들 사이즈가 200KB 이하인가?",
    ],
    "websocket": [
        "연결 인증이 적용되었는가?",
        "하트비트/재연결 로직이 있는가?",
    ],
    "rate-limiting": [
        "Rate limit 초과 시 429 + Retry-After 헤더가 반환되는가?",
    ],
    "webhook": [
        "서명 검증(HMAC-SHA256)이 적용되었는가?",
        "멱등성 키로 중복 처리가 방지되는가?",
    ],
    "graphql": [
        "쿼리 깊이 제한이 설정되었는가?",
        "DataLoader로 N+1이 방지되었는가?",
    ],
    "clean-architecture": [
        "안쪽 계층이 바깥 계층을 import하지 않는가? (의존성 규칙)",
        "비즈니스 로직이 프레임워크에 의존하지 않는가?",
    ],
    "outbox": [
        "이벤트 발행이 DB 트랜잭션과 원자적으로 처리되는가?",
        "컨슈머가 멱등 처리되는가?",
    ],
    "strangler-fig": [
        "신/구 시스템 라우팅이 명확히 분리되었는가?",
        "데이터 동기화 전략이 정의되었는가?",
    ],
    "iac": [
        "인프라가 코드로 정의되었는가? (수동 변경 금지)",
        "시크릿이 코드에 포함되지 않았는가?",
    ],
    "chaos-engineering": [
        "장애 주입 전 폭발 반경이 제한되었는가?",
        "롤백 절차가 사전 준비되었는가?",
    ],
    "bdd": [
        "시나리오가 Given-When-Then 형식인가?",
        "비즈니스 언어로 작성되었는가? (구현 디테일 X)",
    ],
    "funnel": [
        "퍼널 단계가 명확한 이벤트로 측정 가능한가?",
        "세그먼트별 퍼널 분석이 포함되었는가?",
    ],
    "cohort": [
        "코호트 크기가 통계적 유의성을 확보하는가? (최소 100명)",
        "시즌 효과가 보정되었는가?",
    ],
    "dora": [
        "DORA 4개 지표가 세트로 평가되는가?",
        "팀 간 비교가 아닌 시간별 추이로 분석하는가?",
    ],
    "queue": [
        "Dead Letter Queue가 설정되었는가?",
        "핸들러가 멱등적인가?",
    ],
    "resilience": [
        "외부 API 호출에 Circuit Breaker가 적용되었는가?",
        "타임아웃이 계층별로 설정되었는가?",
    ],
    "kubernetes": [
        "리소스 requests/limits가 설정되었는가?",
        "liveness/readiness 프로브가 있는가?",
    ],
    "ux-audit": [
        "Nielsen 10가지 휴리스틱이 검토되었는가?",
        "심각도 등급이 매겨졌는가?",
    ],
    "llm": [
        "토큰 예산이 설정되었는가?",
        "Rate limit 429 재시도가 구현되었는가?",
        "LLM 출력 검증 로직이 있는가?",
    ],
    # ─── Frontend Frameworks ───
    "react": [
        "불필요한 리렌더링이 없는가? (useMemo/useCallback)",
        "key prop이 안정적인 값인가? (index 금지)",
    ],
    "nextjs": [
        "서버/클라이언트 컴포넌트 경계가 명확한가?",
        "메타데이터(title, description)가 페이지별 설정되었는가?",
    ],
    # ─── Architecture Patterns ───
    "hexagonal": [
        "Port/Adapter가 명확히 분리되었는가?",
        "도메인 로직이 외부 인프라에 의존하지 않는가?",
    ],
    "event-sourcing": [
        "이벤트가 불변(immutable)인가?",
        "이벤트 스키마 버전 관리가 고려되었는가?",
    ],
    "gof-patterns": [
        "패턴이 문제 해결을 위해 사용되었는가? (패턴 강박 아닌가?)",
        "SOLID 원칙을 위반하지 않는가?",
    ],
    "repository": [
        "리포지토리가 도메인 언어를 사용하는가? (SQL 노출 금지)",
        "쿼리 메서드가 단일 책임인가?",
    ],
    "solid": [
        "각 클래스가 단일 책임(SRP)을 갖는가?",
        "인터페이스가 클라이언트별로 분리되었는가? (ISP)",
    ],
    # ─── Security ───
    "owasp-api": [
        "API 인증/인가가 모든 엔드포인트에 적용되었는가?",
        "과도한 데이터 노출(Excessive Data Exposure)이 없는가?",
    ],
    "supply-chain": [
        "의존성이 lockfile로 고정되었는가?",
        "알려진 취약점이 있는 패키지가 없는가? (npm audit/safety check)",
    ],
    "mitre": [
        "위협 모델링이 수행되었는가?",
        "탐지 로직이 MITRE ATT&CK 기법과 매핑되었는가?",
    ],
    # ─── Infra / SRE ───
    "observability": [
        "로그/메트릭/트레이스 3축이 구현되었는가?",
        "분산 트레이싱 correlation ID가 전파되는가?",
    ],
    "sre": [
        "SLI/SLO가 정의되었는가?",
        "에러 버짓이 설정되었는가?",
    ],
    "slo": [
        "SLO 목표가 사용자 경험 기반인가?",
        "SLO 위반 시 알림 정책이 있는가?",
    ],
    "incident": [
        "심각도(SEV) 분류 기준이 명확한가?",
        "포스트모템 프로세스가 정의되었는가?",
    ],
    "finops": [
        "리소스에 비용 태그가 적용되었는가?",
        "유휴 리소스 정리 자동화가 있는가?",
    ],
    "cost-optimization": [
        "리소스에 비용 태그가 적용되었는가?",
        "개발환경 자동 종료 스케줄이 있는가?",
    ],
    # ─── Planning ───
    "okr": [
        "Key Result가 측정 가능한 수치인가?",
        "OKR이 상위 목표와 정렬되는가?",
    ],
    "design-sprint": [
        "5일 일정이 명확히 구분되었는가?",
        "프로토타입 테스트 대상이 정의되었는가?",
    ],
    "story-mapping": [
        "사용자 활동(backbone)이 시간 순서로 배치되었는가?",
        "MVP 경계선이 명확한가?",
    ],
    "north-star": [
        "North Star 메트릭이 고객 가치를 반영하는가?",
        "입력 지표(input metrics)가 정의되었는가?",
    ],
    # ─── Marketing / Growth ───
    "aarrr": [
        "AARRR 각 단계의 핵심 지표가 정의되었는가?",
        "단계 간 전환율이 측정 가능한가?",
    ],
    "content-marketing": [
        "타깃 오디언스가 명확히 정의되었는가?",
        "콘텐츠 캘린더가 수립되었는가?",
    ],
    "inbound": [
        "리드 육성(lead nurturing) 흐름이 설계되었는가?",
        "전환 퍼널이 단계별로 추적 가능한가?",
    ],
    # ─── Analytics ───
    "data-pipeline": [
        "파이프라인 실패 시 알림이 설정되었는가?",
        "멱등 재실행이 가능한가?",
    ],
    "etl": [
        "데이터 변환 규칙이 문서화되었는가?",
        "원본 데이터가 보존되는가? (ELT 패턴)",
    ],
    "data-quality": [
        "데이터 유효성 검증 규칙이 자동화되었는가?",
        "이상치(outlier) 탐지가 포함되었는가?",
    ],
    "event-tracking": [
        "이벤트 네이밍 컨벤션이 통일되었는가?",
        "필수 속성(properties)이 누락 없이 전송되는가?",
    ],
    # ─── QA / Testing ───
    "mutation-testing": [
        "뮤턴트 킬 비율이 80% 이상인가?",
        "동등 뮤턴트(equivalent mutant)가 식별되었는가?",
    ],
    "fuzz-testing": [
        "퍼징 대상(입력 표면)이 식별되었는가?",
        "크래시 재현 및 최소화가 수행되는가?",
    ],
    "smoke-test": [
        "핵심 경로가 모두 커버되는가?",
        "배포 직후 자동 실행되는가?",
    ],
    "regression-test": [
        "버그 수정 시 해당 버그 재현 테스트가 추가되었는가?",
        "Flaky 테스트가 격리(quarantine)되었는가?",
    ],
    # ─── Design ───
    "atomic-design": [
        "Atom/Molecule/Organism 계층이 명확한가?",
        "컴포넌트 간 의존성이 단방향인가?",
    ],
    "information-architecture": [
        "네비게이션이 5~7개 이내 주요 메뉴로 구성되었는가?",
        "정보 향기(information scent)가 각 링크에 있는가?",
    ],
    "motion": [
        "애니메이션 시간이 200~500ms 범위인가?",
        "prefers-reduced-motion 미디어 쿼리가 적용되었는가?",
    ],
    "state-management": [
        "전역 상태 최소화 여부",
        "불필요한 리렌더링 방지 확인",
    ],
    "pwa": [
        "Service Worker 등록 확인",
        "오프라인 폴백 페이지 존재",
        "Web App Manifest 유효성",
    ],
    "feature-flag": [
        "플래그 기본값 설정",
        "플래그 정리 주기 계획",
    ],
    "design-tokens": [
        "토큰 네이밍 컨벤션 일관성",
        "다크모드 토큰 매핑 존재",
    ],
    # ─── AI/LLM (New) ───
    "ai-agent": [
        "에이전트 루프에 최대 반복 횟수 제한이 있는가?",
        "도구 호출 결과가 검증되는가?",
    ],
    "guardrails": [
        "입력/출력 가드레일이 모두 적용되었는가?",
        "유해 콘텐츠 필터링이 있는가?",
    ],
    "embedding": [
        "임베딩 차원이 모델과 일치하는가?",
        "텍스트 청킹 전략이 적절한가?",
    ],
    # ─── Content (New) ───
    "api-docs": [
        "모든 엔드포인트에 요청/응답 예시가 있는가?",
        "에러 코드가 문서화되었는가?",
    ],
    "ux-writing": [
        "마이크로카피가 상황에 맞는 톤인가?",
        "에러 메시지가 해결 방법을 안내하는가?",
    ],
    "localization": [
        "날짜/통화 포맷이 로케일에 맞는가?",
        "RTL 언어 지원이 고려되었는가?",
    ],
    # ─── Frontend (New) ───
    "ssr": [
        "서버/클라이언트 하이드레이션 불일치가 없는가?",
        "window/document 참조가 서버에서 안전한가?",
    ],
    "react-native": [
        "네이티브 모듈 링크가 올바른가?",
        "플랫폼별 코드 분기가 적절한가?",
    ],
    "code-splitting": [
        "초기 번들에 불필요한 코드가 포함되지 않았는가?",
        "동적 import의 로딩 상태가 처리되는가?",
    ],
    # ─── Backend (New) ───
    "cache-strategy": [
        "캐시 키 설계가 적절한가? (충돌 방지)",
        "캐시 무효화 전략이 정의되었는가?",
    ],
    "graphql-federation": [
        "서브그래프 간 스키마 충돌이 없는가?",
        "게이트웨이에 쿼리 복잡도 제한이 있는가?",
    ],
    # ─── Infra (New) ───
    "serverless": [
        "콜드 스타트 최적화가 고려되었는가?",
        "실행 시간 제한이 확인되었는가?",
    ],
    "canary": [
        "카나리 비율이 안전한 수준인가? (≤10%)",
        "자동 롤백 조건이 정의되었는가?",
    ],
    "alerting": [
        "알림 피로를 방지하는 임계값 설정인가?",
        "에스컬레이션 정책이 정의되었는가?",
    ],
    # ─── QA (New) ───
    "tdd": [
        "테스트가 구현 코드보다 먼저 작성되었는가?",
        "Red-Green-Refactor 사이클을 따르는가?",
    ],
    "test-doubles": [
        "목(mock)이 과도하게 사용되지 않았는가?",
        "테스트 대역의 동작이 실제 구현과 일치하는가?",
    ],
    "chaos-testing": [
        "장애 주입 전 정상 기준선(baseline)이 측정되었는가?",
        "폭발 반경이 제한되었는가?",
    ],
    # ─── Planning (New) ───
    "roadmap": [
        "로드맵이 시간 기반이 아닌 목표 기반인가?",
        "의존성이 명확히 표시되었는가?",
    ],
    "pricing": [
        "가격 책정 근거가 명시되었는가?",
        "경쟁사 대비 포지셔닝이 고려되었는가?",
    ],
    # ─── Phase 12: New keyword checks ───
    "debounce": [
        "디바운스 딜레이가 적절한가? (300ms 기본)",
        "cleanup이 언마운트 시 실행되는가?",
    ],
    "intersection-observer": [
        "Intersection Observer의 threshold가 적절한가?",
        "unobserve가 cleanup에서 호출되는가?",
    ],
    "offline-first": [
        "오프라인 데이터 동기화 전략이 정의되었는가?",
        "충돌 해결(conflict resolution) 정책이 있는가?",
    ],
    "touch-interaction": [
        "터치 타깃이 44px 이상인가?",
        "스와이프/제스처의 피드백이 즉각적인가?",
    ],
    "render-optimization": [
        "불필요한 리렌더링이 방지되었는가? (memo, useMemo)",
        "가상화(virtualization)가 긴 목록에 적용되었는가?",
    ],
    "snapshot-testing": [
        "스냅샷이 의미 있는 범위만 캡처하는가?",
        "스냅샷 업데이트가 의도적인 변경인지 확인했는가?",
    ],
    "data-governance": [
        "데이터 접근 권한이 역할별로 정의되었는가?",
        "개인정보(PII) 마스킹/암호화가 적용되었는가?",
    ],
    "product-analytics": [
        "핵심 사용자 행동이 이벤트로 추적되는가?",
        "세그먼트별 분석이 가능한 구조인가?",
    ],
    "real-time-analytics": [
        "실시간 처리 지연(latency) 목표가 정의되었는가?",
        "백프레셔(backpressure) 처리가 구현되었는가?",
    ],
    "content-accessibility": [
        "대체 텍스트(alt text)가 모든 이미지에 있는가?",
        "읽기 쉬운 언어(plain language)로 작성되었는가?",
    ],
    "content-metrics": [
        "콘텐츠 KPI가 정의되었는가? (조회수, 체류시간 등)",
        "A/B 테스트로 효과를 측정할 수 있는가?",
    ],
    "content-repurposing": [
        "원본 콘텐츠의 핵심 메시지가 유지되는가?",
        "채널별 포맷이 최적화되었는가?",
    ],
    "content-testing": [
        "제목/CTA의 A/B 테스트가 설계되었는가?",
        "통계적 유의성 기준이 사전 정의되었는가?",
    ],
    "graphql-hybrid": [
        "REST/GraphQL 엔드포인트 간 데이터 일관성이 유지되는가?",
        "클라이언트별 최적 API 방식이 선택되었는가?",
    ],
    "versioning-strategy": [
        "API 버전 관리 방식(URL/헤더)이 통일되었는가?",
        "이전 버전의 지원 종료(sunset) 정책이 있는가?",
    ],
    "animation-principles": [
        "애니메이션이 Disney 12원칙을 따르는가?",
        "prefers-reduced-motion이 존중되는가?",
    ],
    "anchoring-effect": [
        "가격/수치 앵커링이 윤리적인가?",
        "비교 기준이 명확히 제시되는가?",
    ],
    "headline-formula": [
        "헤드라인이 명확한 가치 제안을 포함하는가?",
        "A/B 테스트를 위한 변형이 준비되었는가?",
    ],
    "ab-testing-marketing": [
        "테스트 기간이 충분한가? (최소 2주)",
        "단일 변수 테스트인가? (다변량이면 표본 충분한가?)",
    ],
    "dependency-review": [
        "의존성 라이선스가 프로젝트와 호환되는가?",
        "미사용 의존성이 제거되었는가?",
    ],
    "documentation-review": [
        "공개 API의 문서가 최신인가?",
        "README의 설치/실행 가이드가 정확한가?",
    ],
    "ci-testing": [
        "CI 파이프라인이 PR 머지 전 필수 실행되는가?",
        "테스트 실행 시간이 10분 이내인가?",
    ],
    "error-scenario": [
        "주요 에러 시나리오가 모두 테스트되는가?",
        "에러 메시지가 사용자 친화적인가?",
    ],
    "test-data": [
        "테스트 데이터가 프로덕션과 유사한가?",
        "테스트 간 데이터 격리가 보장되는가?",
    ],
    "performance-audit": [
        "성능 기준선(baseline)이 측정되었는가?",
        "개선 목표가 수치로 정의되었는가?",
    ],
    "estimation-techniques": [
        "추정 방법(planning poker/t-shirt)이 명시되었는가?",
        "불확실성 범위가 표시되었는가?",
    ],
    "rice-scoring": [
        "Reach/Impact/Confidence/Effort가 모두 수치화되었는가?",
        "팀 합의로 점수가 결정되었는가?",
    ],
    "opportunity-tree": [
        "기회가 고객 성과와 연결되는가?",
        "솔루션이 아닌 기회 중심으로 구성되었는가?",
    ],
    "dashboard-monitoring": [
        "대시보드에 핵심 지표(SLI)가 표시되는가?",
        "알림 임계값이 대시보드에서 확인 가능한가?",
    ],
    # ─── Anti-Generic Design ───
    "anti-generic": [
        "3개의 진정으로 다른 디자인 루트가 제시되었는가?",
        "Ban-list에서 제네릭 클리셰가 명시적으로 피해졌는가?",
        "Anti-generic audit이 수행되었는가?",
    ],
    "web-experience": [
        "페이지 전략(청중 온도, 역할, 핵심 주장)이 정의되었는가?",
        "역할 기반 모듈(manifesto/proof band/decision guide)이 사용되었는가?",
        "SaaS 섹션 스택(hero+logo cloud+3 cards+CTA)을 피했는가?",
    ],
    "product-ui": [
        "객체 모델(primary/secondary objects)이 정의되었는가?",
        "쉘 구조가 워크플로우에 특화되어 있는가?",
        "empty/loading/error/permission 상태가 설계되었는가?",
    ],
    "landing-page": [
        "CTA가 above-the-fold에 있는가?",
        "소셜 프루프가 포함되었는가?",
        "내러티브 구조가 제네릭 섹션 스택이 아닌가?",
    ],
    "dashboard": [
        "KPI 카드가 동일한 형태로 반복되지 않는가?",
        "데이터 밀도가 워크플로우에 적합한가?",
    ],
    "styleseed": [
        "단일 강조색 원칙이 지켜졌는가?",
        "섹션 유형이 연속 반복되지 않는가 (visual rhythm)?",
        "그림자가 4-8% opacity 이하인가?",
    ],
    "design-md": [
        "9개 섹션(Theme/Color/Typography/Component/Layout/Depth/Do-Dont/Responsive/Agent)이 포함되었는가?",
        "다크모드 변형이 함께 정의되었는가?",
    ],
    "vuln-analysis": [
        "source-to-sink 경로가 SAST로 열거되었는가?",
        "Multi-Agent(Discovery→Analysis) 파이프라인이 구성되었는가?",
        "False positive 필터링 단계가 있는가?",
    ],
    "vulnerability": [
        "OWASP Top 10 항목이 검토되었는가?",
        "발견된 취약점에 심각도 등급이 매겨졌는가?",
    ],
    "sast": [
        "Semgrep 규칙이 프로젝트 언어에 맞게 설정되었는가?",
        "CI/CD 파이프라인에 자동 스캔이 통합되었는가?",
    ],
}


MAX_POST_CHECKS = 15

# 보안 관련 키워드 — cap 적용 시 우선 보존
_SECURITY_KEYWORDS = frozenset([
    "OWASP", "SQL", "인젝션", "인증", "인가", "XSS", "CORS",
    "토큰", "비밀번호", "해싱", "HTTPS", "민감", "보안", "Rate",
    "ACID", "PCI", "서명", "HMAC", "권한",
])


def _is_security_check(check: str) -> bool:
    return any(kw in check for kw in _SECURITY_KEYWORDS)


def generate_post_checks(
    domains: list[str],
    semantic_keywords: list[str],
) -> list[str]:
    """도메인 + 의미 키워드 기반 POST 검증 체크리스트 생성.

    Returns:
        중복 제거된 체크리스트 항목 리스트 (최대 15개, 보안 항목 우선)
    """
    checks: list[str] = []

    for domain in domains:
        checks.extend(DOMAIN_POST_CHECKS.get(domain, []))

    for keyword in semantic_keywords:
        kw = keyword.lower().strip()
        if kw in KEYWORD_POST_CHECKS:
            checks.extend(KEYWORD_POST_CHECKS[kw])

    # 중복 제거 + 순서 유지
    deduped = list(dict.fromkeys(checks))

    if len(deduped) <= MAX_POST_CHECKS:
        return deduped

    # 보안 항목 우선 보존 후 나머지로 채움
    security = [c for c in deduped if _is_security_check(c)]
    non_security = [c for c in deduped if not _is_security_check(c)]
    result = security[:MAX_POST_CHECKS]
    remaining = MAX_POST_CHECKS - len(result)
    return result + non_security[:remaining]
