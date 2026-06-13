# AI Pipeline — Atomic Skill 기반 코드 생성

## 동작 방식

1. 사용자가 요구사항을 입력하면 **UserPromptSubmit Hook**이 자동 실행
2. Hook이 Haiku로 요구사항을 분류 (도메인, 복잡도, 블룸 레벨, 키워드)
3. 분류 결과에 맞는 Atomic Skill을 선택하고 시스템 프롬프트로 조립
4. 조립된 지시사항이 `## AI Pipeline 지시사항` 블록으로 컨텍스트에 주입됨
5. 이 지시사항을 따라 코드를 작성
6. 작성 후 POST Check 체크리스트로 자가 검증

## 규칙

- `## AI Pipeline 지시사항` 블록이 주입되면 해당 System Prompt를 반드시 따를 것
- System Prompt에 명시된 출력 형식, 품질 기준, 코드 스타일을 준수
- 코드 작성이 끝나면 POST Check 항목을 하나씩 검증
- FAIL 항목이 있으면 코드를 수정한 후 다시 검증
- 분할 실행 모드에서는 도메인 순서대로 작업

## MCP 도구 (ai-pipeline)

필요 시 개별 스킬을 직접 조회할 수 있음:

- `get_skill(skill_id)` — 단일 스킬 조회 (예: `dev.backend.api.role`)
- `get_skills_batch(skill_ids)` — 여러 스킬 일괄 조회
- `search_skills(domain, tags, skill_type)` — 조건 검색
- `assemble_prompt(skill_ids)` — 스킬 목록을 시스템 프롬프트로 조립
- `prepare_plan(input, session_id?)` — 전체 파이프라인: 분류 → 선택 → 조립
- `validate(output, plan_result)` — POST 검증 체크리스트로 출력 검증
- `get_evolution_stats()` — 자가 진화 통계 (Neo4j 필요)
- `run_decay()` — 가중치 감쇠 실행 (Neo4j 필요)
- `get_pipeline_status()` — 파이프라인 상태 (스킬 수, 도메인 등)
- `get_domain_skills(domain)` — 도메인별 스킬 목록
- `get_usage_stats(top_n?)` — 스킬 사용 통계 (상위 N개)
- `get_cost_stats()` — API 비용 통계 (모델별 비용, 세션별 비용)
- `get_recommendations(skill_ids, top_n?)` — 사용 패턴 기반 스킬 추천
- `get_ab_tests(status?)` — A/B 테스트 목록 조회

## 프로젝트 구조

```
skills/              ← Atomic Skill YAML 파일 (도메인별 정리, 버전 관리)
packages/
  hook_engine/       ← 분류(classifier) + 스킬 선택(selector) + A/B 테스트 + 체크리스트
  skill_store/       ← MCP 서버 (14 tools) + 추천 엔진(recommender)
  post_validator/    ← POST 검증 로직
  graph_rag/         ← 하이브리드 선택기 + 동적 가중치 + 자동 수렴
hooks/
  on_prompt.py       ← UserPromptSubmit Hook 스크립트
apps/server/
  pipeline.py        ← Plan 준비 + 토큰 예산 최적화 + 검증 오케스트레이터
  main.py            ← FastAPI 서버 (Prometheus /metrics, /api/costs, /api/recommendations)
apps/dashboard/
  app.py             ← Streamlit 대시보드 (7탭: Skills, Domain, Evolution, Usage, History, Cost, Metrics)
scripts/
  generate_skill.py  ← 스킬 자동 생성 도구
  version_skill.py   ← 스킬 버전 관리 (bump/history/diff)
  evaluate_skills.py ← 스킬 품질 평가 (휴리스틱 점수)
  sync_obsidian.py   ← Obsidian 양방향 동기화
  audit_skills.py    ← 스킬 품질 감사
```
