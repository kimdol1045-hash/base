# AI Pipeline

AI Pipeline은 LLM 코드 생성 과정을 단순한 프롬프트 실행이 아니라, **요구사항 분석, 지식 선택, 실행 지시 조립, 결과 검증**으로 나누어 관리하는 실험적 AI 개발 파이프라인입니다.

이 프로젝트의 핵심 질문은 다음과 같습니다.

> AI에게 일을 맡길 때, 매번 긴 프롬프트를 사람이 다시 쓰지 않고도 도메인별 판단 기준과 검증 절차를 안정적으로 주입할 수 있을까?

AI Pipeline은 이 질문에 대해 `Atomic Skill`, `Hook Engine`, `POST Validator`, `Graph RAG`를 조합한 구조로 접근합니다.

## 문제 정의

일반적인 AI 코딩 워크플로우는 빠르지만 다음 문제가 자주 생깁니다.

- 요구사항이 모호하면 AI가 임의로 설계를 확정합니다.
- 백엔드, 프론트엔드, 보안, QA, 기획 기준이 한 프롬프트 안에서 뒤섞입니다.
- 좋은 답변을 얻기 위해 사용자가 매번 긴 시스템 프롬프트를 다시 작성해야 합니다.
- 결과물이 실제 품질 기준을 통과했는지 별도 검증이 약합니다.
- 반복 작업에서 얻은 판단 기준이 다음 작업으로 축적되지 않습니다.

AI Pipeline은 이 문제를 “더 긴 프롬프트”로 해결하지 않고, 작고 재사용 가능한 Skill 단위와 실행 전후 Hook으로 분리합니다.

## 프로젝트 목표

- 요구사항을 먼저 분류하고, 작업에 필요한 지식만 선택합니다.
- 도메인별 원칙, 패턴, 검증 기준을 `skills/`에 YAML로 축적합니다.
- 선택된 Skill을 실행용 시스템 프롬프트로 조립합니다.
- 생성 결과를 POST 체크리스트로 다시 검증합니다.
- 자주 함께 쓰이는 Skill 조합을 Graph RAG와 사용 기록으로 개선할 수 있는 구조를 만듭니다.

이 프로젝트는 “완성된 SaaS 제품”이라기보다, AI 개발 워크플로우를 실험하고 확장하기 위한 **로컬 우선 파이프라인/지식 시스템**입니다.

## 핵심 아이디어

### 1. Atomic Skill

Atomic Skill은 하나의 작은 판단 단위입니다. 예를 들어 REST API, 입력 검증, 인증, 보안 헤더, UX 접근성, PRD 작성, 테스트 전략 같은 지식을 각각 YAML 파일로 관리합니다.

각 Skill은 대체로 다음 정보를 가집니다.

- 어떤 도메인에 속하는가
- 어떤 이론이나 원칙을 근거로 하는가
- 실행 시 지켜야 할 규칙은 무엇인가
- 결과를 어떻게 검증할 것인가
- 예상 토큰 비용은 어느 정도인가

### 2. Hook Engine

사용자 입력이 들어오면 Hook Engine이 요구사항을 분석합니다.

```text
사용자 요구사항
  -> 도메인/복잡도/키워드 분류
  -> 필요한 Skill 선택
  -> 시스템 프롬프트 조립
  -> POST 체크리스트 생성
```

예를 들어 “로그인 API 만들어줘”라는 입력은 백엔드 API, 인증, 보안, 검증, 테스트 관련 Skill을 함께 활성화합니다.

### 3. POST Validator

AI가 코드를 생성한 뒤에는 결과를 그대로 믿지 않고 체크리스트로 검증합니다.

검증 항목은 작업 도메인과 키워드에 따라 달라집니다. 인증 작업이라면 토큰 만료, 민감정보 로깅, 권한 검증 같은 항목이 붙고, 프론트엔드 작업이라면 접근성, 상태 관리, 렌더링 비용 같은 항목이 붙습니다.

### 4. Graph RAG

Skill은 독립 파일이지만 실제 작업에서는 함께 쓰입니다. Graph RAG 계층은 Skill 간 관계, 사용 이력, 추천 가중치를 다루기 위한 실험 공간입니다.

Neo4j는 관계와 가중치를, Qdrant는 의미 검색을 담당하도록 설계했습니다.

## 사용 시나리오

- Codex/Claude Code 같은 로컬 코딩 에이전트에 MCP 도구로 연결합니다.
- 사용자의 자연어 요구사항을 `prepare_plan`으로 분석합니다.
- 선택된 Skill을 시스템 프롬프트로 조립해 코드 생성에 사용합니다.
- 생성된 결과를 `validate`로 검증합니다.
- 스킬 품질, 사용량, 비용, 추천 정보를 API나 대시보드에서 확인합니다.

## 현재 구현 범위

- 250개 이상의 Atomic Skill YAML
- FastMCP 기반 Skill Store 서버
- 요구사항 분류 및 Skill 선택 Hook Engine
- POST 체크리스트 생성 및 검증 흐름
- FastAPI 기반 API 서버
- Streamlit 기반 대시보드
- Neo4j/Qdrant 기반 Graph RAG 실험 모듈
- Obsidian용 Markdown Vault 변환본
- 스킬 생성, 감사, 동기화, 평가 스크립트

## 아키텍처

```text
사용자 요구사항
     |
     v
Hook Engine
  - 요구사항 분류
  - Skill 선택
  - 프롬프트 조립
  - 검증 체크리스트 생성
     |
     v
AI Executor
  - Codex / Claude Code / 기타 LLM 실행 환경
     |
     v
POST Validator
  - 생성 결과 검증
  - 실패 항목 정리
     |
     v
사용자에게 결과 반환
```

선택적으로 Graph RAG 계층이 Skill 관계 검색과 추천을 보강합니다.

```text
skills/ YAML
   |
   +-- Skill Store MCP
   +-- Hook Engine
   +-- Graph RAG
         +-- Neo4j: 관계/가중치
         +-- Qdrant: 의미 검색
```

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

## 로드맵

- Skill 품질 점수와 추천 가중치 개선
- Graph RAG 기반 Skill 관계 탐색 고도화
- 실행 결과와 검증 결과를 이용한 피드백 루프 강화
- 프로젝트별 Skill Pack 분리
- 대시보드에서 비용, 품질, 사용 패턴을 더 쉽게 비교하는 뷰 추가
- 공개 사용자를 위한 설치 문서와 예제 프로젝트 보강

## 보안 메모

- 실제 `.env` 파일은 커밋하지 않습니다. 공개 저장소에는 `.env.example`만 포함합니다.
- API 키, 토큰, 비밀번호는 GitHub Secrets, 로컬 `.env`, Vault 계열 도구 중 하나로 관리합니다.
- `.mcp.json`, `.claude/`, `.omc/`, 가상환경, 캐시, 로컬 DB 볼륨은 `.gitignore`로 제외합니다.
- Docker Compose의 Neo4j 비밀번호는 고정 기본값을 사용하지 않고 `.env`에서 필수로 주입합니다.
- 공개 전 정규식 기반 키 패턴 스캔을 수행했으며, 실제 키 형식의 토큰은 커밋에 포함하지 않았습니다.

## 라이선스

아직 라이선스 파일이 없습니다. 공개 배포 범위를 명확히 하려면 `LICENSE`를 추가하세요.
