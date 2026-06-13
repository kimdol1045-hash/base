# AI Pipeline — MCP 통합 가이드

AI Pipeline을 다른 프로젝트에서 MCP 서버로 연동하는 방법.

## 사용 가능한 도구 (10개)

| 도구 | 설명 |
|------|------|
| `get_skill(skill_id)` | 단일 Atomic Skill 조회 |
| `get_skills_batch(skill_ids)` | 여러 스킬 일괄 조회 |
| `search_skills(domain, tags, skill_type)` | 조건 기반 스킬 검색 |
| `assemble_prompt(skill_ids)` | 스킬 목록을 시스템 프롬프트로 조립 |
| `prepare_plan(input, session_id?)` | 전체 파이프라인: 분류 → 선택 → 조립 |
| `validate(output, plan_result)` | POST 검증 체크리스트로 출력 검증 |
| `get_evolution_stats()` | 자가 진화 통계 (Neo4j 필요) |
| `run_decay()` | 가중치 감쇠 실행 (Neo4j 필요) |
| `get_pipeline_status()` | 파이프라인 상태 (스킬 수, 도메인 등) |
| `get_domain_skills(domain)` | 도메인별 스킬 목록 |

## 로컬 stdio 모드 (권장)

같은 머신에서 Claude Code가 직접 서버를 실행하는 방식.

### 설정 (.mcp.json)

프로젝트 루트의 `.mcp.json`에 추가:

```json
{
  "mcpServers": {
    "ai-pipeline": {
      "type": "stdio",
      "command": "/absolute/path/to/ai-pipeline/.venv/bin/python",
      "args": ["-m", "packages.skill_store.server"],
      "env": {
        "SKILL_DIR": "/absolute/path/to/ai-pipeline/skills"
      }
    }
  }
}
```

> **중요**: `command`와 `SKILL_DIR`은 반드시 절대 경로로 지정.

### 사용 예시

Claude Code에서 자동으로 도구를 인식합니다:

```
사용자: "로그인 API 만들어줘"
→ Claude Code가 prepare_plan 호출
→ 분류 → 스킬 선택 → 시스템 프롬프트 조립
→ 코드 생성 → validate로 검증
```

## 원격 SSE 모드

서버를 별도 프로세스로 실행하고 SSE로 연결하는 방식.

### 서버 실행

```bash
cd /path/to/ai-pipeline
.venv/bin/python -m packages.skill_store.server --sse
# 기본 포트: 8000
```

### 설정 (.mcp.json)

```json
{
  "mcpServers": {
    "ai-pipeline": {
      "type": "sse",
      "url": "http://server-ip:8000/sse"
    }
  }
}
```

## 원격 Streamable HTTP 모드

```bash
.venv/bin/python -m packages.skill_store.server --streamable-http
```

```json
{
  "mcpServers": {
    "ai-pipeline": {
      "type": "streamable-http",
      "url": "http://server-ip:8000/mcp"
    }
  }
}
```

## Docker 환경

```bash
docker compose up -d
```

Docker 내부에서는 FastAPI 서버가 `/api/plan` 엔드포인트로 동일한 기능을 제공합니다.

## 핵심 워크플로우

```
1. prepare_plan(input="로그인 API") → Plan 반환
   ├── system_prompt: 조립된 지시사항
   ├── post_checks: 검증 체크리스트
   ├── model_hint: haiku/sonnet/opus
   └── max_tokens: 2048/4096/8192

2. (Claude가 코드 생성)

3. validate(output=code, plan_result=plan) → PASS/FAIL
```

## 환경 변수

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `SKILL_DIR` | `./skills` | Atomic Skill YAML 디렉토리 |
| `ANTHROPIC_API_KEY` | — | Haiku 분류기용 API 키 |
| `NEO4J_URI` | `bolt://localhost:7687` | Neo4j 연결 (선택) |
| `QDRANT_URL` | `http://localhost:6333` | Qdrant 연결 (선택) |
| `REDIS_URL` | — | 세션 저장소 (선택, 없으면 인메모리) |

## 트러블슈팅

### "Skill not found" 오류
- `SKILL_DIR` 경로가 올바른지 확인
- 절대 경로 사용 권장

### "Neo4j is unavailable"
- Graph RAG 기능은 선택사항
- Neo4j 없이도 정적 스킬 선택 동작

### prepare_plan 응답이 느림
- 첫 호출 시 Haiku 분류기 콜드 스타트
- `ANTHROPIC_API_KEY`가 설정되어 있는지 확인
