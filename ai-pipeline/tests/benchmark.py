"""Phase 8.5 벤치마크 — 100개 실전 요청으로 파이프라인 품질 평가.

실행: python -m tests.benchmark [--live]
  --live: 실제 API 호출 (비용 발생)
  기본: mock 모드 (분류만 테스트)
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import time
from dataclasses import dataclass, field

logging.basicConfig(level=logging.WARNING)

# ─── 벤치마크 케이스 정의 ───


@dataclass
class BenchmarkCase:
    """벤치마크 테스트 케이스."""
    id: int
    input: str
    expected_domains: list[str]
    expected_keywords: list[str]
    expected_skills_contain: list[str]  # 반드시 포함되어야 할 스킬
    expected_complexity_range: tuple[int, int]  # (min, max)
    expected_model: str  # haiku/sonnet/opus
    category: str  # 분류 카테고리


BENCHMARK_CASES: list[BenchmarkCase] = [
    # ─── Backend (1-5) ───
    BenchmarkCase(
        id=1,
        input="로그인 API 만들어줘. JWT 기반으로.",
        expected_domains=["development.backend"],
        expected_keywords=["auth", "jwt", "login"],
        expected_skills_contain=["dev.backend.auth.role", "dev.backend.auth.jwt-auth"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="backend",
    ),
    BenchmarkCase(
        id=2,
        input="결제 API 설계해줘. 멱등성 보장 필요.",
        expected_domains=["development.backend"],
        expected_keywords=["payment"],
        expected_skills_contain=["dev.backend.api.payment", "dev.backend.patterns.idempotency"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="backend",
    ),
    BenchmarkCase(
        id=3,
        input="PostgreSQL 스키마 설계해줘. 유저, 주문, 상품 테이블.",
        expected_domains=["development.database"],
        expected_keywords=["database"],
        expected_skills_contain=["dev.backend.database.role", "dev.backend.database.schema"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="backend",
    ),
    BenchmarkCase(
        id=4,
        input="간단한 CRUD API 만들어줘",
        expected_domains=["development.backend"],
        expected_keywords=["crud"],
        expected_skills_contain=["dev.backend.api.role", "dev.backend.api.rest"],
        expected_complexity_range=(1, 4),
        expected_model="haiku",
        category="backend",
    ),
    BenchmarkCase(
        id=5,
        input="마이크로서비스 아키텍처로 이벤트 드리븐 주문 시스템 설계해줘. Saga 패턴 적용.",
        expected_domains=["development.backend"],
        expected_keywords=["microservice", "event-driven", "saga"],
        expected_skills_contain=["dev.backend.patterns.saga-pattern", "dev.backend.patterns.event-driven"],
        expected_complexity_range=(7, 10),
        expected_model="opus",
        category="backend",
    ),
    # ─── Frontend (6-8) ───
    BenchmarkCase(
        id=6,
        input="React 대시보드 컴포넌트 만들어줘. 차트랑 테이블 포함.",
        expected_domains=["development.frontend"],
        expected_keywords=["dashboard"],
        expected_skills_contain=["dev.frontend.component.role"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="frontend",
    ),
    BenchmarkCase(
        id=7,
        input="다크모드 지원하는 디자인 시스템 만들어줘",
        expected_domains=["design"],
        expected_keywords=["dark-mode", "design-system"],
        expected_skills_contain=["design.ui-component.role"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="frontend",
    ),
    BenchmarkCase(
        id=8,
        input="폼 유효성 검사 구현해줘. 이메일, 비밀번호, 전화번호 필드.",
        expected_domains=["development.frontend"],
        expected_keywords=["form"],
        expected_skills_contain=["dev.frontend.component.form"],
        expected_complexity_range=(2, 5),
        expected_model="sonnet",
        category="frontend",
    ),
    # ─── Planning (9-12) ───
    BenchmarkCase(
        id=9,
        input="SaaS MVP 기획서 작성해줘. B2B 프로젝트 관리 도구.",
        expected_domains=["planning"],
        expected_keywords=[],
        expected_skills_contain=["planning.prd.role", "planning.prd.mvp"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="planning",
    ),
    BenchmarkCase(
        id=10,
        input="경쟁사 분석해줘. Notion, Monday.com, Asana 비교.",
        expected_domains=["planning"],
        expected_keywords=["competitive-analysis"],
        expected_skills_contain=["planning.competitive-analysis.role"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="planning",
    ),
    BenchmarkCase(
        id=11,
        input="2주 스프린트 플랜 짜줘. 백엔드 API 5개 + 프론트 3페이지.",
        expected_domains=["planning.project-mgmt"],
        expected_keywords=["sprint"],
        expected_skills_contain=["planning.project-mgmt.role"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="planning",
    ),
    BenchmarkCase(
        id=12,
        input="린 캔버스 작성해줘. 온라인 교육 플랫폼.",
        expected_domains=["planning.business"],
        expected_keywords=[],
        expected_skills_contain=["planning.business.role", "planning.business.lean-startup"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="planning",
    ),
    # ─── Marketing (13-15) ───
    BenchmarkCase(
        id=13,
        input="랜딩페이지 카피 써줘. AI 코딩 도구 소개.",
        expected_domains=["marketing"],
        expected_keywords=["landing-page", "copywriting"],
        expected_skills_contain=["marketing.copy.role"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="marketing",
    ),
    BenchmarkCase(
        id=14,
        input="SEO 전략 수립해줘. 기술 블로그 대상.",
        expected_domains=["marketing"],
        expected_keywords=["seo"],
        expected_skills_contain=["marketing.seo.role"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="marketing",
    ),
    BenchmarkCase(
        id=15,
        input="전환율 최적화 전략 세워줘. 가입 퍼널 개선.",
        expected_domains=["marketing.persuasion"],
        expected_keywords=["conversion"],
        expected_skills_contain=["marketing.persuasion.role"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="marketing",
    ),
    # ─── Design + UX (16-17) ───
    BenchmarkCase(
        id=16,
        input="온보딩 플로우 설계해줘. 3단계 이내로.",
        expected_domains=["design.ux-psychology"],
        expected_keywords=["onboarding"],
        expected_skills_contain=["design.ux-psychology.endowed-progress"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="design",
    ),
    BenchmarkCase(
        id=17,
        input="접근성 감사 해줘. WCAG 2.1 AA 기준.",
        expected_domains=["design"],
        expected_keywords=["accessibility"],
        expected_skills_contain=["design.ui-component.accessibility"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="design",
    ),
    # ─── QA + Analytics (18-19) ───
    BenchmarkCase(
        id=18,
        input="코드 리뷰 해줘. 보안 취약점 중심으로.",
        expected_domains=["qa"],
        expected_keywords=["testing"],
        expected_skills_contain=["qa.code-review.role", "qa.code-review.security"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="qa",
    ),
    BenchmarkCase(
        id=19,
        input="A/B 테스트 설계해줘. 가입 버튼 색상 변경.",
        expected_domains=["analytics"],
        expected_keywords=["ab-testing"],
        expected_skills_contain=["analytics.ab-testing"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="analytics",
    ),
    # ─── 복합 (20) ───
    BenchmarkCase(
        id=20,
        input="풀스택 SaaS 만들어줘. 인증, DB, API, 프론트, 배포까지.",
        expected_domains=["development.backend", "development.frontend"],
        expected_keywords=["auth", "database"],
        expected_skills_contain=["dev.backend.api.role", "dev.backend.auth.role"],
        expected_complexity_range=(8, 10),
        expected_model="opus",
        category="complex",
    ),
    # ─── 신규 스킬 검증 (21-30) ───
    BenchmarkCase(
        id=21,
        input="React 커스텀 훅이랑 성능 최적화 패턴 정리해줘.",
        expected_domains=["development.frontend"],
        expected_keywords=["react"],
        expected_skills_contain=["dev.frontend.component.react-patterns", "dev.frontend.component.role"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="frontend",
    ),
    BenchmarkCase(
        id=22,
        input="Next.js App Router로 SSR 페이지 만들어줘.",
        expected_domains=["development.frontend"],
        expected_keywords=["nextjs"],
        expected_skills_contain=["dev.frontend.page.nextjs-patterns"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="frontend",
    ),
    BenchmarkCase(
        id=23,
        input="SRE 팀 SLO/SLI 정의하고 에러 버짓 설정해줘.",
        expected_domains=["development.infra"],
        expected_keywords=["sre", "slo"],
        expected_skills_contain=["dev.infra.deploy.sre"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="infra",
    ),
    BenchmarkCase(
        id=24,
        input="OKR 작성해줘. 다음 분기 엔지니어링 목표.",
        expected_domains=["planning.project-mgmt"],
        expected_keywords=["okr"],
        expected_skills_contain=["planning.project-mgmt.okr"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="planning",
    ),
    BenchmarkCase(
        id=25,
        input="AARRR 퍼널 분석해줘. 모바일 앱 그로스.",
        expected_domains=["marketing.growth"],
        expected_keywords=["aarrr"],
        expected_skills_contain=["marketing.growth.aarrr"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="marketing",
    ),
    BenchmarkCase(
        id=26,
        input="헥사고날 아키텍처로 결제 도메인 리팩토링해줘.",
        expected_domains=["development.backend"],
        expected_keywords=["hexagonal"],
        expected_skills_contain=["dev.backend.patterns.hexagonal"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="backend",
    ),
    BenchmarkCase(
        id=27,
        input="이벤트 소싱으로 주문 이력 관리 시스템 설계해줘.",
        expected_domains=["development.backend"],
        expected_keywords=["event-sourcing"],
        expected_skills_contain=["dev.backend.patterns.event-sourcing"],
        expected_complexity_range=(6, 9),
        expected_model="sonnet",
        category="backend",
    ),
    BenchmarkCase(
        id=28,
        input="Atomic Design으로 컴포넌트 구조 잡아줘.",
        expected_domains=["design"],
        expected_keywords=["atomic-design"],
        expected_skills_contain=["design.ui-component.atomic-design"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="design",
    ),
    BenchmarkCase(
        id=29,
        input="뮤테이션 테스트 도입해줘. 기존 테스트 스위트 품질 평가.",
        expected_domains=["qa"],
        expected_keywords=["mutation-testing"],
        expected_skills_contain=["qa.test-gen.mutation"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="qa",
    ),
    BenchmarkCase(
        id=30,
        input="분산 트레이싱이랑 관측 가능성 시스템 구축해줘. OpenTelemetry 기반.",
        expected_domains=["development.infra"],
        expected_keywords=["observability"],
        expected_skills_contain=["dev.infra.deploy.observability"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="infra",
    ),
    # ─── 확장 벤치마크 (31-50) ───
    BenchmarkCase(
        id=31,
        input="API 엔드포인트 문서를 OpenAPI 스펙 기반으로 작성해줘",
        expected_domains=["content"],
        expected_keywords=["api-docs", "technical-writing"],
        expected_skills_contain=["content.technical-docs"],
        expected_complexity_range=(2, 4),
        expected_model="haiku",
        category="content",
    ),
    BenchmarkCase(
        id=32,
        input="사용자 친화적인 에러 메시지 시스템을 설계해줘",
        expected_domains=["content", "development.frontend"],
        expected_keywords=["error-messages", "ux-writing"],
        expected_skills_contain=["content.error-messages"],
        expected_complexity_range=(4, 6),
        expected_model="sonnet",
        category="content",
    ),
    BenchmarkCase(
        id=33,
        input="실시간 데이터 파이프라인을 Kafka와 Spark로 구축해줘",
        expected_domains=["analytics", "development.backend"],
        expected_keywords=["data-pipeline", "streaming"],
        expected_skills_contain=["analytics.data-pipeline"],
        expected_complexity_range=(6, 8),
        expected_model="sonnet",
        category="analytics",
    ),
    BenchmarkCase(
        id=34,
        input="프로덕트 이벤트 트래킹 시스템을 설계해줘",
        expected_domains=["analytics"],
        expected_keywords=["event-tracking", "analytics"],
        expected_skills_contain=["analytics.event-tracking"],
        expected_complexity_range=(4, 6),
        expected_model="sonnet",
        category="analytics",
    ),
    BenchmarkCase(
        id=35,
        input="데이터 품질 모니터링 대시보드를 만들어줘",
        expected_domains=["analytics", "development.frontend"],
        expected_keywords=["data-quality", "monitoring"],
        expected_skills_contain=["analytics.data-quality"],
        expected_complexity_range=(5, 7),
        expected_model="sonnet",
        category="analytics",
    ),
    BenchmarkCase(
        id=36,
        input="디자인 토큰 시스템을 구축하고 코드로 관리해줘",
        expected_domains=["design"],
        expected_keywords=["design-tokens", "design-system"],
        expected_skills_contain=["design.design-system.tokens"],
        expected_complexity_range=(4, 6),
        expected_model="sonnet",
        category="design",
    ),
    BenchmarkCase(
        id=37,
        input="정보 구조(IA) 설계와 와이어프레임을 만들어줘",
        expected_domains=["design"],
        expected_keywords=["wireframe", "information-architecture"],
        expected_skills_contain=["design.ui-component.role"],
        expected_complexity_range=(3, 5),
        expected_model="sonnet",
        category="design",
    ),
    BenchmarkCase(
        id=38,
        input="React 앱의 전역 상태 관리를 Zustand로 리팩터링해줘",
        expected_domains=["development.frontend"],
        expected_keywords=["state-management", "react"],
        expected_skills_contain=["dev.frontend.component.state-management"],
        expected_complexity_range=(5, 7),
        expected_model="sonnet",
        category="frontend",
    ),
    BenchmarkCase(
        id=39,
        input="기존 웹앱을 PWA로 전환해줘 (오프라인, 푸시 알림)",
        expected_domains=["development.frontend", "development.infra"],
        expected_keywords=["pwa", "offline", "push-notification"],
        expected_skills_contain=["dev.frontend.component.role"],
        expected_complexity_range=(6, 8),
        expected_model="sonnet",
        category="frontend",
    ),
    BenchmarkCase(
        id=40,
        input="Playwright로 E2E 테스트 스위트를 작성해줘",
        expected_domains=["qa.testing"],
        expected_keywords=["e2e-test", "playwright"],
        expected_skills_contain=["qa.test-gen.e2e"],
        expected_complexity_range=(4, 6),
        expected_model="sonnet",
        category="qa",
    ),
    BenchmarkCase(
        id=41,
        input="K6로 부하 테스트 시나리오를 작성해줘",
        expected_domains=["qa.testing"],
        expected_keywords=["load-test", "performance"],
        expected_skills_contain=["qa.test-gen.load-test"],
        expected_complexity_range=(4, 6),
        expected_model="sonnet",
        category="qa",
    ),
    BenchmarkCase(
        id=42,
        input="Kubernetes 배포 매니페스트와 Helm 차트를 만들어줘",
        expected_domains=["development.infra"],
        expected_keywords=["kubernetes", "helm", "deploy"],
        expected_skills_contain=["dev.infra.deploy.kubernetes"],
        expected_complexity_range=(6, 8),
        expected_model="sonnet",
        category="infra",
    ),
    BenchmarkCase(
        id=43,
        input="Feature Flag 시스템을 직접 구현해줘",
        expected_domains=["development.backend"],
        expected_keywords=["feature-flag", "toggle"],
        expected_skills_contain=["dev.backend.api.role"],
        expected_complexity_range=(5, 7),
        expected_model="sonnet",
        category="infra",
    ),
    BenchmarkCase(
        id=44,
        input="1주 디자인 스프린트 계획을 세워줘",
        expected_domains=["planning.business"],
        expected_keywords=["design-sprint", "workshop"],
        expected_skills_contain=["planning.business.design-sprint"],
        expected_complexity_range=(3, 5),
        expected_model="sonnet",
        category="planning",
    ),
    BenchmarkCase(
        id=45,
        input="사용자 스토리 맵을 작성해줘",
        expected_domains=["planning"],
        expected_keywords=["story-mapping", "user-story"],
        expected_skills_contain=["planning.prd.user-story"],
        expected_complexity_range=(3, 5),
        expected_model="sonnet",
        category="planning",
    ),
    BenchmarkCase(
        id=46,
        input="인바운드 마케팅 퍼널 전략을 수립해줘",
        expected_domains=["marketing.growth"],
        expected_keywords=["inbound", "funnel", "content-marketing"],
        expected_skills_contain=["marketing.growth.inbound"],
        expected_complexity_range=(4, 6),
        expected_model="sonnet",
        category="marketing",
    ),
    BenchmarkCase(
        id=47,
        input="이메일 드립 캠페인 시퀀스를 설계해줘",
        expected_domains=["marketing.growth", "marketing.copy"],
        expected_keywords=["email-marketing", "drip-campaign"],
        expected_skills_contain=["marketing.growth.email-sequence"],
        expected_complexity_range=(4, 6),
        expected_model="sonnet",
        category="marketing",
    ),
    BenchmarkCase(
        id=48,
        input="데이터 기반 그로스 해킹 전략을 수립해줘",
        expected_domains=["marketing.growth", "analytics"],
        expected_keywords=["growth", "metrics", "funnel"],
        expected_skills_contain=["marketing.growth.role", "analytics.funnel-analysis"],
        expected_complexity_range=(6, 8),
        expected_model="sonnet",
        category="complex",
    ),
    BenchmarkCase(
        id=49,
        input="SRE 프랙티스와 QA 자동화를 통합 설계해줘",
        expected_domains=["development.infra", "qa.testing"],
        expected_keywords=["sre", "observability", "e2e-test"],
        expected_skills_contain=["dev.infra.sre.role", "qa.test-gen.role"],
        expected_complexity_range=(7, 9),
        expected_model="opus",
        category="complex",
    ),
    BenchmarkCase(
        id=50,
        input="콘텐츠 마케팅 + SEO 통합 전략을 세워줘",
        expected_domains=["content", "marketing.seo"],
        expected_keywords=["content-marketing", "seo", "copywriting"],
        expected_skills_contain=["content.role", "marketing.seo.technical-seo"],
        expected_complexity_range=(5, 7),
        expected_model="sonnet",
        category="complex",
    ),
    # ─── AI/LLM (51-55) ───
    BenchmarkCase(
        id=51,
        input="RAG 파이프라인 구축해줘, 청크 전략이랑 임베딩 모델 선택",
        expected_domains=["development.ai"],
        expected_keywords=["rag", "embedding"],
        expected_skills_contain=["dev.ai.rag-pattern", "dev.ai.embedding"],
        expected_complexity_range=(6, 9),
        expected_model="sonnet",
        category="ai",
    ),
    BenchmarkCase(
        id=52,
        input="AI 에이전트 만들어줘, function calling 기반으로",
        expected_domains=["development.ai"],
        expected_keywords=["ai-agent", "function-calling"],
        expected_skills_contain=["dev.ai.function-calling", "dev.ai.agent-pattern"],
        expected_complexity_range=(6, 9),
        expected_model="sonnet",
        category="ai",
    ),
    BenchmarkCase(
        id=53,
        input="LLM 가드레일 설계해줘, 할루시네이션 방지",
        expected_domains=["development.ai"],
        expected_keywords=["guardrails"],
        expected_skills_contain=["dev.ai.guardrails", "dev.ai.eval-pipeline"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="ai",
    ),
    BenchmarkCase(
        id=54,
        input="프롬프트 엔지니어링 가이드 만들어줘",
        expected_domains=["development.ai", "meta"],
        expected_keywords=["prompt-engineering", "chain-of-thought"],
        expected_skills_contain=["dev.ai.prompt-engineering", "meta.prompt-engineering"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="ai",
    ),
    BenchmarkCase(
        id=55,
        input="멀티모달 AI 서비스 설계, 이미지+텍스트 처리",
        expected_domains=["development.ai"],
        expected_keywords=["multi-modal", "ai-integration"],
        expected_skills_contain=["dev.ai.multi-modal", "dev.ai.streaming-response"],
        expected_complexity_range=(6, 9),
        expected_model="sonnet",
        category="ai",
    ),
    # ─── Security (56-59) ───
    BenchmarkCase(
        id=56,
        input="OWASP Top 10 기반 API 보안 점검해줘",
        expected_domains=["development.security"],
        expected_keywords=["security", "owasp-api"],
        expected_skills_contain=["dev.security.owasp-api", "dev.security.role"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="security",
    ),
    BenchmarkCase(
        id=57,
        input="제로 트러스트 아키텍처 설계",
        expected_domains=["development.security"],
        expected_keywords=["security"],
        expected_skills_contain=["dev.security.zero-trust", "dev.security.role"],
        expected_complexity_range=(7, 10),
        expected_model="opus",
        category="security",
    ),
    BenchmarkCase(
        id=58,
        input="ABAC 기반 권한 시스템 구현",
        expected_domains=["development.backend", "development.security"],
        expected_keywords=["abac", "auth"],
        expected_skills_contain=["dev.backend.auth.abac", "dev.backend.auth.role"],
        expected_complexity_range=(6, 9),
        expected_model="sonnet",
        category="security",
    ),
    BenchmarkCase(
        id=59,
        input="서플라이 체인 보안 점검 체크리스트",
        expected_domains=["development.security"],
        expected_keywords=["supply-chain", "security"],
        expected_skills_contain=["dev.security.supply-chain", "dev.security.role"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="security",
    ),
    # ─── Design System (60-63) ───
    BenchmarkCase(
        id=60,
        input="디자인 토큰 정의해줘, 색상/타이포/스페이싱",
        expected_domains=["design.design-system"],
        expected_keywords=["design-tokens"],
        expected_skills_contain=["design.design-system.tokens"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="design",
    ),
    BenchmarkCase(
        id=61,
        input="컴포넌트 라이브러리 구조 설계",
        expected_domains=["design.design-system"],
        expected_keywords=["component-library"],
        expected_skills_contain=["design.design-system.component-library"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="design",
    ),
    BenchmarkCase(
        id=62,
        input="다크모드 테마 시스템 구현",
        expected_domains=["design.design-system", "development.frontend"],
        expected_keywords=["dark-mode", "theme-system"],
        expected_skills_contain=["design.design-system.theme-system", "design.ui-component.dark-mode"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="design",
    ),
    BenchmarkCase(
        id=63,
        input="와이어프레임 그려줘, 대시보드 레이아웃",
        expected_domains=["design.wireframe"],
        expected_keywords=["wireframe", "dashboard"],
        expected_skills_contain=["design.wireframe.role", "design.wireframe.layout"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="design",
    ),
    # ─── UX Audit (64-66) ───
    BenchmarkCase(
        id=64,
        input="휴리스틱 평가 체크리스트 만들어줘",
        expected_domains=["qa.ux-audit"],
        expected_keywords=["ux-audit"],
        expected_skills_contain=["qa.ux-audit.heuristic-evaluation", "qa.ux-audit.role"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="qa",
    ),
    BenchmarkCase(
        id=65,
        input="접근성 감사 WCAG 2.1 기준으로",
        expected_domains=["qa.ux-audit"],
        expected_keywords=["accessibility"],
        expected_skills_contain=["qa.ux-audit.accessibility-audit", "qa.ux-audit.role"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="qa",
    ),
    BenchmarkCase(
        id=66,
        input="인지 워크스루 진행해줘, 회원가입 플로우",
        expected_domains=["qa.ux-audit"],
        expected_keywords=["ux-audit"],
        expected_skills_contain=["qa.ux-audit.cognitive-walkthrough", "qa.ux-audit.role"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="qa",
    ),
    # ─── Content (67-69) ───
    BenchmarkCase(
        id=67,
        input="API 문서 작성해줘, OpenAPI 스펙 기반",
        expected_domains=["content"],
        expected_keywords=["api-docs", "documentation"],
        expected_skills_contain=["content.api-docs", "content.role"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="content",
    ),
    BenchmarkCase(
        id=68,
        input="UX 라이팅 가이드 만들어줘, 에러 메시지 중심",
        expected_domains=["content"],
        expected_keywords=["ux-writing", "error-messages"],
        expected_skills_contain=["content.ux-writing", "content.error-messages"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="content",
    ),
    BenchmarkCase(
        id=69,
        input="다국어 지원 전략 수립, i18n 포함",
        expected_domains=["content"],
        expected_keywords=["localization", "i18n"],
        expected_skills_contain=["content.localization", "content.role"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="content",
    ),
    # ─── Performance (70-73) ───
    BenchmarkCase(
        id=70,
        input="Web Vitals 최적화해줘, LCP/FID/CLS",
        expected_domains=["development.performance"],
        expected_keywords=["performance"],
        expected_skills_contain=["dev.performance.web-vitals", "dev.performance.role"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="frontend",
    ),
    BenchmarkCase(
        id=71,
        input="Redis 캐싱 전략 설계",
        expected_domains=["development.backend"],
        expected_keywords=["caching", "cache-strategy", "redis"],
        expected_skills_contain=["dev.backend.cache.strategy", "dev.backend.database.redis-patterns"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="frontend",
    ),
    BenchmarkCase(
        id=72,
        input="부하 테스트 시나리오 설계해줘",
        expected_domains=["qa.testing", "development.performance"],
        expected_keywords=["load-test", "testing"],
        expected_skills_contain=["qa.test-gen.load-test", "dev.performance.role"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="frontend",
    ),
    BenchmarkCase(
        id=73,
        input="코드 스플리팅이랑 레이지 로딩 적용",
        expected_domains=["development.frontend"],
        expected_keywords=["code-splitting", "performance"],
        expected_skills_contain=["dev.frontend.performance.code-splitting", "dev.frontend.component.role"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="frontend",
    ),
    # ─── Infra (74-78) ───
    BenchmarkCase(
        id=74,
        input="쿠버네티스 배포 전략 설계, HPA 포함",
        expected_domains=["development.infra"],
        expected_keywords=["kubernetes", "scaling"],
        expected_skills_contain=["dev.infra.deploy.kubernetes", "dev.infra.deploy.scaling"],
        expected_complexity_range=(6, 9),
        expected_model="sonnet",
        category="infra",
    ),
    BenchmarkCase(
        id=75,
        input="모니터링 대시보드 설계, Grafana+Prometheus",
        expected_domains=["development.infra"],
        expected_keywords=["monitoring", "alerting", "observability"],
        expected_skills_contain=["dev.infra.deploy.monitoring", "dev.infra.observability.dashboard"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="infra",
    ),
    BenchmarkCase(
        id=76,
        input="카나리 배포 파이프라인 구축",
        expected_domains=["development.infra"],
        expected_keywords=["canary", "ci-cd"],
        expected_skills_contain=["dev.infra.deploy.canary", "dev.infra.ci.role"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="infra",
    ),
    BenchmarkCase(
        id=77,
        input="서버리스 아키텍처 설계, Lambda 기반",
        expected_domains=["development.infra"],
        expected_keywords=["serverless"],
        expected_skills_contain=["dev.infra.cloud.serverless", "dev.infra.deploy.role"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="infra",
    ),
    BenchmarkCase(
        id=78,
        input="알럿 규칙 설계, 온콜 프로세스 포함",
        expected_domains=["development.infra"],
        expected_keywords=["alerting", "sre", "incident"],
        expected_skills_contain=["dev.infra.observability.alerting", "dev.infra.sre.incident-response"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="infra",
    ),
    # ─── Complex Cross-domain (79-85) ───
    BenchmarkCase(
        id=79,
        input="풀스택 이커머스, 결제+배송+재고관리",
        expected_domains=["development.backend", "development.frontend", "development.database"],
        expected_keywords=["payment", "crud"],
        expected_skills_contain=["dev.backend.api.payment", "dev.frontend.component.role", "dev.backend.database.role"],
        expected_complexity_range=(8, 10),
        expected_model="opus",
        category="complex",
    ),
    BenchmarkCase(
        id=80,
        input="SaaS 멀티테넌시 아키텍처 전체 설계",
        expected_domains=["development.backend", "development.database", "development.security"],
        expected_keywords=["multi-tenancy", "auth", "database"],
        expected_skills_contain=["dev.backend.database.multi-tenancy", "dev.backend.auth.role", "dev.security.role"],
        expected_complexity_range=(8, 10),
        expected_model="opus",
        category="complex",
    ),
    BenchmarkCase(
        id=81,
        input="실시간 채팅 서비스 구현, WebSocket+Redis",
        expected_domains=["development.backend", "development.frontend"],
        expected_keywords=["websocket", "realtime", "redis"],
        expected_skills_contain=["dev.backend.websocket.connection", "dev.backend.database.redis-patterns", "dev.frontend.component.role"],
        expected_complexity_range=(7, 10),
        expected_model="opus",
        category="complex",
    ),
    BenchmarkCase(
        id=82,
        input="마이크로서비스 전환 전략, 모놀리스에서",
        expected_domains=["development.backend", "development.infra"],
        expected_keywords=["microservice", "event-driven", "docker"],
        expected_skills_contain=["dev.backend.patterns.strangler-fig", "dev.backend.patterns.event-driven", "dev.infra.deploy.docker"],
        expected_complexity_range=(8, 10),
        expected_model="opus",
        category="complex",
    ),
    BenchmarkCase(
        id=83,
        input="데이터 파이프라인 ETL + 대시보드",
        expected_domains=["analytics", "development.database"],
        expected_keywords=["data-pipeline", "etl", "dashboard"],
        expected_skills_contain=["analytics.data-pipeline", "analytics.data-visualization", "dev.backend.database.role"],
        expected_complexity_range=(7, 10),
        expected_model="opus",
        category="complex",
    ),
    BenchmarkCase(
        id=84,
        input="CI/CD + 모니터링 + 카나리 배포 풀셋업",
        expected_domains=["development.infra"],
        expected_keywords=["ci-cd", "monitoring", "canary", "docker"],
        expected_skills_contain=["dev.infra.ci.pipeline", "dev.infra.deploy.monitoring", "dev.infra.deploy.canary", "dev.infra.deploy.docker"],
        expected_complexity_range=(7, 10),
        expected_model="opus",
        category="complex",
    ),
    BenchmarkCase(
        id=85,
        input="디자인 시스템 + 프론트엔드 컴포넌트 구현",
        expected_domains=["design.design-system", "development.frontend"],
        expected_keywords=["design-tokens", "component-library", "react"],
        expected_skills_contain=["design.design-system.tokens", "design.design-system.component-library", "dev.frontend.component.role"],
        expected_complexity_range=(7, 10),
        expected_model="opus",
        category="complex",
    ),
    # ─── Analytics (86-88) ───
    BenchmarkCase(
        id=86,
        input="어트리뷰션 모델 설계해줘, 마케팅 채널별",
        expected_domains=["analytics"],
        expected_keywords=["attribution", "metrics"],
        expected_skills_contain=["analytics.attribution-model", "analytics.role"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="analytics",
    ),
    BenchmarkCase(
        id=87,
        input="LTV 예측 모델이랑 이탈 분석",
        expected_domains=["analytics"],
        expected_keywords=["ltv", "churn", "segmentation"],
        expected_skills_contain=["analytics.ltv-calculation", "analytics.churn-prediction"],
        expected_complexity_range=(6, 9),
        expected_model="sonnet",
        category="analytics",
    ),
    BenchmarkCase(
        id=88,
        input="데이터 거버넌스 정책 수립",
        expected_domains=["analytics"],
        expected_keywords=["data-governance", "data-quality"],
        expected_skills_contain=["analytics.data-governance", "analytics.data-quality"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="analytics",
    ),
    # ─── Planning (89-92) ───
    BenchmarkCase(
        id=89,
        input="제품 로드맵 작성해줘, 분기별",
        expected_domains=["planning"],
        expected_keywords=["roadmap"],
        expected_skills_contain=["planning.roadmap", "planning.prd.role"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="planning",
    ),
    BenchmarkCase(
        id=90,
        input="디자인 스프린트 5일 프로세스 설계",
        expected_domains=["planning"],
        expected_keywords=["design-sprint", "discovery"],
        expected_skills_contain=["planning.business.design-sprint", "planning.discovery"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="planning",
    ),
    BenchmarkCase(
        id=91,
        input="디스커버리 단계 리서치 계획",
        expected_domains=["planning"],
        expected_keywords=["discovery", "persona"],
        expected_skills_contain=["planning.discovery", "planning.user-persona.role"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="planning",
    ),
    BenchmarkCase(
        id=92,
        input="이해관계자 매핑이랑 커뮤니케이션 플랜",
        expected_domains=["planning"],
        expected_keywords=["stakeholder"],
        expected_skills_contain=["planning.project-mgmt.stakeholder-management", "planning.project-mgmt.role"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="planning",
    ),
    # ─── Meta (93-95) ───
    BenchmarkCase(
        id=93,
        input="편향 검증 체크리스트 만들어줘",
        expected_domains=["meta"],
        expected_keywords=["bias-check", "cognitive-bias"],
        expected_skills_contain=["meta.bias-prevention.role", "meta.bias-prevention.confirmation-bias"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="complex",
    ),
    BenchmarkCase(
        id=94,
        input="Chain-of-Thought 프롬프트 설계",
        expected_domains=["meta", "development.ai"],
        expected_keywords=["chain-of-thought", "prompt-engineering"],
        expected_skills_contain=["meta.chain-of-thought", "dev.ai.prompt-engineering"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="complex",
    ),
    BenchmarkCase(
        id=95,
        input="구조화된 출력 형식 설계, JSON 스키마",
        expected_domains=["meta"],
        expected_keywords=["structured-output"],
        expected_skills_contain=["meta.structured-output", "meta.output-formatting"],
        expected_complexity_range=(3, 6),
        expected_model="sonnet",
        category="complex",
    ),
    # ─── Growth/Marketing (96-100) ───
    BenchmarkCase(
        id=96,
        input="PLG 전략 수립, 프리미엄→유료 전환",
        expected_domains=["marketing.growth"],
        expected_keywords=["plg", "conversion"],
        expected_skills_contain=["marketing.growth.plg", "marketing.growth.role"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="marketing",
    ),
    BenchmarkCase(
        id=97,
        input="바이럴 루프 설계, 레퍼럴 시스템",
        expected_domains=["marketing.growth"],
        expected_keywords=["viral", "referral"],
        expected_skills_contain=["marketing.growth.viral-loop", "marketing.growth.referral-loop"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="marketing",
    ),
    BenchmarkCase(
        id=98,
        input="라이프사이클 마케팅 이메일 시퀀스",
        expected_domains=["marketing.growth"],
        expected_keywords=["lifecycle", "email-marketing"],
        expected_skills_contain=["marketing.growth.lifecycle-marketing", "marketing.growth.email-sequence"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="marketing",
    ),
    BenchmarkCase(
        id=99,
        input="인바운드 마케팅 전략, 콘텐츠 중심",
        expected_domains=["marketing.growth"],
        expected_keywords=["inbound", "content-marketing"],
        expected_skills_contain=["marketing.growth.inbound", "marketing.growth.content-marketing"],
        expected_complexity_range=(4, 7),
        expected_model="sonnet",
        category="marketing",
    ),
    BenchmarkCase(
        id=100,
        input="링크 빌딩 전략이랑 SEO 시너지",
        expected_domains=["marketing.seo", "marketing.growth"],
        expected_keywords=["link-building", "seo"],
        expected_skills_contain=["marketing.seo.link-building", "marketing.seo.role"],
        expected_complexity_range=(5, 8),
        expected_model="sonnet",
        category="marketing",
    ),
]


# ─── 평가 로직 ───


@dataclass
class CaseResult:
    case_id: int
    category: str
    # 도메인 정확도
    domain_precision: float = 0.0
    domain_recall: float = 0.0
    # 키워드 정확도
    keyword_recall: float = 0.0
    # 스킬 적합도
    skill_recall: float = 0.0
    skill_count: int = 0
    # 복잡도/모델
    complexity_in_range: bool = False
    model_correct: bool = False
    # 종합
    score: float = 0.0
    errors: list[str] = field(default_factory=list)


def evaluate_case(
    case: BenchmarkCase,
    domains: list[str],
    keywords: list[str],
    skills: list[str],
    complexity: int,
    model: str,
) -> CaseResult:
    """단일 케이스 평가."""
    result = CaseResult(case_id=case.id, category=case.category)
    errors = []

    # 도메인 precision/recall
    expected_set = set(case.expected_domains)
    actual_set = set(domains)
    if actual_set:
        result.domain_precision = len(expected_set & actual_set) / len(actual_set)
    if expected_set:
        result.domain_recall = len(expected_set & actual_set) / len(expected_set)
    if result.domain_recall < 1.0:
        missing = expected_set - actual_set
        errors.append(f"도메인 누락: {missing}")

    # 키워드 recall
    if case.expected_keywords:
        matched = sum(1 for k in case.expected_keywords if k in keywords)
        result.keyword_recall = matched / len(case.expected_keywords)
        if result.keyword_recall < 1.0:
            missing = [k for k in case.expected_keywords if k not in keywords]
            errors.append(f"키워드 누락: {missing}")
    else:
        result.keyword_recall = 1.0

    # 스킬 recall
    result.skill_count = len(skills)
    if case.expected_skills_contain:
        matched = sum(1 for s in case.expected_skills_contain if s in skills)
        result.skill_recall = matched / len(case.expected_skills_contain)
        if result.skill_recall < 1.0:
            missing = [s for s in case.expected_skills_contain if s not in skills]
            errors.append(f"스킬 누락: {missing}")
    else:
        result.skill_recall = 1.0

    # 복잡도
    lo, hi = case.expected_complexity_range
    result.complexity_in_range = lo <= complexity <= hi
    if not result.complexity_in_range:
        errors.append(f"복잡도 범위 밖: {complexity} (기대: {lo}-{hi})")

    # 모델
    result.model_correct = model == case.expected_model
    if not result.model_correct:
        errors.append(f"모델 불일치: {model} (기대: {case.expected_model})")

    # 종합 점수 (가중 평균)
    result.score = (
        result.domain_recall * 0.25
        + result.keyword_recall * 0.15
        + result.skill_recall * 0.35
        + (1.0 if result.complexity_in_range else 0.0) * 0.15
        + (1.0 if result.model_correct else 0.0) * 0.10
    )
    result.errors = errors
    return result


# ─── 실행 ───


async def run_benchmark_mock() -> list[CaseResult]:
    """Mock 모드: Haiku 분류 없이 정적 스킬 선택만 평가."""
    from packages.hook_engine.models import Session
    from packages.hook_engine.selector import select_skills

    results: list[CaseResult] = []

    for case in BENCHMARK_CASES:
        session = Session(session_id=f"bench-{case.id}")

        # 도메인/키워드를 기대값으로 직접 주입 (분류 정확도가 아닌 스킬 선택 정확도 측정)
        skills = select_skills(
            case.expected_domains,
            case.expected_keywords,
            case.expected_complexity_range[0],
            session,
        )

        # 복잡도 중간값 사용 (모델 선택 정확도 반영)
        lo, hi = case.expected_complexity_range
        complexity = (lo + hi) // 2
        if complexity <= 3:
            model = "haiku"
        elif complexity <= 6:
            model = "sonnet"
        else:
            model = "opus"

        result = evaluate_case(
            case,
            domains=case.expected_domains,
            keywords=case.expected_keywords,
            skills=skills,
            complexity=complexity,
            model=model,
        )
        results.append(result)

    return results


async def run_benchmark_live() -> list[CaseResult]:
    """Live 모드: 실제 Haiku 분류 + 스킬 선택."""
    from packages.hook_engine.engine import run_hook_engine

    results: list[CaseResult] = []

    for case in BENCHMARK_CASES:
        try:
            plan = await run_hook_engine(
                user_input=case.input,
                session_id=f"bench-live-{case.id}",
            )

            result = evaluate_case(
                case,
                domains=plan.domains,
                keywords=[],  # 분류기가 반환한 키워드는 plan에 없으므로 빈값
                skills=plan.skill_ids,
                complexity=plan.complexity,
                model=plan.executor_model,
            )
        except Exception as e:
            result = CaseResult(case_id=case.id, category=case.category, errors=[str(e)])

        results.append(result)

    return results


def print_report(results: list[CaseResult]) -> None:
    """벤치마크 리포트 출력."""
    print("\n" + "=" * 70)
    print("  Phase 8.5 벤치마크 리포트")
    print("=" * 70)

    total_score = 0.0
    category_scores: dict[str, list[float]] = {}

    for r in results:
        status = "✓" if r.score >= 0.7 else "△" if r.score >= 0.5 else "✗"
        print(f"\n  [{status}] Case {r.case_id:2d} ({r.category:10s}) — score: {r.score:.2f}")
        print(f"       domain_recall={r.domain_recall:.2f}  keyword_recall={r.keyword_recall:.2f}  "
              f"skill_recall={r.skill_recall:.2f}  skills={r.skill_count}")
        if r.errors:
            for e in r.errors:
                print(f"       ⚠ {e}")

        total_score += r.score
        category_scores.setdefault(r.category, []).append(r.score)

    avg = total_score / len(results) if results else 0
    print(f"\n{'─' * 70}")
    print(f"  종합 평균: {avg:.2f} / 1.00  ({len(results)}개 케이스)")
    print(f"  7점+ 달성: {sum(1 for r in results if r.score >= 0.7)}/{len(results)}")

    print("\n  카테고리별:")
    for cat, scores in sorted(category_scores.items()):
        cat_avg = sum(scores) / len(scores)
        print(f"    {cat:12s}: {cat_avg:.2f} ({len(scores)}개)")

    # 스킬 recall이 낮은 케이스 경고
    low_recall = [r for r in results if r.skill_recall < 0.8]
    if low_recall:
        print(f"\n  ⚠ 스킬 recall < 0.8 케이스: {[r.case_id for r in low_recall]}")

    print()


async def main() -> None:
    parser = argparse.ArgumentParser(description="Phase 8.5 벤치마크")
    parser.add_argument("--live", action="store_true", help="실제 API 호출 모드")
    args = parser.parse_args()

    start = time.time()

    if args.live:
        print("🔴 Live mode — 실제 API 호출 (비용 발생)")
        results = await run_benchmark_live()
    else:
        print("🟢 Mock mode — 정적 스킬 선택만 평가")
        results = await run_benchmark_mock()

    elapsed = time.time() - start
    print_report(results)
    print(f"  실행 시간: {elapsed:.2f}s")


if __name__ == "__main__":
    asyncio.run(main())
