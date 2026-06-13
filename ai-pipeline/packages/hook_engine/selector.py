"""Phase 2: Skill 선택 — 도메인 + 키워드 + 복잡도 기반 확정적 선택.

정적 선택(select_skills)과 그래프 기반 하이브리드 선택(select_skills_hybrid)을 제공.
그래프 DB 미가용 시 정적 선택으로 자동 폴백.
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

from .models import Session

logger = logging.getLogger(__name__)

# ─── Token Budget Limits (per model context) ───
MODEL_CONTEXT_LIMITS = {
    "haiku": 8000,    # max system prompt tokens for haiku
    "sonnet": 16000,  # max system prompt tokens for sonnet
    "opus": 32000,    # max system prompt tokens for opus
}

# Skill type priority (higher = kept first when over budget)
SKILL_TYPE_PRIORITY = {
    "role": 5,
    "stack": 4,
    "rule": 3,
    "pattern": 2,
    "verify": 1,
}

SKILL_DIR = Path(os.getenv("SKILL_DIR", Path(__file__).resolve().parent.parent.parent / "skills"))

# ─── 도메인 → 기본 Atomic Skill 매핑 ───

BASE_SKILLS: dict[str, list[str]] = {
    # ─── Development ───
    "development.backend": [
        "dev.backend.api.role",
        "dev.backend.api.rest",
        "dev.backend.api.validation",
        "dev.backend.api.error",
        "dev.backend.api.middleware",
        "dev.backend.api.verify",
        "dev.backend.api.logging",
    ],
    "development.frontend": [
        "dev.frontend.component.role",
        "dev.frontend.component.solid",
        "dev.frontend.component.stack",
        "dev.frontend.component.verify",
        "dev.frontend.page.role",
        "dev.frontend.page.routing",
        "dev.frontend.page.verify",
    ],
    "development.database": [
        "dev.backend.database.role",
        "dev.backend.database.schema",
        "dev.backend.database.query",
        "dev.backend.database.transaction",
        "dev.backend.database.verify",
    ],
    "development.infra": [
        "dev.infra.deploy.role",
        "dev.infra.deploy.env",
        "dev.infra.deploy.docker",
        "dev.infra.deploy.verify",
        "dev.infra.deploy.monitoring",
        "dev.infra.deploy.scaling",
    ],
    "development.security": [
        "dev.security.role",
        "dev.security.owasp",
        "dev.security.cia-triad",
        "dev.security.stride",
        "dev.security.nist-framework",
        "dev.security.defense-in-depth",
        "dev.security.zero-trust",
        "dev.security.verify",
    ],
    "development.performance": [
        "dev.performance.role",
        "dev.performance.web-vitals",
        "dev.performance.caching",
        "dev.performance.budget",
        "dev.performance.amdahl",
        "dev.performance.verify",
    ],
    "development.ai": [
        "dev.ai.prompt-engineering",
        "dev.ai.rag-pattern",
        "dev.ai.function-calling",
        "dev.ai.guardrails",
        "dev.ai.agent-pattern",
        "dev.ai.token-optimization",
        "dev.ai.eval-pipeline",
        "dev.ai.streaming-response",
        "dev.ai.embedding",
        "dev.ai.memory-pattern",
    ],
    # ─── Planning ───
    "planning": [
        "planning.prd.role",
        "planning.prd.jtbd",
        "planning.prd.mvp",
        "planning.prd.user-story",
        "planning.prd.risk",
        "planning.prd.verify",
        "planning.prd.anti-halluc",
    ],
    "planning.business": [
        "planning.business.role",
        "planning.business.lean-startup",
        "planning.business.design-thinking",
        "planning.business.double-diamond",
        "planning.business.tam",
        "planning.business.verify",
    ],
    "planning.project-mgmt": [
        "planning.project-mgmt.role",
        "planning.project-mgmt.agile",
        "planning.project-mgmt.kanban",
        "planning.project-mgmt.estimation",
        "planning.project-mgmt.tech-debt",
        "planning.project-mgmt.verify",
    ],
    # ─── Design ───
    "design": [
        "design.ui-component.role",
        "design.ui-component.gestalt",
        "design.ui-component.typography",
        "design.ui-component.spacing",
        "design.ui-component.responsive",
        "design.ui-component.accessibility",
        "design.ui-component.verify",
        "design.ux-rules.accessibility-touch",
        "design.ux-rules.visual-design",
        "design.anti-generic.role",
        "design.styleseed.visual-rules",
    ],
    "design.ux-psychology": [
        "design.ux-psychology.role",
        "design.ux-psychology.fitts-law",
        "design.ux-psychology.hicks-law",
        "design.ux-psychology.jakobs-law",
        "design.ux-psychology.peak-end",
        "design.ux-psychology.von-restorff",
        "design.ux-psychology.serial-position",
        "design.ux-psychology.aesthetic-usability",
        "design.ux-psychology.doherty-threshold",
        "design.ux-psychology.recognition-over-recall",
        "design.ux-psychology.teslers-law",
        "design.ux-psychology.endowed-progress",
        "design.ux-psychology.zeigarnik",
        "design.ux-psychology.verify",
    ],
    # ─── Marketing ───
    "marketing": [
        "marketing.copy.role",
        "marketing.copy.aida",
        "marketing.copy.headline",
        "marketing.copy.storytelling",
        "marketing.copy.cta",
        "marketing.copy.verify",
    ],
    "marketing.persuasion": [
        "marketing.persuasion.role",
        "marketing.persuasion.hook-model",
        "marketing.persuasion.social-proof",
        "marketing.persuasion.reciprocity",
        "marketing.persuasion.authority",
        "marketing.persuasion.scarcity",
        "marketing.persuasion.verify",
    ],
    "marketing.seo": [
        "marketing.seo.role",
        "marketing.seo.technical-seo",
        "marketing.seo.content-seo",
        "marketing.seo.verify",
    ],
    "marketing.growth": [
        "marketing.growth.role",
        "marketing.growth.growth-hack",
        "marketing.growth.landing-page",
        "marketing.growth.social-media",
        "marketing.growth.email-sequence",
        "marketing.growth.verify",
    ],
    # ─── Analytics / Content / QA / Meta ───
    "analytics": [
        "analytics.role",
        "analytics.ab-testing",
        "analytics.metrics",
        "analytics.funnel-analysis",
        "analytics.cohort-analysis",
        "analytics.bayesian",
        "analytics.verify",
        "analytics.kpi-framework",
        "analytics.data-visualization",
    ],
    "content": [
        "content.role",
        "content.inverted-pyramid",
        "content.readability",
        "content.structure",
        "content.technical-docs",
        "content.verify",
        "content.tone-voice",
        "content.content-strategy",
    ],
    # qa는 후방호환을 위해 유지, qa.code-review / qa.testing 추가
    "qa": [
        "qa.code-review.role",
        "qa.code-review.priority",
        "qa.code-review.readability",
        "qa.code-review.security",
        "qa.code-review.verify",
        "qa.test-gen.role",
        "qa.test-gen.integration",
        "qa.test-gen.verify",
    ],
    "qa.code-review": [
        "qa.code-review.role",
        "qa.code-review.priority",
        "qa.code-review.readability",
        "qa.code-review.security",
        "qa.code-review.bug-analysis",
        "qa.code-review.performance",
        "qa.code-review.verify",
        "qa.code-review.code-smell",
        "qa.code-review.naming-convention",
    ],
    "qa.testing": [
        "qa.test-gen.role",
        "qa.test-gen.unit",
        "qa.test-gen.integration",
        "qa.test-gen.testing-trophy",
        "qa.test-gen.verify",
        "qa.test-gen.tdd",
        "qa.test-gen.test-strategy",
    ],
    "meta": [
        "meta.bias-prevention.role",
        "meta.bias-prevention.confirmation-bias",
        "meta.bias-prevention.availability-bias",
        "meta.bias-prevention.planning-fallacy",
        "meta.bias-prevention.verify",
        "meta.output-validator",
        "meta.prompt-engineering",
        "meta.structured-output",
    ],
    "design.design-system": [
        "design.design-system.tokens",
        "design.design-system.component-library",
        "design.design-system.theme-system",
        "design.design-system.documentation",
        "design.design-system.versioning",
        "design.design-md.template",
    ],
    "design.wireframe": [
        "design.wireframe.role",
        "design.wireframe.layout",
        "design.wireframe.information-architecture",
        "design.wireframe.verify",
    ],
    "qa.ux-audit": [
        "qa.ux-audit.role",
        "qa.ux-audit.heuristic-evaluation",
        "qa.ux-audit.cognitive-walkthrough",
        "qa.ux-audit.accessibility-audit",
        "qa.ux-audit.verify",
    ],
}

# ─── 의미 키워드 → 조건부 Atomic Skill ───

KEYWORD_SKILLS: dict[str, list[str]] = {
    # ─── Auth / Security ───
    "auth": [
        "dev.backend.auth.role", "dev.backend.auth.jwt-auth",
        "dev.backend.auth.rbac", "dev.backend.auth.verify",
    ],
    "jwt": ["dev.backend.auth.jwt-auth", "dev.backend.auth.role"],
    "login": ["dev.backend.auth.jwt-auth", "dev.backend.auth.password", "dev.backend.api.security"],
    "oauth": ["dev.backend.auth.oauth-flow", "dev.backend.auth.role"],
    "social-login": ["dev.backend.auth.oauth-flow", "dev.backend.auth.role"],
    "mfa": ["dev.backend.auth.mfa", "dev.backend.auth.role"],
    "session": ["dev.backend.auth.session-auth", "dev.backend.auth.role"],
    "password": ["dev.backend.auth.password", "dev.backend.auth.role"],
    "security": [
        "dev.security.role", "dev.security.owasp", "dev.security.cia-triad",
        "dev.security.stride", "dev.security.swiss-cheese", "dev.security.saltzer",
        "dev.security.secure-by-design", "dev.security.defense-in-depth",
        "dev.security.zero-trust", "dev.security.verify",
        "dev.backend.security.security-headers", "dev.backend.security.secrets-hygiene",
        "dev.backend.security.error-exposure",
    ],
    "xss": [
        "dev.frontend.security.xss-prevention", "dev.backend.security.input-sanitization",
        "dev.backend.security.security-headers", "dev.security.owasp",
    ],
    "sanitize": [
        "dev.backend.security.input-sanitization", "dev.frontend.security.xss-prevention",
    ],
    "sanitization": [
        "dev.backend.security.input-sanitization", "dev.frontend.security.xss-prevention",
    ],
    "csp": ["dev.backend.security.security-headers"],
    "hsts": ["dev.backend.security.security-headers"],
    "security-headers": ["dev.backend.security.security-headers"],
    "prompt-injection": [
        "dev.ai.prompt-injection", "dev.ai.guardrails",
    ],
    "rls": [
        "dev.backend.database.rls-policy", "dev.backend.database.multi-tenancy",
    ],
    "row-level-security": ["dev.backend.database.rls-policy"],
    "payment": [
        "dev.backend.api.payment", "dev.backend.auth.jwt-auth",
        "dev.backend.patterns.idempotency",
    ],
    # ─── Data ───
    "database": [
        "dev.backend.database.schema", "dev.backend.database.query",
        "dev.backend.database.index", "dev.backend.database.transaction",
    ],
    "migration": ["dev.backend.database.schema", "dev.backend.database.migration"],
    "search": [
        "dev.backend.api.search", "dev.backend.api.filtering",
        "dev.backend.database.query", "dev.backend.database.index",
    ],
    "redis": ["dev.backend.database.redis-patterns"],
    "nosql": ["dev.backend.database.nosql-patterns"],
    "multi-tenancy": ["dev.backend.database.multi-tenancy"],
    "soft-delete": ["dev.backend.database.soft-delete"],
    "connection-pooling": ["dev.backend.database.connection-pooling"],
    # ─── API Design ───
    "crud": ["dev.backend.api.rest", "dev.backend.api.validation"],
    "api-design": ["dev.backend.api.rest", "dev.backend.api.versioning", "dev.backend.api.pagination"],
    "pagination": ["dev.backend.api.pagination"],
    "versioning": ["dev.backend.api.versioning"],
    "filtering": ["dev.backend.api.filtering", "dev.backend.api.search"],
    # ─── Backend Patterns ───
    "ddd": [
        "dev.backend.patterns.role", "dev.backend.patterns.ddd",
        "dev.backend.patterns.cqrs", "dev.backend.patterns.clean-architecture",
        "dev.backend.patterns.verify",
    ],
    "clean-architecture": [
        "dev.backend.patterns.clean-architecture", "dev.backend.patterns.role",
    ],
    "microservice": [
        "dev.backend.patterns.event-driven", "dev.backend.patterns.cqrs",
        "dev.backend.patterns.cap-theorem", "dev.backend.patterns.twelve-factor",
        "dev.backend.patterns.saga-pattern", "dev.backend.patterns.circuit-breaker",
        "dev.backend.patterns.conways-law", "dev.backend.patterns.strangler-fig",
    ],
    "event-driven": [
        "dev.backend.patterns.event-driven", "dev.backend.patterns.message-queue",
        "dev.backend.patterns.outbox-pattern",
    ],
    "queue": ["dev.backend.patterns.message-queue", "dev.backend.api.background-jobs"],
    "background-job": ["dev.backend.api.background-jobs", "dev.backend.patterns.message-queue"],
    "saga": ["dev.backend.patterns.saga-pattern"],
    "circuit-breaker": ["dev.backend.patterns.circuit-breaker", "dev.backend.patterns.retry-patterns"],
    "resilience": [
        "dev.backend.patterns.circuit-breaker", "dev.backend.patterns.retry-patterns",
        "dev.backend.patterns.timeout-patterns", "dev.backend.patterns.health-check",
    ],
    # ─── Frontend ───
    "dashboard": [
        "dev.frontend.component.role", "dev.frontend.component.stack",
        "dev.frontend.page.data-fetching", "design.product-ui.role",
    ],
    "admin": [
        "dev.backend.api.auth", "dev.backend.auth.rbac",
        "dev.backend.api.middleware",
    ],
    "accessibility": [
        "design.ui-component.accessibility", "design.ui-component.color",
        "dev.frontend.component.accessibility-impl",
    ],
    "dark-mode": ["design.ui-component.dark-mode"],
    "form": ["dev.frontend.component.form", "dev.backend.api.validation"],
    "routing": ["dev.frontend.page.routing", "dev.frontend.page.role"],
    "hooks": ["dev.frontend.hook.role", "dev.frontend.hook.patterns", "dev.frontend.hook.verify"],
    "data-fetching": ["dev.frontend.page.data-fetching", "dev.frontend.page.role"],
    "error-handling": ["dev.frontend.component.error-boundary", "dev.backend.api.error"],
    # ─── Performance ───
    "performance": [
        "dev.performance.role", "dev.performance.web-vitals",
        "dev.performance.caching", "dev.performance.budget",
        "dev.performance.amdahl", "dev.performance.littles-law",
        "dev.frontend.component.performance",
    ],
    "caching": ["dev.backend.api.caching", "dev.performance.caching"],
    # ─── Infrastructure ───
    "ci-cd": ["dev.infra.ci.role", "dev.infra.ci.pipeline", "dev.infra.ci.verify"],
    "docker": ["dev.infra.deploy.docker"],
    "monitoring": ["dev.infra.deploy.monitoring", "dev.infra.observability.dashboard", "dev.infra.observability.metrics"],
    "scaling": ["dev.infra.deploy.scaling"],
    "email": ["dev.backend.api.third-party", "dev.backend.api.background-jobs"],
    # ─── Marketing / Persuasion ───
    "seo": [
        "marketing.seo.role", "marketing.seo.technical-seo",
        "marketing.seo.content-seo", "marketing.seo.verify",
        "marketing.copy.seo", "dev.frontend.page.seo",
    ],
    "persuasion": [
        "marketing.persuasion.role", "marketing.persuasion.hook-model",
        "marketing.persuasion.nudge", "marketing.persuasion.social-proof",
        "marketing.persuasion.reciprocity", "marketing.persuasion.authority",
        "marketing.persuasion.anchoring",
    ],
    "conversion": [
        "marketing.persuasion.fogg-model", "marketing.persuasion.scarcity",
        "marketing.persuasion.anchoring", "marketing.persuasion.endowment",
        "marketing.persuasion.prospect-theory", "marketing.copy.cta",
    ],
    "onboarding": [
        "design.ux-psychology.endowed-progress", "design.ux-psychology.zeigarnik",
        "marketing.persuasion.hook-model",
    ],
    "retention": [
        "marketing.persuasion.hook-model", "marketing.persuasion.commitment",
        "marketing.persuasion.mere-exposure", "marketing.persuasion.commitment-consistency",
    ],
    "copywriting": [
        "marketing.copy.role", "marketing.copy.headline", "marketing.copy.storytelling",
        "marketing.copy.elm", "marketing.copy.social-proof-copy", "marketing.copy.aida",
    ],
    # ─── Analytics ───
    "analytics": [
        "analytics.role", "analytics.metrics", "analytics.ab-testing",
        "analytics.funnel-analysis", "analytics.cohort-analysis",
        "analytics.bayesian", "analytics.simpsons-paradox",
    ],
    "ab-testing": ["analytics.ab-testing", "analytics.statistical-significance"],
    "metrics": ["planning.prd.metrics", "analytics.metrics", "analytics.dora-metrics"],
    "funnel": ["analytics.funnel-analysis", "analytics.metrics"],
    "cohort": ["analytics.cohort-analysis", "analytics.metrics"],
    "dora": ["analytics.dora-metrics"],
    # ─── Testing / QA ───
    "testing": [
        "qa.code-review.role", "qa.code-review.priority",
        "qa.code-review.performance", "qa.test-gen.role",
        "qa.test-gen.unit", "qa.test-gen.integration",
        "qa.test-gen.component-test", "qa.test-gen.testing-trophy",
        "qa.test-gen.verify",
    ],
    # ─── Other ───
    "bias-check": [
        "meta.bias-prevention.role", "meta.bias-prevention.confirmation-bias",
        "meta.bias-prevention.survivorship-bias", "meta.bias-prevention.availability-bias",
        "meta.bias-prevention.dunning-kruger", "meta.bias-prevention.framing-effect",
        "meta.bias-prevention.hindsight-bias", "meta.bias-prevention.sunk-cost",
        "meta.output-validator",
    ],
    "documentation": [
        "content.role", "content.structure", "content.readability",
        "content.technical-docs",
    ],
    "file-upload": ["dev.backend.api.file-upload", "dev.backend.api.security"],
    "webhook": ["dev.backend.api.webhook", "dev.backend.patterns.idempotency"],
    "graphql": ["dev.backend.api.graphql"],
    "batch": ["dev.backend.api.batch-operations"],
    "websocket": ["dev.backend.api.websocket", "dev.backend.websocket.connection", "dev.backend.websocket.room"],
    "rate-limiting": ["dev.backend.api.rate-limiting"],
    "third-party": ["dev.backend.api.third-party", "dev.backend.patterns.circuit-breaker"],
    # ─── Frontend Expanded ───
    "state-management": ["dev.frontend.component.state-management"],
    "animation": ["dev.frontend.component.animation"],
    "styling": ["dev.frontend.component.styling"],
    "i18n": ["dev.frontend.component.i18n"],
    "pwa": ["dev.frontend.page.pwa"],
    # ─── Marketing Expanded ───
    "landing-page": ["marketing.growth.landing-page", "marketing.copy.cta", "design.web-experience.role"],
    "email-marketing": ["marketing.growth.email-sequence"],
    "social-media": ["marketing.growth.social-media", "marketing.copy.cta"],
    "growth": [
        "marketing.growth.role", "marketing.growth.growth-hack",
        "marketing.growth.landing-page", "marketing.growth.social-media",
        "marketing.growth.verify",
    ],
    "technical-seo": ["marketing.seo.technical-seo", "marketing.seo.content-seo"],
    # ─── QA Expanded ───
    "e2e-test": ["qa.test-gen.e2e", "qa.test-gen.bdd"],
    "bdd": ["qa.test-gen.bdd", "qa.test-gen.role"],
    "property-based": ["qa.test-gen.property-based"],
    "load-test": ["qa.test-gen.load-test"],
    "component-test": ["qa.test-gen.component-test"],
    "contract-test": ["qa.test-gen.contract-test", "dev.backend.testing.contract-testing", "qa.test-gen.contract-testing"],
    "visual-regression": ["qa.test-gen.visual-regression", "dev.frontend.testing.visual-regression"],
    "ux-audit": ["qa.ux-audit.role", "qa.ux-audit.heuristic-evaluation", "qa.ux-audit.verify"],
    "bug-analysis": ["qa.code-review.bug-analysis"],
    # ─── Design Expanded ───
    "design-system": ["design.design-system.tokens"],
    "wireframe": ["design.wireframe.role", "design.wireframe.layout", "design.wireframe.verify"],
    "interaction": ["design.ui-component.interaction", "design.ui-component.role"],
    # ─── Planning Expanded ───
    "persona": [
        "planning.user-persona.role", "planning.user-persona.empathy-map",
        "planning.user-persona.persona-template", "planning.user-persona.verify",
    ],
    "competitive-analysis": [
        "planning.competitive-analysis.role", "planning.competitive-analysis.porter",
        "planning.competitive-analysis.swot", "planning.competitive-analysis.value-curve",
        "planning.competitive-analysis.verify",
    ],
    "user-story": ["planning.prd.user-story", "planning.prd.role"],
    "sprint": [
        "planning.project-mgmt.sprint-decomposition", "planning.project-mgmt.agile",
        "planning.project-mgmt.toc",
    ],
    "prioritization": [
        "planning.prd.feature-prioritization", "planning.prd.rice",
        "planning.prd.kano-model", "planning.prd.metrics",
    ],
    "cognitive-bias": [
        "marketing.persuasion.cognitive-dissonance", "marketing.persuasion.mere-exposure",
        "marketing.persuasion.prospect-theory", "marketing.persuasion.endowment",
    ],
    "innovation": [
        "planning.business.innovation-diffusion", "planning.business.flow",
        "planning.business.sdt",
    ],
    # ─── AI/LLM ───
    "llm": ["dev.backend.patterns.llm-integration"],
    "rag": ["dev.backend.patterns.rag-pattern", "meta.retrieval-augmented"],
    "ai-integration": ["dev.backend.patterns.llm-integration", "dev.backend.patterns.rag-pattern"],
    # ─── Infra Expanded ───
    "feature-flag": ["dev.infra.deploy.feature-flags"],
    "kubernetes": ["dev.infra.deploy.kubernetes"],
    "rollback": ["dev.infra.deploy.rollback"],
    "secrets": ["dev.infra.deploy.secrets", "dev.backend.security.secrets-hygiene"],
    "api-key": ["dev.backend.auth.api-key", "dev.backend.security.secrets-hygiene"],
    "env": ["dev.backend.security.secrets-hygiene", "dev.infra.deploy.secrets"],
    "blue-green": ["dev.infra.deploy.blue-green"],
    "iac": ["dev.infra.deploy.iac"],
    "terraform": ["dev.infra.deploy.iac", "dev.infra.cloud.terraform"],
    "chaos-engineering": ["dev.infra.deploy.chaos-engineering"],
    # ─── Other ───
    "notification": ["dev.backend.api.websocket"],
    "realtime": ["dev.backend.api.websocket"],
    # ─── Content Expanded ───
    "error-messages": ["content.error-messages", "content.role"],
    "microcopy": ["content.error-messages", "content.role"],
    "changelog": ["content.changelog"],
    "release-notes": ["content.changelog", "content.role", "content.release-notes"],
    # ─── Architecture Expanded ───
    "strangler-fig": ["dev.backend.patterns.strangler-fig"],
    "legacy-migration": ["dev.backend.patterns.strangler-fig"],
    "outbox": ["dev.backend.patterns.outbox-pattern", "dev.backend.patterns.outbox"],
    "nist": ["dev.security.nist-framework", "dev.security.role"],
    "cognitive-load": ["design.ux-psychology.cognitive-load"],
    "scanning-pattern": ["design.ui-component.scanning-patterns"],
    # ─── UX Rules (ui-ux-pro-max) ───
    "ux-rules": [
        "design.ux-rules.accessibility-touch", "design.ux-rules.visual-design",
        "design.ux-rules.layout-performance", "design.ux-rules.forms-navigation",
        "design.ux-rules.charts-checklist",
    ],
    "touch-target": ["design.ux-rules.accessibility-touch"],
    "dark-mode": ["design.ux-rules.visual-design", "design.ui-component.role"],
    "chart": ["design.ux-rules.charts-checklist"],
    "data-visualization": ["design.ux-rules.charts-checklist"],
    "form-ux": ["design.ux-rules.forms-navigation"],
    "navigation-pattern": ["design.ux-rules.forms-navigation"],
    "web-vitals": ["design.ux-rules.layout-performance"],
    "core-web-vitals": ["design.ux-rules.layout-performance"],
    "pre-delivery": ["design.ux-rules.charts-checklist"],
    # ─── Frontend Frameworks (Tier 1) ───
    "react": [
        "dev.frontend.component.react-patterns", "dev.frontend.component.role",
        "dev.frontend.component.solid",
    ],
    "nextjs": [
        "dev.frontend.page.nextjs-patterns", "dev.frontend.page.role",
        "dev.frontend.page.routing",
    ],
    # ─── Architecture Patterns (Tier 1+2) ───
    "hexagonal": ["dev.backend.patterns.hexagonal", "dev.backend.patterns.role"],
    "event-sourcing": [
        "dev.backend.patterns.event-sourcing", "dev.backend.patterns.event-driven",
        "dev.backend.patterns.cqrs",
    ],
    "gof-patterns": ["dev.backend.patterns.gof-patterns"],
    "design-patterns": ["dev.backend.patterns.gof-patterns", "dev.backend.patterns.role"],
    "repository-pattern": ["dev.backend.patterns.repository"],
    "solid-backend": ["dev.backend.patterns.solid", "dev.backend.patterns.role"],
    # ─── Security (Tier 1+2) ───
    "owasp-api": ["dev.security.owasp-api", "dev.security.owasp"],
    "supply-chain": ["dev.security.supply-chain"],
    "mitre": ["dev.security.mitre-attack", "dev.security.role"],
    "mitre-attack": ["dev.security.mitre-attack"],
    # ─── Infra / SRE (Tier 1+2) ───
    "observability": [
        "dev.infra.deploy.observability", "dev.infra.deploy.monitoring",
    ],
    "opentelemetry": ["dev.infra.deploy.observability"],
    "sre": ["dev.infra.deploy.sre", "dev.infra.deploy.role", "dev.infra.sre.role"],
    "slo": ["dev.infra.deploy.sre", "dev.infra.sre.slo"],
    "incident": ["dev.infra.deploy.incident-mgmt", "dev.infra.sre.incident-response", "dev.infra.deploy.role"],
    "postmortem": ["dev.infra.deploy.incident-mgmt"],
    "finops": ["dev.infra.deploy.finops"],
    "cost-optimization": ["dev.infra.deploy.finops"],
    # ─── Planning (Tier 1+2) ───
    "okr": ["planning.project-mgmt.okr", "planning.project-mgmt.role"],
    "design-sprint": ["planning.business.design-sprint", "planning.business.role"],
    "story-mapping": ["planning.prd.story-mapping", "planning.prd.role"],
    "north-star": ["planning.prd.north-star", "analytics.metrics"],
    # ─── Marketing / Growth (Tier 1+2) ───
    "aarrr": ["marketing.growth.aarrr", "marketing.growth.role"],
    "pirate-metrics": ["marketing.growth.aarrr"],
    "content-marketing": ["marketing.growth.content-marketing", "content.role"],
    "inbound": ["marketing.growth.inbound", "marketing.growth.role"],
    "inbound-marketing": ["marketing.growth.inbound"],
    # ─── Analytics (Tier 2) ───
    "data-pipeline": ["analytics.data-pipeline", "analytics.role"],
    "etl": ["analytics.data-pipeline"],
    "data-quality": ["analytics.data-quality", "analytics.role"],
    "event-tracking": ["analytics.event-tracking", "analytics.role"],
    # ─── QA / Testing (Tier 1+2) ───
    "mutation-testing": ["qa.test-gen.mutation", "qa.test-gen.role"],
    "fuzz-testing": ["qa.test-gen.fuzz", "qa.test-gen.role"],
    "smoke-test": ["qa.test-gen.smoke", "qa.test-gen.role"],
    "regression-test": ["qa.test-gen.regression", "qa.test-gen.role"],
    # ─── Design (Tier 1+2) ───
    "atomic-design": ["design.ui-component.atomic-design", "design.ui-component.role"],
    "information-architecture": [
        "design.wireframe.information-architecture", "design.wireframe.role",
    ],
    "motion": ["design.ui-component.motion", "design.ui-component.role"],
    "design-tokens": ["design.design-system.tokens", "design.ui-component.role"],
    "playwright": ["qa.test-gen.e2e", "qa.test-gen.role"],
    "drip-campaign": ["marketing.growth.email-sequence", "marketing.growth.role"],
    # ─── AI/LLM (New) ───
    "ai-agent": ["dev.ai.agent-pattern", "dev.ai.memory-pattern", "dev.ai.guardrails"],
    "embedding": ["dev.ai.embedding", "dev.ai.rag-pattern"],
    "fine-tuning": ["dev.ai.fine-tuning", "dev.ai.eval-pipeline"],
    "guardrails": ["dev.ai.guardrails", "dev.ai.prompt-injection", "dev.ai.prompt-engineering"],
    "prompt-engineering": ["dev.ai.prompt-engineering", "meta.prompt-engineering"],
    "function-calling": ["dev.ai.function-calling", "dev.ai.agent-pattern"],
    "token-optimization": ["dev.ai.token-optimization", "dev.ai.streaming-response"],
    "multi-modal": ["dev.ai.multi-modal", "dev.ai.prompt-engineering"],
    "eval": ["dev.ai.eval-pipeline", "dev.ai.guardrails"],
    "streaming": ["dev.ai.streaming-response", "dev.backend.api.websocket"],
    # ─── Backend (New) ───
    "graphql-federation": ["dev.backend.graphql.federation", "dev.backend.graphql.schema"],
    "graphql-resolver": ["dev.backend.graphql.resolver", "dev.backend.graphql.error-handling"],
    "graphql-subscription": ["dev.backend.graphql.subscription", "dev.backend.graphql.resolver"],
    "abac": ["dev.backend.auth.abac", "dev.backend.auth.role"],
    "sso": ["dev.backend.auth.sso", "dev.backend.auth.role"],
    "api-key": ["dev.backend.auth.api-key", "dev.backend.auth.role"],
    "passwordless": ["dev.backend.auth.passwordless", "dev.backend.auth.role"],
    "cache-strategy": ["dev.backend.cache.strategy", "dev.backend.cache.invalidation", "dev.backend.cache.distributed"],
    "cache-invalidation": ["dev.backend.cache.invalidation", "dev.backend.cache.strategy"],
    "bulkhead": ["dev.backend.patterns.bulkhead", "dev.backend.patterns.circuit-breaker"],
    "dead-letter": ["dev.backend.queue.dead-letter", "dev.backend.queue.retry-strategy"],
    "message-queue": ["dev.backend.queue.message-queue", "dev.backend.queue.retry-strategy"],
    "sidecar": ["dev.backend.patterns.sidecar", "dev.backend.patterns.ambassador"],
    "ambassador": ["dev.backend.patterns.ambassador", "dev.backend.patterns.sidecar"],
    "idempotency": ["dev.backend.api.idempotency", "dev.backend.patterns.idempotency"],
    # ─── Frontend (New) ───
    "suspense": ["dev.frontend.component.suspense", "dev.frontend.page.streaming"],
    "virtual-list": ["dev.frontend.component.virtual-list", "dev.frontend.component.performance"],
    "react-native": ["dev.frontend.mobile.react-native", "dev.frontend.mobile.native-bridge"],
    "ssr": ["dev.frontend.page.ssr", "dev.frontend.page.streaming"],
    "ssg": ["dev.frontend.page.ssg", "dev.frontend.page.isr"],
    "isr": ["dev.frontend.page.isr", "dev.frontend.page.ssg"],
    "code-splitting": ["dev.frontend.performance.code-splitting", "dev.frontend.performance.bundle-optimization"],
    "storybook": ["dev.frontend.testing.storybook", "dev.frontend.testing.component-testing"],
    "bundle-optimization": ["dev.frontend.performance.bundle-optimization", "dev.frontend.performance.code-splitting"],
    "portal": ["dev.frontend.component.portal", "dev.frontend.component.role"],
    "optimistic-update": ["dev.frontend.hook.optimistic-update", "dev.frontend.hook.data-fetching"],
    "custom-hooks": ["dev.frontend.hook.custom-hooks", "dev.frontend.hook.role"],
    "parallel-routes": ["dev.frontend.page.parallel-routes", "dev.frontend.page.nextjs-patterns"],
    "image-optimization": ["dev.frontend.performance.image-optimization", "dev.frontend.performance.web-vitals"],
    # ─── Infra (New) ───
    "serverless": ["dev.infra.cloud.serverless", "dev.infra.deploy.role"],
    "cdn": ["dev.infra.cloud.cdn", "dev.infra.cloud.multi-region"],
    "helm": ["dev.infra.deploy.helm", "dev.infra.deploy.kubernetes"],
    "canary": ["dev.infra.deploy.canary", "dev.infra.deploy.role"],
    "argocd": ["dev.infra.deploy.argocd", "dev.infra.deploy.helm"],
    "alerting": ["dev.infra.observability.alerting", "dev.infra.observability.metrics"],
    "tracing": ["dev.infra.observability.tracing", "dev.infra.observability.logging"],
    "capacity-planning": ["dev.infra.sre.capacity-planning", "dev.infra.sre.role"],
    "incident-response": ["dev.infra.sre.incident-response", "dev.infra.sre.role"],
    "multi-region": ["dev.infra.cloud.multi-region", "dev.infra.cloud.cdn"],
    "aws": ["dev.infra.cloud.aws-well-architected", "dev.infra.cloud.serverless"],
    # ─── Content (New) ───
    "api-docs": ["content.api-docs", "content.technical-docs", "content.structure"],
    "ux-writing": ["content.ux-writing", "content.microcopy", "content.role"],
    "localization": ["content.localization", "dev.frontend.component.i18n"],
    "content-strategy": ["content.content-strategy", "content.content-calendar", "content.content-audit"],
    "help-docs": ["content.help-docs", "content.technical-docs"],
    "seo-writing": ["content.seo-writing", "marketing.seo.content-seo"],
    "content-audit": ["content.content-audit", "content.content-governance", "qa.ux-audit.content-audit"],
    "content-calendar": ["content.content-calendar", "content.content-strategy"],
    "storytelling": ["content.storytelling", "marketing.copy.storytelling"],
    # ─── Analytics (New) ───
    "attribution": ["analytics.attribution-model", "analytics.metrics"],
    "churn": ["analytics.churn-prediction", "analytics.retention-analysis"],
    "ltv": ["analytics.ltv-calculation", "analytics.metrics"],
    "segmentation": ["analytics.segmentation", "analytics.cohort-analysis"],
    "kpi": ["analytics.kpi-framework", "analytics.metric-tree"],
    "north-star": ["analytics.north-star-metric", "planning.prd.north-star"],
    "sql-optimization": ["analytics.sql-optimization", "dev.backend.database.query"],
    "predictive-analytics": ["analytics.predictive-analytics", "analytics.behavioral-analytics"],
    "data-storytelling": ["analytics.data-storytelling", "analytics.data-visualization"],
    "experiment-design": ["analytics.experiment-design", "analytics.ab-testing"],
    # ─── QA (New) ───
    "tdd": ["qa.test-gen.tdd", "qa.test-gen.unit", "qa.test-gen.role"],
    "test-doubles": ["qa.test-gen.test-doubles", "qa.test-gen.role"],
    "api-testing": ["qa.test-gen.api-testing", "dev.backend.testing.api-testing"],
    "chaos-testing": ["qa.test-gen.chaos-testing", "dev.infra.sre.chaos-engineering"],
    "architecture-review": ["qa.code-review.architecture-review", "qa.code-review.role"],
    "security-testing": ["qa.test-gen.security-testing", "dev.security.owasp"],
    "performance-testing": ["qa.test-gen.performance-testing", "qa.code-review.performance"],
    "test-strategy": ["qa.test-gen.test-strategy", "qa.test-gen.testing-trophy"],
    "code-smell": ["qa.code-review.code-smell", "qa.code-review.readability"],
    "naming-convention": ["qa.code-review.naming-convention", "qa.code-review.readability"],
    "cognitive-walkthrough": ["qa.ux-audit.cognitive-walkthrough", "qa.ux-audit.role"],
    "accessibility-audit": ["qa.ux-audit.accessibility-audit", "qa.ux-audit.role"],
    "mobile-audit": ["qa.ux-audit.mobile-audit", "qa.ux-audit.responsive-audit"],
    # ─── Marketing (New) ───
    "plg": ["marketing.growth.plg", "marketing.growth.activation"],
    "referral": ["marketing.growth.referral-loop", "marketing.growth.viral-loop"],
    "viral": ["marketing.growth.viral-loop", "marketing.growth.referral-loop"],
    "lifecycle": ["marketing.growth.lifecycle-marketing", "marketing.growth.email-sequence"],
    "link-building": ["marketing.seo.link-building", "marketing.seo.content-seo"],
    "seo-audit": ["marketing.seo.seo-audit", "marketing.seo.technical-seo"],
    "value-proposition": ["marketing.copy.value-proposition", "marketing.copy.role"],
    "local-seo": ["marketing.seo.local-seo", "marketing.seo.role"],
    "objection-handling": ["marketing.copy.objection-handling", "marketing.copy.cta"],
    "activation": ["marketing.growth.activation", "marketing.growth.aarrr"],
    "cta-optimization": ["marketing.copy.cta-optimization", "marketing.copy.cta"],
    # ─── Meta (New) ───
    "chain-of-thought": ["meta.chain-of-thought", "meta.prompt-engineering"],
    "few-shot": ["meta.few-shot", "meta.prompt-engineering"],
    "tree-of-thought": ["meta.tree-of-thought", "meta.chain-of-thought"],
    "groupthink": ["meta.bias-prevention.groupthink", "meta.bias-prevention.confirmation-bias"],
    "bandwagon": ["meta.bias-prevention.bandwagon", "meta.bias-prevention.groupthink"],
    "self-consistency": ["meta.self-consistency", "meta.chain-of-thought"],
    "role-prompting": ["meta.role-prompting", "meta.system-prompt-design"],
    "structured-output": ["meta.structured-output", "meta.output-formatting"],
    "system-prompt": ["meta.system-prompt-design", "meta.role-prompting"],
    "recency-bias": ["meta.bias-prevention.recency-bias", "meta.bias-prevention.availability-bias"],
    "anchoring-bias": ["meta.bias-prevention.anchoring-bias", "meta.bias-prevention.framing-effect"],
    # ─── Planning (New) ───
    "roadmap": ["planning.roadmap", "planning.prd.role"],
    "discovery": ["planning.discovery", "planning.business.design-thinking"],
    "ice-scoring": ["planning.ice-scoring", "planning.prd.feature-prioritization"],
    "pricing": ["planning.business.pricing-strategy", "planning.business.role"],
    "retrospective": ["planning.project-mgmt.retrospective", "planning.project-mgmt.role"],
    "stakeholder": ["planning.project-mgmt.stakeholder-management", "planning.project-mgmt.role"],
    "go-to-market": ["planning.business.go-to-market", "planning.business.role"],
    "business-model": ["planning.business.business-model-canvas", "planning.business.role"],
    "value-stream": ["planning.business.value-stream-mapping", "planning.business.lean-startup"],
    "dependency-mapping": ["planning.project-mgmt.dependency-mapping", "planning.project-mgmt.role"],
    "capacity": ["planning.project-mgmt.capacity-planning", "dev.infra.sre.capacity-planning"],
    # ─── Design (New) ───
    "progressive-disclosure": ["design.ux-psychology.progressive-disclosure", "design.ux-psychology.role"],
    "empty-states": ["design.ui-component.empty-states", "design.ui-component.role"],
    "skeleton-loading": ["design.ui-component.skeleton-loading", "design.ui-component.role"],
    "micro-interaction": ["design.ui-component.micro-interaction", "design.ui-component.interaction"],
    "toast-notification": ["design.ui-component.toast-notification", "design.ui-component.role"],
    "component-library": ["design.design-system.component-library", "design.design-system.tokens"],
    "theme-system": ["design.design-system.theme-system", "design.design-system.tokens"],
    "paradox-of-choice": ["design.ux-psychology.paradox-of-choice", "design.ux-psychology.hicks-law"],
    "cognitive-load": ["design.ux-psychology.cognitive-load", "design.ux-psychology.role"],
    # ─── Backend Expanded (New) ───
    "websocket-auth": ["dev.backend.websocket.auth", "dev.backend.websocket.connection"],
    "websocket-room": ["dev.backend.websocket.room", "dev.backend.websocket.scaling"],
    "test-containers": ["dev.backend.testing.test-containers", "dev.backend.testing.api-testing"],
    "fixture-factory": ["dev.backend.testing.fixture-factory", "dev.backend.testing.test-containers"],
    # ─── Analytics Expanded (New) ───
    "data-governance": ["analytics.data-governance", "analytics.data-quality"],
    "product-analytics": ["analytics.product-analytics", "analytics.behavioral-analytics"],
    "real-time-analytics": ["analytics.real-time-analytics", "analytics.event-tracking"],
    # ─── Content Expanded (New) ───
    "content-accessibility": ["content.content-accessibility", "design.ui-component.accessibility"],
    "content-repurposing": ["content.content-repurposing", "content.content-strategy"],
    "content-testing": ["content.content-testing", "content.content-metrics"],
    "content-metrics": ["content.content-metrics", "content.content-testing"],
    # ─── Design Expanded (New) ───
    "animation-principles": ["design.ui-component.animation-principles", "design.ui-component.motion"],
    "anchoring-effect": ["design.ux-psychology.anchoring-effect", "design.ux-psychology.role"],
    # ─── Backend API Expanded (New) ───
    "graphql-hybrid": ["dev.backend.api.graphql-rest-hybrid", "dev.backend.api.graphql"],
    "versioning-strategy": ["dev.backend.api.versioning-strategy", "dev.backend.api.versioning"],
    # ─── Backend Testing Expanded (New) ───
    "snapshot-testing": ["dev.backend.testing.snapshot-testing", "qa.test-gen.snapshot-testing"],
    # ─── Frontend Hooks Expanded (New) ───
    "debounce": ["dev.frontend.hook.debounce", "dev.frontend.hook.role"],
    "intersection-observer": ["dev.frontend.hook.intersection-observer", "dev.frontend.hook.role"],
    # ─── Frontend Mobile Expanded (New) ───
    "offline-first": ["dev.frontend.mobile.offline-first", "dev.frontend.page.pwa"],
    "touch-interaction": ["dev.frontend.mobile.touch-interaction", "dev.frontend.mobile.responsive-patterns"],
    "responsive-patterns": ["dev.frontend.mobile.responsive-patterns", "dev.frontend.mobile.touch-interaction"],
    # ─── Frontend Performance Expanded (New) ───
    "render-optimization": ["dev.frontend.performance.render-optimization", "dev.frontend.performance.web-vitals"],
    # ─── Frontend Testing Expanded (New) ───
    "accessibility-testing": ["dev.frontend.testing.accessibility-testing", "qa.test-gen.accessibility-testing"],
    "interaction-testing": ["dev.frontend.testing.interaction-testing", "dev.frontend.testing.storybook"],
    # ─── Infra Expanded (New) ───
    "dashboard-monitoring": ["dev.infra.observability.dashboard", "dev.infra.observability.metrics"],
    # ─── Marketing Expanded (New) ───
    "headline-formula": ["marketing.copy.headline-formula", "marketing.copy.headline"],
    "ab-testing-marketing": ["marketing.growth.ab-testing-marketing", "analytics.ab-testing"],
    # ─── Planning Expanded (New) ───
    "estimation-techniques": ["planning.project-mgmt.estimation-techniques", "planning.project-mgmt.estimation"],
    "rice-scoring": ["planning.rice-scoring", "planning.prd.rice"],
    "opportunity-tree": ["planning.opportunity-solution-tree", "planning.discovery"],
    # ─── QA Code Review Expanded (New) ───
    "dependency-review": ["qa.code-review.dependency-review", "qa.code-review.role"],
    "documentation-review": ["qa.code-review.documentation-review", "qa.code-review.role"],
    # ─── QA Testing Expanded (New) ───
    "ci-testing": ["qa.test-gen.ci-testing", "qa.test-gen.role"],
    "error-scenario": ["qa.test-gen.error-scenario", "qa.test-gen.role"],
    "test-data": ["qa.test-gen.test-data-management", "qa.test-gen.role"],
    # ─── QA UX Audit Expanded (New) ───
    "performance-audit": ["qa.ux-audit.performance-audit", "qa.ux-audit.role"],
    # ─── Anti-Generic Design ───
    "anti-generic": [
        "design.anti-generic.role", "design.styleseed.visual-rules",
    ],
    "generic": ["design.anti-generic.role"],
    "cliche": ["design.anti-generic.role"],
    "signature-move": ["design.anti-generic.role"],
    "divergence": ["design.anti-generic.role"],
    "originality": ["design.anti-generic.role"],
    # ─── Web Experience / Landing ───
    "web-experience": [
        "design.web-experience.role", "design.anti-generic.role",
    ],
    "brand-site": ["design.web-experience.role", "design.anti-generic.role"],
    "campaign-page": ["design.web-experience.role"],
    "pricing-page": ["design.web-experience.role"],
    "narrative": ["design.web-experience.role", "marketing.copy.storytelling"],
    "proof-strategy": ["design.web-experience.role"],
    # ─── Product UI ───
    "product-ui": [
        "design.product-ui.role", "design.anti-generic.role",
    ],
    "app-design": ["design.product-ui.role", "design.anti-generic.role"],
    "ops-tool": ["design.product-ui.role"],
    "shell-pattern": ["design.product-ui.role"],
    "workflow-ui": ["design.product-ui.role"],
    "object-model": ["design.product-ui.role"],
    # ─── StyleSeed ───
    "styleseed": ["design.styleseed.visual-rules"],
    "visual-rhythm": ["design.styleseed.visual-rules"],
    "card-design": ["design.styleseed.visual-rules", "design.ui-component.role"],
    "density": ["design.styleseed.visual-rules", "design.product-ui.role"],
    "grayscale": ["design.styleseed.visual-rules"],
    # ─── DESIGN.md ───
    "design-md": ["design.design-md.template", "design.design-system.tokens"],
    "design-document": ["design.design-md.template"],
    "design-spec": ["design.design-md.template", "design.design-system.tokens"],
    # ─── Vulnerability Analysis ───
    "vuln-analysis": [
        "qa.security.vuln-analysis", "dev.security.owasp",
    ],
    "vulnerability": ["qa.security.vuln-analysis", "dev.security.owasp"],
    "sast": ["qa.security.vuln-analysis", "qa.test-gen.security-testing"],
    "semgrep": ["qa.security.vuln-analysis"],
    "source-to-sink": ["qa.security.vuln-analysis"],
    "code-audit": ["qa.security.vuln-analysis", "qa.code-review.security"],
}

# ─── 도메인 → Skill prefix 매핑 (세션 스킬 유지용) ───

DOMAIN_TO_SKILL_PREFIX: dict[str, str] = {
    "development.backend": "dev.backend",
    "development.frontend": "dev.frontend",
    "development.database": "dev.backend.database",
    "development.infra": "dev.infra",
    "development.security": "dev.security",
    "development.performance": "dev.performance",
    "development.ai": "dev.ai",
    "planning": "planning",
    "planning.business": "planning.business",
    "planning.project-mgmt": "planning.project-mgmt",
    "design": "design",
    "design.ux-psychology": "design.ux-psychology",
    "marketing": "marketing",
    "marketing.persuasion": "marketing.persuasion",
    "marketing.seo": "marketing.seo",
    "marketing.growth": "marketing.growth",
    "analytics": "analytics",
    "content": "content",
    "qa": "qa",
    "qa.code-review": "qa.code-review",
    "qa.testing": "qa.test-gen",
    "meta": "meta",
    "design.wireframe": "design.wireframe",
    "design.design-system": "design.design-system",
    "qa.ux-audit": "qa.ux-audit",
}

# ─── 복잡도별 스킬 수 cap ───

COMPLEXITY_SKILL_CAP: dict[int, int] = {
    3: 12,
    6: 20,
    10: 30,
}


def _trim_to_budget(
    skill_ids: list[str],
    model: str,
    assemble_fn=None,
) -> tuple[list[str], list[str]]:
    """Trim skills to fit within model's token budget.

    Args:
        skill_ids: Selected skill IDs
        model: Target model (haiku/sonnet/opus)
        assemble_fn: Function to load skill data (optional)

    Returns:
        (kept_ids, dropped_ids)
    """
    budget = MODEL_CONTEXT_LIMITS.get(model, MODEL_CONTEXT_LIMITS["sonnet"])

    # Load skill data to get token estimates
    skill_data = []
    for sid in skill_ids:
        parts = sid.split(".")
        if len(parts) < 2:
            skill_data.append({"id": sid, "token_estimate": 100, "type": "rule"})
            continue

        path = SKILL_DIR / "/".join(parts[:-1]) / f"{parts[-1]}.yaml"
        if path.exists():
            try:
                import yaml
                with open(path) as f:
                    data = yaml.safe_load(f)
                skill_data.append({
                    "id": sid,
                    "token_estimate": data.get("token_estimate", 100),
                    "type": data.get("type", "rule"),
                })
            except Exception:
                skill_data.append({"id": sid, "token_estimate": 100, "type": "rule"})
        else:
            skill_data.append({"id": sid, "token_estimate": 100, "type": "rule"})

    # Sort by priority (highest priority first)
    skill_data.sort(key=lambda s: SKILL_TYPE_PRIORITY.get(s["type"], 0), reverse=True)

    kept = []
    dropped = []
    total_tokens = 0

    for s in skill_data:
        if total_tokens + s["token_estimate"] <= budget:
            kept.append(s["id"])
            total_tokens += s["token_estimate"]
        else:
            dropped.append(s["id"])

    if dropped:
        logger.warning(
            "Token budget exceeded for %s (budget=%d): dropped %d skills: %s",
            model, budget, len(dropped), dropped[:5],
        )

    return kept, dropped


def _get_skill_cap(complexity: int) -> int:
    """복잡도에 따른 스킬 수 상한 반환."""
    if complexity <= 3:
        return COMPLEXITY_SKILL_CAP[3]
    if complexity <= 6:
        return COMPLEXITY_SKILL_CAP[6]
    return COMPLEXITY_SKILL_CAP[10]


def _dedupe_preserve_order(items: list[str]) -> list[str]:
    """중복 제거 + 순서 유지."""
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def _cap_skills(skills: list[str], cap: int) -> list[str]:
    """스킬 수를 cap 이하로 제한. role 타입 우선 보존."""
    if len(skills) <= cap:
        return skills
    role_skills = [s for s in skills if s.endswith(".role")]
    non_role_skills = [s for s in skills if not s.endswith(".role")]
    remaining = cap - len(role_skills)
    if remaining <= 0:
        return role_skills[:cap]
    return role_skills + non_role_skills[:remaining]


def select_skills(
    domains: list[str],
    semantic_keywords: list[str],
    complexity: int,
    session: Session,
) -> list[str]:
    """도메인 + 의미 키워드 + 복잡도 + 세션 기반 Atomic Skill 선택.

    Returns:
        선택된 Atomic Skill ID 목록 (중복 없음, 순서 유지)
    """
    skills: list[str] = []

    # 1. 도메인별 기본 Skill
    for domain in domains:
        skills.extend(BASE_SKILLS.get(domain, []))

    # 2. Haiku가 추출한 의미 키워드 기반 추가
    for keyword in semantic_keywords:
        kw = keyword.lower().strip()
        if kw in KEYWORD_SKILLS:
            skills.extend(KEYWORD_SKILLS[kw])

    # 3. 복잡도 높으면 보안/QA/편향 방지 Skill 보강
    if complexity >= 5:
        has_dev = any(d.startswith("development") for d in domains)
        if has_dev:
            skills.append("dev.security.owasp")
            skills.append("qa.code-review.security")
            skills.append("dev.backend.api.logging")
        has_planning = any(d.startswith("planning") for d in domains)
        if has_planning:
            skills.append("meta.bias-prevention.confirmation-bias")
            skills.append("meta.bias-prevention.planning-fallacy")

    # 4. 후속 요청이면 이전 도메인 관련 Skill 유지
    if session.accumulated_skills:
        # 현재 도메인에 매핑되는 prefix 집합을 미리 계산
        current_prefixes: set[str] = set()
        for current_domain in domains:
            mapped = DOMAIN_TO_SKILL_PREFIX.get(current_domain, current_domain)
            current_prefixes.add(mapped)

        for prev_skill in session.accumulated_skills:
            # dev.backend.api.auth → ["dev", "dev.backend", "dev.backend.api"]
            parts = prev_skill.split(".")
            for i in range(1, len(parts)):
                prev_prefix = ".".join(parts[:i])
                if prev_prefix in current_prefixes:
                    skills.append(prev_skill)
                    break

    # 5. A/B test override: if active test exists for domain, use variant's skills
    try:
        from packages.hook_engine.ab_test import get_ab_manager
        for domain in domains:
            ab_test = get_ab_manager().get_active_test_for_domain(domain)
            if ab_test:
                variant = get_ab_manager().get_variant(ab_test.test_id)
                variant_skills = get_ab_manager().get_skills_for_variant(ab_test.test_id, variant)
                if variant_skills:
                    logger.info("A/B test %s: using variant %s skills for domain %s",
                                ab_test.test_id, variant, domain)
                    skills = variant_skills
                    break
    except Exception as e:
        logger.debug("A/B test check skipped: %s", e)

    deduped = _dedupe_preserve_order(skills)

    # 6. 복잡도별 스킬 수 cap 적용
    cap = _get_skill_cap(complexity)
    return _cap_skills(deduped, cap)


async def select_skills_hybrid(
    user_input: str,
    domains: list[str],
    semantic_keywords: list[str],
    complexity: int,
    session: Session,
) -> list[str]:
    """그래프 + 벡터 + 정적 하이브리드 스킬 선택.

    Neo4j/Qdrant 미가용 시 정적 선택으로 폴백.

    Returns:
        선택된 Atomic Skill ID 목록 (중복 없음, 순서 유지)
    """
    # 1. 정적 선택 (항상 실행 — 폴백 + 기준선)
    static_ids = select_skills(domains, semantic_keywords, complexity, session)

    # 2. 그래프 + 벡터 하이브리드 시도
    try:
        from packages.graph_rag.hybrid_selector import hybrid_select

        # 시드: 정적 결과 중 role 타입 스킬 (핵심 시드)
        seed_ids = [s for s in static_ids if s.endswith(".role")]
        if not seed_ids:
            seed_ids = static_ids[:5]  # role이 없으면 상위 5개

        result = await hybrid_select(
            query=user_input,
            seed_ids=seed_ids,
            static_ids=static_ids,
            domain=domains[0] if domains else "",
        )

        if result.skills:
            hybrid_ids = [s.skill_id for s in result.skills]
            logger.info(
                "Hybrid select: %d skills (graph=%d, vector=%d, static=%d)",
                len(hybrid_ids),
                result.graph_count,
                result.vector_count,
                result.static_count,
            )
            deduped = _dedupe_preserve_order(hybrid_ids)
            cap = _get_skill_cap(complexity)
            return _cap_skills(deduped, cap)

    except ImportError:
        logger.debug("graph_rag not available, using static selection")
    except Exception as e:
        logger.warning("Hybrid selection failed, falling back to static: %s", e)

    # 3. 폴백: 정적 결과 반환
    return static_ids
