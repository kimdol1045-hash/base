# Phase 6: Graph RAG 생태계 구축 진행 기록

## 개요
250개 Atomic Skill의 정적 딕셔너리 선택 → Neo4j 지식 그래프 + Qdrant 벡터 DB 기반 확산 활성화 + 의미 검색 + 자가 발전 시스템으로 전환.

---

## 6-1. Neo4j 지식 그래프 (Step 1-6)
- [x] Step 1: docker-compose.yml — Neo4j 5 Community + Qdrant 컨테이너
- [x] Step 2: config.py, models.py, __init__.py — Pydantic Settings + 데이터 모델
- [x] Step 3: schema.py + neo4j_client.py — Cypher 상수 + async 드라이버 래퍼
- [x] Step 4: edge_extractor.py — BASE_SKILLS/KEYWORD_SKILLS에서 582개 엣지 추출
- [x] Step 5: ingest.py + cli.py ingest — 250개 YAML → Neo4j 배치 인제스트
- [x] Step 6: 6-1 완료 ✓

## 6-2. 벡터 DB (Step 7-9)
- [x] Step 7: embeddings.py — OpenAI text-embedding-3-small, 배치 임베딩
- [x] Step 8: vector_client.py + cli.py embed — Qdrant 컬렉션 관리 + 배치 업서트
- [x] Step 9: 6-2 완료 ✓

## 6-3. 확산 활성화 엔진 (Step 10-12)
- [x] Step 10: spread_activation.py — 3홉 Cypher (decay=0.85, threshold 0.50/0.40)
- [x] Step 11: hybrid_selector.py — graph(0.5) + vector(0.3) + static(0.2) 가중 병합
- [x] Step 12: 6-3 완료 ✓

## 6-4. 자가 발전 루프 (Step 13-15)
- [x] Step 13: self_evolution.py — PASS +0.05 / FAIL -0.05 / 감쇠 *0.95 / CO_OCCURS 자동 엣지
- [x] Step 14: community.py — Louvain 커뮤니티 탐지 (GDS) + 도메인 기반 폴백
- [x] Step 15: 6-4 완료 ✓

## 6-5. Hook Engine 연동 (Step 16-20)
- [x] Step 16: selector.py 수정 — select_skills_hybrid() async 래퍼 + 정적 폴백
- [x] Step 17: engine.py 수정 — await select_skills_hybrid() 호출
- [x] Step 18: pipeline.py 수정 — _record_evolution_feedback() 피드백 주입
- [x] Step 19: E2E 통합 테스트 — 21개 테스트 전체 통과
- [x] Step 20: 6-5 완료 ✓

## 6-6. 인프라 마무리 (Step 21-23)
- [x] Step 21: pyproject.toml (neo4j, qdrant-client, openai 추가), .env.example, .gitignore 업데이트
- [x] Step 22: tests/test_graph_rag.py — 21개 테스트 (config, models, edge_extractor, embeddings, hybrid_merge, selector_hybrid)
- [x] Step 23: Phase 6 전체 완료 ✓

---

## 진행 로그

### 2026-04-05: Phase 6 전체 구현 완료

**생성된 파일 (12개):**
```
packages/graph_rag/
├── __init__.py              (91B)
├── config.py                (1.4KB) — Pydantic Settings, 환경변수 기반
├── models.py                (2.0KB) — SkillNode, SkillEdge, ActivatedSkill, HybridResult
├── schema.py                (6.1KB) — Cypher 제약조건/인덱스/쿼리 상수 24개
├── neo4j_client.py          (3.9KB) — async 드라이버 래퍼, 연결 관리
├── vector_client.py         (5.3KB) — Qdrant async 클라이언트
├── edge_extractor.py        (6.1KB) — BASE/KEYWORD → 582개 엣지 추출
├── embeddings.py            (3.5KB) — OpenAI 임베딩 + YAML 로더
├── ingest.py                (5.9KB) — Neo4j + Qdrant 인제스트
├── spread_activation.py     (6.8KB) — 3홉 확산 활성화
├── hybrid_selector.py       (6.2KB) — 3소스 가중 병합
├── self_evolution.py        (5.4KB) — 가중치 업데이트 + 자동 엣지
├── community.py             (3.8KB) — Louvain + 도메인 폴백
└── cli.py                   (6.3KB) — 6개 명령어
```

**수정된 파일 (5개):**
- `docker-compose.yml` — 새로 생성 (Neo4j + Qdrant)
- `pyproject.toml` — neo4j, qdrant-client, openai, pydantic-settings 의존성 추가
- `.env.example` — GRAPH_RAG_* 환경변수 10개 추가
- `.gitignore` — Docker 볼륨 디렉토리 추가
- `packages/hook_engine/selector.py` — select_skills_hybrid() 추가
- `packages/hook_engine/engine.py` — hybrid selector 호출로 변경
- `apps/server/pipeline.py` — _record_evolution_feedback() 추가

**테스트 결과 (Phase 7 포함):**
- 88개 테스트 전체 PASSED (6.22s)
  - test_graph_rag.py: 21개 (config, models, edge_extractor, embeddings, hybrid_merge, selector_hybrid)
  - test_skill_store.py: 18개 (get_skill, batch, assemble_prompt, search, resolve_path)
  - test_hook_engine.py: 28개 (classifier, selector, post_checks, engine 통합)
  - test_post_validator.py: 9개 (PASS/FAIL 판정, graceful fallback)
  - test_pipeline_e2e.py: 12개 (전체 파이프라인, retry, split, error, evolution, session)
- 250개 스킬 로드 확인
- 582개 엣지 추출 확인
- 하이브리드 병합 로직 정확성 검증
- Neo4j 미가용 시 정적 폴백 동작 확인

**핵심 수치:**
| 항목 | 값 |
|------|-----|
| 노드 (스킬) | 250개 |
| 엣지 (초기) | 582개 (REQUIRES, FEEDS, CO_CREATES) |
| BASE_SKILLS 도메인 | 17개 |
| KEYWORD_SKILLS 키워드 | 80+개 |
| 확산 파라미터 | decay=0.85, threshold=0.50/0.40, 3홉 |
| 하이브리드 가중치 | graph=0.5, vector=0.3, static=0.2 |
| 자가 발전 | PASS +0.05, FAIL -0.05, decay *0.95 |

---

## Phase 7: 테스트 — 88개 → 102개 PASSED ✓

### 2026-04-05: Phase 7 + Phase 8 완료

**Phase 7 테스트 파일 (4개):**
- `tests/test_skill_store.py` — 18개 테스트
- `tests/test_hook_engine.py` — 28개 테스트
- `tests/test_post_validator.py` — 9개 → 21개 (8-3 파싱 안정화 테스트 12개 추가)
- `tests/test_pipeline_e2e.py` — 12개 → 14개 (8-4 비용 최적화 테스트 2개 추가)

---

## Phase 8: 품질 개선 + 실전 튜닝 ✓

### 8-1. 벤치마크 (20개 실전 요청)
- `tests/benchmark.py` — 20개 케이스, 8개 카테고리
- **종합 점수: 0.99 / 1.00** (20/20 케이스 7점+ 달성)
- 카테고리별: backend 1.00, frontend 0.97, planning 1.00, marketing 1.00, design 1.00, qa 1.00, analytics 1.00, complex 1.00
- 평가 가중치: domain_recall(0.25) + keyword_recall(0.15) + skill_recall(0.35) + complexity_in_range(0.15) + model_correct(0.10)

### 8-2. 분류 + 검색 정확도
- Mock 모드: 정적 스킬 선택 정확도 0.99 (1개 케이스 모델 경계값 이슈)
- Live 모드: `python tests/benchmark.py --live` (실제 API 호출)
- 벤치마크에 live 모드 포함, Haiku 분류 정확도 측정 가능

### 8-3. POST 검증 개선
- `_parse_validation_response()` 파서 신규 구현
  - "최종 판정: PASS/FAIL" 텍스트 매칭 (공백/콜론 유연)
  - JSON 형식 지원 ({"verdict": "PASS"})
  - 코드블록 내 JSON 지원
  - [PASS]/[FAIL] 항목별 집계 → pass_count, fail_count
  - 판정 불가 시 안전 기본값 PASS
- `ValidationResult`에 pass_count, fail_count, check_details 필드 추가
- 12개 파싱 테스트 추가

### 8-4. 비용 최적화
- **complexity ≤ 2 시 POST 검증 스킵**: API 호출 3회 → 2회 (33% 절감)
- **세션 컨텍스트 크기 제한**: MAX_SESSION_OUTPUTS=10, MAX_SESSION_SKILLS=50
- 파이프라인 상수: `POST_VALIDATION_SKIP_THRESHOLD=2`

**테스트 결과:**
- 102개 테스트 전체 PASSED (5.65s)
- 0개 lint 에러 (ruff)

---

## Phase 8.5: Hook & Skill 고도화 ✓

### 2026-04-05: 프로덕션 안정화 + 대규모 확장

#### 8.5-1. 핵심 버그 수정 (8건)
- 세션 메모리 누수: TTL 3600s + MAX_SESSIONS=1000 + LRU eviction
- 검증 우회: PASS→INCONCLUSIVE 폴백, 단어경계 매칭, 에러 시 INCONCLUSIVE
- Bloom 폴백: CREATE→APPLY 변경
- 복잡도 하한: `max(0, min(int(...), 10))`
- max_tokens: 300→500 (JSON 잘림 방지)
- 복잡도 기반 max_tokens: ≤3→2048, ≤6→4096, >6→8192
- POST 체크리스트 상한: MAX_POST_CHECKS=15
- 하드코딩 상수 추출 (engine.py)

#### 8.5-2. 파이프라인 구조 변경
- Claude API 직접 호출 제거 → Hook 시스템으로 완전 전환
- prepare_plan() / prepare_split_plans() / validate_and_record() 분리
- evolution feedback fire-and-forget (asyncio.create_task)
- 분할 실행 FAIL 시 1회 재시도

#### 8.5-3. Claude Code Hook 통합
| Hook Event | 파일 | 기능 |
|-----------|------|------|
| UserPromptSubmit | hooks/on_prompt.py | 분류→스킬선택→프롬프트 조립→컨텍스트 주입 |
| Stop | hooks/on_stop.py | POST 검증→FAIL 시 블로킹 (MAX_RETRIES=3) |
| PreToolUse (Bash) | hooks/pre_tool_bash.py | 위험 명령 패턴 차단 (rm /, force push 등 16패턴) |
| PreToolUse (Write/Edit) | hooks/pre_tool_write.py | 민감 파일 + 하드코딩 시크릿 탐지 |
| PostToolUse (Write/Edit) | hooks/post_tool_write.py | TS any/console.log/eval 등 코드 품질 경고 |

- hooks/common.py: 공통 .env 파서 모듈
- stderr→파일 리다이렉트 (디버깅 지원)

#### 8.5-4. 신규 도메인 추가 (5개)
- `development.ai` — LLM/RAG 통합
- `marketing.seo` — 기술 SEO
- `marketing.growth` — 그로스 해킹
- `qa.code-review` — 코드 리뷰 전문
- `qa.testing` — 테스트 전문

#### 8.5-5. 신규 Atomic Skill 추가 (51개)
**Tier 1 — 핵심 프레임워크 (12개):**
- React Patterns, Next.js Patterns, Hexagonal Architecture, Event Sourcing
- OWASP API Top 10, Observability, SRE
- OKR, Design Sprint, AARRR
- Atomic Design, Mutation Testing

**Tier 2 — 확장 이론 (19개):**
- GoF Patterns, Repository, SOLID, Supply Chain Security, MITRE ATT&CK
- Story Mapping, North Star, Content Marketing, Inbound
- Data Pipeline, Data Quality, Event Tracking
- Fuzz/Smoke/Regression Testing, Information Architecture, Motion Design
- Incident Management, FinOps

**Tier 3 — 기존 누락 이론 (20개):**
- Funnel/Cohort/DORA Metrics, Technical Docs, Error Messages, Changelog
- Clean Architecture, Strangler Fig, Outbox Pattern, Conway's Law
- NIST Framework, IaC, Chaos Engineering
- BDD, Testing Trophy, Property-Based Testing
- Kano Model, RICE, Cognitive Load, Scanning Patterns

#### 8.5-6. 매핑 확장
- KEYWORD_SKILLS: 96개 → 136개 키워드
- KEYWORD_POST_CHECKS: 28개 → 58개 키워드
- DOMAIN_POST_CHECKS: 17개 → 22개 도메인
- BASE_SKILLS: 17개 → 22개 도메인

**핵심 수치 (업데이트):**
| 항목 | 이전 | 이후 |
|------|------|------|
| 노드 (스킬) | 250개 | 301개 |
| BASE_SKILLS 도메인 | 17개 | 22개 |
| KEYWORD_SKILLS 키워드 | 96개 | 136개 |
| KEYWORD_POST_CHECKS | 28개 | 58개 |
| Hook 이벤트 | 0개 | 5개 |
| 테스트 | 102개 | 106개 |

**테스트 결과:**
- 106개 테스트 전체 PASSED (13.19s)
- Obsidian vault 동기화: 51개 노트 생성, 7개 MOC 업데이트
