"""Phase 1: Haiku 분류 — 도메인/블룸/복잡도/키워드 추출."""

from __future__ import annotations

import json
import logging

import anthropic

from .models import BloomLevel, Session

logger = logging.getLogger(__name__)

CLASSIFY_PROMPT = """다음 요구사항을 분석하세요.

## 요구사항
{user_input}

## 이전 대화 컨텍스트 (있을 경우)
{session_context}

## 분류 기준

도메인 목록 (복수 선택 가능):
- planning: 기획, PRD, 요구사항 정의, 유저 리서치, 페르소나
- planning.business: 비즈니스 모델, 린 스타트업, TAM/SAM/SOM, 디자인 씽킹
- planning.project-mgmt: 프로젝트 관리, 일정, 애자일, 스프린트, 기술부채
- design: UI/UX, 와이어프레임, 디자인 시스템, 컴포넌트 디자인
- design.ux-psychology: UX 심리학, 사용자 행동, 인지 편향, 피츠 법칙, 힉스 법칙
- design.wireframe: 와이어프레임, 레이아웃, 정보 구조
- design.design-system: 디자인 시스템, 토큰, 컴포넌트 라이브러리, 테마
- development.frontend: 프론트엔드, React/Next.js 컴포넌트, 페이지, 훅
- development.backend: API, 서버, 인증, 미들웨어, 엔드포인트
- development.database: DB 스키마, 쿼리, 마이그레이션, 인덱스
- development.infra: 배포, CI/CD, Docker, 모니터링, 환경변수
- development.security: 보안, OWASP, 취약점 분석, 인증 보안, 제로 트러스트
- development.performance: 성능 최적화, Web Vitals, 캐싱 전략, 로드 테스트
- development.ai: LLM 통합, RAG, AI 파이프라인, 프롬프트 엔지니어링, 에이전트
- marketing: 카피, SEO, 광고, 랜딩페이지
- marketing.persuasion: 설득, 행동경제학, 넛지, 전환율 최적화, 소셜 프루프
- marketing.seo: SEO 전략, 기술 SEO, 콘텐츠 SEO, 검색 최적화
- marketing.growth: 그로스해킹, 바이럴, 이메일 마케팅, 소셜미디어
- analytics: 데이터 분석, A/B 테스트, 지표 설계, 통계
- content: 콘텐츠 작성, 기술 문서, 블로그, 카피라이팅
- qa.code-review: 코드 리뷰, 버그 분석, 보안 리뷰
- qa.testing: 테스트 전략, 단위/통합/E2E 테스트, TDD, BDD
- qa.ux-audit: UX 감사, 휴리스틱 평가, 접근성 감사, 인지 워크스루
- meta: 편향 방지, 사고 오류 검증, 메타인지

블룸 레벨:
- REMEMBER: 정보 조회/나열
- UNDERSTAND: 설명/요약/정리
- APPLY: 기존 패턴 적용
- ANALYZE: 구조 분석/원인 파악
- EVALUATE: 비교/평가/리뷰
- CREATE: 새로 생성/구현

복잡도 (0~10):
- 0~3: 단일 도메인, 명확한 요구사항
- 4~6: 다중 도메인 또는 약간 모호
- 7~10: 다중 도메인 + 모호 + 대규모

semantic_keywords: 요구사항에서 감지된 기술적 키워드.
가능한 값: auth, jwt, login, oauth, social-login, mfa, session, password,
payment, database, migration, redis, nosql, multi-tenancy, security,
file-upload, webhook, graphql, graphql-federation, batch, websocket, rate-limiting, third-party,
realtime, caching, cache-strategy, search, i18n, email, crud, dashboard, admin, notification,
analytics, product-analytics, seo, seo-audit, technical-seo, performance, testing, e2e-test, load-test,
ux-audit, bug-analysis, ddd, microservice, event-driven, queue, background-job,
saga, circuit-breaker, bulkhead, dead-letter, resilience, ci-cd, docker, monitoring, scaling,
kubernetes, helm, canary, argocd, feature-flag, rollback, secrets, blue-green, serverless, cdn,
ab-testing, conversion, retention, onboarding, landing-page, email-marketing, growth,
accessibility, dark-mode, animation, styling, state-management, pwa, design-system,
persuasion, bias-check, documentation, api-docs, api-design, pagination, versioning,
llm, rag, ai-agent, ai-integration, embedding, fine-tuning, guardrails, prompt-engineering,
function-calling, token-optimization, multi-modal, eval, streaming,
chain-of-thought, few-shot, tree-of-thought, structured-output,
soft-delete, connection-pooling, filtering, form, routing, hooks, data-fetching,
error-handling, copywriting, ux-writing, social-media, component-test, contract-test,
visual-regression, snapshot-testing, wireframe, interaction, persona, competitive-analysis,
user-story, sprint, prioritization, cognitive-bias, innovation, metrics,
funnel, cohort, dora, bdd, tdd, test-doubles, api-testing, chaos-testing,
property-based, clean-architecture, architecture-review,
strangler-fig, legacy-migration, outbox, nist, iac, terraform,
chaos-engineering, error-messages, microcopy, changelog, release-notes,
cognitive-load, scanning-pattern, progressive-disclosure, empty-states, skeleton-loading, micro-interaction,
react, nextjs, suspense, virtual-list, react-native, ssr, ssg, code-splitting, storybook,
hexagonal, event-sourcing, owasp-api, supply-chain, abac, sso,
observability, opentelemetry, alerting, tracing, capacity-planning, sre, slo, incident, finops,
okr, design-sprint, story-mapping, north-star, roadmap, discovery, pricing, retrospective, stakeholder,
aarrr, content-marketing, inbound, localization, content-strategy,
plg, referral, viral, lifecycle, link-building,
attribution, churn, ltv, segmentation, kpi, sql-optimization,
data-pipeline, etl, data-quality, data-governance, event-tracking,
mutation-testing, fuzz-testing, smoke-test, regression-test,
atomic-design, information-architecture, motion, design-tokens, component-library, theme-system,
micro-frontends, repository, gof-patterns, solid-backend,
debounce, intersection-observer, offline-first, render-optimization

## 분류 예시

예시 1: "로그인 API 만들어줘"
{{"domains": ["development.backend"], "bloom": "CREATE", "complexity": 3, "semantic_keywords": ["auth", "login", "jwt"], "is_followup": false, "reasoning": "백엔드 인증 API 생성"}}

예시 2: "React로 대시보드 페이지 만들어줘, 차트랑 테이블 포함"
{{"domains": ["development.frontend"], "bloom": "CREATE", "complexity": 5, "semantic_keywords": ["dashboard", "react", "state-management"], "is_followup": false, "reasoning": "프론트엔드 대시보드 UI 생성, 차트+테이블 복합"}}

예시 3: "RAG 파이프라인 구축해줘, 벡터DB 연동"
{{"domains": ["development.ai", "development.database"], "bloom": "CREATE", "complexity": 7, "semantic_keywords": ["rag", "embedding", "ai-agent"], "is_followup": false, "reasoning": "AI RAG + DB 연동, 다중 도메인"}}

예시 4: "SEO 최적화 체크리스트 만들어줘"
{{"domains": ["marketing.seo"], "bloom": "APPLY", "complexity": 3, "semantic_keywords": ["seo", "technical-seo", "seo-audit"], "is_followup": false, "reasoning": "SEO 체크리스트 적용"}}

예시 5: "기존 코드 리뷰해줘, 보안 취약점 중심으로"
{{"domains": ["qa.code-review", "development.security"], "bloom": "EVALUATE", "complexity": 5, "semantic_keywords": ["bug-analysis", "security", "owasp-api"], "is_followup": false, "reasoning": "코드 리뷰 + 보안 평가"}}

예시 6: "A/B 테스트 지표 설계하고 분석 방법 정리해줘"
{{"domains": ["analytics"], "bloom": "ANALYZE", "complexity": 4, "semantic_keywords": ["ab-testing", "metrics", "funnel"], "is_followup": false, "reasoning": "분석 도메인, 지표 설계+분석"}}

예시 7: "와이어프레임 만들고 디자인 시스템 토큰 정의해줘"
{{"domains": ["design.wireframe", "design.design-system"], "bloom": "CREATE", "complexity": 6, "semantic_keywords": ["wireframe", "design-tokens", "component-library"], "is_followup": false, "reasoning": "디자인 다중 도메인 생성"}}

예시 8: "이전에 만든 API에 TDD로 테스트 추가해줘"
{{"domains": ["qa.testing"], "bloom": "APPLY", "complexity": 4, "semantic_keywords": ["tdd", "testing", "api-testing"], "is_followup": true, "reasoning": "이전 작업 후속, 테스트 추가"}}

## JSON으로만 응답하세요. 다른 텍스트 없이.
{{"domains": ["도메인1"], "bloom": "CREATE", "complexity": 3, "semantic_keywords": ["auth"], "is_followup": false, "reasoning": "근거 1줄"}}"""


_REQUIRED_KEYS = {"domains", "bloom", "complexity"}


def _is_valid_classification(data: dict) -> bool:
    """파싱된 JSON이 분류 결과인지 검증."""
    return isinstance(data, dict) and _REQUIRED_KEYS.issubset(data.keys())


def _parse_json_response(text: str) -> dict:
    """Claude 응답에서 JSON을 추출한다."""
    # ```json 블록 추출
    if "```" in text:
        for block in text.split("```"):
            block = block.strip()
            if block.startswith("json"):
                block = block[4:].strip()
            try:
                data = json.loads(block)
                if _is_valid_classification(data):
                    return data
            except (json.JSONDecodeError, ValueError):
                continue
    # 순수 JSON
    try:
        data = json.loads(text.strip())
        if _is_valid_classification(data):
            return data
    except (json.JSONDecodeError, ValueError):
        pass
    # 실패 시 기본값
    logger.warning("Failed to parse classification JSON: %s", text[:200])
    return {
        "domains": ["planning"],
        "bloom": "APPLY",
        "complexity": 3,
        "semantic_keywords": [],
        "is_followup": False,
        "reasoning": "parse_failed",
    }


async def classify_with_haiku(
    user_input: str,
    session: Session,
    client: anthropic.AsyncAnthropic | None = None,
) -> dict:
    """Haiku 1회 호출로 도메인/블룸/복잡도/키워드 분류.

    Returns:
        { domains, bloom: BloomLevel, complexity, semantic_keywords, is_followup }
    """
    if client is None:
        client = anthropic.AsyncAnthropic()

    # 세션 컨텍스트 구성
    session_context = "없음 (첫 요청)"
    if session.active_domains:
        recent_skills = session.accumulated_skills[-5:]
        session_context = (
            f"활성 도메인: {session.active_domains}, "
            f"이전 Skill: {recent_skills}"
        )

    prompt = CLASSIFY_PROMPT.format(
        user_input=user_input,
        session_context=session_context,
    )

    try:
        response = await client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text
        result = _parse_json_response(text)
    except Exception as e:
        logger.error("Haiku classification failed: %s", e)
        result = {
            "domains": ["planning"],
            "bloom": "APPLY",
            "complexity": 3,
            "semantic_keywords": [],
            "is_followup": False,
        }

    # BloomLevel enum 변환
    bloom_str = result.get("bloom", "APPLY").upper()
    try:
        bloom = BloomLevel[bloom_str]
    except KeyError:
        bloom = BloomLevel.APPLY

    return {
        "domains": result.get("domains", ["planning"]),
        "bloom": bloom,
        "complexity": max(0, min(int(result.get("complexity", 3)), 10)),
        "semantic_keywords": result.get("semantic_keywords", []),
        "is_followup": result.get("is_followup", False),
    }
