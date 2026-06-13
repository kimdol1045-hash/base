# AI Pipeline

Atomic Skill과 Hook Engine을 이용해 사용자 요구사항을 분류하고, 필요한 지시사항을 조립한 뒤, 결과물을 체크리스트로 검증하는 AI 코드 생성 보조 파이프라인입니다.

## 핵심 기능

- 요구사항 분류: 입력을 도메인, 복잡도, 블룸 레벨, 키워드로 분류합니다.
- Atomic Skill 조립: `skills/`의 YAML 지식을 선택해 시스템 프롬프트로 구성합니다.
- POST 검증: 생성된 출력이 요구사항과 품질 기준을 만족하는지 체크리스트로 확인합니다.
- MCP 연동: `packages/skill_store/server.py`를 통해 Codex/Claude Code 등에서 도구로 사용할 수 있습니다.
- Graph RAG 선택기: Neo4j, Qdrant, OpenAI Embedding을 이용한 하이브리드 스킬 선택을 지원합니다.
- 대시보드/API: FastAPI 서버와 Streamlit 대시보드로 상태, 비용, 사용량, 추천 정보를 확인합니다.

## 저장소 구조

```text
ai-pipeline/
  apps/server/        FastAPI API 서버
  apps/dashboard/     Streamlit 대시보드
  hooks/              프롬프트/도구 실행 훅
  packages/
    hook_engine/      분류, 스킬 선택, 검증 계획
    skill_store/      MCP 서버와 추천 엔진
    post_validator/   POST 검증 로직
    graph_rag/        Neo4j/Qdrant 기반 Graph RAG
  scripts/            스킬 생성, 감사, 동기화, 평가 도구
  skills/             Atomic Skill YAML 파일
  tests/              테스트 코드
graph-rag-vault/      Obsidian용으로 변환된 스킬 문서
tools/                보조 생성 스크립트
```

## 빠른 시작

```bash
cd ai-pipeline
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,dashboard,metrics]"
cp .env.example .env
```

`.env`에 필요한 값을 채웁니다. 최소 실행에는 `ANTHROPIC_API_KEY`가 필요하고, Graph RAG 기능을 쓰려면 `GRAPH_RAG_OPENAI_API_KEY`와 `GRAPH_RAG_NEO4J_PASSWORD`도 설정합니다.

```bash
openssl rand -base64 32
```

위 명령으로 만든 값을 `GRAPH_RAG_NEO4J_PASSWORD`에 넣는 것을 권장합니다.

## 실행

API 서버:

```bash
cd ai-pipeline
uvicorn apps.server.main:app --reload
```

대시보드:

```bash
cd ai-pipeline
streamlit run apps/dashboard/app.py
```

Docker 기반 로컬 서비스:

```bash
cd ai-pipeline
docker compose up -d
```

Docker Compose는 `.env`의 `GRAPH_RAG_NEO4J_PASSWORD`가 비어 있으면 시작하지 않도록 설정되어 있습니다.

## 주요 API

- `POST /api/plan`: 사용자 요구사항을 분석하고 실행 계획과 시스템 프롬프트를 반환합니다.
- `POST /api/validate`: 생성된 출력과 계획을 받아 체크리스트 검증 결과를 반환합니다.
- `GET /health`: 서버 상태를 확인합니다.
- `GET /metrics`: Prometheus 메트릭을 반환합니다. `prometheus_client` 설치 시 사용 가능합니다.

## MCP 사용

로컬 MCP 서버로 사용할 때는 프로젝트별 `.mcp.json`에 절대 경로를 지정합니다. 개인 경로가 들어가는 `.mcp.json`은 이 저장소에서 추적하지 않습니다.

```json
{
  "mcpServers": {
    "ai-pipeline": {
      "type": "stdio",
      "command": "/absolute/path/to/ai-pipeline/.venv/bin/python",
      "args": ["-m", "packages.skill_store.server"],
      "env": {
        "SKILL_DIR": "/absolute/path/to/ai-pipeline/skills",
        "PYTHONPATH": "/absolute/path/to/ai-pipeline"
      }
    }
  }
}
```

자세한 내용은 [ai-pipeline/docs/mcp-integration.md](ai-pipeline/docs/mcp-integration.md)를 참고하세요.

## 테스트와 품질 점검

```bash
cd ai-pipeline
pytest
ruff check .
python scripts/audit_skills.py
```

## 보안 메모

- 실제 `.env` 파일은 커밋하지 않습니다. 공개 저장소에는 `.env.example`만 포함합니다.
- API 키, 토큰, 비밀번호는 GitHub Secrets, 로컬 `.env`, Vault 계열 도구 중 하나로 관리합니다.
- `.mcp.json`, `.claude/`, `.omc/`, 가상환경, 캐시, 로컬 DB 볼륨은 `.gitignore`로 제외합니다.
- Docker Compose의 Neo4j 비밀번호는 고정 기본값을 사용하지 않고 `.env`에서 필수로 주입합니다.
- 공개 전 정규식 기반 키 패턴 스캔을 수행했으며, 실제 키 형식의 토큰은 커밋에 포함하지 않았습니다.

## 라이선스

아직 라이선스 파일이 없습니다. 공개 배포 범위를 명확히 하려면 `LICENSE`를 추가하세요.
