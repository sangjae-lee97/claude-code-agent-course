# PROGRESS — 프로젝트 진행 기록

이 파일은 **작업이 끝날 때마다 반드시 갱신**합니다.

---

## 현재 상태 요약

공식 진행 상태 (원래 STEP 01~18 기준):

```text
STEP 01 개발환경 확인                      → DONE
STEP 02 수집 데이터 명세                    → DONE
STEP 03 채용공고 페이지 접근 테스트          → DONE
STEP 04 소량 데이터 수집                    → DONE  (실데이터: 07-A)
STEP 05 DataFrame 기본 구조 확인            → DONE  (실데이터: 07-B)
STEP 06 전처리 / 중복 제거                  → DONE  (실데이터: 07-C)
STEP 07 신규 공고 판별                      → DONE  (실데이터: 07-D)
STEP 08 기본 분석 / 관련 공고 필터링         → DONE  (실데이터: 07-E ~ 07-G)
STEP 09 Gemini API 연동                    → DONE  (준비·연결 테스트: 07-H ~ 07-I, 실제 공고 요약: STEP 09 셀)
STEP 10 Gemini 결과 검증                    → DONE  (에스코어 1건, 15개 항목 비교, 불일치 0)
STEP 11 Markdown 보고서 생성                → DONE  (reports/ax_job_report.md, 3331자)
STEP 12 Slack 발송                          → NOT_STARTED
STEP 13 ~ 18                               → NOT_STARTED
```

**현재 공식 진행 위치: STEP 12 Slack 발송 (NOT_STARTED)**

STEP 11 결과 요약:

```text
- reports/ax_job_report.md 생성 (웹 요청·Gemini 호출 없음, history CSV 읽기 전용)
- 8개 장: 분석 기준 / 데이터 요약 / 필터 결과 / 주요 공고 5건 / Gemini 분석 예시 / Gemini 검증 결과 / 제한 사항 / 다음 단계
- 사실과 AI 설명 구분: [데이터 기반 사실] / [Gemini 생성 설명] / [STEP 10 검증 결과] 이름표, Gemini 문장은 인용 블록
- 집계 값은 현재 CSV로 다시 계산 → 이전 STEP 결과와 동일
```

STEP 10 결과 요약:

```text
- 검증 공고: 에스코어 / AX 컨설턴트 채용 (STEP 09에서 응답 받은 1건, GS리테일은 503으로 제외)
- 원본: data/processed/jobs_history.csv (읽기 전용), Gemini 응답: STEP 09 셀에 저장된 원문 (API 재호출 없음)
- 15개 항목: 일치 7 / 의미상 일치 3 / 검증 불가 5 / 불일치 0
- 원본과 다른 사실 없음, "확인 불가" 4개 항목 적절히 처리
- 원본 밖 해석 1건: AX 약어 풀이 "AX(AI Transformation)" → 검증 불가로 기록
- 에스코어 1건 기준 결과이며, Gemini 전체 품질로 일반화하지 않음
```

STEP 09 결과 요약:

```text
- .env 구조 준비, GEMINI_API_KEY 설정, google-genai 2.25.0 설치, 연결 테스트 성공 (07-H ~ 07-I)
- 실제 채용공고 2건(GS리테일, 에스코어)을 gemini-3.6-flash에 전달, 호출 2회
  - 에스코어: 응답 수신 (요청 형식대로, 상세 업무/기술 스택/자격요건/우대사항 → "확인 불가")
  - GS리테일: 503 UNAVAILABLE (Gemini 서버 일시 과부하) — 호출 한도 2회로 재시도하지 않음
- API Key 미노출 확인, 응답은 메모리 변수 gemini_results에만 저장 (파일 저장 없음)
```

다음 작업:

```text
STEP 12 Slack 발송

(참고) 발송할 보고서: reports/ax_job_report.md
(참고) STEP 09에서 GS리테일 공고는 503 오류로 응답을 받지 못했고, STEP 10은 에스코어 1건만 검증했다.
Notebook 작성은 항상 작업 계획(Markdown) → 실제 코드(Code) → 실행 결과 해석/분석/요약(Markdown) 3셀 패턴을 따른다.
앞으로는 07-J, 07-K처럼 세부 번호를 늘리지 않고 원래 STEP 번호(STEP 09, STEP 10 …)를 사용한다.
```

---

## STEP 진행표

| STEP | 작업 | 상태 | 완료 기준 | Notebook 근거 |
|---:|---|---|---|---|
| 00 | Git / Python / Jupyter 환경 준비 | ✅ DONE | Fork, Clone, upstream, .venv, 패키지, 커널 | — |
| 01 | 개발환경 확인 Notebook | ✅ DONE | Python/OS/import 셀 실행 성공 | STEP 01 |
| 02 | 수집 데이터 명세 | ✅ DONE | 한 행 의미와 컬럼 확정 | STEP 02 |
| 03 | 채용공고 페이지 접근 테스트 | ✅ DONE | HTTP 상태/Content-Type/응답 확인 | STEP 03 |
| 04 | 소량 데이터 수집 | ✅ DONE | 1개 → 5~10개 공고 확인 | 07-A (실데이터 5건) |
| 05 | DataFrame 기본 구조 확인 | ✅ DONE | 컬럼/shape/head/결측/중복 확인 | 07-B |
| 06 | 전처리 / 중복 제거 | ✅ DONE | 결측/중복/날짜 처리 검증 | 07-C |
| 07 | 신규 공고 판별 | ✅ DONE | 기존 vs 신규 URL 구분 | 07-D |
| 08 | 기본 분석 / 관련 공고 필터링 | ✅ DONE | 기본 통계와 필터 검증 | 07-E, 07-F, 07-G |
| 09 | Gemini API 연동 | ✅ DONE | 일부 공고 요약 성공 | 07-H, 07-I (준비·연결 테스트), STEP 09 (실제 공고 요약) |
| 10 | Gemini 결과 검증 | ✅ DONE | 원문과 AI 결과 비교 | STEP 10 (에스코어 1건) |
| 11 | Markdown 보고서 생성 | ✅ DONE | reports에 보고서 생성 | STEP 11 (`reports/ax_job_report.md`) |
| 12 | Slack 발송 | ⬜ NOT_STARTED | 실제 채널 도착 확인 | — |
| 13 | Gmail 발송 | ⬜ NOT_STARTED | 실제 메일 도착 확인 | — |
| 14 | 함수화 | ⬜ NOT_STARTED | Notebook 코드를 src로 분리 | — |
| 15 | main.py 통합 | ⬜ NOT_STARTED | 전체 순서 연결 | — |
| 16 | 로컬 전체 실행 검증 | ⬜ NOT_STARTED | `python main.py` 성공 | — |
| 17 | GitHub Actions 수동 실행 | ⬜ NOT_STARTED | Run workflow 성공 | — |
| 18 | GitHub Actions 주간 실행 | ⬜ NOT_STARTED | schedule 등록 | — |

공식 STEP 04~07의 완료 판단은 **실데이터 세부 검증(07-A ~ 07-D) 결과**를 기준으로 한다.
Notebook의 STEP 04~07 셀(샘플 데이터)은 과거 프로토타입 기록이다. (아래 "개발 과정 세부 검증 기록" 참고)

---

## 개발 과정 세부 검증 기록 (07-A ~ 07-I)

Notebook의 `STEP 07-A` ~ `STEP 07-I` 셀은 개발 과정의 상세 실험 기록이므로 **삭제하거나 이름을 바꾸지 않고 그대로 보존**한다.
원래 STEP과의 연결은 다음과 같다.

| 세부 기록 | 내용 | 연결되는 공식 STEP |
|---|---|---|
| 07-A | 실제 JobKorea 소량 크롤링 검증 | STEP 04 소량 데이터 수집 |
| 07-B | 날짜 데이터 전달 검증 (`jobs` → `df_real_jobs`) | STEP 05 DataFrame 기본 구조 확인 |
| 07-C | 실데이터 중복 확인 및 제거 (`df_unique_jobs`) | STEP 06 전처리 / 중복 제거 |
| 07-D | 신규 공고 판별 및 이력 초기화 (`jobs_history.csv`) | STEP 07 신규 공고 판별 |
| 07-E | 실데이터 기본 분석 | STEP 08 기본 분석 |
| 07-F | AX/AI 관련 공고 1차 필터링 | STEP 08 관련 공고 필터링 |
| 07-G | 키워드 필터 오탐 검증 및 개선 | STEP 08 관련 공고 필터링 |
| 07-H | Gemini API 환경변수 준비 | STEP 09 Gemini API 연동 (사전 준비) |
| 07-I | Gemini API 최소 연결 테스트 | STEP 09 Gemini API 연동 (연결 테스트) |

요약:
- 07-A ~ 07-D → 원래 STEP 04~07을 실데이터로 재검증한 세부 작업
- 07-E ~ 07-G → 원래 STEP 08 기본 분석 / 관련 공고 필터링의 세부 검증
- 07-H ~ 07-I → 원래 STEP 09 Gemini API 연동의 사전 준비 / 연결 테스트

### 과거 프로토타입 기록 — 샘플 데이터 실습 (Notebook STEP 04 ~ 07)

- 잡코리아 접속 제한(STEP 03) 때문에, 실데이터 수집 전에 직접 만든 샘플 5건(`df_jobs`)으로 파이프라인을 연습한 기록
- Notebook STEP 04(샘플 준비) → STEP 05(구조 확인) → STEP 06(전처리) → STEP 07(`previous_urls` 샘플 이력으로 신규 판별)
- 이후 같은 과정을 실데이터로 다시 검증했으므로(07-A ~ 07-D), **공식 STEP 04~07 완료 여부는 실데이터 결과로 판단**한다.
- 샘플 셀은 프로토타입 기록으로 보존하며 수정하지 않는다. 별도의 "진행 중" 상태로 관리하지 않는다.
- 실데이터 DataFrame(`df_real_jobs` 등)과 샘플 DataFrame(`df_jobs`)은 이름을 분리해 서로 덮어쓰지 않는다.

### 07-A 실제 JobKorea 소량 크롤링 검증 → STEP 04 (완료)

- 사용 URL: `https://www.jobkorea.co.kr/Search/?stext=ax&tabType=recruit` (검색어 `ax`, 1페이지, 최대 5건)
- 기본 `requests.get()` → 상태 코드 200이지만 **보안정책 페이지** (title "보안정책")
- 일반 브라우저 User-Agent 헤더로 1회만 재요청 → 실제 검색 결과 HTML 수신
  (title: `'ax' 관련 📢 채용공고 | 총 888건의 검색결과`)
- 반복 공고 블록: `div[data-sentry-component="CardJob"]` (1페이지 20개)
- HTML 카드에서 추출: `company_name`, `job_title`, `career`, `location`, `job_url`
- 날짜는 화면 카드 HTML에 없고, 같은 응답의 Next.js script JSON(`self.__next_f.push(...)`)의 공고 목록에 존재
  - `posted_date` = `applicationPeriod.start` = **지원 제출 시작일** (예: `2026-09-21`)
  - `closing_date` = `applicationPeriod.end` = **지원 제출 마감일** (예: `2026-10-01 23:00`)
  - `createdAt`(사이트 등록 시각)은 사용하지 않음
  - 카드 순서가 아니라 공고 ID(`job_url` 끝 숫자)로 JSON과 매칭
- `search_keyword`="ax", `collected_at`=수집 시각 추가 → 9개 필드
- 첫 공고(GS리테일) 날짜가 브라우저 화면 `09/21 등록 · 10/01 마감`과 일치함을 사용자가 확인

### 07-B 날짜 데이터 전달 검증 → STEP 05 (완료)

- `jobs` → `df_real_jobs` DataFrame 변환 (샘플 `df_jobs`는 덮어쓰지 않음)
- shape: **(5, 9)**, 9개 컬럼 모두 결측 **0건**
- `pd.to_datetime(errors="coerce")` 변환 실패: `posted_date` **0건**, `closing_date` **0건**
  (변환은 별도 변수로만 확인, 원본 날짜 문자열은 보존)

### 07-C 실데이터 중복 확인 및 제거 → STEP 06 (완료)

- 대상: `df_real_jobs` (실데이터 5건), 기준: `job_url`
- 범위: 현재 5건 **내부** 중복만 확인 (이전 실행 결과와 비교하지 않음)
- 실행 결과 (STEP 07-A → 07-B → 07-C 순서로 실행):
  - 중복 확인 전: **5건**, 중복 행: **0건**, 중복 제거 후: **5건**, 제거: **0건**
  - ㈜NAVER 공고 2건은 제목이 비슷하지만 `job_url`이 달라 서로 다른 공고로 판단됨
  - 원본 `df_real_jobs` 보존 확인, 중복 제거 결과는 `df_unique_jobs`(5건)에 저장

### 07-D 신규 공고 판별 및 이력 초기화 → STEP 07 (완료)

- 이력 파일: `data/processed/jobs_history.csv` (프로젝트 루트 기준, `notebooks/`에서 실행 시 상위 폴더를 루트로 계산)
  - 실행 전에는 `data/` 폴더와 history 파일이 없었음 → 이 단계에서 생성
- 기준: `job_url`이 history의 `job_url` 집합에 없으면 신규
- 1차 실행 (첫 실행): 현재 5건 / 기존 이력 0건 / 신규 **5건** / 업데이트 후 이력 **5건**
- 2차 실행 (같은 5건으로 재실행): 기존 이력 5건 / 신규 **0건** / 업데이트 후 이력 **5건** (중복 누적 없음)
- 원본 `df_real_jobs`, `df_unique_jobs` 보존 확인, `new_jobs_df` / `updated_history_df` 역할 분리
- 참고:
  - 2차 실행은 재크롤링 없이 같은 5건으로 로직만 검증함
  - history는 `keep="last"`로 저장 → 같은 공고 재수집 시 `collected_at`이 최신 시각으로 갱신됨 ("처음 발견 시각" 보존은 후속 검토)
  - 07-D 셀은 실행할 때마다 history CSV를 다시 저장함
  - `data/`는 현재 git에서 추적되지 않은 새 폴더 (`.gitignore` 대상 여부 미결정)

### 07-E 실데이터 기본 분석 → STEP 08 (완료)

- 분석 대상: `df_unique_jobs` (원본 수정 없음)
- 실행 결과 (07-A → 07-B → 07-C → 07-E 순서로 실행, **현재 5건 기준**):
  - 전체 공고: **5건**, 검색어: `ax` 5건
  - 회사별: ㈜NAVER 2 / GS리테일 1 / 에스코어 1 / ㈜슈프리마 1
  - 지역별: 경기 성남시 3 / 서울 강남구 외 1 1 / 서울 송파구 1
  - 경력별: 경력 3 / 경력3년↑ 1 / 경력7년↑ 1
  - 지원 시작일 범위: 2026-07-01 ~ 2026-09-21, 지원 마감일 범위: 2026-09-29 10:00 ~ 2026-10-25 23:00
- 신규 공고 수: 검증 실행에서는 07-D를 실행하지 않아 `new_jobs_df` 없음 → "확인하지 못했습니다" 출력
  (history 재저장 방지를 위해 07-D 제외. 신규 판별은 07-D에서 검증 완료되었으므로 완료를 막지 않음)
- 특이사항: 경력 값이 화면 문구 그대로라 `경력` / `경력3년↑` / `경력7년↑`가 별도로 집계됨,
  `서울 강남구 외 1`처럼 다중 근무지 요약 문구가 있음 → 값 정리 규칙은 후속 검토
- 표본 5건이므로 시장 전체 경향으로 해석하지 않음

### 07-F AX/AI 관련 공고 1차 필터링 → STEP 08 (완료)

- Gemini 미사용 — Python 문자열 검색만 사용
- 대상: `df_unique_jobs`의 `job_title`만 (회사명·상세 본문은 후속 검토)
- 키워드 13개: AX, AI, 인공지능, 생성형 AI, 생성형AI, LLM, Machine Learning, 머신러닝,
  Data Scientist, 데이터 사이언티스트, AI Engineer, AI 엔지니어, 데이터 분석 (소문자로 바꿔 비교)
- 실행 결과: 전체 **5건** / 통과 **5건** / 제외 **0건**, 5건 모두 `AX` 하나로만 매칭
- 결과: `df_filtered_jobs` (5행 × 10열, `matched_keywords` 컬럼은 이 복사본에만 추가), `df_unique_jobs` 보존 확인
- 해석: "1차 후보"로만 봄 — 최종 의미 판단은 Gemini 단계에서 수행
- 한계: 검색어가 `ax`라 전부 통과 → 제외되는 경우는 이 데이터로 확인하지 못함,
  단순 포함 검색이라 부분 문자열 오탐 가능성 있음 → 07-G에서 검증

### 07-G 키워드 필터 오탐 검증 및 개선 → STEP 08 (완료)

- 웹 재요청 없이 테스트 제목 12개(요청된 10개 + 한글이 바로 붙은 경우 2개)로 검증
- 새 함수 `find_matched_keywords_safe()` (07-F 함수는 수정하지 않음):
  - 영문 키워드(AX, AI, LLM, Machine Learning, Data Scientist, AI Engineer)
    → 앞뒤에 영문자·숫자가 없을 때만 매칭 (`(?<![A-Za-z0-9])키워드(?![A-Za-z0-9])`, 대소문자 무시)
  - 한글이 들어 있는 키워드 → 기존처럼 포함 검색
- 결과: 테스트 **12개 중 12개 통과, 실패 0**
  - 기존 포함 검색: Tax / Max(`AX`), Maintenance / Training(`AI`) **4건 오탐**
  - `\b` 방식: 한글이 붙은 `AX담당자`, `AI기반` **2건 누락** (Python에서는 한글도 단어 글자로 취급)
  - 개선 방식: 오탐 0, 누락 0
- 실데이터 적용 결과(`df_filtered_jobs_safe`)는 07-A → 07-B → 07-C → 07-G 순서로 실행하면 생성됨
  (history CSV 제목 5개를 읽기만 해서 확인한 결과 5건 모두 `['AX']` 매칭)
- 한계: 정규식은 직무 의미를 판단하지 않음, `OpenAI`처럼 영문자가 붙은 표현은 `AI`로 매칭되지 않음

### 07-H Gemini API 환경변수 준비 → STEP 09 사전 준비 (완료)

- Gemini API 호출 없음 — 키 보관·로딩 준비만 진행
- 새로 만든 파일 (프로젝트 루트 `chapter11/ax-job-agent/`):
  - `.gitignore`: `.env`, `.venv/`, `__pycache__/`, `.ipynb_checkpoints/` 제외
    (이전에는 저장소 전체에 `.gitignore`가 없었고, `.venv/`만 venv 내부 `.gitignore`로 제외되고 있었음)
  - `.env.example`: `GEMINI_API_KEY=`, `SLACK_WEBHOOK_URL=`, `GMAIL_USER=`, `GMAIL_APP_PASSWORD=` (모두 빈 값, Git 포함)
  - `git check-ignore`로 `.env` 제외 / `.env.example` 포함 확인
- Notebook: `.env` 탐색 → 있으면 `load_dotenv()`, `GEMINI_API_KEY`는 "설정됨 / 미설정"만 출력 (값·길이 미출력)
- 최초 실행 시 `.env` 없음 → 이후 사용자가 `.env`를 직접 작성, `GEMINI_API_KEY` 설정됨 확인
- 참고: `data/`(history CSV)는 아직 `.gitignore` 대상이 아님 (Git 포함 여부 미결정)

### 07-I Gemini API 최소 연결 테스트 → STEP 09 연결 테스트 (완료)

- 패키지: 프로젝트 `.venv`에 공식 SDK `google-genai` 2.25.0 설치 (구버전 `google-generativeai` 미사용)
  - 함께 설치된 의존성: pydantic, google-auth, cryptography, websockets, tenacity 등
- Notebook: `.env` 로드 → `genai.Client(api_key=...)` → `client.models.generate_content()` **1회**
  - 키가 없으면 호출하지 않고 안내만 출력, 오류 시 오류 메시지 안의 키는 `***`로 가림
- 실행 결과:
  - `.env` 있음, `GEMINI_API_KEY` 설정됨
  - 모델: `gemini-3.6-flash`
  - 호출 성공, 응답: **"Gemini API 연결 성공"**
  - 저장된 셀 출력에 키 문자열 없음 확인
  - SDK 안내 메시지(`Direct use of automatic function calling (AFC) ...`)가 stderr에 출력됨 — 오류 아님, AFC 미사용
- 주의: 셀을 실행할 때마다 API 1회 호출
- 이 테스트는 "연결 확인"까지였고, 실제 공고 요약은 아래 "STEP 09 실제 채용공고 Gemini 요약 호출"에서 진행

### STEP 09 실제 채용공고 Gemini 요약 호출 (완료)

- Notebook 셀 제목: `# STEP 09. 실제 채용공고 Gemini 요약 호출` (세부 번호 대신 공식 STEP 번호 사용)
- Notebook 마지막에 3셀 세트 추가 (기존 셀 수정 없음)
- 데이터: 웹 재요청 없이 `df_unique_jobs`가 있으면 사용, 없으면 `data/processed/jobs_history.csv`를 읽기 전용으로 사용
  - 이번 실행: 커널에 `df_unique_jobs`가 없어 history CSV 사용 (파일 변경 없음 — 체크섬 동일)
- 전달 공고: 앞 **2건** (GS리테일, 에스코어), 전달 필드: company_name, job_title, career, location,
  posted_date(지원 시작일), closing_date(지원 마감일), search_keyword, job_url
- 프롬프트 제약: "제공된 정보만 사용, 세부 업무·기술 스택·자격요건 추측 금지, 확인할 수 없는 항목은 '확인 불가'" + 응답 형식 지정
- 모델: `gemini-3.6-flash`, 호출 **2회** (공고당 1회, 재시도 없음)
- 결과:
  - 에스코어: **응답 수신** — 요청 형식대로 작성, [확인 불가]의 4개 항목 모두 "확인 불가"
  - GS리테일: **실패** — `ServerError 503 UNAVAILABLE` ("This model is currently experiencing high demand ... try again later")
  - 호출 성공 1 / 실패 1
- API Key 노출 없음 (저장된 셀 출력에 키 문자열 없음 확인)
- 응답은 메모리 변수 `gemini_results`에만 저장 (DataFrame / CSV 저장 없음)
- 응답의 정확성 평가는 하지 않음 → STEP 10에서 원본 데이터와 비교
- 주의: 셀을 다시 실행하면 Gemini가 최대 2회 다시 호출됨

### STEP 10 Gemini 결과 검증 (완료)

- Notebook 셀 제목: `# STEP 10. Gemini 결과 검증`, Notebook 마지막에 3셀 세트 추가 (기존 셀 수정 없음)
- Gemini API 호출 없음, 웹 요청 없음, STEP 09 재실행 없음
- 원본: `data/processed/jobs_history.csv`의 에스코어 행 (읽기 전용, 체크섬 동일)
- Gemini 응답: STEP 09 셀에 저장된 에스코어 응답 원문을 코드에 옮겨 적어 사용
- 판정 방식: 글자가 같으면 코드가 "일치"로 자동 판정, 글자가 다른 항목은 사람이 판정과 이유를 직접 기록
- 결과 (15개 항목):
  - 일치 **7**: 회사명, 공고 제목, 경력([확인 가능한 정보]), 지역, 지원 시작일, 지원 마감일, 검색어
  - 의미상 일치 **3**: 경력([한줄 요약] "경력직"), 한줄 요약, AX/AI 관련성("AX 관련 컨설팅 직무" — 제목 근거 합리적 요약)
  - 검증 불가 **5**: AX 약어 풀이 `AX(AI Transformation)`(원본에 없는 해석), 상세 업무, 상세 기술 스택, 자격요건, 우대사항
  - 불일치 **0**
- 환각 의심: 원본과 다른 사실 없음. 원본 밖 내용은 약어 풀이 1건 → "검증 불가"로 기록
- "확인 불가" 처리: 상세 업무/기술 스택/자격요건/우대사항 4개 모두 적절
- 제한: 에스코어 1건 기준이며, "의미상 일치/검증 불가"는 사람의 판단 — Gemini 전체 품질로 일반화하지 않음
- `job_url`은 Gemini 응답 형식에 없어 비교에서 제외

### STEP 11 Markdown 보고서 생성 (완료)

- Notebook 셀 제목: `# STEP 11. Markdown 보고서 생성`, Notebook 마지막에 3셀 세트 추가 (기존 셀 수정 없음)
- 웹 요청 없음, Gemini API 호출 없음, STEP 09/10 재실행 없음
- 입력:
  - `data/processed/jobs_history.csv` (읽기 전용, 체크섬 동일) → pandas로 집계 다시 계산
  - Gemini 설명: STEP 09 셀 출력에 저장된 에스코어 응답 원문을 코드에 옮겨 적음
  - 검증 결과: STEP 10 셀 출력의 판정 개수를 코드에 옮겨 적음
- 출력: `reports/ax_job_report.md` (`reports/` 폴더 새로 생성), **3331자**
- 보고서 구조: 1. 분석 기준 / 2. 현재 수집 데이터 요약 / 3. AX/AI 관련 공고 필터 결과 / 4. 주요 공고(5건 표)
  / 5. Gemini 분석 예시 / 6. Gemini 검증 결과 / 7. 제한 사항 / 8. 다음 단계
- 다시 계산한 집계 값이 이전 STEP(07-E, 07-F)과 같음을 확인
- 사실과 AI 설명 구분:
  - 각 장에 `[데이터 기반 사실]` / `[Gemini 생성 설명]` / `[STEP 10 검증 결과]` 이름표
  - Gemini 문장은 인용(`>`) 블록 안에만 두고 "Gemini가 생성한 설명이며, STEP 10에서 원본 데이터와 비교 검증" 문구 표시
  - STEP 10 판정은 사람의 판단이 섞여 있어 pandas 사실과 다른 이름표 사용
- 일반화 표현("시장 전체", "대부분의 기업" 등) 없음 확인
- 주의: 셀을 다시 실행하면 보고서 파일을 덮어씀

### 실데이터 흐름 남은 특이사항

- 일부 공고의 `applicationPeriod.end`가 `2070-01-01` — 의미 미검증 (상시채용 여부로 임의 해석하지 않음)
- 실제 페이지를 받으려면 브라우저 User-Agent 헤더가 필요함
- 사이트 내부 HTML/JSON 구조가 바뀌면 파싱 로직이 영향을 받을 수 있음
- `posted_date` 컬럼명이 실제 의미(지원 제출 시작일)와 다름 — 향후 리팩터링 시 `application_start_date` / `application_end_date`로 변경 검토
- 07-A 셀은 실행할 때마다 검색 페이지 요청 2회(기본 1회 + User-Agent 1회)가 발생함

---

## 완료된 작업 상세 (환경 / STEP 01 ~ 03 / 샘플 프로토타입)

### Git / Repository

- 원본 PUBLIC Repository Fork 완료
- Fork 저장소 Clone 완료
- Local Repository 경로 생성 완료
- `origin` 확인 완료
- `upstream` 추가 완료
- 별도 작업 브랜치는 만들지 않고 `main`에서 진행하기로 결정

### Python / Virtual Environment

- `.venv` 생성 완료
- `.venv` 활성화 완료
- Python 버전: `3.14.6`
- 가상환경 Python 경로 확인 완료

확인된 Python:

```text
C:\dev\claude-code-agent-course\chapter11\ax-job-agent\.venv\Scripts\python.exe
```

### 설치 패키지

완료:
- pandas
- requests
- beautifulsoup4
- jupyter
- python-dotenv
- ipykernel
- google-genai (STEP 09 / 07-I에서 추가)

### Jupyter

등록된 커널:

```text
Python (ax-job-agent)
```

### Notebook / STEP 01

- `notebooks/ax_job_pipeline.ipynb` 생성 완료
- 커널 `Python (ax-job-agent)` 선택 확인 완료
- Python 버전 / Platform 출력 셀 실행 성공
- pandas / requests / BeautifulSoup import 셀 실행 성공
- 사용자가 VS Code에서 직접 실행 및 결과 확인 완료
- 실행 결과 해석 Markdown 셀 작성 완료

### Notebook / STEP 02

- `notebooks/ax_job_pipeline.ipynb`의 "STEP 02. 수집 데이터 명세" 셀을 사용자가 직접 재작성
- 한 행 = 채용공고 1건으로 확정
- 컬럼 9개로 확정 (pandas DataFrame `columns_spec`으로 정의):
  `company_name`(회사명), `job_title`(공고 제목), `career`(경력 조건), `location`(근무 지역),
  `posted_date`, `closing_date`, `job_url`(공고 URL),
  `search_keyword`(공고를 발견한 검색어), `collected_at`(수집 시각)
- 처음에는 검색 결과에서 안정적으로 얻을 수 있는 정보만 사용하기로 결정 (초기 이전에 논의했던 13개 컬럼안은 폐기)
- 이후 실데이터 구현(07-A)에서 날짜 컬럼 의미를 확정:
  `posted_date` = 지원 제출 시작일(`applicationPeriod.start`), `closing_date` = 지원 제출 마감일(`applicationPeriod.end`)
  (STEP 02 Notebook 셀의 "등록일 / 마감일" 표기는 당시 기록이며, 현재 의미는 `docs/PROJECT_SPEC.md` 기준)

### Notebook / STEP 03

- `notebooks/ax_job_pipeline.ipynb`에 "STEP 03. 채용공고 페이지 접근 테스트" 셀 추가
- 요청 URL: `https://www.jobkorea.co.kr/Search/?stext=AI`
- 실행 결과 (Claude Code가 동일 요청을 독립적으로 재실행하여 검증 완료):
  - 상태 코드: `200`
  - Content-Type: `text/html`
  - 응답 길이: `3675`
  - 반환된 HTML은 실제 채용공고 검색 결과가 아니라 **잡코리아 보안정책 안내 페이지**
    - `<title>`: "보안정책"
    - `<h1>`: "서비스 이용 안내"
    - 본문: "현재 보안 정책에 따라 고객님의 접속이 일시적으로 제한되었습니다."
      (해외 IP 접속, 짧은 시간 과도한 접속, 위험 IP 분류, 비정상 접속 패턴 등을 차단 사유로 안내)
- 결론:
  - 단순 `requests.get()` 요청은 잡코리아 보안 정책에 의해 차단되는 것으로 확인됨
  - **상태 코드 200만으로는 정상적인 데이터 수집이라고 판단하면 안 된다**는 교훈 확인
  - 당시에는 샘플 데이터로 다음 단계를 진행하기로 결정 → 이후 07-A에서 일반 브라우저 User-Agent 1회 요청으로 실데이터 수집

### [프로토타입] Notebook STEP 04 — 소량 샘플 데이터 준비

- 방향: 잡코리아 접속 제한을 우회하지 않고, 파이프라인 학습을 위해 실습용 샘플 데이터 사용
- STEP 02에서 정의한 9개 컬럼을 그대로 사용해 실습용 채용공고 **5건**을 직접 작성
- `pd.DataFrame(sample_jobs)`로 `df_jobs` 생성, 실행 결과: `데이터 크기: (5, 9)`
- 해석 셀에 명시: "현재 데이터는 실제 크롤링 결과가 아니라 이후 전처리와 분석을 연습하기 위한 샘플 데이터"

### [프로토타입] Notebook STEP 05 — DataFrame 기본 구조 확인

- `df_jobs` 5행 × 9열, 컬럼 9개 확인, 결측 0개, `job_url` 중복 0건

### [프로토타입] Notebook STEP 06 — 전처리 / 중복 제거

- 전처리 전후 shape: **(5, 9)** → **(5, 9)**, 제거된 행 0개
- 날짜 컬럼 3개(`posted_date`, `closing_date`, `collected_at`) → `datetime64[us]`, 변환 실패 `NaT` 0개
- 문자열 컬럼 6개 앞뒤 공백 제거 (샘플에는 공백이 없어 값 변화 없음)
- pandas 3.x에서 문자열 dtype이 `object`가 아니라 `str`로 표시될 수 있음을 해석 셀에 기록
- 전체 Notebook 재실행은 STEP 03의 외부 요청을 다시 발생시키므로, 필요한 셀만 선택 실행

### [프로토타입] Notebook STEP 07 — 신규 공고 판별

- 샘플 `df_jobs`(5건)와 샘플 이전 이력 `previous_urls`(`job/1`, `job/2`)를 `isin()`으로 비교
- 결과: 전체 5건 / 기존 2건 / 신규 3건 (`new_jobs`: 회사C, 회사D, 회사E)
- 공식 STEP 07 완료 판단은 실데이터 07-D 결과를 기준으로 함

---

## Local Agent용 현재 프롬프트

Claude Code 또는 Codex에 아래 범위만 전달합니다.

```text
현재 프로젝트는 AX 채용정보 Agent Pipeline입니다.
프로젝트 경로: chapter11/ax-job-agent (브랜치 main)
나는 Python 데이터 분석 초보자입니다.

현재 단계는 STEP 12 Slack 발송입니다.
STEP 01~11은 완료되었습니다 (docs/PROGRESS.md 참고).
- STEP 09: 실제 공고 2건을 gemini-3.6-flash에 전달 → 에스코어 응답 수신, GS리테일 503 실패
- STEP 10: 에스코어 응답을 원본 CSV와 비교 → 15개 항목 중 불일치 0
- STEP 11: reports/ax_job_report.md 생성

이번 작업만 수행해 주세요.

Notebook 작성 규칙:
- 모든 작업은 작업 계획(Markdown Cell) → 실제 코드(Code Cell) → 실행 결과 해석/분석/요약(Markdown Cell) 순서의 3셀 세트로 작성합니다.
- 새 셀 제목은 원래 STEP 번호(STEP 12)를 사용합니다.

목표:
- 보고서 내용을 Slack으로 발송하고 실제 채널 도착을 확인합니다. (발송 방식과 범위는 Orchestrator가 정함)

하지 말 것:
- API Key / Webhook URL 출력
- 불필요한 Gemini 호출 / 웹 재요청
- Gmail 구현
- main.py 작성
- 다음 STEP 구현

완료 조건:
- 실제 Slack 채널에 도착한 것을 사람이 직접 확인
- 실행 결과 해석 Markdown Cell 작성
```

---

## 작업 종료 시 갱신 규칙

매 작업 종료 후 이 문서에서 최소 아래 5개를 갱신합니다.

1. `현재 상태 요약`
2. STEP 진행표의 상태
3. 실제 실행 결과
4. 발견한 오류 / 해결 방법
5. 다음에 해야 할 **딱 한 STEP**

예시:

```text
STEP 03 완료

확인 결과:
- HTTP 200
- Content-Type text/html
- 응답 길이 123456
- 검색 결과 HTML 확인

다음 STEP:
STEP 04 소량 데이터 수집
```

---

## Agent 교대 시 인수인계 규칙

Claude Code ↔ Codex를 바꿀 때 새 Agent에 반드시 전달:

```text
1. 프로젝트 목표
2. 현재 STEP
3. 완료된 STEP
4. 수정 대상 파일
5. 현재 실제 상태
6. 이번에 해야 할 작업
7. 이번에 하면 안 되는 작업
8. 완료 조건
```

새 Agent가 이전 대화를 알고 있다고 가정하지 않습니다.

---

## 오류 기록

현재 등록된 오류:

```text
날짜: 2026-09-23
STEP: 03 채용공고 페이지 접근 테스트
명령/셀: requests.get("https://www.jobkorea.co.kr/Search/?stext=AI", timeout=10)
오류 메시지: (예외 없음, 상태 코드 200이지만 내용이 검색 결과가 아님)
원인: 잡코리아 보안 정책에 의한 접속 제한으로 추정
  (User-Agent 미설정 등으로 봇/자동화 요청으로 판단되었을 가능성)
해결 방법: 당시에는 샘플 데이터로 파이프라인 개발을 계속 진행 → 07-A에서 일반 브라우저 User-Agent 1회 요청으로 해결
재실행 결과: Claude Code가 동일 코드로 직접 재현 — 동일하게 보안정책 페이지 반환 확인
```

```text
날짜: 2026-09-23
STEP: 07-A 실제 JobKorea 소량 크롤링 검증 (공식 STEP 04)
명령/셀: requests.get("https://www.jobkorea.co.kr/Search/?stext=ax&tabType=recruit", timeout=10)
오류 메시지: (예외 없음, 상태 코드 200이지만 보안정책 페이지 반환)
원인: User-Agent가 없는 기본 요청을 자동화 요청으로 판단한 것으로 추정
해결 방법: 일반 브라우저 User-Agent 헤더를 붙여 1회만 재요청 (다른 우회 기법·반복 재시도는 사용하지 않음)
재실행 결과: 실제 검색 결과 HTML 수신, 공고 5건 추출 성공
```

```text
날짜: 2026-09-23
STEP: 07-A 실제 JobKorea 소량 크롤링 검증 (공식 STEP 04)
명령/셀: STEP 07-A 코드 셀 (posted_date / closing_date 추출)
오류 메시지: (예외 없음, posted_date / closing_date가 None)
원인: 화면 카드 HTML에는 날짜 텍스트가 없고, 날짜는 같은 응답의 Next.js script JSON에만 존재
해결 방법: script JSON의 applicationPeriod.start / end를 공고 ID로 매칭해 추출
재실행 결과: 5건 모두 날짜 수집, STEP 07-B에서 결측 0 / 변환 실패 0 확인
```

```text
날짜: 2026-09-23
STEP: 09 실제 채용공고 Gemini 요약 호출
명령/셀: client.models.generate_content(model="gemini-3.6-flash", ...) — GS리테일 공고
오류 메시지: ServerError 503 UNAVAILABLE — "This model is currently experiencing high demand.
  Spikes in demand are usually temporary. Please try again later."
원인: Gemini 서버 측 일시적 과부하 (코드·API 키 문제 아님 — 같은 셀의 다음 호출은 성공)
해결 방법: 호출 한도(최대 2회) 때문에 재시도하지 않음. 필요하면 시간을 두고 STEP 09 셀을 한 번만 다시 실행
재실행 결과: (재실행하지 않음 — STEP 10은 성공한 에스코어 1건만 검증하기로 결정)
```

오류가 생기면 아래 형식으로 추가:

```text
날짜:
STEP:
명령/셀:
오류 메시지:
원인:
해결 방법:
재실행 결과:
```
