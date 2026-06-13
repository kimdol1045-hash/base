# AI 풀스택 파이프라인 마스터 문서
## 150개 이론 · 35개 Hook · Graph RAG · 연결형 Claude Skills 통합 아키텍처

> **목적:** 검증된 학술 이론 150개를 기반으로 AI의 할루시네이션을 원천 차단하고,  
> 온톨로지 기반 확산 활성화 + Graph RAG DB + 35개 Hook으로  
> 기획·디자인·프론트엔드·백엔드·DB·보안·QA·배포·마케팅·분석 전 프로세스를  
> 신뢰도 높게 자동화한다.

---

# PART 1: 전체 아키텍처

## 1-1. 3-Layer 시스템 구조

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1: THEORETICAL FOUNDATION (학문적 기반)            │
│  150개 이론 · 논문 → AI 판단의 근거                        │
│  인지심리학 20 + 연결/시스템 10 + 교육학 10 + UX 15        │
│  + 설득/마케팅 16 + SW공학 10 + 편향 10 + 비즈니스 7       │
│  + 백엔드 8 + DB 6 + 보안 8 + QA 8 + DevOps 6            │
│  + 성능 5 + 프로젝트관리 5 + 분석 4 + 콘텐츠 2            │
└──────────────────────┬──────────────────────────────────┘
                       │ 근거 주입
┌──────────────────────▼──────────────────────────────────┐
│  LAYER 2: SKILL ONTOLOGY GRAPH (연결형 Skill 네트워크)    │
│  40+ Skill 노드 · 가중치 엣지 · 확산 활성화                │
│  5개 도메인: 기획/디자인/개발/마케팅/QA                     │
│  각 Skill = 블룸 레벨 + 인지 시스템 + 이론 기반 + 훅 연결   │
│  ┌─────────────────────────────────────────────────┐    │
│  │  35개 Hook = Skill 감싸는 미들웨어                │    │
│  │  Core 5 + Cognitive 5 + Security 5 + QA 5       │    │
│  │  + Data 4 + Performance 3 + Engineering 4       │    │
│  │  + Evolution 4                                   │    │
│  └─────────────────────────────────────────────────┘    │
└──────────────────────┬──────────────────────────────────┘
                       │ 저장 · 검색 · 학습
┌──────────────────────▼──────────────────────────────────┐
│  LAYER 3: GRAPH RAG DB (지식 그래프 + 벡터 DB)            │
│  Neo4j: 관계/엣지/확산활성화/자가발전/추적                  │
│  Supabase pgvector: 자연어 의미 검색/실행 로그 축적         │
└─────────────────────────────────────────────────────────┘
```

## 1-2. 핵심 설계 원칙

| 원칙 | 학문적 근거 | 구현 |
|------|-----------|------|
| 하나의 Skill이 아닌 Skill 네트워크가 작동 | 확산 활성화 (Collins & Loftus, 1975) | 온톨로지 그래프에서 관련 Skill 동시 활성화 |
| Skill 네트워크 전체가 하나의 인지 시스템 | 분산 인지 (Hutchins, 1995) | 양방향 정보 흐름, 공유 컨텍스트 |
| AI 판단은 검증된 이론에 기반 | 스키마 이론 (Bartlett, 1932) | 도메인 스키마 사전 주입 |
| 매 실행마다 자기 검증 | 메타인지 MGV (Flavell, 1979 / Oh & Gobet, 2025) | Monitor→Generate→Verify 루프 |
| 자주 쓰이는 조합이 강화됨 | 확산 활성화 + 의도적 연습 (Ericsson, 1993) | 엣지 가중치 자동 업데이트 |
| 다층 방어로 오류 차단 | 스위스 치즈 모델 (Reason, 1990) | 35개 Hook이 PRE/DURING/POST에서 다층 검증 |

---

# PART 2: 이론 총람 — 150개 이론 + 논문 레퍼런스

## A. 인지심리학 / 기억 / 학습 (20개)

| # | 이론 | 논문 | 핵심 원리 | Skill 적용 |
|---|------|------|----------|-----------|
| 1 | 인지부하 이론 | Sweller (1988) *Cognitive Science* 12(2) 257-285 | 작업기억 한계: 내재적/외재적/본질적 부하 | Skill 최소 단위 분할, 컨텍스트 정리 |
| 2 | LLM 인지부하 | Zhang et al. (2024) *arXiv:2509.19517* | LLM도 fragility tipping point 존재 | 프롬프트 길이 제한, 주의 잔류 방지 |
| 3 | 밀러의 법칙 | Miller (1956) *Psych. Rev.* 63(2) 81-97 | 작업기억 7±2 청크 | 변수/출력 7개 이내 |
| 4 | 청킹 | Chase & Simon (1973) *Cognitive Psychology* 4(1) 55-81 | 전문가는 의미 단위로 묶어 처리 | 관련 Skill을 청크로 그룹핑 |
| 5 | 이중과정 이론 | Kahneman (2011) *Thinking, Fast and Slow* / Evans (2008) *Ann. Rev. Psych.* 59 255-278 | 시스템 1(직관) vs 시스템 2(분석) | 복잡도별 Skill 라우팅 |
| 6 | 스키마 이론 | Bartlett (1932) *Remembering* / Rumelhart (1980) *Theoretical Issues in Reading* / Anderson (1977) | 기존 지식 구조가 새 정보 해석 좌우 | 도메인 스키마 사전 주입 → 할루시네이션 감소 |
| 7 | ELM (정교화 가능성) | Petty & Cacioppo (1986) *Adv. Exp. Social Psych.* 19 123-205 | 설득의 중심 경로(논리) vs 주변 경로(단서) | 마케팅: 관여도별 카피 전략 분기 |
| 8 | 메타인지 | Flavell (1979) *Am. Psychologist* 34(10) 906-911 | 자기 인지에 대한 인지: 지식/경험/과제/전략 | MGV 루프 |
| 9 | MGV 프레임워크 | Oh & Gobet (2025) *arXiv:2510.16374* COLM Workshop | Flavell을 LLM에 구현. 정확도 75% vs SELF-REFINE 68% | 모든 Skill에 MGV 내장 |
| 10 | 심적 모델 | Johnson-Laird (1983) *Mental Models* Harvard UP | 명제가 아닌 심적 모델로 추론 | 구체적 시나리오 기반 동작 |
| 11 | 이중 부호화 | Paivio (1971) *Imagery and Verbal Processes* / (1986) *Mental Representations* | 시각+언어 이중 부호화 → 이해 향상 | 텍스트+시각 동시 출력 |
| 12 | 처리 수준 | Craik & Lockhart (1972) *JVLVB* 11(6) 671-684 | 깊은 처리(의미적) → 강한 기억 | 의미적 구조 처리 |
| 13 | 간격 효과 | Ebbinghaus (1885) *Über das Gedächtnis* / Cepeda et al. (2006) *Psych. Bull.* 132(3) 354-380 | 분산 학습 > 집중 학습 | 온톨로지 점진적 강화 |
| 14 | 인터리빙 | Rohrer & Taylor (2007) *Instructional Science* 35(6) 481-498 | 다른 유형 섞어 연습 → 전이력 향상 | Skill 조합 다양화 |
| 15 | 검색 연습 | Roediger & Karpicke (2006) *Psych. Science* 17(3) 249-255 | 정보 인출 행위 자체가 학습 강화 | Verify 단계 = Skill 자체 강화 |
| 16 | 바람직한 어려움 | Bjork (1994) *Metacognition: Knowing about Knowing* MIT Press 185-205 | 적절한 어려움이 장기 학습에 도움 | 적절한 도전 수준 유지 |
| 17 | 인지적 유연성 | Spiro et al. (1988) *Cognitive Science Society* | 복잡 영역은 다중 관점 접근 필요 | 크로스 도메인 Skill 연결 |
| 18 | 인지적 도제 | Collins, Brown & Newman (1989) *Knowing, Learning, and Instruction* 453-494 | 모델링→코칭→스캐폴딩→페이딩 | AI 스캐폴딩 6단계 조절 |
| 19 | 상황 학습 | Lave & Wenger (1991) *Situated Learning* Cambridge UP | 학습은 실천 공동체 참여로 발생 | 서비스 데이터 축적 = Skill 실천 이력 |
| 20 | 전문성/의도적 연습 | Ericsson et al. (1993) *Psych. Rev.* 100(3) 363-406 | 의도적 연습 → 전문성 | 온톨로지 자가 발전 = 의도적 연습 |

## B. 확산 / 연결 / 시스템 (10개)

| # | 이론 | 논문 | 핵심 원리 | Skill 적용 |
|---|------|------|----------|-----------|
| 21 | **확산 활성화** | Collins & Loftus (1975) *Psych. Rev.* 82(6) 407-428 | 노드 활성화 → 연결 노드로 가중치 기반 전파 | **연결형 Skill 아키텍처 핵심** |
| 22 | 분산 인지 | Hutchins (1995) *Cognition in the Wild* MIT Press / Hollan et al. (2000) *ACM TOCHI* 7(2) 174-196 | 인지 = 사람+도구+환경에 분산 | Skill 네트워크 = 하나의 인지 시스템 |
| 23 | 활동 이론 | Engeström (1987) *Learning by Expanding* / (2000) *Ergonomics* 43(7) 960-974 | 6요소 삼각형 + 모순이 발전 동력 | 모순 감지 Hook, 시스템 설계 |
| 24 | 구조 매핑 | Gentner (1983) *Cognitive Science* 7(2) 155-170 | 유추 = 관계 구조의 매핑 | 크로스 도메인 Skill 전이 |
| 25 | SME 엔진 | Falkenhainer et al. (1989) *AI* 41(1) 1-63 | 구조 매핑의 계산 모델 | 유사 구조 Skill 간 자동 지식 전이 |
| 26 | 정보 수렵 | Pirolli & Card (1999) *Psych. Rev.* 106(4) 643-675 | 정보 탐색 = 비용 대비 가치 극대화 | UX: 정보 냄새(scent) 설계 |
| 27 | 시스템 사고 | Senge (1990) *The Fifth Discipline* | 전체 시스템의 피드백 루프로 이해 | 파이프라인 피드백 루프 설계 |
| 28 | 사이버네틱스 | Wiener (1948) *Cybernetics* MIT Press | 피드백 기반 자기 조절 | Hook의 MGV 루프 |
| 29 | 복잡적응시스템 | Holland (1995) *Hidden Order* / (1992) *Daedalus* 121(1) 17-30 | 단순 규칙 → 복잡한 적응 행동 창발 | 단순 Skill 규칙들이 모여 복잡한 프로덕트 생성 |
| 30 | Conway의 법칙 | Conway (1968) *Datamation* 14(4) 28-31 | 시스템 구조 = 조직 구조의 복사본 | Skill 아키텍처가 프로덕트에 반영 |

## C. 교육학 / 학습 설계 (10개)

| # | 이론 | 논문 | 핵심 원리 | Skill 적용 |
|---|------|------|----------|-----------|
| 31 | 블룸 택소노미 | Anderson & Krathwohl (2001) *Taxonomy for Learning* | 인지 6단계: Remember→Create | Skill 체이닝 순서 결정 |
| 32 | ZPD | Vygotsky (1978) *Mind in Society* Harvard UP | 최적 학습 영역 + 점진적 지원 | 입력 구체성별 스캐폴딩 |
| 33 | 스캐폴딩 | Wood, Bruner & Ross (1976) *JCPP* 17(2) 89-100 | 스캐폴딩의 실험적 검증 | 모호한 입력 → 단계적 안내 |
| 34 | 구성주의 | Piaget (1976) / Bruner (1966) *Toward a Theory of Instruction* | 지식은 전달 아닌 구성 | 추론 과정+근거 함께 출력 |
| 35 | 경험 학습 | Kolb (1984) *Experiential Learning* | 구체경험→반성→개념화→실험 | 프로젝트 실행→리뷰→패턴 추출 |
| 36 | 역방향 설계 | Wiggins & McTighe (1998) *Understanding by Design* | 결과에서 역방향으로 설계 | 기획: 결과→기능→구현 순서 |
| 37 | ADDIE | Branson et al. (1975) *Interservice Procedures for ISD* | 분석→설계→개발→구현→평가 | 프로덕트 파이프라인 프레임 |
| 38 | 멀티미디어 학습 | Mayer (2009) *Multimedia Learning* Cambridge UP | 시각+청각 채널 분리 | 텍스트와 시각 역할 분리 |
| 39 | 생성 학습 | Fiorella & Mayer (2015) *Learning as a Generative Activity* | 요약/매핑/자기설명 → 깊은 학습 | Skill이 자기설명 포함 출력 |
| 40 | 자기조절학습 | Zimmerman (2002) *Theory Into Practice* 41(2) 64-70 | 계획→실행 모니터링→자기반성 | MGV 루프와 직접 대응 |

## D. UX / 디자인 심리학 (15개)

| # | 이론 | 논문 | Skill 적용 |
|---|------|------|-----------|
| 41 | 힉스 법칙 | Hick (1952) *QJEP* 4(1) 11-26 | UI 옵션 최소화 |
| 42 | 피츠 법칙 | Fitts (1954) *JEP* 47(6) 381-391 | CTA 44px+, 중요 요소 크고 가까이 |
| 43 | 게슈탈트 원리 | Wertheimer (1923) *Psych. Forschung* 4 301-350 | 시각적 그룹핑, 레이아웃 |
| 44 | 제이콥 법칙 | Nielsen (2000/1993) *Usability Engineering* | 검증된 UI 패턴 우선 |
| 45 | 재인 vs 회상 | Nielsen (1993) | 선택지 제시 > 빈칸 입력 |
| 46 | 폰 레스토프 효과 | Von Restorff (1933) *Psych. Forschung* 18 299-342 | CTA 시각적 차별화 |
| 47 | 직렬 위치 효과 | Murdock (1962) *JEP* 64(5) 482-488 | 핵심 기능을 처음/마지막 배치 |
| 48 | 자이가르닉 효과 | Zeigarnik (1927) *Psych. Forschung* 9 1-85 | 프로그레스 바로 완료 동기 유발 |
| 49 | 피크엔드 규칙 | Kahneman et al. (1993) *Psych. Science* 4(6) 401-405 | 핵심 순간+마지막 경험에 집중 |
| 50 | 심미적 사용성 | Tractinsky et al. (2000) *Interacting with Computers* 13(2) 127-145 | 미적 품질도 기본값 |
| 51 | 진행 기부 효과 | Nunes & Drèze (2006) *J. Consumer Research* 32(4) 504-512 | 온보딩: 2/7로 표시 |
| 52 | 도허티 임계값 | Doherty & Thadhani (1982) *IBM Systems J.* 21(3) 305-317 | 응답 400ms 이내 |
| 53 | 테슬러 법칙 | Tesler (2007) / Norman (2007) | Skill이 복잡성 흡수 |
| 54 | 정보 수렵 (UX) | Pirolli & Card (1999) / Chi et al. (2001) *CHI 2001* | 명확한 레이블링 |
| 55 | (도허티 확장) | Doherty (1982) | 프론트엔드 성능 목표 |

## E. 설득 / 행동경제학 / 마케팅 (16개)

| # | 이론 | 논문 | Skill 적용 |
|---|------|------|-----------|
| 56 | AIDA | Strong (1925) *Psychology of Selling* | marketing.copy 구조 |
| 57 | JTBD | Christensen (2003) *Innovator's Solution* | planning.problem-definition |
| 58 | Hook Model | Eyal (2014) *Hooked* | SaaS 리텐션 설계 |
| 59 | 넛지 이론 | Thaler & Sunstein (2008) *Nudge* Yale UP | 전환율 최적화 |
| 60 | 앵커링 효과 | Tversky & Kahneman (1974) *Science* 185 1124-1131 | 가격 제시 전략 |
| 61 | 프로스펙트 이론 | Kahneman & Tversky (1979) *Econometrica* 47(2) 263-291 | 손실 회피 기반 카피 |
| 62 | 사회적 증거 | Cialdini (1984) *Influence* Ch.4 | 리뷰 수, 사용자 수 표시 |
| 63 | 희소성 | Cialdini (1984) Ch.7 / Worchel et al. (1975) *JPSP* 32(5) | 한정 수량/마감 표시 |
| 64 | 권위 | Cialdini (1984) Ch.6 / Milgram (1963) *JASP* 67(4) | 전문가 추천, 인증 배지 |
| 65 | 상호성 | Cialdini (1984) Ch.2 / Gouldner (1960) *ASR* 25(2) | 무료 가치 → 유료 전환 |
| 66 | 일관성 | Cialdini (1984) Ch.3 / Festinger (1957) | 마이크로 커밋먼트 |
| 67 | 포그 행동 모델 | Fogg (2009) *Persuasive Technology* ACM Article 40 | CTA: 동기×능력×촉발 |
| 68 | 인지 부조화 | Festinger (1957) *Theory of Cognitive Dissonance* | 투자 시간으로 이탈 비용 증가 |
| 69 | 소유 효과 | Thaler (1980) *JEBO* 1(1) 39-60 | 맞춤 데이터 → 해지 어려움 |
| 70 | 단순 노출 | Zajonc (1968) *JPSP* 9(2) 1-27 | 리타겟팅, 브랜드 반복 노출 |
| 71 | 포터 5 Forces | Porter (1979) *HBR* 57(2) 137-145 | 경쟁사 분석 |

## F. 소프트웨어 공학 (10개)

| # | 이론 | 출처 | Skill 적용 |
|---|------|------|-----------|
| 72 | SOLID | Martin (2003) *Agile Software Development* | 1Skill=1책임 |
| 73 | DRY/KISS | Hunt & Thomas (1999) *Pragmatic Programmer* | 중복 Skill 금지 |
| 74 | 관심사 분리 | Dijkstra (1982/1974) *Selected Writings* EWD 447 | 도메인별 분리 |
| 75 | Unix 철학 | McIlroy et al. (1978) *BSTJ* 57(6) / Raymond (2003) | 작은 Skill + 파이프 연결 |
| 76 | Brooks의 법칙 | Brooks (1975) *Mythical Man-Month* | 기존 Skill 최적화 우선 |
| 77 | 옥캄의 면도날 | William of Ockham (c.1320) | 가장 단순한 해결책 |
| 78 | PDCA | Deming (1986) *Out of the Crisis* | 피드백 루프 |
| 79 | 카이젠 | Imai (1986) *Kaizen* | 점진적 개선 |
| 80 | 파레토 법칙 | Pareto (1896) / Juran (1951) | 핵심 20%에 집중 |
| 81 | Conway의 법칙 | Conway (1968) *Datamation* 14(4) 28-31 | 시스템=조직 구조 |

## G. 의사결정 / 편향 — 할루시네이션 방지 핵심 (10개)

| # | 편향 | 논문 | 방지 대상 |
|---|------|------|----------|
| A1 | 확증 편향 | Wason (1960) *QJEP* 12(3) / Nickerson (1998) *Rev. Gen. Psych.* 2(2) | 기존 결론만 지지하는 증거 찾기 |
| A2 | 더닝-크루거 | Kruger & Dunning (1999) *JPSP* 77(6) 1121-1134 | AI 능력 과대평가 |
| A3 | 제한된 합리성 | Simon (1955) *QJE* 69(1) 99-118 | 최적해 아닌 만족해 인지 |
| A4 | 만족화 | Simon (1956) *Psych. Rev.* 63(2) 129-138 | MVP: "충분히 좋은" 해 빠르게 |
| A5 | 프레이밍 효과 | Tversky & Kahneman (1981) *Science* 211 453-458 | 표현 방식에 따른 판단 왜곡 |
| A6 | 가용성 편향 | Tversky & Kahneman (1973) *Cognitive Psychology* 5(2) 207-232 | 최근 트렌드 과대평가 |
| A7 | 생존자 편향 | Wald (1943) *Statistical Research Group* | 성공 사례만 보고 결론 |
| A8 | 매몰 비용 | Arkes & Blumer (1985) *OBHDP* 35(1) 124-140 | 잘못된 방향 유지 |
| A9 | 계획 오류 | Buehler, Griffin & Ross (1994) *JPSP* 67(3) 366-381 | 시간 과소 추정 |
| A10 | 후견 편향 | Fischhoff (1975) *JEP:HPP* 1(3) 288-299 | "처음부터 알고 있었다" 착각 |

## H. 비즈니스 / 혁신 (7개)

| # | 이론 | 출처 | Skill 적용 |
|---|------|------|-----------|
| B1 | 린 스타트업 | Ries (2011) *The Lean Startup* | Build-Measure-Learn |
| B2 | 더블 다이아몬드 | Design Council (2005) | 발산→수렴→발산→수렴 |
| B3 | 디자인 사고 | Brown (2008) *HBR* 86(6) / (2009) *Change by Design* | 공감→정의→발상→프로토→테스트 |
| B4 | TAM | Davis (1989) *MIS Quarterly* 13(3) 319-340 | 유용성+사용 용이성→수용 |
| B5 | 혁신 확산 | Rogers (1962/2003) *Diffusion of Innovations* | 채택자 세그먼트별 전략 |
| B6 | 플로우 | Csikszentmihalyi (1990) *Flow* | 도전≈능력→몰입 |
| B7 | 자기결정 이론 | Deci & Ryan (1985) / Ryan & Deci (2000) *Am. Psych.* 55(1) 68-78 | 자율성+유능감+관계성 |

## I~IX. 엔지니어링 영역 (52개)

### 백엔드/API (8개)

| # | 이론 | 논문 | Skill 적용 |
|---|------|------|-----------|
| 99 | CAP 정리 | Brewer (2000) PODC / Gilbert & Lynch (2002) *SIGACT News* 33(2) / Brewer (2012) *Computer* 45(2) 23-29 | DB 선택 기준 |
| 100 | ACID | Haerder & Reuter (1983) *ACM Computing Surveys* 15(4) 287-317 | 핵심 트랜잭션 필수 |
| 101 | REST | Fielding (2000) PhD Dissertation UC Irvine Ch.5 | API 설계 규칙 |
| 102 | DDD | Evans (2003) *Domain-Driven Design* / Akbari et al. (2025) *JSS* SLR | 복잡한 비즈니스 로직 구조화 |
| 103 | 12-Factor | Wiggins (2011) 12factor.net | 배포 체크리스트 |
| 104 | 이벤트 주도 | Hohpe & Woolf (2003) *Enterprise Integration Patterns* | 서비스 간 느슨한 결합 |
| 105 | CQRS | Young (2010) / Fowler (2011) | 읽기/쓰기 모델 분리 |
| 106 | 멱등성 | RFC 7231 (2014) Section 4.2.2 | 결제 API 중복 안전 |

### DB/데이터 (6개)

| # | 이론 | 논문 | Skill 적용 |
|---|------|------|-----------|
| 107 | 정규화 | Codd (1970) *CACM* 13(6) 377-387 / Kent (1983) *CACM* 26(2) | 스키마 설계 |
| 108 | 비정규화 | Hellerstein et al. (2007) *Found. & Trends in DB* 1(2) | 읽기 최적화 |
| 109 | 이벤트 소싱 | Fowler (2005) / Betts et al. (2012) Microsoft P&P | 이력 완전 보존 |
| 110 | 데이터 메시 | Dehghani (2022) *Data Mesh* O'Reilly | 도메인별 데이터 소유 |
| 111 | 스키마 전략 | Stonebraker et al. (2010) *CACM* 53(1) 64-71 | 읽기/쓰기 시 스키마 |
| 112 | PACELC | Abadi (2012) *Computer* 45(2) 37-42 | 지연-일관성 균형 |

### 보안 (8개)

| # | 이론 | 논문 | Skill 적용 |
|---|------|------|-----------|
| 113 | 스위스 치즈 | Reason (1990) *Human Error* / *Phil. Trans. Royal Soc. B* 327 475-484 | 다층 방어 설계 |
| 114 | CIA 삼각형 | ISO/IEC 27001:2022 | 기밀성·무결성·가용성 |
| 115 | Saltzer-Schroeder 8원칙 | Saltzer & Schroeder (1975) *Proc. IEEE* 63(9) 1278-1308 / Smith (2012) *IEEE S&P* 10(6) 20-25 | 최소 권한, 완전 중재, 실패 안전 등 |
| 116 | OWASP Top 10 | OWASP Foundation (2021) | 코드 리뷰 체크리스트 |
| 117 | STRIDE | Shostack (2014) *Threat Modeling* Wiley | 위협 모델링 자동화 |
| 118 | 제로 트러스트 | Kindervag (2010) Forrester / NIST SP 800-207 (2020) | 모든 요청 검증 |
| 119 | 심층 방어 | NSA (2012) / Reason (1990) 확장 | 다층 계층별 방어 |
| 120 | Security by Design | Cavoukian (2009) *Privacy by Design* / GDPR Art.25 | 설계 단계부터 보안 |

### QA/테스팅 (8개)

| # | 이론 | 논문 | Skill 적용 |
|---|------|------|-----------|
| 121 | 테스트 피라미드 | Cohn (2009) *Succeeding with Agile* / Vocke (2018) | 유닛:통합:E2E=70:20:10 |
| 122 | 동치 분할 | Myers (1979) *Art of Software Testing* | 테스트 케이스 자동 생성 |
| 123 | 경계값 분석 | Myers (1979) | min, max, min±1 자동 생성 |
| 124 | 뮤테이션 테스팅 | DeMillo et al. (1978) *Computer* 11(4) 34-41 | 테스트 품질 검증 |
| 125 | 탐색적 테스팅 | Bach (2003) *Testing Practitioner* | 예상 외 시나리오 생성 |
| 126 | 시프트 레프트 | Larry Smith (2001) *Dr. Dobb's* | 코드+테스트 동시 생성 |
| 127 | 카오스 엔지니어링 | Basiri et al. (2016) *IEEE Software* 33(3) 35-41 | 장애 시나리오 자동 생성 |
| 128 | 오류 관리 | Frese & Keith (2015) *Ann. Rev. Org. Psych.* 2 661-687 | 실패→학습 기회 |

### 서버/인프라/DevOps (6개)

| # | 이론 | 출처 | Skill 적용 |
|---|------|------|-----------|
| 129 | SRE | Beyer et al. (2016) *Site Reliability Engineering* O'Reilly | SLO 기반 알림 |
| 130 | 관측 가능성 3축 | Sridharan (2018) *Distributed Systems Observability* | 로그+메트릭+트레이스 |
| 131 | 불변 인프라 | Morris (2016) *Infrastructure as Code* O'Reilly | 이미지 기반 배포 |
| 132 | GitOps | Weaveworks (2017) / Limoncelli (2018) *Queue* 16(3) | git push → 자동 배포 |
| 133 | 블루/그린 배포 | Humble & Farley (2010) *Continuous Delivery* Ch.10 | 무중단 배포 |
| 134 | 피처 플래그 | Fowler (2010) / Schermann et al. (2018) *IEEE Software* 35(2) | 점진적 롤아웃 |

### 성능 (5개)

| # | 이론 | 논문 | Skill 적용 |
|---|------|------|-----------|
| 135 | 암달의 법칙 | Amdahl (1967) *AFIPS* 30 483-485 | 직렬 구간이 성능 한계 |
| 136 | 리틀의 법칙 | Little (1961) *OR* 9(3) 383-387 | 서버 용량 계획 |
| 137 | 80/20 성능 | Knuth (1974) *ACM Surveys* 6(4) + Pareto 확장 | 핫스팟 집중 최적화 |
| 138 | 도허티 (재) | Doherty (1982) | 400ms 목표 |
| 139 | 웹 성능 예산 | Google Web Vitals (2020) / Grigorik (2013) *High Performance Browser Networking* | LCP<2.5s, FID<100ms, CLS<0.1 |

### 프로젝트 관리 (5개)

| # | 이론 | 출처 | Skill 적용 |
|---|------|------|-----------|
| 140 | 제약 이론 | Goldratt (1984/1990) *The Goal* | 병목 식별→집중 개선 |
| 141 | 칸반 | Ohno (1988) *Toyota Production System* / Anderson (2010) | WIP 제한 |
| 142 | 스크럼 | Schwaber & Sutherland (2020) *Scrum Guide* | 스프린트 리뷰 |
| 143 | 애자일 선언문 | Beck et al. (2001) agilemanifesto.org | 운영 철학 |
| 144 | 기술 부채 | Cunningham (1992) OOPSLA / Kruchten et al. (2012) *IEEE Software* 29(6) | 부채 추적+상환 |

### 데이터 분석 (4개) + 콘텐츠 (2개)

| # | 이론 | 논문 | Skill 적용 |
|---|------|------|-----------|
| 145 | 베이즈 정리 | Bayes (1763) *Phil. Trans.* 53 370-418 | 가중치 업데이트 근거 |
| 146 | A/B 테스트 | Kohavi et al. (2009) *DMKD* 18(1) 140-181 | 변형 테스트 설계 |
| 147 | 통계적 유의성 | Fisher (1925) / Wasserstein & Lazar (2016) *Am. Statistician* 70(2) | 실험 결과 해석 |
| 148 | 심슨의 역설 | Simpson (1951) *JRSS B* 13(2) 238-241 | 세그먼트별 분석 필수 |
| 149 | 역피라미드 | Pöttker (2003) *Journalism Studies* 4(4) 501-511 | 결론 먼저 |
| 150 | 가독성 공식 | Flesch (1948) *J. Applied Psych.* 32(3) 221-233 | 타겟별 가독성 |

---

# PART 3: 연결형 Skill 아키텍처

## 3-1. 확산 활성화 모델 (Collins & Loftus, 1975 직접 구현)

```
[사용자 입력: "쇼핑몰 리뷰 자동 답변 SaaS 만들어줘"]
     │
     ▼ 벡터 DB 의미 검색
[Seed Node: planning.prd-generation] (활성화 = 1.0)
     │
     ▼ 그래프 DB 확산 (decay=0.85, threshold=0.40)
     │
     ├─ 0.765 → planning.problem-definition
     ├─ 0.808 → planning.user-persona
     ├─ 0.723 → planning.feature-prioritization
     ├─ 0.680 → planning.competitive-analysis
     ├─ 0.638 → design.wireframe
     │    └─ 0.434 → design.ui-component
     ├─ 0.595 → dev.backend.api
     │    └─ 0.405 → dev.backend.auth
     └─ 0.425 → marketing.copy
     
     ▼ 블룸 순서 정렬 (C2 Hook)
Layer 0 (Understand): competitive-analysis ∥ problem-definition
Layer 1 (Analyze):    user-persona ∥ feature-prioritization
Layer 2 (Create):     prd-generation
Layer 3 (Create):     wireframe ∥ ui-component
Layer 4 (Create):     backend.api ∥ backend.auth
Layer 5 (Apply):      marketing.copy

━━━ 각 Layer 실행 시 Hook 발동 상세 ━━━
[모든 Layer 공통]
  PRE:  C3(context-cleanup) → 이전 Layer 잔류 컨텍스트 제거
        G1(schema-activator) → 해당 도메인 스키마 로드
        G2(mgv-monitor) → 난이도 평가, 전략 선택
  POST: C5(output-validate) → 출력 종합 검증
        G4(mgv-verify) → 메타인지 검증
        V1(weight-updater) → 엣지 가중치 업데이트

[Layer 0~2: 기획 Skill]
  추가 PRE:  G3(bias-scanner) → 편향 사전 감지
  추가 POST: G5(bias-postcheck) → 확증편향/계획오류 사후 감지

[Layer 3: 디자인 Skill]
  추가 POST: P1(response-time) → 성능 목표 제시
             P2(web-vitals) → 성능 예산 설정

[Layer 4: 개발 Skill]
  추가 DURING: S1(security-layer) → 인증+인가+검증+로깅 다층 확인
               D1(data-integrity) → 트랜잭션 경계 확인
  추가 POST:   S2(owasp-scanner) → OWASP 취약점 스캔
               S3(stride-checker) → 위협 모델링
               S4(least-privilege) → 최소 권한 감사
               Q4(shift-left) → 테스트 동반 생성 강제
               E2(solid) → SOLID 준수 / E3(rest) → REST 준수

[Layer 5: 마케팅 Skill]
  추가 POST: G5(bias-postcheck) → 과장/편향 사후 감지

[전체 완료 후]
  V2(pattern-learner) → 이번 실행의 Skill 조합 패턴 학습
  V3(error-analyzer) → 실패 발생 시 원인 분석
```

## 3-2. 온톨로지 Skill Tree

```
ROOT
├── 📋 기획 (Planning) — 9개
│   ├── planning.problem-definition
│   ├── planning.user-persona
│   ├── planning.user-story
│   ├── planning.competitive-analysis
│   ├── planning.market-sizing
│   ├── planning.prd-generation
│   ├── planning.feature-prioritization
│   ├── planning.sprint-decomposition
│   └── planning.kpi-definition
├── 🎨 디자인 (Design) — 8개
│   ├── design.wireframe
│   ├── design.ui-component
│   ├── design.design-system
│   ├── design.responsive-layout
│   ├── design.color-typography
│   ├── design.interaction-pattern
│   ├── design.accessibility
│   └── design.prototype
├── 💻 개발 (Development) — 13개
│   ├── dev.frontend.component
│   ├── dev.frontend.state
│   ├── dev.frontend.routing
│   ├── dev.frontend.styling
│   ├── dev.frontend.animation
│   ├── dev.backend.api
│   ├── dev.backend.auth
│   ├── dev.backend.database
│   ├── dev.backend.payment
│   ├── dev.backend.integration
│   ├── dev.infra.deployment
│   ├── dev.infra.cicd
│   └── dev.infra.monitoring
├── 📢 마케팅 (Marketing) — 8개
│   ├── marketing.copy
│   ├── marketing.seo
│   ├── marketing.landing-page
│   ├── marketing.ad-creative
│   ├── marketing.email-sequence
│   ├── marketing.social-media
│   ├── marketing.analytics
│   └── marketing.growth-hack
├── 🧪 QA — 8개
│   ├── qa.unit-test
│   ├── qa.integration-test
│   ├── qa.e2e-test
│   ├── qa.code-review
│   ├── qa.performance
│   ├── qa.security
│   ├── qa.ux-audit
│   └── qa.bug-analysis
├── 🔗 공유 (Shared) — 3개
│   ├── dev.shared.types              # 공통 타입 정의
│   ├── dev.shared.utils              # 유틸리티 함수
│   └── dev.shared.constants          # 상수/설정값
└── 🔧 메타 (Meta) — 5개
    ├── meta.context-analyzer
    ├── meta.complexity-scorer
    ├── meta.conflict-detector
    ├── meta.hallucination-guard
    └── meta.output-validator
```

## 3-3. Skill 노드 정의 스키마 (v2+v3 통합)

```yaml
skill_node:
  id: "dev.backend.api"
  domain: "development"
  bloom_level: "Create"
  cognitive_system: 2
  max_variables: 7
  
  # v2 필드: 입력/출력/제약
  input:
    required: [기능명세, 기술스택]
    optional: [기존코드, 디자인시스템]
  output:
    format: "API 코드 + Zod 스키마 + 에러 응답 + cURL"
    validation: "qa.integration-test 연계"
  constraints:
    - "TypeScript strict mode"
    - "Zod 입력 검증 필수"
    - "parameterized query만 사용"
    - "환경변수 하드코딩 금지"
  
  # v3 필드: 이론/메타인지/엣지
  theoretical_base:
    primary: ["#101 REST (Fielding, 2000)", "#72 SOLID (Martin, 2003)"]
    secondary: ["#102 DDD (Evans, 2003)", "#106 멱등성 (RFC 7231)"]
    safety: ["#115 Saltzer 8원칙", "#116 OWASP", "#114 CIA"]
  
  metacognition: # Flavell MGV
    monitor: ["입력 스키마 정의되었는가?", "인증 필요 여부 판단"]
    verify: ["SQL 인젝션 방지 여부", "적절한 HTTP 상태 코드", "에러 핸들링"]
  
  # 구조 매핑 (Gentner, 1983) — 크로스 도메인 전이
  structural_analogs:
    - analog_skill: "qa.bug-analysis"
      shared_structure: "문제정의 → 원인분석 → 해결책 → 검증"
      transfer_type: "분석 프레임워크 공유"
    - analog_skill: "planning.problem-definition"
      shared_structure: "현상 파악 → 원인 추론 → 해결 방안 → 검증"
      transfer_type: "문제 해결 프레임 공유"
  
  # 분산 인지 (Hutchins, 1995) — 공유 컨텍스트
  shared_context:
    reads_from: ["prd_document", "tech_stack_config", "db_schema"]
    writes_to: ["api_endpoints", "api_documentation", "error_codes"]
  
  edges:
    strong: [{target: "dev.backend.auth", weight: 0.90}]
    medium: [{target: "dev.backend.database", weight: 0.75}]
    weak: [{target: "qa.integration-test", weight: 0.65}]
    cross_domain: [{target: "planning.prd-generation", weight: 0.45}]
  
  hooks:
    pre: [C1, C2, C3, G1, G2, E1]
    during: [C4, S1, D1]
    post: [C5, G4, G5, S2, S3, S4, Q4, E2, E3, E4]
    error: [V3]
    always: [V1, V2]
```

## 3-4. 엣지 가중치 의미 (5단계)

| 범위 | 의미 | 동작 |
|------|------|------|
| 0.90~1.00 | **필수 동시 활성화** | 거의 항상 함께 실행. 하나 없으면 다른 하나도 불완전 |
| 0.70~0.89 | **강한 연결** | 대부분 함께 실행. 특별한 이유 없으면 동반 활성화 |
| 0.50~0.69 | **조건부 연결** | 맥락에 따라 활성화. 입력 키워드/도메인이 맞을 때만 |
| 0.30~0.49 | **약한 연결** | 특정 조건에서만 활성화. 확산 임계값(0.40) 경계 |
| 0.00~0.29 | **비활성** | 관계 없음. 확산되지 않음 |

**자가 발전 규칙:**
- 함께 성공 → weight += 0.05 (최대 1.0)
- 함께 실패 → weight -= 0.05 (최소 0.10)
- 30일 미사용 → weight *= 0.95
- 3회+ 동시 활성화 미연결 → 새 엣지 생성 (초기 0.40)

---

# PART 4: Hook 시스템 v3 — 35개 전문 Hook

## 4-1. Hook 분류

| 카테고리 | 코드 | 수량 | 발동 시점 |
|---------|------|------|----------|
| 🔵 Core | C1~C5 | 5 | PRE/DURING/POST |
| 🟢 Cognitive | G1~G5 | 5 | PRE/POST |
| 🔴 Security | S1~S5 | 5 | DURING/POST |
| 🟡 Quality | Q1~Q5 | 5 | POST |
| 🟠 Data | D1~D4 | 4 | DURING/POST |
| ⚡ Performance | P1~P3 | 3 | POST |
| 🟣 Engineering | E1~E4 | 4 | PRE/POST |
| ⚪ Evolution | V1~V4 | 4 | FEEDBACK |

## 4-2. 전체 Hook 상세

### 🔵 CORE (5개)

**C1. activation-spreader** — 확산 활성화 엔진
- 이론: #21 Collins & Loftus (1975)
- 벡터 DB → Seed Node → 그래프 DB 확산 → 도메인별 Hook 동반 활성화

**C2. bloom-sequencer** — 블룸 순서 정렬
- 이론: #31 Anderson & Krathwohl (2001)
- 강제 순서: Remember→Understand→Apply→Analyze→Evaluate→Create
- Create Skill은 반드시 Analyze 이하 1개+ 완료 후 실행

**C3. context-cleanup** — 컨텍스트 정리
- 이론: #1 Sweller (1988), #2 Zhang (2024), #3 Miller (1956)
- 필요 변수만 전달 (7개 이내), 외재적 부하 제거, 주의 잔류 방지
- 도메인 전환 시 컨텍스트 전체 리셋

**C4. cognitive-load-monitor** — 인지부하 실시간 감시
- 이론: #1 Sweller, #3 Miller, #A9 계획오류
- 변수 7개 초과 → 자동 분할 / 프롬프트 3000토큰 초과 → 압축
- 한 Skill에서 판단 3개 이상 → 분할

**C5. output-validate** — 출력 종합 검증
- 이론: #8 Flavell (1979), #34 Piaget, #20 Ericsson
- 완전성 / 근거 포함 / 할루시네이션 / 블룸 일치 / 밀러 준수 체크
- 실패 시: 재시도(2회) → 분해 → 에스컬레이션

### 🟢 COGNITIVE (5개)

**G1. schema-activator** — 스키마 사전 활성화
- 이론: #6 Bartlett (1932), #4 Chase & Simon (1973)
- Skill 도메인에 맞는 스키마(지식 구조) 사전 로드
- 기획→JTBD/포터, 개발→SOLID/REST, 보안→Saltzer/OWASP, 마케팅→AIDA/ELM

**G2. mgv-monitor** — 메타인지 모니터 (Phase 1)
- 이론: #8 Flavell (1979), #9 Oh & Gobet (2025), #5 Kahneman, #32 Vygotsky
- 과제 난이도 평가 → 전략 선택 (시스템1 vs 2)
- 스캐폴딩 강도 결정 (구체적→낮음, 모호→높음, 극모호→문제정의부터)

**G3. bias-scanner** — 편향 사전 감지
- 이론: #A1 확증편향, #A5 프레이밍, #A6 가용성, #A7 생존자
- 입력이 특정 프레이밍에 갇혀 있지 않은가? → "장단점 균형" 제약 추가
- 성공 사례만 참조? → "실패 사례도 분석" 제약 추가

**G4. mgv-verify** — 메타인지 검증 (Phase 3)
- 이론: #9 Oh & Gobet, #15 Roediger, #39 Fiorella, #A2 Kruger & Dunning, #17 Spiro
- 자기설명 포함 여부 / 확신도 과대평가 여부 / 대안 관점 제시 여부
- 검증 결과 → G2에 피드백 (전략 개선)

**G5. bias-postcheck** — 편향 사후 감지
- 이론: #A1~A10 전체
- 확증편향: 기존 관점만 지지? → 반대 관점 추가
- 더닝-크루거: 과도한 확신? → 불확실성 표현 추가
- 계획오류: 낙관적 추정? → 1.5배 버퍼 추가

### 🔴 SECURITY (5개)

**S1. security-layer-check** — 보안 레이어 검증
- 이론: #113 Reason (1990), #119 NSA 심층방어
- 최소 3개 레이어: 인증 + 인가 + 입력검증 + 로깅
- 각 레이어 "구멍" 감지 → 코드 자동 추가 제안

**S2. owasp-scanner** — OWASP 취약점 스캔
- 이론: #116 OWASP Top 10 (2021)
- A01 접근제어: RLS/인증 / A03 인젝션: parameterized query/XSS 이스케이핑
- A05 설정오류: 환경변수 하드코딩/CORS / A07 인증실패: 해싱/토큰만료
- Critical → 출력 차단, 수정 후 재실행

**S3. stride-checker** — STRIDE 위협 모델링
- 이론: #117 Shostack (2014)
- 스푸핑(인증) / 변조(검증) / 부인(로그) / 정보유출(암호화) / DoS(Rate limit) / 권한상승(RBAC)
- High → 보안 Skill 자동 활성화

**S4. least-privilege-audit** — 최소 권한 + Saltzer 8원칙 감사
- 이론: #115 Saltzer & Schroeder (1975)
- 토큰 범위, DB 접근 범위, 환경변수 노출, 사용자 역할
- 8원칙 전체: 기계경제, 실패안전, 완전중재, 개방설계, 권한분리, 최소권한, 최소공유, 심리적수용

**S5. cia-compliance** — CIA 삼각형 준수
- 이론: #114 ISO 27001, #120 Security by Design
- 기밀성(암호화 저장/전송) / 무결성(변조 감지) / 가용성(SPOF 없음)

### 🟡 QUALITY (5개)

**Q1. test-pyramid-balance** — 테스트 균형
- 이론: #121 Cohn (2009)
- 이상: 유닛:통합:E2E = 70:20:10
- 역피라미드/아이스크림콘 감지 → 부족 레벨 자동 생성

**Q2. boundary-value-gen** — 경계값 자동 생성
- 이론: #122 동치분할, #123 경계값분석 (Myers, 1979)
- 각 입력: min, min-1, min+1, max, max-1, max+1, 0, null, empty, 긴 문자열, 특수문자

**Q3. edge-case-scanner** — 엣지 케이스 탐지
- 이론: #125 Bach (2003), #128 Frese & Keith (2015)
- 동시성, 네트워크 끊김, 빈 상태, 대량 데이터, 시간대, 유니코드

**Q4. shift-left-enforcer** — 테스트 동반 강제
- 이론: #126 시프트레프트
- 프론트엔드 컴포넌트 → 유닛 테스트 동반 필수
- 백엔드 API → 통합 테스트 + cURL 동반 필수
- DB 스키마 → 마이그레이션 + 시드 데이터 동반 필수

**Q5. tech-debt-tracker** — 기술 부채 추적
- 이론: #144 Cunningham (1992)
- TODO/FIXME/HACK, 하드코딩, 중복 코드, 타입 any, 빈 catch 블록
- 지식 그래프에 TechDebt 노드 저장 → 임계값 초과 시 상환 스프린트 제안

### 🟠 DATA (4개)

**D1. data-integrity-guard** — 데이터 무결성 감시
- 이론: #100 ACID, #109 이벤트소싱
- 핵심 트랜잭션 ACID 보장 / 트랜잭션 경계+rollback 확인

**D2. normalization-check** — 정규화 검증
- 이론: #107 Codd (1970)
- 3NF 이상 정규화 / 의도적 비정규화는 주석 근거 필수

**D3. cap-advisor** — CAP 트레이드오프 조언
- 이론: #99 Brewer (2000), #112 PACELC Abadi (2012)
- 이 기능에 일관성 vs 가용성 중 어떤 것이 더 중요한지 판단

**D4. acid-enforcer** — ACID + 멱등성 강제
- 이론: #100 ACID, #106 RFC 7231
- 결제 API 필수: 멱등성 + ACID + 재시도 안전

### ⚡ PERFORMANCE (3개)

**P1. response-time-check** — 400ms 임계값
- 이론: #52 Doherty (1982)
- 초과 예상 → 비동기, 캐싱, 레이지 로딩 제안

**P2. web-vitals-budget** — 웹 성능 예산
- 이론: #139 Google Web Vitals
- LCP<2.5s, FID<100ms, CLS<0.1 / 초과 → 이미지 최적화, 코드 스플리팅

**P3. bottleneck-identifier** — 병목 식별
- 이론: #135 Amdahl (1967), #140 Goldratt (1984), #80 Pareto
- 20% 코드=80% 문제 → 핫스팟 식별, 직렬 구간 최적화 우선

### 🟣 ENGINEERING (4개)

**E1. principle-loader** — 도메인별 원칙 자동 로드
- frontend: SOLID.S, 컴포넌트 분리, 성능 예산
- backend: REST 6원칙, DDD, 12-Factor, 멱등성
- database: 정규화 3NF+, CAP/PACELC, ACID
- infra: 불변 인프라, GitOps, SRE 에러 버짓

**E2. solid-compliance** — SOLID 원칙 준수
- 이론: #72 Martin (2003)
- S: 2개 이상 변경 이유 → 분리 / O: 기존 코드 수정 필요 → 확장 포인트

**E3. rest-compliance** — REST 원칙 준수
- 이론: #101 Fielding (2000)
- 리소스 기반 URL, 적절한 HTTP 메서드/상태코드, 무상태성

**E4. twelve-factor-check** — 12-Factor 체크
- 이론: #103 Wiggins (2011)
- 설정 분리, 의존성 선언, 빌드/릴리스/실행 분리, 무상태 프로세스 등 12항목

### ⚪ EVOLUTION (4개)

**V1. weight-updater** — 가중치 업데이트
- 이론: #21 Collins & Loftus, #20 Ericsson, #145 Bayes
- 성공: weight += 0.05 / 실패: -= 0.05 / 미사용 30일: *= 0.95
- 3회+ 동시 활성화 미연결 Skill → 새 엣지 (0.40)

**V2. pattern-learner** — 패턴 학습
- 이론: #19 Lave & Wenger, #35 Kolb, #79 Imai, #24 Gentner
- A→B→C 5회 반복 → composite Skill / 반복 실패 → anti-pattern
- 유사 구조 발견 → 크로스 도메인 엣지 생성

**V3. error-analyzer** — 오류 분석
- 이론: #128 Frese & Keith, #113 Reason
- 원인 분류: 입력부족/이론미적용/복잡도초과/외부데이터오류
- 어떤 Hook이 잡았어야 했는가 분석 → 해당 Hook 강화

**V4. theory-recommender** — 이론 추천
- 이론: #6 Bartlett 스키마 활성화
- 활성화된 Skill에 아직 적용되지 않은 관련 이론 탐색 및 추천

## 4-3. 도메인별 Hook 자동 활성화 규칙

```yaml
development:
  always: [C1, C2, C3, C4, C5, G1, G2, G4]
  auto: [S1, S2, S4, Q4, E1, E2]
  conditional: {backend: [S3, S5, D1, D4, E3, E4], frontend: [P1, P2], database: [D2, D3]}

planning:
  always: [C1, C2, C3, C5, G1, G2, G4]
  auto: [G3, G5]

marketing:
  always: [C1, C2, C3, C5, G1, G2, G4]
  auto: [G3, G5]

qa:
  always: [C1, C2, C3, C5, G1, G2, G4]
  auto: [Q1, Q2, Q3, S2]

post_all:
  always: [V1, V2]
  on_error: [V3]
  periodic: [V4]
```

---

# PART 5: DB 아키텍처 — Graph RAG

## 5-1. 왜 Graph RAG인가

| 요구사항 | 온톨로지 | 지식그래프 | 벡터DB | **Graph RAG** |
|---------|---------|----------|--------|-------------|
| 확산 활성화 | ✗ | ✓✓✓ | ✗ | **✓✓✓** |
| 관계/엣지 저장 | ✓✓ | ✓✓✓ | ✗ | **✓✓✓** |
| 가중치 업데이트 | ✗ | ✓✓✓ | ✗ | **✓✓✓** |
| 정확한 라벨링 | ✓✓✓ | ✓✓ | ✓ | **✓✓✓** |
| Multi-hop 추론 | ✓✓ | ✓✓✓ | ✗ | **✓✓✓** |
| 자연어 매칭 | ✗ | ✗ | ✓✓✓ | **✓✓✓** |
| 추적 가능성 | ✓✓✓ | ✓✓✓ | ✗ | **✓✓✓** |
| 서비스 데이터 축적 | ✗ | ✓✓ | ✓✓✓ | **✓✓✓** |

## 5-2. 2-Layer 구조

```
사용자 입력 → [벡터 DB: 의미 매칭] → Seed Nodes
                                          ↓
         [지식 그래프: 확산 활성화/관계 추론/자가 발전]
                                          ↓
                                   Execution DAG → Skill 실행
                                          ↓
         결과 → [벡터 DB에 임베딩 저장] + [지식 그래프에 패턴 저장]
```

## 5-3. 기술 스택

| 레이어 | 기술 | 역할 |
|--------|------|------|
| 지식 그래프 | Neo4j (커뮤니티, 무료) | 관계/엣지/확산활성화/자가발전/추적 |
| 벡터 DB | Supabase pgvector | 자연어 의미 검색/실행 로그 축적 |
| 임베딩 | Claude/OpenAI Embedding API | 텍스트→벡터 변환 |

## 5-4. Neo4j 스키마 (핵심)

```cypher
// Skill 노드
CREATE (:Skill {id, domain, bloomLevel, cognitiveSystem, maxVariables, 
  activationValue, executionCount, successRate, lastUsed, systemPrompt})

// Theory 노드
CREATE (:Theory {id, name, nameEn, category, authors, year, paper,
  journal, volume, pages, corePrinciple, skillDomains, skillApplication})

// Project 노드
CREATE (:Project {id, name, status, createdAt, targetUser})

// ExecutionLog 노드
CREATE (:ExecutionLog {id, timestamp, inputSummary, activatedSkills,
  success, tokenUsage, userFeedback})

// 엣지 유형
(s1)-[:REQUIRES {weight, type: "prerequisite"}]->(s2)
(s1)-[:FEEDS {weight, type: "downstream"}]->(s2)
(s1)-[:CO_CREATES {weight, type: "bidirectional"}]->(s2)
(s1)-[:STRUCTURALLY_ANALOGOUS {weight, sharedStructure}]->(s2)
(t)-[:GROUNDS {application, priority}]->(s)
(t1)-[:RELATED_TO {type, note}]->(t2)
(t1)-[:SUPPORTED_BY {note}]->(t2)
(proj)-[:USED_SKILL {timestamp}]->(s)
(log)-[:EXECUTED]->(s)
```

## 5-5. 확산 활성화 쿼리

```cypher
MATCH (seed:Skill {id: $seedId})
SET seed.activationValue = 1.0
WITH seed
MATCH (seed)-[r1]->(hop1:Skill)
WHERE r1.weight * 0.85 >= 0.40
SET hop1.activationValue = r1.weight * 0.85
WITH hop1
MATCH (hop1)-[r2]->(hop2:Skill)
WHERE hop2.activationValue = 0.0 AND hop1.activationValue * r2.weight * 0.85 >= 0.40
SET hop2.activationValue = hop1.activationValue * r2.weight * 0.85
// 활성화된 Skill을 블룸 순서로 반환
MATCH (s:Skill) WHERE s.activationValue > 0
RETURN s ORDER BY CASE s.bloomLevel
  WHEN 'Remember' THEN 1 WHEN 'Understand' THEN 2 WHEN 'Apply' THEN 3
  WHEN 'Analyze' THEN 4 WHEN 'Evaluate' THEN 5 WHEN 'Create' THEN 6 END
```

## 5-6. 자가 발전 쿼리

```cypher
// 성공 시 강화
MATCH (s1:Skill)-[r]->(s2:Skill)
WHERE s1.id IN $executed AND s2.id IN $executed AND $success = true
SET r.weight = CASE WHEN r.weight + 0.05 > 1.0 THEN 1.0 ELSE r.weight + 0.05 END

// 실패 시 약화
...SET r.weight = CASE WHEN r.weight - 0.05 < 0.10 THEN 0.10 ELSE r.weight - 0.05 END

// 새 연결 자동 생성 (3회+ 동시 활성화)
MATCH (s1:Skill), (s2:Skill)
WHERE s1.id IN $executed AND s2.id IN $executed AND NOT (s1)-[]-(s2)
WITH s1, s2, COUNT(*) as co WHERE co >= 3
CREATE (s1)-[:DISCOVERED {weight: 0.40, createdAt: datetime()}]->(s2)

// 미사용 감쇠 (30일)
MATCH ()-[r]->() WHERE r.lastReinforced < datetime() - duration('P30D')
SET r.weight = CASE WHEN r.weight * 0.95 < 0.10 THEN 0.10 ELSE r.weight * 0.95 END
```

## 5-7. Supabase pgvector 스키마

```sql
CREATE TABLE skill_embeddings (
  id TEXT PRIMARY KEY, skill_id TEXT, embedding VECTOR(1536),
  description TEXT, domain TEXT, bloom_level TEXT, created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE theory_embeddings (
  id TEXT PRIMARY KEY, theory_id TEXT, embedding VECTOR(1536),
  content TEXT, source_paper TEXT, created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE TABLE execution_embeddings (
  id TEXT PRIMARY KEY, project_id TEXT, embedding VECTOR(1536),
  input_text TEXT, output_summary TEXT, skills_used TEXT[],
  success BOOLEAN, created_at TIMESTAMPTZ DEFAULT NOW()
);
CREATE INDEX ON skill_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 20);
CREATE INDEX ON execution_embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
```

---

# PART 6: 서비스 데이터 축적 파이프라인

```
[프로젝트 실행]
  → 1. 입력: 원문→벡터DB, 메타→지식그래프
  → 2. Skill 실행: EXECUTED 엣지, 출력 임베딩
  → 3. 피드백: 성공→가중치 강화 / 실패→원인 추적
  → 4. 패턴: composite Skill 생성, anti-pattern 등록
```

**라벨링 정확도 3중 검증:**
1. **스키마 제약** (Neo4j): bloomLevel 6값 강제, weight 0~1 범위
2. **이론 기반** (자동): Create가 Remember 없이 호출되면 경고
3. **사용 기반** (자가 발전): 라벨과 실제 사용 패턴 불일치 → 재라벨링 제안

---

# PART 7: 프로세스 플로우 × 이론 × Hook 매핑

```
아이디어 입력
  ▼
🧠 기획 ──── 이론: JTBD, Bloom, ZPD, ELM, Porter, 역방향설계
              Hook: C1~C5, G1~G5 (편향 감지 강화)
  ▼
🎨 디자인 ── 이론: 게슈탈트, 힉스, 피츠, 제이콥, 정보수렵, 피크엔드
              Hook: C1~C5, G1, G4, P1, P2
  ▼
📐 DB 설계 ── 이론: Codd 정규화, CAP, ACID, PACELC, 이벤트소싱
              Hook: D1~D4, E1
  ▼
💻 프론트 ── 이론: SOLID, 컴포넌트분리, 성능예산, 도허티, 인지부하
              Hook: C1~C5, G1, G2, G4, Q4, E2, P1, P2
  ▼
⚙️ 백엔드 ── 이론: REST, DDD, CQRS, 12-Factor, 이벤트주도, 멱등성
              Hook: C1~C5, G1, S1~S5, D1, D4, E1~E4, Q4
  ▼
🔒 보안 ──── 이론: 스위스치즈, CIA, Saltzer 8원칙, OWASP, STRIDE, 제로트러스트
              Hook: S1~S5 (전체 활성화)
  ▼
🧪 QA ────── 이론: 테스트피라미드, 동치분할, 경계값, 시프트레프트, 오류관리
              Hook: Q1~Q5, S2, G4, G5
  ▼
🚀 배포 ──── 이론: SRE, 관측가능성3축, GitOps, 블루그린, 피처플래그, 카오스
              Hook: E4, P1
  ▼
📊 분석 ──── 이론: 베이즈, A/B테스트, 통계적유의성, 심슨의역설
              Hook: G5 (편향 사후 감지)
  ▼
📈 마케팅 ── 이론: AIDA, ELM, Cialdini 6원칙, 넛지, 포그, Hook모델
              Hook: C1~C5, G1~G5
  ▼
🔄 피드백 ── 이론: PDCA, 카이젠, 린스타트업, Kolb, 자기조절학습
              Hook: V1~V4 (자가 발전)
  └──→ 아이디어 입력으로 순환
```

---

# PART 8: 누락분 보완 — Skill 시스템 프롬프트 + 매핑 테이블 + 파이프라인 상세

## 8-1. 7개 핵심 Skill 시스템 프롬프트

### `planning.prd-generation`
```
[System Prompt]
당신은 시니어 프로덕트 매니저입니다.

## 학문적 기반
- Jobs-to-be-Done (Christensen, 2003): 고객의 "할 일" 중심 문제 정의
- Bloom's Create Level (Anderson & Krathwohl, 2001): 정보 종합→새 문서 구성
- CLT (Sweller, 1988): PRD 섹션 7개 이내
- 구성주의 (Piaget): 판단 근거 함께 제시

## 출력 구조 (고정)
1. 문제 정의 — 누구의 어떤 고통인가? (JTBD 프레임)
2. 솔루션 요약 — 핵심 가치 제안 1문장
3. 타겟 유저 — 페르소나 2개 (인구통계+행동패턴+핵심니즈)
4. 핵심 기능 — MVP 기준 최대 5개 (ICE 점수 포함)
5. 유저 플로우 — 핵심 시나리오 1개 단계별
6. 성공 지표 — KPI 3개 (측정 방법 포함)
7. 1차 스프린트 — 2주 기준 태스크 분해

## 자기 검증
- 각 기능이 문제 정의와 직접 연결되는가?
- "이 기능 없으면 MVP 작동 불가?"  테스트
- 검증 불가능한 주장에 "검증 필요" 태그
```

### `planning.competitive-analysis`
```
[System Prompt]
당신은 시장 조사 전문 분석가입니다.

## 학문적 기반
- Bloom's Analyze Level: 경쟁 구도 구조 분해
- Porter 5 Forces (1979): 산업 경쟁력 체계적 평가
- CLT: 경쟁사 최대 5개로 제한

## 출력 구조
1. 직접 경쟁사 3~5개: 기능/가격/타겟/약점 비교표
2. 간접 경쟁사 2~3개: 대체재 분석
3. 차별화 기회: 1-star 리뷰에서 도출한 불만 패턴
4. 포지셔닝 맵: 가격 vs 기능 2x2 매트릭스
5. 진입 전략: 기존 시장 대비 우위 포인트

## 자기 검증
- 추론과 사실 명확히 구분
- 검증 불가 주장에 "검증 필요" 태그
```

### `design.ui-component`
```
[System Prompt]
당신은 시니어 UI 엔지니어입니다.

## 학문적 기반
- 게슈탈트 원리 (Wertheimer, 1923): 근접성, 유사성 기반 그룹핑
- 힉스 법칙 (Hick, 1952): 선택지 최소화
- 피츠 법칙 (Fitts, 1954): 중요 요소 크고 접근 쉽게
- 제이콥 법칙 (Nielsen): 익숙한 패턴 우선

## 기술 제약
- React + TypeScript + Tailwind CSS + shadcn/ui
- 모바일 퍼스트, 반응형 필수, 다크모드 기본
- WCAG 2.1 AA 접근성 준수

## 출력: 컴포넌트 TSX + Props 인터페이스 + 사용 예시
## 자기 검증: 모바일 320px 깨짐? CTA 44px? 색상 대비 4.5:1?
```

### `dev.frontend.component`
```
[System Prompt]
당신은 시니어 프론트엔드 엔지니어입니다.

## 학문적 기반
- SOLID.S (Martin, 2003): 컴포넌트 하나의 책임
- DRY: 반복 로직 커스텀 훅 분리
- CLT (Sweller): 한 컴포넌트 로직 7±2 규칙 내

## 기술 스택: Next.js 14+ / TypeScript strict / Tailwind / Supabase
## 코딩 규칙
- 함수형 컴포넌트, 커스텀 훅 분리, 에러 바운더리 필수
- try-catch 비동기 래핑, 친절한 에러 메시지
- 환경변수 하드코딩 절대 금지

## 출력: 컴포넌트(.tsx) + 커스텀 훅(.ts) + 타입(.ts)
## 자기 검증: TS 타입 에러? 불필요 리렌더링? 로딩/에러/빈 상태 처리?
```

### `dev.backend.api`
```
[System Prompt]
당신은 시니어 백엔드 엔지니어입니다.

## 학문적 기반
- REST (Fielding, 2000): 무상태, 리소스 기반, 균일 인터페이스
- SOLID.I (Martin): 필요 인터페이스만 노출
- 방어적 프로그래밍: 모든 입력 불신
- 12-Factor (Wiggins, 2011): 설정 분리, 무상태

## 기술 스택: Next.js API Routes 또는 Supabase Edge Functions / Zod 입력 검증
## 보안 절대 규칙
- SQL 인젝션 방지: parameterized query만
- 인증 토큰 검증 필수 / Rate limiting / CORS 명시
- 민감 정보 로깅 금지

## 출력: API 코드 + Zod 스키마 + 에러 응답 형식 + cURL 명령어
## 자기 검증: 모든 입력 검증? 적절한 HTTP 상태 코드? 인증 없는 엔드포인트 의도적?
```

### `marketing.copy`
```
[System Prompt]
당신은 전환율 최적화 전문 카피라이터입니다.

## 학문적 기반
- AIDA (Strong, 1925): Attention→Interest→Desire→Action
- ELM (Petty & Cacioppo, 1986): 고관여→중심 경로, 저관여→주변 경로
- 넛지 (Thaler & Sunstein, 2008): 선택 설계 행동 유도
- 앵커링 (Tversky & Kahneman, 1974): 가격/가치 제시 순서
- 프로스펙트 (Kahneman & Tversky, 1979): 손실 회피 프레이밍

## 출력 규칙
- 헤드라인: 7단어 이내, 핵심 가치 or 고통 포인트
- 서브헤드: 구체적 이점 1가지
- 본문: 문제→공감→솔루션→증거→CTA
- CTA: 행동 동사 + 구체적 결과

## 자기 검증: 3초 내 핵심 파악? CTA 명확? 과장/검증불가 주장?
```

### `qa.code-review`
```
[System Prompt]
당신은 시니어 코드 리뷰어입니다.

## 학문적 기반
- Bloom's Evaluate Level: 기준에 따라 코드 판단
- CLT: 피드백 카테고리별 구조화
- 구성주의: "왜" 문제인지 설명하여 학습 효과

## 리뷰 기준 (우선순위)
1. 보안 취약점 (Critical) — OWASP Top 10 기준
2. 버그/논리 오류 (High)
3. 성능 이슈 (Medium)
4. 코드 스타일/가독성 (Low)
5. 개선 제안 (Info)

## 출력: 심각도별 이슈 리스트 (위치+문제+이유+수정제안) + 품질 점수(1~10) + 잘된 점
## 자기 검증: 수정 제안 컴파일 가능? 기술 스택 일치? 우선순위 적절?
```

---

## 8-2. Claude Project 즉시 사용 시스템 프롬프트

```
# AI 풀스택 파이프라인 운영 시스템

## 당신의 역할
기획·디자인·개발·마케팅·QA를 아우르는 풀스택 AI 시스템입니다.
모든 응답은 아래 학문적 원칙을 기반으로 합니다.

## 핵심 원칙 (모든 응답에 적용)

### 인지부하 관리 (Sweller, 1988)
- 한 번에 하나의 명확한 과제만 처리
- 변수/조건 7개 초과 시 자동 분할 (Miller, 1956)
- 이전 대화의 불필요한 맥락은 현재 판단에 영향 주지 않음

### 블룸 택소노미 준수 (Anderson & Krathwohl, 2001)
- Remember→Understand→Apply→Analyze→Evaluate→Create 순서 준수
- "만들어줘" 요청이라도 먼저 문제 정의→분석→생성
- 단계 건너뛰기 금지

### 메타인지 MGV 루프 (Flavell, 1979 / Oh & Gobet, 2025)
- Monitor: 과제 난이도 평가, 전략 선택
- Generate: 선택된 전략으로 실행
- Verify: 출력 자기 검증 (할루시네이션, 근거, 대안)

### 할루시네이션 방지
- 불확실한 정보 → "검증 필요" 표시
- 입력에 없는 수치/이름 임의 생성 금지
- 추론과 사실 명확 구분

### 편향 감지 (Kahneman & Tversky)
- 확증편향: 기존 관점만 지지하지 않는가?
- 계획오류: 시간/비용 추정 낙관적이지 않은가? → 1.5배 버퍼
- 생존자편향: 실패 사례도 분석했는가?

## 도메인별 행동 규칙

### 기획: JTBD 프레임, 기능 5개 이내 MVP, ICE/RICE 점수
### 디자인: 모바일 퍼스트, Tailwind+shadcn/ui, 게슈탈트 원리, CTA 44px+
### 개발: Next.js 14+/TS/Tailwind/Supabase, SOLID, REST, 12-Factor
### 보안: Saltzer 8원칙, OWASP Top 10, 스위스 치즈 다층 방어, 최소 권한
### QA: 테스트 피라미드(유닛70:통합20:E2E10), 경계값, 시프트 레프트
### 마케팅: AIDA, ELM(관여도별 분기), Cialdini 6원칙
### DB: Codd 정규화 3NF+, CAP/PACELC 판단, ACID 필수(결제)
### 성능: 도허티 400ms, Web Vitals(LCP<2.5s, FID<100ms, CLS<0.1)

## 복잡한 요청 처리 프로세스
1. 입력 분석 → 도메인/복잡도 판별
2. 블룸 순서로 단계 구성
3. 각 단계 출력 → 다음 단계 입력
4. 단계 간 정보 충돌 시 보고
5. 최종 출력에 자기 검증 결과 포함
```

---

## 8-3. 활동 이론 Engeström 6요소 매핑 테이블

```
         [도구/매개물 = Claude Skills]
                /    \
  [주체=사용자] ───── [객체=프로덕트] → [결과=배포+수익]
        |       \    /       |
  [규칙=기술제약]  [공동체=타겟유저]  [분업=Skill간 역할분담]
```

| Engeström 요소 | Claude Skill 시스템 대응 |
|---------------|----------------------|
| 주체 (Subject) | 사용자 (의사결정자) |
| 도구 (Tools) | Claude Skills (AI 도구들) |
| 객체 (Object) | 만들려는 프로덕트/서비스 |
| 규칙 (Rules) | 기술 스택 제약, 디자인 원칙, 코딩 컨벤션, 150개 이론 |
| 공동체 (Community) | 타겟 유저, 시장, 경쟁사 |
| 분업 (Division of Labor) | Skill 간 역할 분담 (기획/디자인/개발/QA) |
| 결과 (Outcome) | 배포된 서비스 + 수익 + 학습 데이터 |
| **모순 (Contradiction)** | **Skill 출력 간 충돌 → 발전의 동력 (contradiction-resolver Hook)** |

---

## 8-4. 확산 활성화 — 단일 vs 연결형 비교

| 항목 | 기존 (단일 Skill 호출) | 연결형 (확산 활성화) |
|------|---------------------|-------------------|
| 트리거 | 사용자가 Skill 지정 | 하나 트리거→관련 Skill 자동 활성화 |
| 실행 방식 | 순차적만 가능 | 병렬+순차 혼합 (DAG) |
| 맥락 공유 | Skill 간 맥락 단절 | 공유 컨텍스트 사용 |
| 학습 | 매번 동일 | 자주 쓰는 조합 링크 강화 |
| 보안/QA | 별도 요청 필요 | 코드 Skill 활성화 시 보안/QA Hook 자동 동반 |
| 이론 근거 | 없음 | Collins & Loftus (1975) 직접 구현 |

---

## 8-5. 기존 7개 → 35개 Hook 매핑 테이블

| 기존 Hook (v1) | 신규 Hook (v3) | 변경 사항 |
|---------------|---------------|----------|
| activation-spreader | C1 | 도메인별 Hook 동반 활성화 기능 추가 |
| skill-router | C1 + C2 | 확산 활성화와 블룸 순서를 분리 |
| context-cleanup | C3 + C4 | 사전 정리 + 실시간 부하 감시 분리 |
| output-validate | C5 + G4 + G5 | 기본/메타인지/편향 검증 3분할 |
| error-recovery | V3 + C5(retry) | 오류 분석과 복구 분리 |
| conflict-detector | C5(conflict) + D3 | 범용 + 데이터 특화 분리 |
| fetch-guard | G1(일부) | 스키마 활성화로 흡수 |
| *(없음)* | **S1~S5 (5개)** | **보안 Hook 완전 신규** |
| *(없음)* | **Q1~Q5 (5개)** | **QA Hook 완전 신규** |
| *(없음)* | **D1~D4 (4개)** | **데이터 Hook 완전 신규** |
| *(없음)* | **P1~P3 (3개)** | **성능 Hook 완전 신규** |
| *(없음)* | **E1~E4 (4개)** | **공학 Hook 완전 신규** |
| *(없음)* | **G1~G5 (5개)** | **인지 Hook 대폭 확장** |
| *(없음)* | **V1~V4 (4개)** | **진화 Hook 체계화** |

---

## 8-6. Hook 전체 실행 흐름 상세 다이어그램

```
[사용자 입력]
     │
     ▼
━━━ PRE-EXECUTION ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
│ 🔵 C1 activation-spreader  → Seed Node 탐색 + 확산 + 도메인 Hook 동반
│ 🔵 C2 bloom-sequencer      → 활성화된 Skill 블룸 순서 정렬
│ 🔵 C3 context-cleanup      → 외재적 부하 제거, 7개 이내 전달
│ 🟢 G1 schema-activator     → 도메인 스키마 사전 로드
│ 🟢 G2 mgv-monitor          → 난이도 평가, 전략(S1/S2) 선택, 스캐폴딩 결정
│ 🟢 G3 bias-scanner         → 입력 프레이밍/가용성/생존자 편향 사전 감지
│ 🟣 E1 principle-loader     → 도메인별 공학 원칙 자동 로드
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     │
     ▼
━━━ DURING-EXECUTION ━━━━━━━━━━━━━━━━━━━━━━━━━
│ 🔵 C4 cognitive-load-monitor → 변수7개/프롬프트3000토큰/판단3개 초과 감시
│ 🔴 S1 security-layer-check   → 인증+인가+검증+로깅 3층+ 확인
│ 🟠 D1 data-integrity-guard   → ACID 트랜잭션 경계 확인
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     │
     ▼
━━━ POST-EXECUTION ━━━━━━━━━━━━━━━━━━━━━━━━━━━
│ 🔵 C5 output-validate        → 완전성/근거/할루시네이션/블룸/밀러 종합 검증
│ 🟢 G4 mgv-verify             → 자기설명/확신도/대안 검증, G2에 피드백
│ 🟢 G5 bias-postcheck         → 확증/더닝크루거/매몰비용/계획오류 사후 감지
│ 🔴 S2 owasp-scanner          → OWASP Top 10 취약점 스캔
│ 🔴 S3 stride-checker         → STRIDE 6카테고리 위협 모델링
│ 🔴 S4 least-privilege-audit  → Saltzer 8원칙 + 최소 권한 감사
│ 🔴 S5 cia-compliance         → 기밀성/무결성/가용성 준수
│ 🟡 Q1 test-pyramid-balance   → 유닛:통합:E2E 비율 검증
│ 🟡 Q2 boundary-value-gen     → 경계값 자동 생성 (min,max,0,null,특수문자)
│ 🟡 Q3 edge-case-scanner      → 동시성/네트워크/빈상태/대량/시간대/유니코드
│ 🟡 Q4 shift-left-enforcer    → 코드+테스트 동반 생성 강제
│ 🟡 Q5 tech-debt-tracker      → TODO/하드코딩/중복/any/빈catch 추적
│ 🟠 D2 normalization-check    → 3NF+ 정규화 검증
│ 🟠 D3 cap-advisor            → 일관성 vs 가용성 트레이드오프 조언
│ 🟠 D4 acid-enforcer          → 결제 API 멱등성+ACID 강제
│ ⚡ P1 response-time-check    → 400ms 임계값
│ ⚡ P2 web-vitals-budget      → LCP/FID/CLS 예산
│ ⚡ P3 bottleneck-identifier  → 암달+파레토 병목 식별
│ 🟣 E2 solid-compliance       → S.O.L.I.D 5원칙 준수
│ 🟣 E3 rest-compliance        → REST 6원칙 준수
│ 🟣 E4 twelve-factor-check    → 12항목 체크
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
     │
     ▼
━━━ ERROR/FEEDBACK ━━━━━━━━━━━━━━━━━━━━━━━━━━━
│ ⚪ V1 weight-updater         → 성공+0.05/실패-0.05/미사용×0.95/신규엣지0.40
│ ⚪ V2 pattern-learner        → composite Skill/anti-pattern/크로스도메인 엣지
│ ⚪ V3 error-analyzer         → 원인분류+레이어분석+방지규칙 추가
│ ⚪ V4 theory-recommender     → 미적용 관련 이론 탐색 및 추천
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 8-7. 서비스 데이터 축적 4단계 상세 파이프라인

```
[사용자가 프로젝트 실행]
      │
      ▼
┌──────────────────────────────────┐
│  1단계: 입력 기록                  │
│  - 원문 텍스트 → 벡터 DB 임베딩     │ (execution_embeddings)
│  - 메타데이터 → 지식 그래프          │ (ExecutionLog 노드)
│  - 프로젝트 연결 → Project 노드      │ (PART_OF 엣지)
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  2단계: Skill 실행 & 결과 기록      │
│  - 어떤 Skill 활성화 → EXECUTED 엣지 │ (지식 그래프)
│  - 각 Skill 입출력 데이터 → 벡터 임베딩│ (벡터 DB)
│  - 실행 시간, 토큰 사용량 → 노드 속성  │ (지식 그래프)
│  - Hook 발동 이력 → Hook 실행 로그     │ (지식 그래프)
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  3단계: 피드백 반영                 │
│  - 사용자 피드백 (성공/수정/실패)     │
│  - 성공 → V1: 엣지 가중치 +0.05     │ (지식 그래프)
│  - 실패 → V3: 원인 Skill 역추적      │ (그래프 경로 추적)
│  - 수정 내용 → 벡터 저장             │ (유사 실패 방지용)
│  - Hook 실패 → V3: 어떤 Hook이       │
│    잡았어야 했는가 분석 → Hook 강화    │
└──────────┬───────────────────────┘
           │
           ▼
┌──────────────────────────────────┐
│  4단계: 패턴 학습                   │
│  - 자주 함께 쓰이는 Skill 조합 감지   │ → V2: 새 엣지 생성
│  - 반복 체인(A→B→C ×5) 감지         │ → V2: composite Skill
│  - 유사 입력→동일 결과 캐싱           │ → 벡터 유사도 매칭
│  - 반복 실패 패턴                    │ → V2: anti-pattern 등록
│  - 크로스 도메인 구조 유사성 발견      │ → V2: 구조 매핑 엣지
│  - 미사용 30일 엣지 감쇠             │ → V1: weight ×0.95
└──────────────────────────────────┘
```

---

## 8-8. 커버리지 개선 전/후 비교 테이블

| 프로세스 영역 | 기존 98개 | 추가 | 최종 150개 | 개선 |
|-------------|----------|------|----------|------|
| 기획/전략 | ★★★★★ (15) | +0 | ★★★★★ (15) | 유지 |
| 디자인/UX | ★★★★★ (18) | +0 | ★★★★★ (18) | 유지 |
| 마케팅/전환 | ★★★★★ (16) | +0 | ★★★★★ (16) | 유지 |
| 인지/학습 | ★★★★★ (20) | +0 | ★★★★★ (20) | 유지 |
| 프론트엔드 | ★★☆☆☆ (5) | +2 | ★★★★☆ (7) | ↑↑ |
| **백엔드/API** | ★☆☆☆☆ (3) | **+8** | ★★★★☆ (11) | **↑↑↑** |
| **데이터베이스** | ☆☆☆☆☆ (0) | **+6** | ★★★☆☆ (6) | **↑↑↑↑** |
| **서버/DevOps** | ☆☆☆☆☆ (0) | **+6** | ★★★☆☆ (6) | **↑↑↑↑** |
| **보안** | ☆☆☆☆☆ (0) | **+8** | ★★★★☆ (8) | **↑↑↑↑** |
| **QA/테스팅** | ★☆☆☆☆ (2) | **+8** | ★★★★☆ (10) | **↑↑↑** |
| **성능** | ☆☆☆☆☆ (0) | **+5** | ★★★☆☆ (5) | **↑↑↑↑** |
| 프로젝트 관리 | ★☆☆☆☆ (2) | +5 | ★★★★☆ (7) | ↑↑↑ |
| 데이터 분석 | ☆☆☆☆☆ (0) | +4 | ★★★☆☆ (4) | ↑↑↑↑ |
| 시스템/연결 | ★★★★★ (10) | +0 | ★★★★★ (10) | 유지 |
| 편향/의사결정 | ★★★★★ (10) | +0 | ★★★★★ (10) | 유지 |
| 비즈니스 | ★★★★☆ (7) | +0 | ★★★★☆ (7) | 유지 |

---

## 8-9. 이론 간 지식 그래프 연결 구조

```cypher
// 이론 간 관계 — 확산 활성화 시 관련 이론도 함께 활성화

// 인지부하 ↔ 밀러 (지지 관계)
(:Theory {id:"cognitive-load"}) -[:SUPPORTED_BY {note:"작업기억 한계를 7±2로 정량화"}]->
(:Theory {id:"millers-law"})

// 이중과정 ↔ ELM (병렬 프레임워크)
(:Theory {id:"dual-process"}) -[:RELATED_TO {type:"parallel", note:"시스템1/2 = 주변/중심 경로"}]->
(:Theory {id:"elm"})

// 스위스치즈 ↔ 심층방어 (확장)
(:Theory {id:"swiss-cheese"}) -[:RELATED_TO {type:"extension", note:"다층 방어 원칙 공유"}]->
(:Theory {id:"defense-in-depth"})

// CAP ↔ PACELC (확장)
(:Theory {id:"cap-theorem"}) -[:RELATED_TO {type:"extension", note:"파티션 없을 때 L vs C 추가"}]->
(:Theory {id:"pacelc"})

// 메타인지 ↔ MGV ↔ 자기조절학습 (구현 체인)
(:Theory {id:"metacognition"}) -[:IMPLEMENTED_BY]-> (:Theory {id:"mgv-framework"})
(:Theory {id:"metacognition"}) -[:RELATED_TO {type:"parallel"}]-> (:Theory {id:"self-regulated-learning"})

// 확산활성화 ↔ 스키마이론 (보완)
(:Theory {id:"spreading-activation"}) -[:RELATED_TO {type:"complementary"}]->
(:Theory {id:"schema-theory"})

// SOLID ↔ 관심사분리 ↔ Unix철학 (같은 원칙의 다른 표현)
(:Theory {id:"solid"}) -[:RELATED_TO {type:"same-principle"}]-> (:Theory {id:"separation-of-concerns"})
(:Theory {id:"separation-of-concerns"}) -[:RELATED_TO {type:"same-principle"}]-> (:Theory {id:"unix-philosophy"})

// Saltzer8원칙 ↔ OWASP ↔ STRIDE (보안 체계 연결)
(:Theory {id:"saltzer-schroeder"}) -[:GROUNDS]-> (:Theory {id:"owasp-top10"})
(:Theory {id:"saltzer-schroeder"}) -[:GROUNDS]-> (:Theory {id:"stride"})

// 테스트피라미드 ↔ 시프트레프트 ↔ 카오스엔지니어링 (QA 체계)
(:Theory {id:"test-pyramid"}) -[:RELATED_TO {type:"complementary"}]-> (:Theory {id:"shift-left"})
(:Theory {id:"shift-left"}) -[:RELATED_TO {type:"extension"}]-> (:Theory {id:"chaos-engineering"})

// 의도적연습 ↔ 카이젠 ↔ 경험학습 (자가 발전 근거 체인)
(:Theory {id:"deliberate-practice"}) -[:RELATED_TO {type:"parallel"}]-> (:Theory {id:"kaizen"})
(:Theory {id:"kaizen"}) -[:RELATED_TO {type:"parallel"}]-> (:Theory {id:"experiential-learning"})
```

**활성화 규칙:** 보안 Skill 활성화 → #113 스위스치즈 → RELATED_TO → #119 심층방어 → GROUNDS → #116 OWASP → GROUNDS → #117 STRIDE → 보안 이론 체인 전체가 함께 활성화

---

## 8-10. 이론 적용 우선 순서 (Phase별)

## 8-11. 2차 누락 보완

### (1) 구성주의 출력 4요소 (모든 Skill 출력에 포함 필수)
```
모든 Skill 출력에 반드시 포함:
1. 결과물 자체
2. "왜 이 결정을 했는가" (근거 — 어떤 이론/데이터에 기반)
3. "다른 선택지는 무엇이었는가" (대안 — 최소 1개)
4. "어디서 불확실한가" (한계 — "검증 필요" 태그)

→ 사용자가 AI 출력을 블라인드 수용이 아닌 공동 구성(co-construction)으로 처리
→ 이론: 구성주의 (Piaget, 1976 / Bruner, 1966)
```

### (2) SOLID 5원칙 ↔ Claude Skill 대응 상세 테이블
| SOLID | 원칙 | Claude Skill 대응 |
|-------|------|------------------|
| S (Single Responsibility) | 클래스/모듈은 하나의 변경 이유만 가짐 | 1 Skill = 1 책임. 2개 이상 도메인에 걸치면 분할 |
| O (Open/Closed) | 확장에 열려있고 수정에 닫혀있음 | Skill은 새 이론/규칙 추가는 가능하되, 기존 로직 수정 불필요 |
| L (Liskov Substitution) | 하위 타입은 상위 타입을 대체 가능 | 같은 카테고리 Skill은 교체 가능 (예: qa.unit-test ↔ qa.integration-test) |
| I (Interface Segregation) | 클라이언트가 불필요한 인터페이스에 의존하지 않음 | 각 Skill은 필요한 입력/출력만 노출. 전체 컨텍스트 전달 금지 |
| D (Dependency Inversion) | 고수준이 저수준에 의존하지 않고 추상화에 의존 | 구체 Skill이 아닌 추상 카테고리(planning, design 등)에 의존 |

### (3) 4가지 DB 방식별 강점/약점 상세

**온톨로지 (OWL/RDF)**
- 강점: ① 엄격한 스키마→라벨링 정확도 최고 ② 추론 엔진(Reasoner)으로 암묵적 관계 자동 도출 ③ SPARQL 복잡 질의 ④ 형식적 지식 표현 최적 ⑤ 클래스 계층+속성+제약 조건
- 약점: ① 엣지 가중치 없음→확산 활성화 불가 ② 실시간 업데이트 느림 ③ 비정형 자연어 검색 불가 ④ 스키마 변경 비용 높음 ⑤ 콜드 스타트 구축 비용 매우 높음

**지식 그래프 (Neo4j/ArangoDB)**
- 강점: ① 엣지에 가중치 저장→확산 활성화 직접 구현 ② 관계 유형/방향 자연스러움 ③ 실시간 가중치 업데이트 ④ Multi-hop 순회 네이티브 ⑤ 추적 가능성 투명 ⑥ Cypher 패턴 매칭 강력 ⑦ 노드 속성으로 라벨링
- 약점: ① 비정형 자연어 의미 검색 약함 ② 의미적 유사도 계산 약함 ③ 대규모 전체 그래프 순회 시 성능 ④ 초기 스키마 설계 노력

**벡터 DB (Pinecone/Weaviate/Qdrant)**
- 강점: ① 자연어 의미 검색 최강 ② 비정형 데이터 대규모 저장/검색 ③ 구축 속도 빠름 ④ 스케일링 용이
- 약점: ① 관계/엣지 없음→확산 활성화 불가 ② 가중치 없음→자가 발전 불가 ③ Multi-hop 불가 ④ 추적 불가 ⑤ 의미적 유사하지만 논리적 무관한 결과 가능 ⑥ 관계 라벨링 불가

**Graph RAG (지식 그래프 + 벡터 DB)**
- 강점: ① 확산 활성화 (그래프) ② 의미 검색 (벡터) ③ 관계+가중치 (그래프) ④ Multi-hop (그래프) ⑤ 추적 가능 (그래프) ⑥ 라벨링 (그래프+온톨로지적 제약) ⑦ 크로스 도메인 (벡터 유사도) ⑧ 서비스 데이터 축적 (양쪽 분담)
- 약점: ① 구현 복잡도 (2시스템 운영) ② 초기 구축 비용 ③ 동기화 관리

### (4) 대안 기술 스택

```
[지식 그래프]
  Primary: Neo4j 커뮤니티 에디션 (무료)
    - Cypher 쿼리 직관적, APOC 확산 알고리즘 내장, GDS 중심성/커뮤니티
  대안: ArangoDB (멀티모델 — 그래프+문서+키벨류)
    - 하나의 DB로 그래프+문서 모두 → 운영 복잡도 감소
    - 단, 순수 그래프 성능은 Neo4j 우세

[벡터 DB]
  Primary: Supabase pgvector (기존 스택에 확장만 추가)
    - 별도 벡터 DB 불필요, 인프라 단순화
  대안 (스케일 시): Qdrant (오픈소스, 셀프호스팅)
    - 필터링+벡터 검색 동시, 대규모 데이터에서 pgvector보다 성능 우세

[임베딩]
  Primary: Claude/OpenAI Embedding API
  대안 (비용 절약): sentence-transformers 로컬 실행
```

### (5) S2 OWASP 누락 체크항목 보완

```yaml
# 기존에 누락된 A02, A04 추가:
A02_cryptographic_failures:
  check: "민감 데이터(비밀번호, 토큰, 개인정보) 평문 저장 여부"
  check: "HTTPS 미강제 여부"
  check: "약한 암호화 알고리즘 사용 여부 (MD5, SHA1)"
  check: "하드코딩된 시크릿/키 존재 여부"

A04_insecure_design:
  check: "위협 모델링 수행 여부 → S3(STRIDE) 연동"
  check: "비즈니스 로직에 악용 가능한 흐름 존재 여부"
  check: "Rate limiting 미설정된 민감 엔드포인트 여부"
  check: "인증 없이 접근 가능한 관리 기능 여부"
```

### (6) E4 twelve-factor-check 12개 항목 전체

```yaml
E4_twelve_factors:
  I_codebase: "하나의 코드베이스 — 여러 배포"
  II_dependencies: "의존성 명시적 선언 (package.json/requirements.txt)"
  III_config: "설정을 환경변수로 분리 (코드에 하드코딩 금지)"
  IV_backing_services: "외부 서비스(DB, 캐시, 큐)를 첨부 리소스로 취급"
  V_build_release_run: "빌드/릴리스/실행 단계 엄격 분리"
  VI_processes: "무상태 프로세스로 실행"
  VII_port_binding: "포트 바인딩으로 서비스 내보내기"
  VIII_concurrency: "프로세스 모델로 스케일 아웃"
  IX_disposability: "빠른 시작과 우아한 종료 (graceful shutdown)"
  X_dev_prod_parity: "개발/스테이징/프로덕션 환경 최대한 동일"
  XI_logs: "로그를 이벤트 스트림으로 취급 (파일에 쓰지 않음)"
  XII_admin_processes: "관리 작업을 일회성 프로세스로 실행"
```

### (7) 확산 활성화 쿼리 — 3홉째 복원

```cypher
// 기존 2홉에서 3홉으로 복원:
// ... (1홉, 2홉 동일) ...

// 3홉 확산
WITH hop2
MATCH (hop2)-[r3]->(hop3:Skill)
WHERE hop3.activationValue = 0.0
  AND hop2.activationValue * r3.weight * 0.85 >= 0.40
SET hop3.activationValue = hop2.activationValue * r3.weight * 0.85

// 최종: 활성화된 모든 Skill 블룸 순서 반환
MATCH (s:Skill) WHERE s.activationValue > 0
RETURN s.id, s.bloomLevel, s.activationValue, s.cognitiveSystem
ORDER BY CASE s.bloomLevel
  WHEN 'Remember' THEN 1 WHEN 'Understand' THEN 2
  WHEN 'Apply' THEN 3 WHEN 'Analyze' THEN 4
  WHEN 'Evaluate' THEN 5 WHEN 'Create' THEN 6
END, s.activationValue DESC
```

### (8) 주의 제어 이론 — LLM 대응 설명

```
▸ 주의 제어 이론 (Posner, 1980 / Desimone & Duncan, 1995)

핵심: 주의력은 유한한 자원이며, 선택적으로 배분된다.

LLM 대응: Transformer의 Attention 메커니즘도 컨텍스트가 길어지면
"주의력 잔류(Attentional Residue)"가 발생하여 이전 맥락이
현재 판단을 오염시킨다. (Zhang et al., 2024 — LLM 인지부하 논문에서 실증)

Claude Skill 적용:
- 각 Skill은 독립적 컨텍스트로 실행 (이전 Skill의 잔류 attention 차단)
- Hook C3(context-cleanup)이 Skill 전환 시 컨텍스트 클린업
- 필요한 정보만 명시적으로 전달 (암묵적 맥락 의존 금지)
- 도메인 전환 시 컨텍스트 전체 리셋
```

### (9) 청킹 구체 예시

```
▸ 청킹 적용 예시 — Skill을 의미 있는 단위로 묶기

"프론트엔드 개발" 청크:
  = [dev.frontend.component + dev.frontend.state 
     + dev.frontend.styling + dev.frontend.routing]
  → 개별 로드보다 청크 단위 로드가 빠르고 정확

"인증 시스템" 청크:
  = [dev.backend.auth + dev.backend.api(인증 엔드포인트) 
     + qa.security(인증 테스트)]
  → 도메인이 다르지만 의미적으로 하나의 청크

"MVP 스캐폴드" 청크:
  = [planning.prd + design.wireframe + dev.frontend.component]
  → 자주 함께 실행되어 composite Skill로 자동 승격 후보

이론 근거: Chase & Simon (1973) — 체스 마스터는 개별 말이 아닌
의미 있는 패턴(청크)으로 인식하여 작업기억 한계를 극복
```

---

## 8-12. 3차 누락 보완

### (1) 블룸 레벨 ↔ 스킬 유형 매핑 테이블

| 블룸 레벨 | 스킬 유형 | 예시 |
|----------|----------|------|
| Create | 생성 스킬 | 코드 생성, UI 설계, 카피 작성, PRD 작성 |
| Evaluate | 평가 스킬 | 코드 리뷰, 성능 분석, UX 검수, A/B 테스트 분석 |
| Analyze | 분석 스킬 | 요구사항 분해, 버그 원인 분석, 경쟁사 분석 |
| Apply | 적용 스킬 | 디자인 패턴 적용, 코딩 컨벤션 적용, 템플릿 적용 |
| Understand | 이해 스킬 | PRD 요약, 기술 문서 해석, 유저 니즈 파악 |
| Remember | 참조 스킬 | API 레퍼런스 조회, 라이브러리 문서, 기존 패턴 검색 |

**핵심 규칙:** 높은 레벨 Skill은 반드시 낮은 레벨 Skill의 출력을 입력으로 받아야 한다.
Remember 없이 Create를 바로 호출하면 할루시네이션 발생 확률 급증.

### (2) 블룸 체이닝 구체 예시

```
예: "랜딩페이지 만들어줘"

  Remember  → [기존 랜딩페이지 패턴 조회 — 고전환율 사례 검색]
  Understand → [타겟 유저의 핵심 니즈 파악 — 페르소나 분석]
  Analyze   → [경쟁사 랜딩페이지 구조 분해 — 헤더/히어로/CTA/사회적증거 패턴]
  Apply     → [검증된 전환율 패턴 적용 — AIDA 구조, 게슈탈트 원리]
  Create    → [실제 랜딩페이지 코드 생성 — Next.js + Tailwind]
  Evaluate  → [UX 감사 + 성능 체크 — OWASP, Web Vitals, 접근성]

→ 중간 단계를 건너뛰면 할루시네이션 확률 급증
→ 확산 활성화로 필요한 단계가 자동 활성화되므로 건너뛰기 방지
```

### (3) C1(activation-spreader) 도메인 분류 키워드 규칙

```yaml
# C1의 1단계: 도메인 감지 (벡터 검색 전 1차 필터)
domain_detection:
  method: "키워드 매칭 + 벡터 의미 검색 병행"
  
  keyword_rules: # 빠른 1차 필터
    planning:
      keywords: [기획, PRD, 요구사항, 유저, 페르소나, 기능, 스프린트, MVP, 시장]
    design:
      keywords: [디자인, UI, UX, 컴포넌트, 레이아웃, 색상, 와이어프레임, 프로토타입]
    development:
      keywords: [코드, 함수, API, DB, 컴포넌트, 빌드, 배포, 서버, 인증, 결제]
    marketing:
      keywords: [마케팅, 카피, SEO, 광고, 전환율, 퍼널, 랜딩, 이메일, 소셜]
    qa:
      keywords: [테스트, 버그, 리뷰, 성능, 보안, 검증, QA, 에러]
    multi_domain:
      trigger: "2개 이상 도메인 키워드 동시 감지 → 멀티 도메인 플래그"
  
  vector_search: # 키워드로 안 잡히는 경우 벡터 의미 검색
    fallback: "키워드 매칭 실패 시 벡터 DB 코사인 유사도로 도메인 판별"
```

### (4) C1 블룸 레벨 추정 키워드

```yaml
# C1의 2단계: 블룸 레벨 추정
bloom_estimation:
  Create:    ["만들어줘", "생성", "구현", "설계", "개발", "작성", "빌드"]
  Evaluate:  ["검토해줘", "리뷰", "평가", "감사", "검증", "비교 분석"]
  Analyze:   ["분석해줘", "분해", "원인", "구조", "왜", "패턴 파악"]
  Apply:     ["적용해줘", "변환", "사용", "활용", "구성"]
  Understand:["설명해줘", "요약", "정리", "해석", "이해"]
  Remember:  ["찾아줘", "알려줘", "검색", "조회", "레퍼런스"]
```

### (5) C1 복잡도 점수 산정 (factors + thresholds)

```yaml
# C1의 3단계: 복잡도 점수 산정
complexity_scoring:
  factors:
    - name: "변수 개수"
      condition: "7개 초과 시"
      score: "+2점"
    - name: "의존성 깊이"
      condition: "3단계 초과 시"
      score: "+2점"
    - name: "모호성 수준"
      condition: "구체적 명세 부재 시"
      score: "+1점"
    - name: "도메인 교차"
      condition: "2개 이상 도메인에 걸칠 때"
      score: "+1점/교차 도메인"
  
  thresholds:
    simple:  "0~3점 → 시스템 1 Skill (빠른 실행, 낮은 토큰, CoT 없이)"
    medium:  "4~6점 → 시스템 2 Skill (표준 Chain-of-Thought)"
    complex: "7점+  → 멀티 Skill 파이프라인 (DAG 구성, 병렬+순차)"
```

### (6) 모순 감지 구체 예시

```yaml
# 모순(Contradiction) 감지 — Engeström 활동 이론 기반
contradiction_examples:
  
  technical:
    example: "design.ui-component가 모달 팝업 제안 vs dev.frontend.component가 인라인 폼 제안"
    resolution: "사용자에게 양쪽 장단점 제시 → 선택 요청"
  
  business:
    example: "planning.user-persona가 '가격 민감한 자영업자' vs marketing.copy가 '프리미엄 포지셔닝'"
    resolution: "포지셔닝 재검토 → planning.prd-generation 재활성화"
  
  cross_domain:
    example: "dev.backend.api가 동기 처리 설계 vs dev.infra.deployment가 서버리스 아키텍처 제안"
    resolution: "Gentner 구조 매핑으로 구조적 불일치 감지 → 상위 레벨 통합 원칙 수립"
  
  theory_conflict:
    example: "힉스 법칙(선택지 줄여라) vs 사용자 요구(더 많은 옵션 원함)"
    resolution: "프로그레시브 디스클로저 제안 — 기본은 줄이되 '더 보기'로 확장"
```

---

## 8-13. 4차 누락 보완 (최종)

### (1) 전체 온톨로지 그래프 다이어그램 (정적 초기 가중치)

```
                    ┌─────────────────────────────────────┐
                    │    SKILL ONTOLOGY GRAPH (초기 가중치)  │
                    └─────────────────────────────────────┘

  [planning.problem-definition] ←──0.95──→ [planning.user-persona]
         │                                        │
         │ 0.90                                   │ 0.80
         ▼                                        ▼
  [planning.prd-generation] ←────0.85────→ [planning.feature-prioritization]
         │                                        │
         │ 0.75                                   │ 0.70
         ▼                                        ▼
  [design.wireframe] ←──────0.80──────→ [design.ui-component]
         │                                        │
         │ 0.70                                   │ 0.85
         ▼                                        ▼
  [dev.frontend.component] ←──0.90──→ [dev.frontend.styling]
         │                                        │
         │ 0.75                                   │ 0.60
         ▼                                        ▼
  [dev.backend.api] ←─────0.80─────→ [dev.backend.auth]
         │                                │
         │ 0.75                           │ 0.70
         ▼                                ▼
  [dev.backend.database] ←──0.65──→ [dev.backend.payment]
         │
         │ 0.65
         ▼
  [qa.unit-test] ←────0.85────→ [qa.code-review]

  ─── 크로스 도메인 링크 (구조 매핑 기반) ───
  [planning.competitive-analysis] ←──0.50──→ [marketing.copy]
  [planning.kpi-definition] ←──0.55──→ [marketing.analytics]
  [design.interaction-pattern] ←──0.60──→ [marketing.landing-page]
  [qa.bug-analysis] ←──0.45──→ [planning.sprint-decomposition]
```

### (2) 확산 활성화 5단계 알고리즘 (통합 블록)

```yaml
activation_spreading_algorithm:
  
  step_1_initial_activation:
    trigger: "사용자 자연어 입력"
    process:
      - 벡터 DB 의미 검색으로 Seed Skill 1~3개 선택
      - 키워드 매칭으로 보완 (8-12 (3) 참조)
      - Seed Skill의 활성화 값 = 1.0
  
  step_2_spreading:
    formula: "A(child) = A(parent) × edge_weight × decay_rate"
    parameters:
      decay_rate: 0.85
      threshold: 0.40
      max_depth: 3  # 최대 3홉
    process:
      - Seed에서 연결된 모든 Skill로 활성화 확산
      - 확산값 = 부모_활성화 × 엣지_가중치 × 0.85
      - 임계값(0.40) 이상인 Skill만 활성화
      - 이미 활성화된 Skill은 스킵 (중복 방지)
      - 최대 3홉까지 재귀 확산
  
  step_3_bloom_ordering:
    process:
      - 활성화된 Skill들을 블룸 택소노미 순서로 정렬
      - Remember → Understand → Apply → Analyze → Evaluate → Create
      - 같은 블룸 레벨의 Skill은 병렬 실행 허용
      - 높은 블룸 레벨은 낮은 레벨 완료 후 실행
      - Create가 Analyze 이하 없이 단독이면 → 누락 Skill 자동 삽입
  
  step_4_execution:
    process:
      - 활성화된 Skill 그래프를 실행 계획(DAG)으로 변환
      - 의존성(REQUIRES 엣지)이 없는 Skill들은 병렬 실행
      - 공유 컨텍스트(shared_context)에 각 Skill 출력을 누적
      - 각 Skill 실행 전후로 해당 도메인 Hook 발동
  
  step_5_feedback:
    process:
      - 실행 결과에 따라 엣지 가중치 업데이트
      - 성공적 조합: 가중치 += 0.05 (최대 1.0)
      - 실패/충돌 조합: 가중치 -= 0.05 (최소 0.10)
      - 30일 미사용: 가중치 *= 0.95
      - 3회+ 동시 활성화 미연결 Skill → 새 엣지 생성 (0.40)
      - 이것이 온톨로지의 "자가 발전" 메커니즘
```

### (3) 150개 논문 Full 레퍼런스 (전체 제목 + DOI)

> 마스터 PART 2의 축약 레퍼런스를 보완하는 전체 인용 정보.
> Neo4j Theory 노드의 paper/doi 필드에 직접 입력용.

**A. 인지심리학 (20개)**

| # | Full Reference |
|---|---------------|
| 1 | Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science*, 12(2), 257-285. doi:10.1207/s15516709cog1202_4 |
| 2 | Zhang, Y. et al. (2024). Cognitive load limits in large language models: Benchmarking. *arXiv:2509.19517* |
| 3 | Miller, G.A. (1956). The magical number seven, plus or minus two: Some limits on our capacity for processing information. *Psychological Review*, 63(2), 81-97. doi:10.1037/h0043158 |
| 4 | Chase, W.G. & Simon, H.A. (1973). Perception in chess. *Cognitive Psychology*, 4(1), 55-81. doi:10.1016/0010-0285(73)90004-2 |
| 5 | Kahneman, D. (2011). *Thinking, Fast and Slow*. Farrar, Straus and Giroux. / Evans, J.St.B.T. (2008). Dual-processing accounts of reasoning, judgment, and social cognition. *Annual Review of Psychology*, 59, 255-278. doi:10.1146/annurev.psych.59.103006.093629 |
| 6 | Bartlett, F.C. (1932). *Remembering: A Study in Experimental and Social Psychology*. Cambridge UP. / Rumelhart, D.E. (1980). Schemata: The building blocks of cognition. In R.J. Spiro et al. (Eds.), *Theoretical Issues in Reading Comprehension*. Erlbaum. / Anderson, R.C. (1977). The notion of schemata and the educational enterprise. In R.C. Anderson et al. (Eds.), *Schooling and the Acquisition of Knowledge*. Erlbaum. |
| 7 | Petty, R.E. & Cacioppo, J.T. (1986). The elaboration likelihood model of persuasion. *Advances in Experimental Social Psychology*, 19, 123-205. doi:10.1016/S0065-2601(08)60214-2 |
| 8 | Flavell, J.H. (1979). Metacognition and cognitive monitoring: A new area of cognitive-developmental inquiry. *American Psychologist*, 34(10), 906-911. doi:10.1037/0003-066X.34.10.906 |
| 9 | Oh, S. & Gobet, F. (2025). Before you think, monitor: Implementing Flavell's metacognitive framework in LLMs. *arXiv:2510.16374*. Workshop on LLM Explainability, COLM 2025. |
| 10 | Johnson-Laird, P.N. (1983). *Mental Models: Towards a Cognitive Science of Language, Inference, and Consciousness*. Harvard UP. |
| 11 | Paivio, A. (1971). *Imagery and Verbal Processes*. Holt, Rinehart & Winston. / Paivio, A. (1986). *Mental Representations: A Dual Coding Approach*. Oxford UP. |
| 12 | Craik, F.I.M. & Lockhart, R.S. (1972). Levels of processing: A framework for memory research. *Journal of Verbal Learning and Verbal Behavior*, 11(6), 671-684. doi:10.1016/S0022-5371(72)80001-X |
| 13 | Ebbinghaus, H. (1885). *Über das Gedächtnis*. Duncker & Humblot. / Cepeda, N.J. et al. (2006). Distributed practice in verbal recall tasks: A review and quantitative synthesis. *Psychological Bulletin*, 132(3), 354-380. doi:10.1037/0033-2909.132.3.354 |
| 14 | Rohrer, D. & Taylor, K. (2007). The shuffling of mathematics problems improves learning. *Instructional Science*, 35(6), 481-498. doi:10.1007/s11251-007-9015-8 |
| 15 | Roediger, H.L. & Karpicke, J.D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science*, 17(3), 249-255. doi:10.1111/j.1467-9280.2006.01693.x |
| 16 | Bjork, R.A. (1994). Memory and metamemory considerations in the training of human beings. In J. Metcalfe & A. Shimamura (Eds.), *Metacognition: Knowing about Knowing*. MIT Press, 185-205. |
| 17 | Spiro, R.J. et al. (1988). Cognitive flexibility theory: Advanced knowledge acquisition in ill-structured domains. In *Tenth Annual Conference of the Cognitive Science Society*. Erlbaum. |
| 18 | Collins, A., Brown, J.S. & Newman, S.E. (1989). Cognitive apprenticeship: Teaching the crafts of reading, writing, and mathematics. In L.B. Resnick (Ed.), *Knowing, Learning, and Instruction*. Erlbaum, 453-494. |
| 19 | Lave, J. & Wenger, E. (1991). *Situated Learning: Legitimate Peripheral Participation*. Cambridge UP. doi:10.1017/CBO9780511815355 |
| 20 | Ericsson, K.A., Krampe, R.T. & Tesch-Römer, C. (1993). The role of deliberate practice in the acquisition of expert performance. *Psychological Review*, 100(3), 363-406. doi:10.1037/0033-295X.100.3.363 |

**B. 확산/연결/시스템 (10개)**

| # | Full Reference |
|---|---------------|
| 21 | Collins, A.M. & Loftus, E.F. (1975). A spreading-activation theory of semantic processing. *Psychological Review*, 82(6), 407-428. doi:10.1037/0033-295X.82.6.407 |
| 22 | Hutchins, E. (1995). *Cognition in the Wild*. MIT Press. / Hollan, J., Hutchins, E. & Kirsh, D. (2000). Distributed cognition: Toward a new foundation for HCI research. *ACM TOCHI*, 7(2), 174-196. doi:10.1145/353485.353487 |
| 23 | Engeström, Y. (1987). *Learning by Expanding: An Activity-Theoretical Approach to Developmental Research*. Helsinki: Orienta-Konsultit. / Engeström, Y. (2000). Activity theory as a framework for analyzing and redesigning work. *Ergonomics*, 43(7), 960-974. doi:10.1080/001401300409143 |
| 24 | Gentner, D. (1983). Structure-mapping: A theoretical framework for analogy. *Cognitive Science*, 7(2), 155-170. doi:10.1207/s15516709cog0702_3 |
| 25 | Falkenhainer, B., Forbus, K.D. & Gentner, D. (1989). The structure-mapping engine: Algorithm and examples. *Artificial Intelligence*, 41(1), 1-63. doi:10.1016/0004-3702(89)90077-5 |
| 26 | Pirolli, P. & Card, S. (1999). Information foraging. *Psychological Review*, 106(4), 643-675. doi:10.1037/0033-295X.106.4.643 |
| 27 | Senge, P. (1990). *The Fifth Discipline: The Art & Practice of the Learning Organization*. Doubleday. |
| 28 | Wiener, N. (1948). *Cybernetics: Or Control and Communication in the Animal and the Machine*. MIT Press. |
| 29 | Holland, J.H. (1995). *Hidden Order: How Adaptation Builds Complexity*. Addison-Wesley. / Holland, J.H. (1992). Complex adaptive systems. *Daedalus*, 121(1), 17-30. |
| 30 | Conway, M.E. (1968). How do committees invent? *Datamation*, 14(4), 28-31. |

**C. 교육학 (10개)**

| # | Full Reference |
|---|---------------|
| 31 | Bloom, B.S. (1956). *Taxonomy of Educational Objectives: The Classification of Educational Goals*. David McKay. / Anderson, L.W. & Krathwohl, D.R. (2001). *A Taxonomy for Learning, Teaching, and Assessing: A Revision of Bloom's Taxonomy*. Longman. |
| 32 | Vygotsky, L.S. (1978). *Mind in Society: The Development of Higher Psychological Processes*. Harvard UP. |
| 33 | Wood, D., Bruner, J. & Ross, G. (1976). The role of tutoring in problem solving. *Journal of Child Psychology and Psychiatry*, 17(2), 89-100. doi:10.1111/j.1469-7610.1976.tb00381.x |
| 34 | Piaget, J. (1976). Piaget's theory. In B. Inhelder & H.H. Chipman (Eds.), *Piaget and His School*. Springer. / Bruner, J. (1966). *Toward a Theory of Instruction*. Belknap Press. |
| 35 | Kolb, D.A. (1984). *Experiential Learning: Experience as the Source of Learning and Development*. Prentice-Hall. |
| 36 | Wiggins, G. & McTighe, J. (1998). *Understanding by Design*. ASCD. |
| 37 | Branson, R.K. et al. (1975). *Interservice Procedures for Instructional Systems Development*. U.S. Army TRADOC. |
| 38 | Mayer, R.E. (2009). *Multimedia Learning* (2nd ed.). Cambridge UP. doi:10.1017/CBO9780511811678 |
| 39 | Fiorella, L. & Mayer, R.E. (2015). *Learning as a Generative Activity: Eight Learning Strategies that Promote Understanding*. Cambridge UP. doi:10.1017/CBO9781107707085 |
| 40 | Zimmerman, B.J. (2002). Becoming a self-regulated learner: An overview. *Theory Into Practice*, 41(2), 64-70. doi:10.1207/s15430421tip4102_2 |

**D. UX/디자인 (15개)**

| # | Full Reference |
|---|---------------|
| 41 | Hick, W.E. (1952). On the rate of gain of information. *Quarterly Journal of Experimental Psychology*, 4(1), 11-26. doi:10.1080/17470215208416600 |
| 42 | Fitts, P.M. (1954). The information capacity of the human motor system in controlling the amplitude of movement. *Journal of Experimental Psychology*, 47(6), 381-391. doi:10.1037/h0055392 |
| 43 | Wertheimer, M. (1923). Untersuchungen zur Lehre von der Gestalt II. *Psychologische Forschung*, 4(1), 301-350. doi:10.1007/BF00410640 |
| 44 | Nielsen, J. (2000). End of web design. *Nielsen Norman Group*. / Nielsen, J. (1993). *Usability Engineering*. Academic Press. |
| 45 | Nielsen, J. (1993). *Usability Engineering*. Academic Press. Ch.5 Usability Heuristics. |
| 46 | Von Restorff, H. (1933). Über die Wirkung von Bereichsbildungen im Spurenfeld. *Psychologische Forschung*, 18(1), 299-342. doi:10.1007/BF02409636 |
| 47 | Murdock, B.B. (1962). The serial position effect of free recall. *Journal of Experimental Psychology*, 64(5), 482-488. doi:10.1037/h0045106 |
| 48 | Zeigarnik, B. (1927). Über das Behalten von erledigten und unerledigten Handlungen. *Psychologische Forschung*, 9(1), 1-85. doi:10.1007/BF02409755 |
| 49 | Kahneman, D., Fredrickson, B.L., Schreiber, C.A. & Redelmeier, D.A. (1993). When more pain is preferred to less: Adding a better end. *Psychological Science*, 4(6), 401-405. doi:10.1111/j.1467-9280.1993.tb00589.x |
| 50 | Tractinsky, N., Katz, A.S. & Ikar, D. (2000). What is beautiful is usable. *Interacting with Computers*, 13(2), 127-145. doi:10.1016/S0953-5438(00)00031-X |
| 51 | Nunes, J.C. & Drèze, X. (2006). The endowed progress effect: How artificial advancement increases effort. *Journal of Consumer Research*, 32(4), 504-512. doi:10.1086/500480 |
| 52 | Doherty, W.J. & Thadhani, A.J. (1982). The economic value of rapid response time. *IBM Systems Journal*, 21(3), 305-317. doi:10.1147/sj.213.0305 |
| 53 | Tesler, L. (2007). The law of conservation of complexity. *Interactions*, 14(3). / Norman, D.A. (2007). *The Design of Future Things*. Basic Books. |
| 54 | Pirolli, P. & Card, S. (1999). [위 #26] / Chi, E.H. et al. (2001). Using information scent to model user information needs and actions on the web. *CHI 2001*. ACM, 490-497. doi:10.1145/365024.365325 |
| 55 | [위 #52 동일] |

**E. 설득/마케팅 (16개)**

| # | Full Reference |
|---|---------------|
| 56 | Strong, E.K. (1925). *The Psychology of Selling and Advertising*. McGraw-Hill. |
| 57 | Christensen, C.M. & Raynor, M.E. (2003). *The Innovator's Solution*. Harvard Business School Press. / Ulwick, A.W. (2005). *What Customers Want*. McGraw-Hill. |
| 58 | Eyal, N. (2014). *Hooked: How to Build Habit-Forming Products*. Portfolio/Penguin. |
| 59 | Thaler, R.H. & Sunstein, C.R. (2008). *Nudge: Improving Decisions About Health, Wealth, and Happiness*. Yale UP. |
| 60 | Tversky, A. & Kahneman, D. (1974). Judgment under uncertainty: Heuristics and biases. *Science*, 185(4157), 1124-1131. doi:10.1126/science.185.4157.1124 |
| 61 | Kahneman, D. & Tversky, A. (1979). Prospect theory: An analysis of decision under risk. *Econometrica*, 47(2), 263-291. doi:10.2307/1914185 |
| 62 | Cialdini, R.B. (1984). *Influence: The Psychology of Persuasion*. William Morrow. Ch.4. |
| 63 | Cialdini (1984) Ch.7 / Worchel, S., Lee, J. & Adewole, A. (1975). Effects of supply and demand on ratings of object value. *JPSP*, 32(5), 906-914. doi:10.1037/0022-3514.32.5.906 |
| 64 | Cialdini (1984) Ch.6 / Milgram, S. (1963). Behavioral study of obedience. *JASP*, 67(4), 371-378. doi:10.1037/h0040525 |
| 65 | Cialdini (1984) Ch.2 / Gouldner, A.W. (1960). The norm of reciprocity: A preliminary statement. *American Sociological Review*, 25(2), 161-178. doi:10.2307/2092623 |
| 66 | Cialdini (1984) Ch.3 / Festinger, L. (1957). *A Theory of Cognitive Dissonance*. Stanford UP. |
| 67 | Fogg, B.J. (2009). A behavior model for persuasive design. *Persuasive Technology: 4th Intl Conference*. ACM, Article 40. doi:10.1145/1541948.1541999 |
| 68 | Festinger, L. (1957). *A Theory of Cognitive Dissonance*. Stanford UP. |
| 69 | Thaler, R.H. (1980). Toward a positive theory of consumer choice. *Journal of Economic Behavior & Organization*, 1(1), 39-60. doi:10.1016/0167-2681(80)90051-7 |
| 70 | Zajonc, R.B. (1968). Attitudinal effects of mere exposure. *Journal of Personality and Social Psychology*, 9(2, Pt.2), 1-27. doi:10.1037/h0025848 |
| 71 | Porter, M.E. (1979). How competitive forces shape strategy. *Harvard Business Review*, 57(2), 137-145. / Porter, M.E. (1980). *Competitive Strategy*. Free Press. |

**F. SW공학 (10개)**

| # | Full Reference |
|---|---------------|
| 72 | Martin, R.C. (2003). *Agile Software Development: Principles, Patterns, and Practices*. Prentice-Hall. / Martin, R.C. (2000). Design principles and design patterns. objectmentor.com. |
| 73 | Hunt, A. & Thomas, D. (1999). *The Pragmatic Programmer: From Journeyman to Master*. Addison-Wesley. |
| 74 | Dijkstra, E.W. (1982). On the role of scientific thought. In *Selected Writings on Computing: A Personal Perspective*. Springer, 60-66. (EWD 447, 1974) |
| 75 | McIlroy, M.D., Pinson, E.N. & Tague, B.A. (1978). UNIX time-sharing system: Foreword. *Bell System Technical Journal*, 57(6), 1899-1904. / Raymond, E.S. (2003). *The Art of Unix Programming*. Addison-Wesley. |
| 76 | Brooks, F.P. (1975). *The Mythical Man-Month: Essays on Software Engineering*. Addison-Wesley. |
| 77 | William of Ockham (c.1320). *Summa Logicae*. / Baker, A. (2016). Simplicity. *Stanford Encyclopedia of Philosophy*. |
| 78 | Deming, W.E. (1986). *Out of the Crisis*. MIT Press. / Shewhart, W.A. (1939). *Statistical Method from the Viewpoint of Quality Control*. Dover. |
| 79 | Imai, M. (1986). *Kaizen: The Key to Japan's Competitive Success*. McGraw-Hill. |
| 80 | Pareto, V. (1896). *Cours d'économie politique*. F. Rouge. / Juran, J.M. (1951). *Quality Control Handbook*. McGraw-Hill. |
| 81 | Conway, M.E. (1968). [위 #30 동일] |

**G. 편향 (10개)**

| # | Full Reference |
|---|---------------|
| A1 | Wason, P.C. (1960). On the failure to eliminate hypotheses in a conceptual task. *QJEP*, 12(3), 129-140. doi:10.1080/17470216008416717 / Nickerson, R.S. (1998). Confirmation bias: A ubiquitous phenomenon in many guises. *Review of General Psychology*, 2(2), 175-220. doi:10.1037/1089-2680.2.2.175 |
| A2 | Kruger, J. & Dunning, D. (1999). Unskilled and unaware of it: How difficulties in recognizing one's own incompetence lead to inflated self-assessments. *JPSP*, 77(6), 1121-1134. doi:10.1037/0022-3514.77.6.1121 |
| A3 | Simon, H.A. (1955). A behavioral model of rational choice. *Quarterly Journal of Economics*, 69(1), 99-118. doi:10.2307/1884852 |
| A4 | Simon, H.A. (1956). Rational choice and the structure of the environment. *Psychological Review*, 63(2), 129-138. doi:10.1037/h0042769 |
| A5 | Tversky, A. & Kahneman, D. (1981). The framing of decisions and the psychology of choice. *Science*, 211(4481), 453-458. doi:10.1126/science.7455683 |
| A6 | Tversky, A. & Kahneman, D. (1973). Availability: A heuristic for judging frequency and probability. *Cognitive Psychology*, 5(2), 207-232. doi:10.1016/0010-0285(73)90033-9 |
| A7 | Wald, A. (1943). *A Method of Estimating Plane Vulnerability Based on Damage of Survivors*. Statistical Research Group, Columbia University. SRG Memo 256. |
| A8 | Arkes, H.R. & Blumer, C. (1985). The psychology of sunk cost. *Organizational Behavior and Human Decision Processes*, 35(1), 124-140. doi:10.1016/0749-5978(85)90049-4 |
| A9 | Buehler, R., Griffin, D. & Ross, M. (1994). Exploring the "planning fallacy": Why people underestimate their task completion times. *JPSP*, 67(3), 366-381. doi:10.1037/0022-3514.67.3.366 |
| A10 | Fischhoff, B. (1975). Hindsight ≠ foresight: The effect of outcome knowledge on judgment under uncertainty. *JEP: Human Perception and Performance*, 1(3), 288-299. doi:10.1037/0096-1523.1.3.288 |

**H. 비즈니스 (7개)**

| # | Full Reference |
|---|---------------|
| B1 | Ries, E. (2011). *The Lean Startup: How Today's Entrepreneurs Use Continuous Innovation to Create Radically Successful Businesses*. Crown Business. |
| B2 | British Design Council (2005). *The Design Process: The 'Double Diamond' Design Process Model*. |
| B3 | Brown, T. (2008). Design thinking. *Harvard Business Review*, 86(6), 84-92. / Brown, T. (2009). *Change by Design: How Design Thinking Transforms Organizations and Inspires Innovation*. HarperBusiness. |
| B4 | Davis, F.D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. *MIS Quarterly*, 13(3), 319-340. doi:10.2307/249008 |
| B5 | Rogers, E.M. (1962). *Diffusion of Innovations*. Free Press. (5th ed., 2003) |
| B6 | Csikszentmihalyi, M. (1990). *Flow: The Psychology of Optimal Experience*. Harper & Row. / Csikszentmihalyi, M. (1975). *Beyond Boredom and Anxiety*. Jossey-Bass. |
| B7 | Deci, E.L. & Ryan, R.M. (1985). *Intrinsic Motivation and Self-Determination in Human Behavior*. Plenum. / Ryan, R.M. & Deci, E.L. (2000). Self-determination theory and the facilitation of intrinsic motivation, social development, and well-being. *American Psychologist*, 55(1), 68-78. doi:10.1037/0003-066X.55.1.68 |

**I. 엔지니어링 (52개)**

| # | Full Reference |
|---|---------------|
| 99 | Brewer, E. (2000). Towards robust distributed systems. *PODC 2000 Keynote*. / Gilbert, S. & Lynch, N. (2002). Brewer's conjecture and the feasibility of consistent, available, partition-tolerant web services. *ACM SIGACT News*, 33(2), 51-59. doi:10.1145/564585.564601 / Brewer, E. (2012). CAP twelve years later: How the "rules" have changed. *Computer*, 45(2), 23-29. doi:10.1109/MC.2012.37 |
| 100 | Haerder, T. & Reuter, A. (1983). Principles of transaction-oriented database recovery. *ACM Computing Surveys*, 15(4), 287-317. doi:10.1145/289.291 |
| 101 | Fielding, R.T. (2000). *Architectural Styles and the Design of Network-Based Software Architectures*. PhD Dissertation, University of California, Irvine. Ch.5. |
| 102 | Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley. / Akbari, A. et al. (2025). Domain-driven design in software development: A systematic literature review. *Journal of Systems and Software*, 219, 112055. doi:10.1016/j.jss.2025.112055 |
| 103 | Wiggins, A. (2011). *The Twelve-Factor App*. Heroku. https://12factor.net |
| 104 | Hohpe, G. & Woolf, B. (2003). *Enterprise Integration Patterns: Designing, Building, and Deploying Messaging Solutions*. Addison-Wesley. |
| 105 | Young, G. (2010). *CQRS Documents*. cqrs.files.wordpress.com. / Fowler, M. (2011). CQRS. martinfowler.com. |
| 106 | RFC 7231 (2014). *Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content*. IETF. Section 4.2.2 Idempotent Methods. |
| 107 | Codd, E.F. (1970). A relational model of data for large shared data banks. *Communications of the ACM*, 13(6), 377-387. doi:10.1145/362384.362685 / Codd, E.F. (1971). Further normalization of the data base relational model. *Courant Computer Science Symposia 6*. / Kent, W. (1983). A simple guide to five normal forms in relational database theory. *Communications of the ACM*, 26(2), 120-125. doi:10.1145/358024.358054 |
| 108 | Hellerstein, J.M., Stonebraker, M. & Hamilton, J. (2007). Architecture of a database system. *Foundations and Trends in Databases*, 1(2), 141-259. doi:10.1561/1900000002 |
| 109 | Fowler, M. (2005). Event sourcing. martinfowler.com. / Betts, D. et al. (2012). *Exploring CQRS and Event Sourcing*. Microsoft Patterns & Practices. |
| 110 | Dehghani, Z. (2022). *Data Mesh: Delivering Data-Driven Value at Scale*. O'Reilly. |
| 111 | Stonebraker, M. et al. (2010). MapReduce and parallel DBMSs: Friends or foes? *Communications of the ACM*, 53(1), 64-71. doi:10.1145/1629175.1629197 |
| 112 | Abadi, D. (2012). Consistency tradeoffs in modern distributed database system design. *Computer*, 45(2), 37-42. doi:10.1109/MC.2012.33 |
| 113 | Reason, J. (1990). *Human Error*. Cambridge UP. / Reason, J. (1990). The contribution of latent human failures to the breakdown of complex systems. *Phil. Trans. Royal Society B*, 327(1241), 475-484. doi:10.1098/rstb.1990.0090 |
| 114 | ISO/IEC 27001:2022. *Information security, cybersecurity and privacy protection — Information security management systems — Requirements*. |
| 115 | Saltzer, J.H. & Schroeder, M.D. (1975). The protection of information in computer systems. *Proceedings of the IEEE*, 63(9), 1278-1308. doi:10.1109/PROC.1975.9939 / Smith, R.E. (2012). A contemporary look at Saltzer and Schroeder's 1975 design principles. *IEEE Security & Privacy*, 10(6), 20-25. doi:10.1109/MSP.2012.85 |
| 116 | OWASP Foundation (2021). *OWASP Top 10:2021*. https://owasp.org/Top10/ |
| 117 | Shostack, A. (2014). *Threat Modeling: Designing for Security*. Wiley. |
| 118 | Kindervag, J. (2010). *No More Chewy Centers: Introducing the Zero Trust Model of Information Security*. Forrester Research. / Rose, S. et al. (2020). *Zero Trust Architecture*. NIST SP 800-207. doi:10.6028/NIST.SP.800-207 |
| 119 | NSA (2012). *Defense in Depth: A Practical Strategy for Achieving Information Assurance in Today's Highly Networked Environments*. |
| 120 | Cavoukian, A. (2009). *Privacy by Design: The 7 Foundational Principles*. Information and Privacy Commissioner of Ontario. / GDPR Article 25 (2016). |
| 121 | Cohn, M. (2009). *Succeeding with Agile: Software Development Using Scrum*. Addison-Wesley. / Vocke, H. (2018). The practical test pyramid. martinfowler.com. |
| 122 | Myers, G.J. (1979). *The Art of Software Testing*. Wiley. (3rd ed., 2011, with Sandler & Badgett) |
| 123 | Myers, G.J. (1979). [위 #122 동일] |
| 124 | DeMillo, R.A., Lipton, R.J. & Sayward, F.G. (1978). Hints on test data selection: Help for the practicing programmer. *Computer*, 11(4), 34-41. doi:10.1109/C-M.1978.218136 / Jia, Y. & Harman, M. (2011). An analysis and survey of the development of mutation testing. *IEEE TSE*, 37(5), 649-678. doi:10.1109/TSE.2010.62 |
| 125 | Bach, J. (2003). Exploratory testing explained. In *The Testing Practitioner* (2nd ed.). UTN Publishers. |
| 126 | Smith, L. (2001). Shift-left testing. *Dr. Dobb's Journal*. |
| 127 | Basiri, A. et al. (2016). Chaos engineering. *IEEE Software*, 33(3), 35-41. doi:10.1109/MS.2016.60 / Rosenthal, C. & Jones, N. (2020). *Chaos Engineering: System Resiliency in Practice*. O'Reilly. |
| 128 | Frese, M. & Keith, N. (2015). Action errors, error management, and learning in organizations. *Annual Review of Organizational Psychology and Organizational Behavior*, 2, 661-687. doi:10.1146/annurev-orgpsych-032414-111353 |
| 129 | Beyer, B., Jones, C., Petoff, J. & Murphy, N.R. (2016). *Site Reliability Engineering: How Google Runs Production Systems*. O'Reilly. |
| 130 | Sridharan, C. (2018). *Distributed Systems Observability: A Guide to Building Robust Systems*. O'Reilly. / Majors, C., Fong-Jones, L. & Miranda, G. (2022). *Observability Engineering*. O'Reilly. |
| 131 | Morris, K. (2016). *Infrastructure as Code: Managing Servers in the Cloud*. O'Reilly. (2nd ed., 2020) |
| 132 | Weaveworks (2017). Operations by pull request. / Limoncelli, T.A. (2018). GitOps: A path to more self-service IT. *Queue*, 16(3), 29-44. doi:10.1145/3236386.3237207 |
| 133 | Humble, J. & Farley, D. (2010). *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Addison-Wesley. Ch.10. |
| 134 | Fowler, M. (2010). Feature toggles (aka feature flags). martinfowler.com. / Schermann, G. et al. (2018). Continuous experimentation: Challenges, implementation techniques, and current research. *IEEE Software*, 35(2), 26-31. doi:10.1109/MS.2017.4541044 |
| 135 | Amdahl, G.M. (1967). Validity of the single processor approach to achieving large scale computing capabilities. *AFIPS Conference Proceedings*, 30, 483-485. doi:10.1145/1465482.1465560 |
| 136 | Little, J.D.C. (1961). A proof for the queuing formula: L = λW. *Operations Research*, 9(3), 383-387. doi:10.1287/opre.9.3.383 / Little, J.D.C. (2011). Little's law as viewed on its 50th anniversary. *Operations Research*, 59(3), 535-549. doi:10.1287/opre.1110.0941 |
| 137 | Knuth, D.E. (1974). Structured programming with go to statements. *ACM Computing Surveys*, 6(4), 261-301. doi:10.1145/356635.356640 ("Premature optimization is the root of all evil") |
| 138 | [위 #52 동일] |
| 139 | Google (2020). *Web Vitals*. web.dev/vitals/ / Grigorik, I. (2013). *High Performance Browser Networking*. O'Reilly. |
| 140 | Goldratt, E.M. (1984). *The Goal: A Process of Ongoing Improvement*. North River Press. / Goldratt, E.M. (1990). *Theory of Constraints*. North River Press. |
| 141 | Ohno, T. (1988). *Toyota Production System: Beyond Large-Scale Production*. Productivity Press. / Anderson, D.J. (2010). *Kanban: Successful Evolutionary Change for Your Technology Business*. Blue Hole Press. |
| 142 | Schwaber, K. & Sutherland, J. (2020). *The Scrum Guide*. scrumguides.org. / Schwaber, K. (2004). *Agile Project Management with Scrum*. Microsoft Press. |
| 143 | Beck, K. et al. (2001). *Manifesto for Agile Software Development*. agilemanifesto.org. |
| 144 | Cunningham, W. (1992). The WyCash portfolio management system. *OOPSLA '92 Experience Report*. / Kruchten, P., Nord, R.L. & Ozkaya, I. (2012). Technical debt: From metaphor to theory and practice. *IEEE Software*, 29(6), 18-21. doi:10.1109/MS.2012.167 |
| 145 | Bayes, T. (1763). An essay towards solving a problem in the doctrine of chances. *Philosophical Transactions of the Royal Society*, 53, 370-418. doi:10.1098/rstl.1763.0053 |
| 146 | Kohavi, R., Longbotham, R., Sommerfield, D. & Henne, R.M. (2009). Controlled experiments on the web: Survey and practical guide. *Data Mining and Knowledge Discovery*, 18(1), 140-181. doi:10.1007/s10618-008-0114-1 |
| 147 | Fisher, R.A. (1925). *Statistical Methods for Research Workers*. Oliver & Boyd. / Wasserstein, R.L. & Lazar, N.A. (2016). The ASA's statement on p-values: Context, process, and purpose. *The American Statistician*, 70(2), 129-133. doi:10.1080/00031305.2016.1154108 |
| 148 | Simpson, E.H. (1951). The interpretation of interaction in contingency tables. *Journal of the Royal Statistical Society B*, 13(2), 238-241. doi:10.1111/j.2517-6161.1951.tb00088.x |
| 149 | Pöttker, H. (2003). News and its communicative quality: The inverted pyramid—when and why did it appear? *Journalism Studies*, 4(4), 501-511. doi:10.1080/1461670032000136596 |
| 150 | Flesch, R. (1948). A new readability yardstick. *Journal of Applied Psychology*, 32(3), 221-233. doi:10.1037/h0057532 / Kincaid, J.P. et al. (1975). *Derivation of New Readability Formulas*. Research Branch Report 8-75, Naval Technical Training Command. |
|-------|------|----------|------|------|
| 1 (즉시) | ~1주 | #1~10, #21~24, #31~34, #72~74 | 25개 | Skill 뼈대: 인지/학습/시스템 핵심 |
| 2 (1주) | 1~2주 | #41~55 | 15개 | 디자인 Skill 주입 |
| 3 (2주) | 2~3주 | #56~71 | 16개 | 마케팅 Skill 주입 |
| 4 (3주) | 3~4주 | #99~106, #107~112 | 14개 | 백엔드+DB Skill 주입 |
| 5 (4주) | 4~5주 | #113~120, #121~128 | 16개 | 보안+QA Hook 강화 |
| 6 (5주) | 5~6주 | #A1~A10 | 10개 | 할루시네이션 방지 Hook 강화 |
| 7 (6주) | 6~8주 | #129~150 + 나머지 | 나머지 | DevOps+성능+분석+콘텐츠 |

---

# PART 9: 멀티모델 + Custom MCP + Hook 알고리즘 아키텍처

> **핵심 전환 3가지:**
> 1. Hook = 선언적 yaml → **실행 가능한 알고리즘** (입력→분기→출력→에러)
> 2. Skill = 시스템 프롬프트 내장 → **Custom MCP 서버에서 동적 호출**
> 3. 단일 모델 → **Router Model(판단) + Executor Model(생성) 분리**

---

## 9-1. 왜 멀티모델인가

```
문제: Claude 본체 하나가 Hook 판단 + Skill 실행을 동시에 처리
     → #1 인지부하 이론 위반 (한 주체에 과부하)
     → #5 이중과정 이론: 시스템 1(빠른 판단)과 시스템 2(깊은 생성)을 하나가 처리

해결: 역할별 모델 분리
     → Router Model = 시스템 1 (빠른 판단, 분기, 라우팅)
     → Executor Model = 시스템 2 (깊은 생성, 코드, 기획, 디자인)
     → Validator Model = 메타인지 (자기 검증, 편향 감지)
```

| 역할 | 모델 | 담당 | 이론 근거 |
|------|------|------|----------|
| **Router** | Claude Haiku (경량/빠름) | Hook 알고리즘 실행, 도메인 분류, 복잡도 산정, Skill 라우팅, MCP 호출 결정 | #5 시스템 1 (Kahneman) |
| **Executor** | Claude Sonnet/Opus (고성능) | 실제 Skill 실행: 코드 생성, PRD 작성, 디자인, 마케팅 카피 | #5 시스템 2 (Kahneman) |
| **Validator** | Claude Haiku (경량) | 출력 검증: C5/G4/G5/S2 Hook 실행, 할루시네이션 체크, 편향 감지 | #8 메타인지 (Flavell) |

---

## 9-2. 전체 아키텍처

```
[사용자 입력]
      │
      ▼
┌─────────────────────────────────────────────────────────┐
│  ROUTER MODEL (Claude Haiku — 빠른 판단)                  │
│                                                          │
│  Hook 알고리즘 실행기:                                     │
│  C1(activation-spreader) → C2(bloom-sequencer)           │
│  C3(context-cleanup) → G2(mgv-monitor)                  │
│  G3(bias-scanner) → E1(principle-loader)                 │
│                                                          │
│  판단 결과:                                               │
│  • seed_skills: [planning.prd, dev.backend.api]          │
│  • activated_skills: 9개 (확산 활성화)                     │
│  • execution_dag: [[Layer0], [Layer1], ...]               │
│  • cognitive_system: 2 (Sonnet 사용)                      │
│  • activated_hooks: [S1,S2,S4,Q4,E2,...]                 │
│  • activated_theories: [JTBD, SOLID, REST, ...]          │
│                                                          │
│  MCP 호출:                                                │
│  • mcp__vector-db__semantic_search                       │
│  • mcp__graph-db__spread_activation                      │
│  • mcp__theory-knowledge__get_theories_for_domain        │
└──────────────────────┬──────────────────────────────────┘
                       │ DAG + 컨텍스트 + 이론
                       ▼
┌─────────────────────────────────────────────────────────┐
│  EXECUTOR MODEL (Claude Sonnet/Opus — 깊은 생성)          │
│                                                          │
│  DAG의 각 Layer를 순차/병렬 실행:                           │
│  Layer 0: mcp__planning__competitive_analysis ∥           │
│           mcp__planning__problem_definition               │
│  Layer 1: mcp__planning__user_persona ∥                   │
│           mcp__planning__feature_prioritization           │
│  Layer 2: mcp__planning__prd_generation                  │
│  Layer 3: mcp__design__wireframe ∥ ui_component          │
│  Layer 4: mcp__dev__backend_api ∥ backend_auth           │
│                                                          │
│  각 Skill은 Custom MCP 서버의 tool로 호출                  │
│  Skill 내용은 Executor에 내장되지 않음 → MCP에서 동적 로드   │
└──────────────────────┬──────────────────────────────────┘
                       │ 각 Layer 출력
                       ▼
┌─────────────────────────────────────────────────────────┐
│  VALIDATOR MODEL (Claude Haiku — 메타인지 검증)            │
│                                                          │
│  POST Hook 알고리즘 실행:                                  │
│  C5(output-validate) → 완전성/할루시네이션/블룸 일치         │
│  G4(mgv-verify) → 자기설명/확신도/대안 검증                  │
│  G5(bias-postcheck) → 확증편향/더닝크루거/계획오류           │
│  S2(owasp-scanner) → OWASP Top 10 취약점 스캔             │
│  S3(stride-checker) → STRIDE 위협 모델링                   │
│  Q4(shift-left-enforcer) → 테스트 동반 강제                │
│  P1/P2 → 성능 예산 체크                                    │
│                                                          │
│  판정:                                                    │
│  • PASS → 사용자에게 출력                                  │
│  • FAIL(경미) → Executor에 수정 지시 + 재실행               │
│  • FAIL(심각) → 출력 차단 + 사용자에게 보고                  │
│                                                          │
│  피드백:                                                   │
│  V1(weight-updater) → mcp__graph-db__update_weights      │
│  V2(pattern-learner) → mcp__graph-db 패턴 저장            │
└─────────────────────────────────────────────────────────┘
```

---

## 9-3. 모델 간 통신 프로토콜

```yaml
router_to_executor:
  payload:
    execution_dag: [[{skill_id, mcp_server, mcp_tool, params}], ...]
    context: {cleaned_context_per_skill}
    theories: {skill_id: [theory_summaries]}
    constraints: {skill_id: [constraints]}
    cognitive_system: 1 | 2
    scaffolding_level: "LOW" | "MEDIUM" | "HIGH"

executor_to_validator:
  payload:
    skill_outputs: [{skill_id, output, tokens_used, execution_time}]
    original_dag: {위와 동일}
    accumulated_context: {공유 컨텍스트 풀}

validator_to_user:
  IF passed:
    final_output: "Executor 출력 (검증 통과)"
  IF failed_minor:
    feedback_to_executor: "수정 지시 + 재실행"
  IF failed_critical:
    block_output: "차단 + 이유 설명 + 대안 제시"

validator_to_graph_db:
  weight_update: {executed_skills, success}
  pattern_data: {execution_chain, success, failure_reason}
```

---

## 9-4. Custom MCP 서버 설계

### MCP 서버 목록 (9개)

| 서버 | 역할 | tool 수 | 호출자 |
|------|------|--------|-------|
| `planning-skills` | 기획 도메인 Skill | 9 | Executor |
| `design-skills` | 디자인 도메인 Skill | 8 | Executor |
| `dev-skills` | 개발 도메인 Skill | 16 | Executor |
| `marketing-skills` | 마케팅 도메인 Skill | 8 | Executor |
| `qa-skills` | QA 도메인 Skill | 8 | Executor |
| `security-check` | 보안 검증 도구 | 5 | Validator |
| `graph-db` | Neo4j 확산 활성화 + 가중치 | 6 | Router + Validator |
| `vector-db` | pgvector 의미 검색 + 로그 | 3 | Router + Validator |
| `theory-knowledge` | 150개 이론/논문 지식 | 4 | Router + Executor |

### MCP 서버 구현 예시 (FastMCP)

```python
# planning-skills MCP Server
from mcp.server.fastmcp import FastMCP

planning = FastMCP("planning-skills")

@planning.tool()
def prd_generation(
    idea: str,
    target_market: str = "",
    tech_constraints: str = "",
    theories: str = "",       # Router가 주입한 이론
    constraints: str = ""     # Router가 주입한 제약
) -> str:
    """PRD 자동 생성. JTBD+Bloom Create 기반. 7섹션 출력."""
    return PROMPT_TEMPLATE.format(...)

@planning.tool()
def competitive_analysis(market: str, max_competitors: int = 5) -> str:
    """경쟁사 분석. Porter 5F + Bloom Analyze 기반."""
    ...

@planning.tool()
def user_persona(problem: str, target_description: str = "") -> str:
    """유저 페르소나 생성."""
    ...

# ... (problem_definition, user_story, market_sizing, 
#      feature_prioritization, sprint_decomposition, kpi_definition)
```

```python
# graph-db MCP Server — Neo4j 연동
from mcp.server.fastmcp import FastMCP
from neo4j import GraphDatabase

graph = FastMCP("graph-db")

@graph.tool()
def spread_activation(
    seed_skill_ids: list[str],
    decay: float = 0.85,
    threshold: float = 0.40,
    max_depth: int = 3
) -> dict:
    """확산 활성화 실행. seed→엣지→관련Skill 전파. DAG 반환."""
    with driver.session() as session:
        result = session.run(SPREAD_ACTIVATION_CYPHER, 
            seeds=seed_skill_ids, decay=decay, threshold=threshold)
        return format_dag(result)

@graph.tool()
def update_weights(executed_skills: list[str], success: bool) -> dict:
    """실행 결과 기반 엣지 가중치 업데이트. 성공+0.05/실패-0.05."""
    ...

@graph.tool()
def get_skill_theories(skill_id: str) -> list[dict]:
    """Skill에 연결된 이론/논문 조회. GROUNDS 엣지 순회."""
    ...

@graph.tool()
def get_dependencies(skill_id: str) -> list[dict]:
    """Skill의 선행 의존성 조회. REQUIRES 엣지."""
    ...

@graph.tool()
def create_edge(source: str, target: str, weight: float, type: str) -> dict:
    """새 엣지 생성 (자가 발전)."""
    ...

@graph.tool()
def get_co_occurrence(skill_a: str, skill_b: str) -> int:
    """두 Skill의 동시 활성화 횟수 조회."""
    ...
```

```python
# theory-knowledge MCP Server
from mcp.server.fastmcp import FastMCP

theory = FastMCP("theory-knowledge")

@theory.tool()
def get_theories_for_domain(domain: str) -> list[dict]:
    """도메인에 해당하는 이론 목록. {id, name, core_principle, application}"""
    ...

@theory.tool()
def get_theory_detail(theory_id: str) -> dict:
    """이론 상세. {id, name, authors, year, paper, journal, doi, principle, application}"""
    ...

@theory.tool()
def find_related_theories(theory_id: str) -> list[dict]:
    """관련 이론 탐색. RELATED_TO/SUPPORTED_BY 엣지."""
    ...

@theory.tool()
def recommend_unused_theories(skill_id: str) -> list[dict]:
    """아직 적용되지 않은 관련 이론 추천."""
    ...
```

---

## 9-5. Hook 알고리즘 (핵심 7개 — 실행 가능 형식)

> 모든 Hook: `ALGORITHM Name(INPUT) → OUTPUT { PROCESS + ERROR_HANDLING }`

### C1. activation-spreader (Router Model이 실행)

```
ALGORITHM ActivationSpreader(user_input: string) → ActivatedSkillDAG

  PROCESS:
    // Step 1: Seed 탐색 (Vector DB MCP)
    seeds ← CALL mcp__vector-db__semantic_search(query=user_input, top_k=3)

    // Step 2: 키워드 보완
    domains ← detect_domains_by_keywords(user_input)
    // 기획=[기획,PRD,유저,페르소나,기능], 디자인=[UI,UX,컴포넌트,레이아웃],
    // 개발=[코드,함수,API,DB,빌드], 마케팅=[카피,SEO,광고,퍼널], QA=[테스트,버그,리뷰]

    // Step 3: 블룸 레벨 추정
    bloom ← estimate_bloom(user_input)
    // "만들어줘"→Create, "검토해줘"→Evaluate, "분석해줘"→Analyze,
    // "적용해줘"→Apply, "설명해줘"→Understand, "찾아줘"→Remember

    // Step 4: 복잡도 점수 (0~10)
    score ← 0
    IF count_variables(user_input) > 7: score += 2
    IF len(domains) > 1: score += len(domains) - 1
    IF is_ambiguous(user_input): score += 1
    IF dependency_depth > 3: score += 2

    // Step 5: 모델 선택 (#5 Kahneman)
    IF score <= 3: executor_model ← "haiku"      // 단순→경량
    ELSE IF score <= 6: executor_model ← "sonnet"  // 보통→표준
    ELSE: executor_model ← "opus"                   // 복잡→최고성능

    // Step 6: 확산 활성화 (Graph DB MCP)
    spread ← CALL mcp__graph-db__spread_activation(
      seeds=seeds.skill_ids, decay=0.85, threshold=0.40, max_depth=3)

    // Step 7: 도메인별 Hook 동반 활성화
    hooks ← BASE_HOOKS  // [C1~C5, G1, G2, G4, V1, V2]
    FOR skill IN spread.activated_skills:
      IF skill.domain == "development": hooks.add([S1,S2,S4,Q4,E1,E2])
        IF "backend" IN skill.id: hooks.add([S3,S5,D1,D4,E3,E4])
        IF "frontend" IN skill.id: hooks.add([P1,P2])
        IF "database" IN skill.id: hooks.add([D2,D3])
      IF skill.domain IN ["planning","marketing"]: hooks.add([G3,G5])
      IF skill.domain == "qa": hooks.add([Q1,Q2,Q3])

    // Step 8: 이론 로드 (Theory MCP)
    theories ← CALL mcp__theory-knowledge__get_theories_for_domain(domains)
    FOR t IN theories:
      related ← CALL mcp__theory-knowledge__find_related_theories(t.id)
      theories.extend(related)

    // Step 9: DAG 구성 → C2
    dag ← CALL C2(spread.activated_skills, bloom)

    RETURN {dag, hooks, theories, executor_model, score}

  ERROR_HANDLING:
    IF vector_db TIMEOUT: fallback to keyword-based seed selection
    IF graph_db TIMEOUT: use seeds only (no spreading)
    IF no skills found: RETURN {error: "NEED_CLARIFICATION"}
```

### C5. output-validate (Validator Model이 실행)

```
ALGORITHM OutputValidate(skill, output, context) → ValidationResult

  PROCESS:
    issues ← []

    // 1. 완전성
    FOR field IN skill.output.format:
      IF field NOT IN output: issues.add(CRITICAL, "누락: {field}")

    // 2. 할루시네이션
    claims ← extract_specific_claims(output)  // 수치, 이름, 날짜
    FOR claim IN claims:
      IF claim NOT derivable_from(context):
        issues.add(CRITICAL, "입력에 없는 정보: {claim}")

    // 3. 근거 포함 (#34 구성주의 4요소)
    IF NOT contains_reasoning(output): issues.add(MEDIUM, "판단 근거 미포함")
    IF NOT contains_alternative(output): issues.add(LOW, "대안 미제시")
    IF NOT contains_uncertainty(output): issues.add(LOW, "한계/불확실성 미표시")

    // 4. 블룸 일치
    IF estimate_bloom(output) != skill.bloom_level:
      issues.add(MEDIUM, "블룸 레벨 불일치")

    // 5. 밀러 준수
    IF count_sections(output) > 9: issues.add(LOW, "항목 9개 초과")

    // 6. 충돌 감지
    contradictions ← find_contradictions(output, previous_outputs)
    FOR c IN contradictions: issues.add(HIGH, c)

    // 판정
    critical ← count(issues, CRITICAL)
    score ← 10 - (critical * 3) - (count(issues, HIGH) * 2) - (len(issues) * 0.5)
    passed ← (critical == 0 AND score >= 6)

    IF NOT passed:
      IF retry_count < 2: RETURN RETRY with issues
      ELSE IF decomposable: RETURN DECOMPOSE
      ELSE: RETURN ESCALATE to user

    RETURN {passed: TRUE, score, issues}
```

### S2. owasp-scanner (Validator Model이 실행)

```
ALGORITHM OWASPScanner(code_output, skill) → SecurityReport

  PROCESS:
    vulns ← []

    // A01: Broken Access Control
    IF NOT has_auth_check(code): vulns.add(CRITICAL, "인증 없는 엔드포인트")
    IF NOT has_rls(code) AND "database" IN skill: vulns.add(HIGH, "RLS 미설정")

    // A02: Cryptographic Failures
    IF has_plaintext_secret(code): vulns.add(CRITICAL, "평문 비밀 저장")
    IF has_weak_crypto(code, [md5,sha1]): vulns.add(HIGH, "약한 해시")
    IF has_hardcoded_key(code): vulns.add(CRITICAL, "하드코딩 시크릿")

    // A03: Injection
    IF has_string_concat_sql(code): vulns.add(CRITICAL, "SQL 인젝션")
    IF NOT has_input_validation(code): vulns.add(HIGH, "입력 검증 없음")
    IF has_raw_html(code): vulns.add(HIGH, "XSS 취약")

    // A04: Insecure Design
    IF NOT has_rate_limit(code): vulns.add(HIGH, "Rate limit 없음")
    IF NOT stride_checked(skill): vulns.add(MEDIUM, "위협 모델링 미수행")

    // A05: Misconfiguration
    IF has_cors_wildcard(code): vulns.add(MEDIUM, "CORS '*'")
    IF has_verbose_error(code): vulns.add(MEDIUM, "에러에 내부정보")

    // A07: Auth Failures
    IF NOT has_password_hash(code) AND "auth" IN skill: vulns.add(CRITICAL, "미해싱")
    IF NOT has_token_expiry(code) AND "auth" IN skill: vulns.add(HIGH, "토큰 무만료")

    IF count(vulns, CRITICAL) > 0: RETURN {passed: FALSE, action: BLOCK_AND_FIX}
    RETURN {passed: TRUE, vulns}
```

### G2. mgv-monitor (Router Model이 실행)

```
ALGORITHM MGVMonitor(skill, context, dag) → Strategy

  PROCESS:
    // Phase 1: 과제 변수 평가 (#8 Flavell MKTask)
    difficulty ← dag.complexity_score
    has_input ← all(field IN context FOR field IN skill.input.required)
    prereqs_met ← all(dep.completed FOR dep IN skill.dependencies)

    // Phase 2: 전략 선택 (#5 Kahneman)
    IF difficulty <= 3 AND has_input:
      strategy ← "SYSTEM_1"; cot ← FALSE
    ELSE IF difficulty <= 6:
      strategy ← "SYSTEM_2"; cot ← TRUE
    ELSE:
      strategy ← "SYSTEM_2_EXTENDED"; cot ← TRUE; self_explain ← TRUE

    // Phase 3: 스캐폴딩 (#32 Vygotsky ZPD)
    specificity ← measure_specificity(context)
    IF specificity > 0.8: scaffolding ← "LOW"    // 구체적→바로 실행
    ELSE IF specificity > 0.4: scaffolding ← "MEDIUM"  // 확인 후 실행
    ELSE: scaffolding ← "HIGH"  // 문제 정의부터

    // Phase 4: 선행 조건
    IF NOT has_input: RETURN BLOCKED("입력 부족", missing_fields)
    IF NOT prereqs_met: RETURN BLOCKED("선행 Skill 미완료", pending_skills)

    RETURN {strategy, cot, self_explain, scaffolding}
```

### V1. weight-updater (Validator Model이 실행)

```
ALGORITHM WeightUpdater(executed_skills, success) → UpdateResult

  PROCESS:
    // 가중치 조정 (#21 Collins & Loftus + #145 Bayes)
    FOR pair IN all_pairs(executed_skills):
      edge ← CALL mcp__graph-db__get_edge(pair.a, pair.b)
      IF edge EXISTS:
        IF success: new_w ← min(edge.weight + 0.05, 1.0)
        ELSE: new_w ← max(edge.weight - 0.05, 0.10)
        CALL mcp__graph-db__update_edge(pair.a, pair.b, new_w)
      ELSE IF success:
        co ← CALL mcp__graph-db__get_co_occurrence(pair.a, pair.b)
        IF co >= 3:
          CALL mcp__graph-db__create_edge(pair.a, pair.b, 0.40, "DISCOVERED")

    // 로그 저장
    CALL mcp__vector-db__log_execution(executed_skills, success)

    // 미사용 감쇠 (매일 1회)
    IF is_daily_decay():
      stale ← CALL mcp__graph-db__get_stale_edges(days=30)
      FOR e IN stale:
        CALL mcp__graph-db__update_edge(e.src, e.tgt, max(e.weight*0.95, 0.10))
```

---

## 9-6. 실행 흐름 전체 시퀀스

```
[사용자] "쇼핑몰 리뷰 자동 답변 SaaS 만들어줘"
    │
    ▼
[Router Model (Haiku)]
    ├─ C1: mcp__vector-db__semantic_search → seeds 3개
    ├─ C1: mcp__graph-db__spread_activation → 9개 Skill 활성화
    ├─ C1: 복잡도=8 → executor_model="opus"
    ├─ C1: mcp__theory-knowledge → 이론 20개 로드
    ├─ C2: 블룸 순서 DAG 구성 (6 Layer)
    ├─ C3: 각 Layer별 컨텍스트 정리 (7개 이내)
    ├─ G1: 도메인별 스키마 준비
    ├─ G2: 전략=SYSTEM_2, scaffolding=LOW
    └─ G3: 편향 사전 감지 → "실패 사례도 분석" 제약 추가
    │
    ▼ DAG + 컨텍스트 + 이론 + 제약 전달
[Executor Model (Opus)]
    ├─ Layer 0: mcp__planning__competitive_analysis ∥ problem_definition
    ├─ Layer 1: mcp__planning__user_persona ∥ feature_prioritization
    ├─ Layer 2: mcp__planning__prd_generation
    ├─ Layer 3: mcp__design__wireframe ∥ ui_component
    ├─ Layer 4: mcp__dev__backend_api ∥ backend_auth
    │   [DURING] Router: C4(부하감시) + S1(보안레이어) + D1(데이터무결성)
    └─ Layer 5: mcp__marketing__copy
    │
    ▼ 전체 출력 전달
[Validator Model (Haiku)]
    ├─ C5: 완전성/할루시네이션/블룸/밀러/충돌 검증
    ├─ G4: 자기설명/확신도/대안 검증
    ├─ G5: 확증편향/더닝크루거/계획오류 사후 감지
    ├─ S2: OWASP 스캔 (Layer 4 코드)
    ├─ S3: STRIDE 위협 모델링
    ├─ S4: 최소 권한 감사 (Saltzer 8원칙)
    ├─ Q4: 테스트 동반 강제
    ├─ P1/P2: 성능 예산 체크
    │
    ├─ 판정: PASS → 사용자에게 출력
    │   or FAIL → Executor에 수정 지시 + 재실행 (최대 2회)
    │   or CRITICAL → 차단 + 보고
    │
    ├─ V1: mcp__graph-db__update_weights (가중치 학습)
    └─ V2: mcp__graph-db 패턴 저장 (자가 발전)
```

---

## 9-7. 비용/성능 최적화

| 항목 | Router (Haiku) | Executor (Sonnet/Opus) | Validator (Haiku) |
|------|---------------|----------------------|-------------------|
| 호출 빈도 | 매 요청 1회 | 매 요청 N회 (Layer 수) | 매 요청 1회 |
| 토큰 사용 | 적음 (~500) | 많음 (~2000/Skill) | 적음 (~800) |
| 비용 비중 | ~5% | ~85% | ~10% |
| 지연 | ~200ms | ~2-5s/Skill | ~300ms |

**최적화 규칙:**
```
IF complexity <= 3:
  // 단순 작업 → Executor도 Haiku 사용 (비용 절약)
  executor_model ← "haiku"
  skip_validator ← FALSE  // 검증은 항상

IF complexity <= 6:
  // 보통 작업 → Sonnet
  executor_model ← "sonnet"

IF complexity >= 7:
  // 복잡 작업 → Opus
  executor_model ← "opus"
  // Validator도 Sonnet으로 승격 (복잡한 출력 검증)
  validator_model ← "sonnet"
```

---

## 9-8. 기존 마스터 문서 PART와의 관계

| 기존 PART | 이 섹션에서의 전환 |
|----------|----------------|
| PART 3 (Skill 아키텍처) | Skill = MCP 서버의 tool로 외부화 |
| PART 4 (35개 Hook) | Hook = 알고리즘으로 전환, Router/Validator가 실행 |
| PART 5 (Graph RAG DB) | graph-db MCP 서버로 접근 |
| PART 6 (데이터 축적) | vector-db MCP + graph-db MCP로 자동화 |
| PART 7 (프로세스 매핑) | Router가 자동 판단 → 해당 MCP 서버 호출 |

---

# PART 10: 구현 로드맵

# PART 10: 구현 로드맵 (멀티모델 + MCP 반영)

| 주차 | 작업 | 결과물 |
|------|------|--------|
| 1 | Neo4j + pgvector 세팅, 54개 Skill + 150 Theory 노드 + 초기 엣지 | 기본 지식 그래프 |
| 1 | graph-db MCP + vector-db MCP + theory-knowledge MCP 서버 구축 | 인프라 MCP 3개 |
| 2 | planning-skills MCP + design-skills MCP 서버 구축 | 기획+디자인 Skill MCP |
| 2 | Router Model 시스템 프롬프트 + C1/C2/C3/G2 알고리즘 구현 | 라우팅 엔진 |
| 3 | dev-skills MCP 서버 구축 (frontend + backend + infra + shared) | 개발 Skill MCP |
| 3 | Validator Model + C5/G4/G5/S2/Q4 알고리즘 구현 | 검증 엔진 |
| 4 | marketing-skills MCP + qa-skills MCP + security-check MCP | 나머지 도메인 MCP |
| 4 | 전체 파이프라인 통합 테스트 (Router→Executor→Validator 순환) | E2E 동작 |
| 5 | V1/V2 자가 발전 알고리즘 + 실행 로그 파이프라인 | 자가 발전 시작 |
| 5 | 첫 실전 프로젝트 (SaaS MVP) | 데이터 축적 시작 |
| 6+ | 나머지 Hook 알고리즘 구현 + 성능 최적화 + 비용 최적화 | 고도화 |

---

# PART 11: Atomic Skill 분해 + 외부 Hook 엔진 아키텍처

> **핵심 전환:**
> 1. Skill = 거대한 시스템 프롬프트 → **최소 단위(Atomic) 프롬프트 조각**으로 분해
> 2. Hook = Claude 내부 실행 → **외부 서버에서 실행**, 결과만 Claude에 주입
> 3. Claude는 **조립된 컨텍스트만 받아서 실행**에만 집중

---

## 11-1. Atomic Skill 설계 원칙

### 왜 쪼개는가

```
기존: dev.backend.api (하나의 거대 Skill = ~800토큰)
  → 인증 불필요한 공개 API에도 보안 규칙 전체가 주입됨
  → 토큰 낭비 + 불필요한 제약이 오히려 출력 품질 저하

전환: dev.backend.api를 관심사별로 분해
  → 필요한 조각만 조립 → 컨텍스트 최소화 → 집중도 향상
```

### 분해 기준: 관심사(Concern) 단위

하나의 Atomic Skill은 **하나의 명확한 관심사**만 다룬다.

| 기준 | 설명 | 예시 |
|------|------|------|
| 단일 관심사 | 하나의 주제/규칙 세트만 포함 | "API 인증 규칙"은 인증만, 정규화는 별도 |
| 자기 완결적 | 다른 조각 없이도 의미가 통함 | "Zod 입력 검증 패턴"만 읽어도 적용 가능 |
| 조합 가능 | 다른 조각과 충돌 없이 합칠 수 있음 | "REST 규칙" + "보안 규칙" 동시 주입 가능 |
| 적정 크기 | 100~400토큰 | 너무 작으면(10토큰) 관리 폭발, 너무 크면(1000+) 기존과 동일 |

---

## 11-2. Atomic Skill 분해 예시

### 기존 `dev.backend.api` → 7개 Atomic Skill로 분해

```
기존 (1개, ~800토큰):
  dev.backend.api = 역할 + 학문적 기반 + 기술 스택 + 보안 규칙 + 출력 형식 + 자기 검증

분해 후 (7개, 각 100~300토큰):
  dev.backend.api.role          — 역할 정의 + 출력 형식
  dev.backend.api.rest          — REST 6원칙 (Fielding)
  dev.backend.api.validation    — Zod 입력 검증 패턴
  dev.backend.api.auth          — 인증/인가 규칙 (JWT, RLS)
  dev.backend.api.error         — 에러 핸들링 + HTTP 상태코드
  dev.backend.api.security      — OWASP 방어 (인젝션, XSS, CORS)
  dev.backend.api.verify        — 자기 검증 체크리스트
```

### 분해된 Atomic Skill 실제 내용

```yaml
# dev.backend.api.role (120토큰)
id: "dev.backend.api.role"
domain: "development.backend"
type: "role"      # role | rule | pattern | verify
content: |
  당신은 시니어 백엔드 엔지니어입니다.
  기술 스택: Next.js API Routes 또는 Supabase Edge Functions.
  출력: API 코드 + Zod 스키마 + 에러 응답 형식 + cURL 예시.
  TypeScript strict mode 필수.
tags: ["backend", "api", "role"]
token_estimate: 120
```

```yaml
# dev.backend.api.rest (180토큰)
id: "dev.backend.api.rest"
domain: "development.backend"
type: "rule"
theory: "#101 REST (Fielding, 2000)"
content: |
  REST 원칙 준수:
  - 리소스 기반 URL: /users/{id} (동사 금지)
  - HTTP 메서드: GET(조회) POST(생성) PUT(전체수정) PATCH(부분수정) DELETE(삭제)
  - 무상태: 서버에 세션 저장 금지, 매 요청에 인증 토큰 포함
  - 적절한 상태코드: 200/201/204/400/401/403/404/409/422/500
  - 일관된 응답 형식: { data, error, meta }
tags: ["backend", "api", "rest", "architecture"]
token_estimate: 180
```

```yaml
# dev.backend.api.validation (150토큰)
id: "dev.backend.api.validation"
domain: "development.backend"
type: "pattern"
theory: "#72 SOLID.D — 방어적 프로그래밍"
content: |
  모든 외부 입력은 Zod로 검증. 예외 없음.
  - 요청 body → z.object({...}).parse(req.body)
  - 쿼리 파라미터 → z.string().uuid() 등 타입별 검증
  - 검증 실패 → 422 + { error: { field, message } }
  - 절대 금지: any 타입, 검증 없는 직접 사용, req.body 그대로 DB 전달
tags: ["backend", "api", "validation", "zod", "security"]
token_estimate: 150
```

```yaml
# dev.backend.api.auth (200토큰)
id: "dev.backend.api.auth"
domain: "development.backend"
type: "rule"
theory: "#115 Saltzer 최소권한, #116 OWASP A07"
content: |
  인증/인가 규칙:
  - 모든 비공개 엔드포인트: JWT 검증 필수 (Supabase Auth 또는 커스텀)
  - 토큰 위치: Authorization: Bearer {token} (쿠키 사용 시 httpOnly+secure+sameSite)
  - 인가: RLS(Row Level Security) 우선, 불가 시 미들웨어에서 role 체크
  - 토큰 만료: access 15분 / refresh 7일 / 절대 로컬스토리지 저장 금지
  - 공개 엔드포인트는 명시적으로 // PUBLIC 주석 표기
tags: ["backend", "api", "auth", "jwt", "security"]
token_estimate: 200
```

```yaml
# dev.backend.api.error (150토큰)
id: "dev.backend.api.error"
domain: "development.backend"
type: "pattern"
content: |
  에러 핸들링 패턴:
  - 모든 핸들러를 try-catch로 래핑
  - 에러 응답 형식 통일: { error: { code, message, details? } }
  - 사용자 에러(4xx): 구체적 메시지 / 서버 에러(5xx): 일반 메시지 + 내부 로깅
  - 에러 코드 일관성: AUTH_REQUIRED, FORBIDDEN, NOT_FOUND, VALIDATION_ERROR, INTERNAL
  - 절대 금지: 스택 트레이스 노출, 빈 catch 블록, 에러 무시
tags: ["backend", "api", "error-handling"]
token_estimate: 150
```

```yaml
# dev.backend.api.security (200토큰)
id: "dev.backend.api.security"
domain: "development.backend"
type: "rule"
theory: "#116 OWASP Top 10"
content: |
  보안 필수 규칙:
  - SQL 인젝션: parameterized query만 사용 (문자열 연결 절대 금지)
  - XSS: 출력 이스케이핑, Content-Type 헤더 명시
  - CORS: 허용 origin 명시적 나열 (와일드카드 금지, 개발환경 제외)
  - Rate Limiting: 인증 엔드포인트 분당 10회, 일반 분당 100회
  - 민감 정보: 비밀번호/토큰/카드번호 로깅 절대 금지
  - 환경변수: process.env로만 접근, 하드코딩 금지
tags: ["backend", "api", "security", "owasp"]
token_estimate: 200
```

```yaml
# dev.backend.api.verify (120토큰)
id: "dev.backend.api.verify"
domain: "development.backend"
type: "verify"
theory: "#8 Flavell MGV"
content: |
  자기 검증 체크리스트:
  - [ ] 모든 입력이 Zod로 검증되는가?
  - [ ] 적절한 HTTP 상태코드를 사용하는가?
  - [ ] 인증 없는 엔드포인트가 의도적인가?
  - [ ] SQL 인젝션 가능 경로가 없는가?
  - [ ] 에러 응답이 일관된 형식인가?
  - [ ] 환경변수가 하드코딩되지 않았는가?
tags: ["backend", "api", "verification", "checklist"]
token_estimate: 120
```

### 전체 도메인 분해 맵

```
planning (기존 9개 Skill → 27개 Atomic)
├── planning.prd
│   ├── .role          — PM 역할 + 출력 7섹션 구조
│   ├── .jtbd          — JTBD 프레임워크 규칙
│   ├── .mvp           — MVP 기능 제한 (5개 이내, ICE 점수)
│   ├── .verify        — 자기 검증 체크리스트
│   └── .anti-halluc   — 검증불가 주장 태깅 규칙
├── planning.competitive-analysis
│   ├── .role          — 분석가 역할 + 출력 구조
│   ├── .porter        — Porter 5 Forces 프레임
│   ├── .positioning   — 포지셔닝 맵 작성 규칙
│   └── .verify        — 추론/사실 구분 규칙
├── planning.user-persona
│   ├── .role          — 페르소나 구조 (인구+행동+니즈)
│   └── .verify
└── ... (user-story, market-sizing, feature-prioritization, sprint, kpi)

design (기존 8개 → 24개 Atomic)
├── design.ui-component
│   ├── .role          — UI 엔지니어 역할 + TSX 출력
│   ├── .gestalt       — 게슈탈트 원리 (근접/유사/폐쇄)
│   ├── .accessibility — WCAG 2.1 AA + CTA 44px + 대비 4.5:1
│   ├── .responsive    — 모바일 퍼스트 + 브레이크포인트
│   ├── .stack         — React + Tailwind + shadcn/ui 제약
│   └── .verify
├── design.wireframe
│   ├── .role
│   ├── .layout        — 레이아웃 패턴 (Z/F/그리드)
│   └── .verify
└── ...

development (기존 16개 → 56개 Atomic)
├── dev.backend.api (위 7개 예시)
├── dev.backend.auth
│   ├── .role
│   ├── .jwt           — JWT 구현 패턴
│   ├── .rls           — Supabase RLS 패턴
│   ├── .session       — 세션 관리 규칙
│   └── .verify
├── dev.backend.database
│   ├── .role
│   ├── .schema        — 스키마 설계 규칙 (3NF)
│   ├── .migration     — 마이그레이션 패턴
│   ├── .query         — 쿼리 최적화 규칙
│   └── .verify
├── dev.frontend.component (4개)
├── dev.frontend.page (4개)
├── dev.frontend.hook (3개)
├── dev.frontend.state (3개)
├── dev.infra.deploy (4개)
├── dev.infra.ci (3개)
└── dev.shared.types (2개)

marketing (기존 8개 → 24개 Atomic)
├── marketing.copy
│   ├── .role
│   ├── .aida          — AIDA 프레임
│   ├── .elm           — 관여도별 분기 (중심/주변 경로)
│   ├── .cta           — CTA 작성 규칙
│   ├── .anti-halluc   — 과장/검증불가 차단
│   └── .verify
└── ...

qa (기존 8개 → 20개 Atomic)
├── qa.code-review
│   ├── .role
│   ├── .priority      — 심각도 기준 (Critical→Info)
│   ├── .security      — OWASP 관점 리뷰
│   ├── .output        — 이슈 리스트 + 품질 점수 형식
│   └── .verify
└── ...
```

**총계: 기존 49개 Skill → 약 151개 Atomic Skill**
**평균 토큰: 150~200토큰/조각, 일반적 요청에 5~8개 조합 = 750~1,600토큰**

---

## 11-3. Atomic Skill 저장소 — MCP 서버 설계

### 단일 MCP 서버: `skill-store`

기존 9개 도메인별 MCP를 **1개 skill-store MCP로 통합**한다.
Atomic Skill은 결국 YAML/JSON 데이터이므로 도메인별 서버 분리가 불필요하다.

```python
# skill-store MCP Server
from mcp.server.fastmcp import FastMCP
import yaml
from pathlib import Path

store = FastMCP("skill-store")

# Atomic Skill 파일들은 /skills 디렉토리에 YAML로 저장
SKILL_DIR = Path("./skills")

def load_skill(skill_id: str) -> dict:
    """YAML 파일에서 Atomic Skill 로드"""
    parts = skill_id.split(".")
    # dev.backend.api.auth → skills/dev/backend/api/auth.yaml
    path = SKILL_DIR / "/".join(parts[:-1]) / f"{parts[-1]}.yaml"
    if not path.exists():
        return None
    return yaml.safe_load(path.read_text())

@store.tool()
def get_skill(skill_id: str) -> dict:
    """단일 Atomic Skill 조회.
    예: get_skill('dev.backend.api.auth')
    → { id, domain, type, theory, content, tags, token_estimate }
    """
    skill = load_skill(skill_id)
    if not skill:
        return {"error": f"Skill not found: {skill_id}"}
    return skill

@store.tool()
def get_skills_batch(skill_ids: list[str]) -> list[dict]:
    """여러 Atomic Skill 일괄 조회. Hook 엔진이 결정한 목록을 한 번에 가져온다.
    예: get_skills_batch(['dev.backend.api.role', 'dev.backend.api.rest', 'dev.backend.api.auth'])
    """
    results = []
    for sid in skill_ids:
        skill = load_skill(sid)
        if skill:
            results.append(skill)
    return results

@store.tool()
def search_skills(
    domain: str = "",
    tags: list[str] = [],
    type: str = ""
) -> list[dict]:
    """조건 기반 Atomic Skill 검색. 태그, 도메인, 타입으로 필터.
    예: search_skills(domain='development.backend', tags=['security'])
    → 해당 조건에 맞는 Skill 목록 (content 제외, id+tags+token_estimate만)
    """
    results = []
    for path in SKILL_DIR.rglob("*.yaml"):
        skill = yaml.safe_load(path.read_text())
        if domain and not skill.get("domain", "").startswith(domain):
            continue
        if type and skill.get("type") != type:
            continue
        if tags and not set(tags).intersection(set(skill.get("tags", []))):
            continue
        results.append({
            "id": skill["id"],
            "domain": skill.get("domain"),
            "type": skill.get("type"),
            "tags": skill.get("tags", []),
            "token_estimate": skill.get("token_estimate", 0)
        })
    return results

@store.tool()
def assemble_prompt(skill_ids: list[str]) -> str:
    """Atomic Skill들을 하나의 시스템 프롬프트로 조립.
    Hook 엔진이 결정한 skill_ids를 받아 최종 프롬프트 문자열을 반환.
    """
    sections = []
    total_tokens = 0

    for sid in skill_ids:
        skill = load_skill(sid)
        if not skill:
            continue
        content = skill["content"]
        total_tokens += skill.get("token_estimate", len(content) // 4)

        # type별 섹션 구분
        if skill["type"] == "role":
            sections.insert(0, content)  # role은 항상 최상단
        elif skill["type"] == "verify":
            sections.append(f"## 자기 검증\n{content}")  # verify는 항상 최하단
        elif skill["type"] == "rule":
            sections.append(f"## 규칙: {skill.get('theory', '')}\n{content}")
        elif skill["type"] == "pattern":
            sections.append(f"## 패턴\n{content}")

    assembled = "\n\n".join(sections)

    return {
        "prompt": assembled,
        "total_tokens": total_tokens,
        "skill_count": len(skill_ids)
    }
```

### 디렉토리 구조

```
skills/
├── planning/
│   ├── prd/
│   │   ├── role.yaml
│   │   ├── jtbd.yaml
│   │   ├── mvp.yaml
│   │   ├── verify.yaml
│   │   └── anti-halluc.yaml
│   ├── competitive-analysis/
│   │   ├── role.yaml
│   │   ├── porter.yaml
│   │   └── ...
│   └── ...
├── design/
│   ├── ui-component/
│   │   ├── role.yaml
│   │   ├── gestalt.yaml
│   │   ├── accessibility.yaml
│   │   └── ...
│   └── ...
├── dev/
│   ├── backend/
│   │   ├── api/
│   │   │   ├── role.yaml
│   │   │   ├── rest.yaml
│   │   │   ├── validation.yaml
│   │   │   ├── auth.yaml
│   │   │   ├── error.yaml
│   │   │   ├── security.yaml
│   │   │   └── verify.yaml
│   │   ├── auth/
│   │   ├── database/
│   │   └── ...
│   ├── frontend/
│   └── infra/
├── marketing/
│   ├── copy/
│   └── ...
└── qa/
    ├── code-review/
    └── ...
```

---

## 11-4. 외부 Hook 엔진 설계

### 핵심 원칙

```
Hook = Claude 외부에서 실행되는 판단 로직
     = 분류(Haiku 1회) + 규칙 기반 선택(코드) + 템플릿 조립(코드)
     = 입력(요구사항) → 출력(Atomic Skill ID 목록 + 검증 체크리스트)
```

Hook 로직은 **2단계 하이브리드**이다.
- Phase 1 분류: **Haiku 1회 호출** (키워드 매칭은 오분류가 많으므로 LLM 분류 사용, 비용 ~0.001원)
- Phase 2~3 선택/조립: **확정적 코드** (규칙 분기, DB 조회, 템플릿)

### 아키텍처

```
[사용자 요구사항]
      │
      ▼
┌─────────────────────────────────────────────────────┐
│  HOOK ENGINE (Node.js / Python 서버)                  │
│                                                      │
│  Phase 1: 분류 — Haiku 1회 호출                       │
│  ├─ 도메인 분류 (복수 가능)                             │
│  ├─ 블룸 레벨 추정                                    │
│  ├─ 복잡도 점수 산정                                   │
│  ├─ 의미적 키워드 추출 (auth, payment 등)               │
│  └─ 후속 요청 여부 판단 (세션 연속성)                    │
│                                                      │
│  Phase 2: Skill 선택 — 확정적 코드                     │
│  ├─ 도메인 → 기본 Atomic Skill 세트                    │
│  ├─ 추출된 키워드 → 조건부 Atomic Skill                 │
│  └─ 복잡도 → 검증 Skill 추가 여부                      │
│                                                      │
│  Phase 3: 검증 규칙 + 프롬프트 조립 — 확정적 코드        │
│  ├─ 도메인별 POST 체크리스트 생성                       │
│  └─ 템플릿 기반 프롬프트 조립 (섹션별 구조화)             │
│                                                      │
│  출력: SkillAssemblyPlan + 조립된 시스템 프롬프트         │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  CLAUDE (Executor)                                   │
│  시스템 프롬프트 = 템플릿으로 조립된 자연스러운 프롬프트    │
│  사용자 메시지 = 원본 요구사항 (+ 세션 컨텍스트)          │
│  → 실행에만 집중                                       │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│  POST VALIDATOR (Hook Engine에서 실행)                 │
│  Phase 3에서 생성한 체크리스트로 출력 검증                │
│  PASS → 사용자에게 반환                                │
│  FAIL → Claude 재호출 (체크리스트 + 실패 사유 첨부)      │
└─────────────────────────────────────────────────────┘
```

### Hook Engine 구현

```python
# hook_engine.py — 외부 Hook 서버
import json
import anthropic
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

client = anthropic.Anthropic()

class BloomLevel(Enum):
    REMEMBER = 1
    UNDERSTAND = 2
    APPLY = 3
    ANALYZE = 4
    EVALUATE = 5
    CREATE = 6

@dataclass
class SkillAssemblyPlan:
    """Hook 엔진의 최종 출력. 이것이 MCP와 Claude에 전달된다."""
    skill_ids: list[str]           # 조립할 Atomic Skill ID 목록
    post_checks: list[str]         # POST 검증 체크리스트
    domains: list[str]             # 감지된 도메인 (복수)
    bloom_level: BloomLevel        # 추정 블룸 레벨
    complexity: int                # 복잡도 점수 (0~10)
    executor_model: str            # 사용할 모델 (haiku/sonnet/opus)
    token_budget: int              # 예상 토큰 소비
    assembled_prompt: str          # 템플릿으로 조립된 최종 시스템 프롬프트
    is_followup: bool              # 이전 대화의 후속 요청인가
    warnings: list[str] = field(default_factory=list)

# ─── 세션 관리 ───

@dataclass
class Session:
    """대화 세션. 연속 요청 시 컨텍스트를 유지한다."""
    session_id: str
    history: list[SkillAssemblyPlan] = field(default_factory=list)
    active_domains: list[str] = field(default_factory=list)
    previous_outputs: list[str] = field(default_factory=list)
    accumulated_skills: list[str] = field(default_factory=list)

# 세션 저장소 (실제 구현에서는 Redis 등 사용)
_sessions: dict[str, Session] = {}

def get_or_create_session(session_id: str) -> Session:
    if session_id not in _sessions:
        _sessions[session_id] = Session(session_id=session_id)
    return _sessions[session_id]

# ═══════════════════════════════════════════════════
# Phase 1: Haiku 분류 (LLM 1회 호출)
# ═══════════════════════════════════════════════════

CLASSIFY_PROMPT = """다음 요구사항을 분석하세요.

## 요구사항
{user_input}

## 이전 대화 컨텍스트 (있을 경우)
{session_context}

## 분류 기준

도메인 목록 (복수 선택 가능):
- planning: 기획, PRD, 요구사항 정의, 유저 리서치
- design: UI/UX, 와이어프레임, 디자인 시스템
- development.frontend: 프론트엔드, React/Next.js 컴포넌트, 페이지
- development.backend: API, 서버, 인증, 미들웨어
- development.database: DB 스키마, 쿼리, 마이그레이션
- development.infra: 배포, CI/CD, 모니터링
- marketing: 카피, SEO, 광고, 랜딩페이지
- qa: 테스트, 코드 리뷰, 버그 분석

블룸 레벨:
- REMEMBER: 정보 조회/나열
- UNDERSTAND: 설명/요약/정리
- APPLY: 기존 패턴 적용
- ANALYZE: 구조 분석/원인 파악
- EVALUATE: 비교/평가/리뷰
- CREATE: 새로 생성/구현

## JSON으로만 응답하세요. 다른 텍스트 없이.
{{
  "domains": ["도메인1", "도메인2"],
  "bloom": "CREATE",
  "complexity": 0-10,
  "semantic_keywords": ["auth", "payment", ...],
  "is_followup": false,
  "reasoning": "분류 근거 1줄"
}}"""

async def classify_with_haiku(
    user_input: str,
    session: Session
) -> dict:
    """Haiku 1회 호출로 도메인/블룸/복잡도/키워드 분류.
    비용: ~0.001원, 레이턴시: ~200ms"""

    # 세션 컨텍스트 구성
    session_context = "없음"
    if session.active_domains:
        session_context = (
            f"활성 도메인: {session.active_domains}, "
            f"이전 Skill: {session.accumulated_skills[-5:]}"  # 최근 5개만
        )

    prompt = CLASSIFY_PROMPT.format(
        user_input=user_input,
        session_context=session_context,
    )

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    # JSON 파싱
    text = response.content[0].text
    # JSON 블록만 추출 (```json ... ``` 또는 순수 JSON)
    if "```" in text:
        text = text.split("```json")[-1].split("```")[0]
    result = json.loads(text.strip())

    return {
        "domains": result["domains"],
        "bloom": BloomLevel[result["bloom"]],
        "complexity": min(int(result["complexity"]), 10),
        "semantic_keywords": result.get("semantic_keywords", []),
        "is_followup": result.get("is_followup", False),
    }

# ═══════════════════════════════════════════════════
# Phase 2: Skill 선택 (확정적 코드)
# ═══════════════════════════════════════════════════

# 도메인 → 기본 Atomic Skill 매핑
BASE_SKILLS = {
    "development.backend": [
        "dev.backend.api.role",
        "dev.backend.api.rest",
        "dev.backend.api.validation",
        "dev.backend.api.error",
        "dev.backend.api.verify",
    ],
    "development.frontend": [
        "dev.frontend.component.role",
        "dev.frontend.component.solid",
        "dev.frontend.component.stack",
        "dev.frontend.component.verify",
    ],
    "development.database": [
        "dev.backend.database.role",
        "dev.backend.database.schema",
        "dev.backend.database.query",
        "dev.backend.database.verify",
    ],
    "development.infra": [
        "dev.infra.deploy.role",
        "dev.infra.deploy.docker",
        "dev.infra.deploy.env",
        "dev.infra.deploy.verify",
    ],
    "planning": [
        "planning.prd.role",
        "planning.prd.jtbd",
        "planning.prd.mvp",
        "planning.prd.verify",
        "planning.prd.anti-halluc",
    ],
    "design": [
        "design.ui-component.role",
        "design.ui-component.gestalt",
        "design.ui-component.responsive",
        "design.ui-component.stack",
        "design.ui-component.verify",
    ],
    "marketing": [
        "marketing.copy.role",
        "marketing.copy.aida",
        "marketing.copy.cta",
        "marketing.copy.verify",
    ],
    "qa": [
        "qa.code-review.role",
        "qa.code-review.priority",
        "qa.code-review.output",
        "qa.code-review.verify",
    ],
}

# 의미 키워드 → 추가 Atomic Skill 매핑
# (Haiku가 추출한 semantic_keywords 기반 — 키워드 매칭보다 정확)
KEYWORD_SKILLS = {
    "auth": ["dev.backend.api.auth", "dev.backend.api.security"],
    "jwt": ["dev.backend.api.auth"],
    "login": ["dev.backend.api.auth", "dev.backend.api.security"],
    "payment": ["dev.backend.api.auth", "dev.backend.api.security",
                "dev.backend.database.acid"],
    "database": ["dev.backend.database.schema", "dev.backend.database.query"],
    "migration": ["dev.backend.database.migration"],
    "seo": ["marketing.copy.seo"],
    "accessibility": ["design.ui-component.accessibility"],
    "darkmode": ["design.ui-component.darkmode"],
    "performance": ["dev.frontend.component.performance"],
    "security": ["dev.backend.api.security", "dev.backend.api.auth"],
    "file-upload": ["dev.backend.api.security", "dev.backend.api.validation"],
    "realtime": ["dev.backend.api.websocket"],
    "caching": ["dev.backend.api.caching"],
    "search": ["dev.backend.database.query", "dev.backend.database.index"],
    "i18n": ["dev.frontend.component.i18n"],
    "email": ["dev.backend.api.auth", "dev.infra.deploy.env"],
}

def select_skills(
    domains: list[str],
    semantic_keywords: list[str],
    complexity: int,
    session: Session
) -> list[str]:
    """도메인 + 의미 키워드 + 복잡도 + 세션 기반 Atomic Skill 선택."""
    skills = []

    # 1. 도메인별 기본 Skill
    for domain in domains:
        skills.extend(BASE_SKILLS.get(domain, []))

    # 2. Haiku가 추출한 의미 키워드 기반 추가 Skill
    for keyword in semantic_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in KEYWORD_SKILLS:
            skills.extend(KEYWORD_SKILLS[keyword_lower])

    # 3. 복잡도 높으면 검증 Skill 보강
    if complexity >= 5:
        for domain in domains:
            if domain.startswith("development"):
                skills.append("dev.backend.api.security")
                skills.append("qa.code-review.security")

    # 4. 후속 요청이면 이전 Skill 유지 (세션 연속성)
    #    → 이전에 auth Skill을 로딩했으면, 후속 요청에서도 유지
    if session.accumulated_skills:
        # 이전 Skill 중 현재 도메인과 관련된 것만 유지
        for prev_skill in session.accumulated_skills:
            prev_domain = ".".join(prev_skill.split(".")[:2])
            for current_domain in domains:
                if current_domain.startswith(prev_domain.replace("dev.", "development.")):
                    skills.append(prev_skill)

    # 중복 제거 + 순서 유지
    seen = set()
    unique = []
    for s in skills:
        if s not in seen:
            seen.add(s)
            unique.append(s)

    return unique

# ═══════════════════════════════════════════════════
# Phase 3: POST 체크리스트 + 프롬프트 조립
# ═══════════════════════════════════════════════════

DOMAIN_POST_CHECKS = {
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
    ],
    "development.database": [
        "3NF 이상 정규화가 적용되었는가?",
        "인덱스가 적절히 설정되었는가?",
        "마이그레이션이 롤백 가능한가?",
    ],
    "planning": [
        "각 기능이 문제 정의와 직접 연결되는가?",
        "검증 불가능한 주장에 '검증 필요' 태그가 있는가?",
        "MVP 기능이 5개를 초과하지 않는가?",
    ],
    "design": [
        "CTA가 44px 이상인가?",
        "색상 대비 4.5:1 이상인가?",
        "모바일 퍼스트로 설계되었는가?",
    ],
    "marketing": [
        "3초 내 핵심을 파악할 수 있는가?",
        "CTA가 명확한가?",
        "과장/검증불가 주장이 없는가?",
    ],
}

# 의미 키워드별 추가 체크 (Haiku가 추출한 키워드 기반)
KEYWORD_POST_CHECKS = {
    "auth": [
        "OWASP Top 10 취약점이 없는가?",
        "민감 정보가 로그에 노출되지 않는가?",
        "토큰 만료 정책이 적용되었는가?",
    ],
    "payment": [
        "ACID 트랜잭션이 보장되는가?",
        "멱등성 키가 적용되었는가?",
        "PCI DSS 관련 데이터가 평문 저장되지 않는가?",
    ],
    "file-upload": [
        "파일 타입 검증이 있는가?",
        "파일 크기 제한이 있는가?",
    ],
}

def generate_post_checks(
    domains: list[str],
    semantic_keywords: list[str]
) -> list[str]:
    """도메인 + 의미 키워드 기반 POST 검증 체크리스트 생성."""
    checks = []

    for domain in domains:
        checks.extend(DOMAIN_POST_CHECKS.get(domain, []))

    for keyword in semantic_keywords:
        keyword_lower = keyword.lower()
        if keyword_lower in KEYWORD_POST_CHECKS:
            checks.extend(KEYWORD_POST_CHECKS[keyword_lower])

    return list(dict.fromkeys(checks))  # 중복 제거 + 순서 유지

# ─── 프롬프트 템플릿 조립 ───

ASSEMBLY_TEMPLATE = """{role}

## 기술 스택
{stack}

## 이 작업에서 반드시 지켜야 할 규칙
{rules}

## 출력 형식
{output_format}

## 작성 후 스스로 검증할 것
{verification}"""

def assemble_prompt_from_skills(
    skill_ids: list[str],
    skill_store  # MCP 클라이언트
) -> str:
    """Atomic Skill들을 자연스러운 프롬프트로 조립.
    YAML 이어붙이기가 아닌 템플릿 기반 섹션 구조화."""

    skills = skill_store.get_skills_batch(skill_ids)

    # type별로 분류
    role_parts = []
    stack_parts = []
    rule_parts = []
    pattern_parts = []
    verify_parts = []

    for skill in skills:
        content = skill["content"]
        skill_type = skill.get("type", "rule")

        if skill_type == "role":
            role_parts.append(content)
        elif skill_type == "stack":
            stack_parts.append(content)
        elif skill_type == "rule":
            theory = skill.get("theory", "")
            header = f"({theory})" if theory else ""
            rule_parts.append(f"### {skill['id'].split('.')[-1]} {header}\n{content}")
        elif skill_type == "pattern":
            pattern_parts.append(content)
        elif skill_type == "verify":
            verify_parts.append(content)

    # 규칙과 패턴을 하나로 합치기
    all_rules = rule_parts + pattern_parts

    prompt = ASSEMBLY_TEMPLATE.format(
        role="\n".join(role_parts) if role_parts else "당신은 시니어 풀스택 엔지니어입니다.",
        stack="\n".join(stack_parts) if stack_parts else "프로젝트 기술 스택에 맞춰 작업하세요.",
        rules="\n\n".join(all_rules) if all_rules else "일반적인 베스트 프랙티스를 따르세요.",
        output_format="요청에 맞는 형식으로 출력하세요.",
        verification="\n".join(verify_parts) if verify_parts else "출력의 정확성을 스스로 검증하세요.",
    )

    return prompt

# ═══════════════════════════════════════════════════
# 통합 실행
# ═══════════════════════════════════════════════════

async def run_hook_engine(
    user_input: str,
    session_id: str,
    skill_store  # MCP 클라이언트
) -> SkillAssemblyPlan:
    """Hook 엔진 메인. 요구사항 → SkillAssemblyPlan 반환."""

    session = get_or_create_session(session_id)

    # Phase 1: Haiku 분류 (~200ms, ~0.001원)
    classification = await classify_with_haiku(user_input, session)

    domains = classification["domains"]
    bloom = classification["bloom"]
    complexity = classification["complexity"]
    semantic_keywords = classification["semantic_keywords"]
    is_followup = classification["is_followup"]

    # 후속 요청이면 이전 도메인 유지 + 새 도메인 추가
    if is_followup and session.active_domains:
        merged = list(dict.fromkeys(session.active_domains + domains))
        domains = merged

    # 모델 선택
    if complexity <= 3:
        model = "haiku"
    elif complexity <= 6:
        model = "sonnet"
    else:
        model = "opus"

    # Phase 2: Skill 선택 (확정적 코드, <1ms)
    skill_ids = select_skills(domains, semantic_keywords, complexity, session)

    # 토큰 예산 추정
    token_budget = len(skill_ids) * 170

    # Phase 3: POST 체크리스트 + 프롬프트 조립 (확정적 코드)
    post_checks = generate_post_checks(domains, semantic_keywords)
    assembled_prompt = assemble_prompt_from_skills(skill_ids, skill_store)

    # 경고
    warnings = []
    if token_budget > 3000:
        warnings.append(f"토큰 예산 {token_budget} 초과. Skill 수 줄이기 권장.")
    if len(domains) > 3:
        warnings.append("도메인 4개 이상. 작업 분할 권장.")

    plan = SkillAssemblyPlan(
        skill_ids=skill_ids,
        post_checks=post_checks,
        domains=domains,
        bloom_level=bloom,
        complexity=complexity,
        executor_model=model,
        token_budget=token_budget,
        assembled_prompt=assembled_prompt,
        is_followup=is_followup,
        warnings=warnings,
    )

    # 세션 업데이트
    session.history.append(plan)
    session.active_domains = domains
    session.accumulated_skills = list(dict.fromkeys(
        session.accumulated_skills + skill_ids
    ))

    return plan
```

### 실행 예시 1: 단순 요청

```
입력: "유저 로그인 API 만들어줘. JWT 인증 방식으로."

Phase 1 — Haiku 분류 (~200ms, ~0.001원):
  → { domains: ["development.backend"],
      bloom: "CREATE", complexity: 2,
      semantic_keywords: ["auth", "jwt", "login"],
      is_followup: false }

Phase 2 — Skill 선택 (<1ms):
  base_skills  = [role, rest, validation, error, verify]  (5개, 도메인 기본)
  keyword_add  = [auth, security]  (semantic_keywords: "auth"+"login")
  total = 7개 Atomic Skill

Phase 3 — 조립 + 체크리스트 (<1ms):
  조립된 프롬프트:
  ┌──────────────────────────────────────────┐
  │ 당신은 시니어 백엔드 엔지니어입니다.        │
  │ 기술 스택: Next.js API Routes...          │
  │                                          │
  │ ## 이 작업에서 반드시 지켜야 할 규칙       │
  │ ### rest (REST Fielding, 2000)            │
  │ - 리소스 기반 URL...                      │
  │ ### validation                            │
  │ - Zod 검증 필수...                        │
  │ ### auth (Saltzer 최소권한)               │
  │ - JWT 검증 필수...                        │
  │ ### security (OWASP Top 10)              │
  │ - SQL 인젝션 방지...                      │
  │                                          │
  │ ## 작성 후 스스로 검증할 것               │
  │ - 모든 입력 Zod 검증?                     │
  │ - 인증 없는 엔드포인트 의도적?             │
  └──────────────────────────────────────────┘

  post_checks = [Zod 검증, SQL 인젝션, OWASP, 토큰 만료, ...]
  executor_model: "haiku" (complexity=2)
  token_budget: ~1,190

→ Claude 호출: 시스템 프롬프트 ~1,120토큰 + 사용자 메시지
→ POST 검증: Haiku가 체크리스트로 출력 검증
→ 총 비용: Haiku 3회 (분류 + 실행 + 검증) ≈ 0.01~0.03원
```

### 실행 예시 2: 후속 요청 (세션 연속성)

```
[이전 요청: "유저 로그인 API 만들어줘"]  ← 세션에 기록됨
[후속 요청: "여기에 소셜 로그인도 추가해줘"]

Phase 1 — Haiku 분류:
  세션 컨텍스트 주입: "활성 도메인: [development.backend], 이전 Skill: [role, rest, auth, ...]"
  → { domains: ["development.backend"],
      bloom: "CREATE", complexity: 3,
      semantic_keywords: ["oauth", "social-login", "auth"],
      is_followup: true }  ← Haiku가 후속 요청으로 판단

Phase 2 — Skill 선택:
  is_followup=true → 이전 도메인 유지
  base_skills = [role, rest, validation, error, verify]  (도메인 기본)
  keyword_add = [auth, security]  ("auth" 키워드)
  session_add = [auth, security]  (이전 세션에서 이미 사용 → 자동 유지)
  new_add     = [oauth]           (새 키워드 "oauth" → 소셜 로그인 Skill)
  total = 8개 (중복 제거)

→ 이전 대화에서 만든 코드 위에 소셜 로그인을 자연스럽게 추가
→ 세션 컨텍스트가 있으므로 "여기에"가 정확히 이전 출력을 가리킴
```

### 실행 예시 3: 복합 요청 (자동 분할)

```
입력: "SaaS MVP 전체 설계해줘. 기획부터 배포까지."

Phase 1 — Haiku 분류:
  → { domains: ["planning", "design", "development.frontend",
                 "development.backend", "development.infra"],
      bloom: "CREATE", complexity: 8,
      semantic_keywords: ["mvp", "fullstack", "deploy"],
      is_followup: false }

Phase 2 — Skill 선택:
  → 5개 도메인 × 4~5개 = 22개 Atomic Skill
  → 경고: "도메인 4개 이상. 작업 분할 권장."
  → token_budget = 3,740 → "토큰 예산 초과. Skill 수 줄이기 권장."

파이프라인이 자동 분할:
  Step 1: planning 도메인 (5개 Skill, ~850토큰) → Opus
  Step 2: design 도메인 (5개 Skill, ~850토큰) → Sonnet
  Step 3: dev.frontend + dev.backend (10개 Skill, ~1,700토큰) → Opus
  Step 4: dev.infra (4개 Skill, ~680토큰) → Sonnet

→ Claude 4번 순차 호출, 각 Step의 출력이 다음 Step의 컨텍스트에 포함
→ 세션에 전체 이력 기록 → 이후 "프론트엔드 수정해줘" 같은 후속 요청 가능
```

### 실행 예시 4: 키워드 없는 모호한 요청

```
입력: "유저 프로필 수정 기능 만들어줘"

기존 키워드 매칭 방식: → 매칭 실패 → 기본값 "planning" → ❌ 오분류

Haiku 분류 방식:
  → { domains: ["development.backend", "development.frontend"],
      bloom: "CREATE", complexity: 4,
      semantic_keywords: ["user-profile", "crud", "auth"],
      is_followup: false }
  → ✅ 백엔드(API) + 프론트(폼 컴포넌트) 정확히 분류
  → "auth" 키워드도 추출 (프로필 수정 = 인증 필요)
```

---

## 11-5. POST Validator 통합

POST 검증은 Hook Engine에서 **체크리스트를 생성**하고, Claude에게 **자기 검증을 요청**하는 방식이다.

```python
# post_validator.py

async def validate_output(
    output: str,
    plan: SkillAssemblyPlan,
    claude_client
) -> dict:
    """Claude 출력을 POST 검증."""

    if not plan.post_checks:
        return {"status": "PASS", "output": output}

    # 체크리스트를 Claude에게 전달하여 자기 검증
    validation_prompt = f"""다음 출력을 아래 체크리스트로 검증하세요.
각 항목에 PASS/FAIL과 사유를 적으세요.

## 출력
{output}

## 체크리스트
{chr(10).join(f'- [ ] {check}' for check in plan.post_checks)}

## 응답 형식
각 항목: [PASS/FAIL] 사유
최종 판정: PASS (전체 통과) 또는 FAIL (1개 이상 실패)
실패 시: 수정 사항 구체적 나열
"""

    result = await claude_client.messages.create(
        model="claude-haiku-4-5-20251001",  # 검증은 경량 모델
        max_tokens=1000,
        messages=[{"role": "user", "content": validation_prompt}]
    )

    validation_text = result.content[0].text

    if "최종 판정: PASS" in validation_text:
        return {"status": "PASS", "output": output}
    else:
        # FAIL → 수정 지시와 함께 재호출
        return {
            "status": "FAIL",
            "issues": validation_text,
            "action": "RETRY"  # 호출자가 수정 프롬프트로 재호출
        }
```

---

## 11-6. 전체 실행 플로우 (End-to-End)

```python
# pipeline.py — 전체 파이프라인 오케스트레이터

import anthropic
from hook_engine import run_hook_engine, get_or_create_session
from post_validator import validate_output

client = anthropic.Anthropic()

# 모델 ID 매핑
MODEL_MAP = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6-20260401",
    "opus": "claude-opus-4-6-20260401",
}

async def execute_pipeline(
    user_input: str,
    session_id: str,
    skill_store,  # MCP 클라이언트
) -> str:
    """요구사항 → Hook Engine → Claude 실행 → POST 검증.
    세션을 유지하여 연속 대화를 지원한다."""

    session = get_or_create_session(session_id)

    # 1. Hook Engine (Haiku 분류 1회 + 확정적 코드)
    plan = await run_hook_engine(user_input, session_id, skill_store)

    # 2. 토큰 초과 시 자동 분할
    if plan.token_budget > 3000 and len(plan.domains) > 1:
        return await execute_pipeline_split(user_input, session_id, plan, skill_store)

    # 3. 대화 이력 구성 (후속 요청이면 이전 출력 포함)
    messages = []
    if plan.is_followup and session.previous_outputs:
        # 이전 대화 맥락을 유지
        last_output = session.previous_outputs[-1]
        messages.append({"role": "user", "content": session.history[-2].original_input
                         if len(session.history) > 1 else ""})
        messages.append({"role": "assistant", "content": last_output})
    messages.append({"role": "user", "content": user_input})

    # 4. Claude 실행 (조립된 프롬프트 사용)
    response = client.messages.create(
        model=MODEL_MAP[plan.executor_model],
        max_tokens=4096,
        system=plan.assembled_prompt,  # 템플릿으로 조립된 자연스러운 프롬프트
        messages=messages,
    )
    output = response.content[0].text

    # 5. POST 검증
    validation = await validate_output(output, plan, client)

    if validation["status"] == "PASS":
        session.previous_outputs.append(output)
        return output

    # 6. FAIL → 수정 재시도 (최대 2회)
    for retry in range(2):
        retry_prompt = f"""이전 출력에서 다음 문제가 발견되었습니다:
{validation['issues']}

수정하여 다시 작성하세요."""

        messages_retry = messages + [
            {"role": "assistant", "content": output},
            {"role": "user", "content": retry_prompt},
        ]

        response = client.messages.create(
            model=MODEL_MAP[plan.executor_model],
            max_tokens=4096,
            system=plan.assembled_prompt,
            messages=messages_retry,
        )
        output = response.content[0].text
        validation = await validate_output(output, plan, client)

        if validation["status"] == "PASS":
            session.previous_outputs.append(output)
            return output

    # 3회 실패 → 출력 + 경고 반환
    session.previous_outputs.append(output)
    return f"{output}\n\n⚠️ 자동 검증 미통과 항목:\n{validation['issues']}"


async def execute_pipeline_split(
    user_input: str,
    session_id: str,
    plan: "SkillAssemblyPlan",
    skill_store,
) -> str:
    """복합 요청을 도메인별로 분할 실행.
    각 Step의 출력이 다음 Step의 컨텍스트에 포함된다."""

    session = get_or_create_session(session_id)
    results = []

    # 도메인 실행 순서 (기획→디자인→개발→QA→마케팅)
    DOMAIN_ORDER = [
        "planning", "design",
        "development.frontend", "development.backend", "development.database",
        "development.infra", "qa", "marketing"
    ]

    ordered_domains = [d for d in DOMAIN_ORDER if d in plan.domains]

    for domain in ordered_domains:
        # 해당 도메인의 Skill만 필터
        domain_skills = [s for s in plan.skill_ids
                         if s.startswith(domain.replace("development.", "dev."))]

        if not domain_skills:
            continue

        # 이전 Step 출력을 컨텍스트로 주입
        context = ""
        if results:
            context = "\n\n---\n이전 단계 결과 요약:\n" + "\n".join(
                f"[{r['domain']}] {r['output'][:500]}..." for r in results
            )

        domain_prompt = assemble_prompt_from_skills(domain_skills, skill_store)

        response = client.messages.create(
            model=MODEL_MAP[plan.executor_model],
            max_tokens=4096,
            system=domain_prompt,
            messages=[{"role": "user", "content": user_input + context}],
        )

        output = response.content[0].text
        results.append({"domain": domain, "output": output})

    # 전체 결과 합산
    final_output = "\n\n---\n\n".join(
        f"## {r['domain']}\n{r['output']}" for r in results
    )

    session.previous_outputs.append(final_output)
    return final_output
```

---

## 11-7. 기존 PART와의 관계

| 기존 | 변경 |
|------|------|
| PART 3 Skill 노드 (49개 거대 Skill) | → **151개 Atomic Skill로 분해**, 스키마는 간소화 (id/domain/type/content/tags) |
| PART 4 Hook 35개 (Claude 내부 실행) | → **Hook Engine 외부 서버로 이전**, Haiku 분류 1회 + 확정적 코드 |
| PART 8 Skill 시스템 프롬프트 | → **Atomic Skill YAML 파일로 대체**, 템플릿 기반 조립 |
| PART 9 멀티모델 3개 (Router+Executor+Validator) | → **Haiku(분류) + Executor(실행) + Haiku(검증)**, Router 모델을 Hook Engine 외부 코드 + Haiku 1회로 대체 |
| PART 9 MCP 9개 | → **skill-store 1개 + graph-db 1개 + vector-db 1개 = 3개로 축소** |
| 대화 연속성 없음 (1회성 파이프라인) | → **Session 객체로 세션 관리**, 후속 요청 시 도메인/Skill/출력 이력 유지 |

### 제거/흡수된 Hook

| Hook | 처리 | 이유 |
|------|------|------|
| C1 activation-spreader | → Haiku 분류 `classify_with_haiku` + `select_skills` | Haiku가 도메인/키워드 분류, 코드가 Skill 선택 |
| C2 bloom-sequencer | → Haiku 분류에서 bloom 필드 반환 | Haiku가 자연어로 블룸 레벨 추정 (키워드보다 정확) |
| C3 context-cleanup | → 템플릿 기반 `assemble_prompt_from_skills` | 필요한 조각만 조립하므로 정리 자체가 불필요 |
| C4 cognitive-load-monitor | → Hook Engine 토큰 예산 + `execute_pipeline_split` | 토큰 초과 시 도메인별 자동 분할 실행 |
| C5 output-validate | → `post_validator.py` | Haiku로 체크리스트 기반 검증 |
| G1 schema-activator | → `BASE_SKILLS` + `KEYWORD_SKILLS`에 흡수 | 도메인/키워드별 Skill이 스키마 역할 |
| G2 mgv-monitor | → Haiku 분류의 complexity 필드 | 복잡도 산정을 Haiku가 수행 |
| G3 bias-scanner | → POST 체크리스트에 편향 항목 추가 | 사후 검증으로 통합 |
| S1~S5 보안 | → Atomic Skill (.security, .auth) + `KEYWORD_POST_CHECKS["auth"]` | Skill 내용 + 키워드 기반 사후 검증 |
| Q1~Q5 품질 | → `DOMAIN_POST_CHECKS` | 도메인별 자동 체크리스트 |
| V1~V2 진화 | → 유지 (graph-db에 실행 로그 저장) | 장기적 가치, 향후 연동 |

### 3가지 핵심 개선 요약

| 문제 | 기존 (11-4 초판) | 수정 후 |
|------|-----------------|---------|
| **오분류** | 키워드 매칭 → "유저 프로필 수정" 분류 실패 | Haiku 1회 호출 → 의미 기반 분류 (비용 ~0.001원) |
| **부자연스러운 프롬프트** | YAML 조각 이어붙이기 | 템플릿 기반 섹션 구조화 (role→stack→rules→verify) |
| **대화 끊김** | 1회성 파이프라인, 매번 처음부터 | Session 객체로 도메인/Skill/출력 이력 유지 |

---

## 11-8. 수정된 구현 로드맵

| 주차 | 작업 | 결과물 |
|------|------|--------|
| 1 | Atomic Skill YAML 작성: planning 27개 + dev.backend 21개 | 핵심 도메인 Skill 48개 |
| 1 | skill-store MCP 서버 구축 (get_skill, get_skills_batch, assemble_prompt) | Skill 서빙 인프라 |
| 2 | Hook Engine 구현 (detect_domain, select_skills, generate_post_checks) | 외부 라우팅 엔진 |
| 2 | POST Validator 구현 + pipeline.py 통합 | E2E 파이프라인 동작 |
| 3 | 나머지 Atomic Skill 작성: design 24개 + dev.frontend 14개 + marketing 24개 + qa 20개 | 전체 151개 완성 |
| 3 | 첫 실전 테스트: 요구사항 10개로 파이프라인 검증 | 품질 베이스라인 측정 |
| 4 | graph-db MCP 연동 (가중치 자가 발전 V1/V2) | 학습 루프 시작 |
| 5+ | 실전 데이터 기반 Atomic Skill 튜닝 + 조건부 규칙 개선 | 점진적 고도화 |
