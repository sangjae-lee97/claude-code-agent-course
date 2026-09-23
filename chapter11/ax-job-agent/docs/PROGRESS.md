# PROGRESS — 프로젝트 진행 기록

이 파일은 **작업이 끝날 때마다 반드시 갱신**합니다.

---

## 현재 상태 요약

현재 단계:

```text
STEP 00 환경 준비 완료
STEP 01 개발환경 확인 Notebook 완료
STEP 02 수집 데이터 명세 완료 (컬럼 9개 확정)
STEP 03 채용공고 페이지 접근 테스트 완료 (보안정책 페이지 반환, 우회하지 않기로 결정)
STEP 04 소량 샘플 데이터 준비 완료 (실습용 샘플 5건 DataFrame 생성)
STEP 05 DataFrame 기본 구조 확인 완료
STEP 06 전처리 / 중복 제거 완료
STEP 07 신규 공고 판별 진행 중 (샘플 데이터 기준 Notebook 셀 작성·실행 완료, 사용자 최종 확인 전)
STEP 07-A 실제 JobKorea 소량 크롤링 검증 완료 (실데이터 5건, 지원 시작일/마감일 포함)
STEP 07-B 날짜 데이터 전달 검증 완료 (DataFrame (5, 9), 결측 0, 날짜 변환 실패 0)
STEP 07-C 실데이터 중복 확인 및 제거 완료 (중복 0건, df_unique_jobs 5건, 원본 보존)
STEP 07-D 신규 공고 판별 및 이력 초기화 완료 (1차 신규 5건 → 2차 신규 0건, history 5건 유지)
STEP 07-E 실데이터 기본 분석 완료 (회사/지역/경력/검색어별 집계, 지원 기간 범위 확인)
STEP 07-F AX/AI 관련 공고 1차 필터링 완료 (5건 중 5건 통과, 모두 'AX' 매칭, 부분 문자열 오탐 가능성 발견)
STEP 07-G 키워드 필터 오탐 검증 및 개선 완료 (테스트 12/12 통과, 오탐 4건·누락 2건 해결)
STEP 07-H Gemini API 환경변수 준비 완료 (.env 작성, GEMINI_API_KEY 설정됨, 키 값 미출력)
STEP 07-I Gemini API 최소 연결 테스트 진행 중 (gemini-3.6-flash 1회 호출 성공, 사용자 최종 확인 전)
```

두 가지 작업 흐름 (혼동 주의):

```text
[샘플 데이터 실습]  STEP 04 ~ 07
  - 직접 만든 샘플 5건(df_jobs)으로 DataFrame 확인 / 전처리 / 신규 공고 판별을 연습한 기록
  - 프로토타입 기록으로 보존하며 수정하지 않는다

[실데이터 검증 흐름]  STEP 07-A ~
  - 실제 JobKorea 검색 결과에서 수집한 공고(jobs → df_real_jobs)로 같은 과정을 다시 검증
  - 07-A 수집 → 07-B DataFrame 전달 → 07-C 중복 확인 → 07-D 이전 실행 이력(jobs_history.csv)과 비교 → 07-E 기본 분석 → 07-F 키워드 1차 필터링 → 07-G 키워드 오탐 검증/개선 → 07-H Gemini API 환경변수 준비 → 07-I Gemini API 최소 연결 테스트
  - 샘플 STEP 07의 이력은 코드 안의 목록(previous_urls)이고, 실데이터 07-D의 이력은 실제 CSV 파일이다
  - 샘플 STEP의 완료 여부와 실데이터 STEP의 완료 여부는 따로 관리한다
```

다음 작업:

```text
[실데이터] 사용자가 STEP 07-I 셀 출력("Gemini 응답: Gemini API 연결 성공")을 확인하고
           STEP 07-I 완료 여부를 결정한다. (셀을 실행할 때마다 API 1회 호출됨)
[샘플] STEP 07 신규 공고 판별 결과 확인은 별도로 남아 있다.
Notebook 작성은 항상 작업 계획(Markdown) → 실제 코드(Code) → 실행 결과 해석/분석/요약(Markdown) 3셀 패턴을 따른다.
```

---

## STEP 진행표

| STEP | 작업 | 상태 | 완료 기준 |
|---:|---|---|---|
| 00 | Git / Python / Jupyter 환경 준비 | ✅ 완료 | Fork, Clone, upstream, .venv, 패키지, 커널 |
| 01 | 개발환경 확인 Notebook | ✅ 완료 | Python/OS/import 셀 실행 성공 |
| 02 | 수집 데이터 명세 | ✅ 완료 | 한 행 의미와 컬럼 확정 |
| 03 | 채용공고 페이지 접근 테스트 | ✅ 완료 (이슈 발견) | HTTP 상태/Content-Type/응답 확인 |
| 04 | 소량 데이터 수집 | ✅ 완료 (실제 크롤링 대신 샘플 5건 사용) | 1개 → 5~10개 공고 확인 |
| 05 | DataFrame 기본 구조 확인 | ✅ 완료 | 컬럼/shape/head/결측/중복 확인 |
| 06 | 전처리 / 중복 제거 | ✅ 완료 | 결측/중복/날짜 처리 검증 |
| 07 | 신규 공고 판별 | ⏳ 진행 중 | 기존 vs 신규 URL 구분 |
| 07-A | 실제 JobKorea 소량 크롤링 검증 | ✅ 완료 | 실제 검색 결과 HTML에서 최대 5건 추출 |
| 07-B | 날짜 데이터 전달 검증 | ✅ 완료 | 지원 시작일/마감일이 DataFrame까지 유지 |
| 07-C | 실데이터 중복 확인 및 제거 | ✅ 완료 | job_url 기준 5건 내부 중복 확인, 원본 보존 |
| 07-D | 신규 공고 판별 및 이력 초기화 | ✅ 완료 | 1차 실행 전부 신규·history 생성, 2차 실행 신규 0건·history 유지 |
| 07-E | 실데이터 기본 분석 | ✅ 완료 | 회사/지역/경력/검색어별 공고 수, 지원 기간 범위 확인 |
| 07-F | AX/AI 관련 공고 1차 필터링 | ✅ 완료 | job_title 키워드 필터, 공고별 매칭 키워드 확인, 원본 보존 |
| 07-G | 키워드 필터 오탐 검증 및 개선 | ✅ 완료 | 테스트 제목 전부 기대 결과 일치, 실데이터에 개선 필터 적용 |
| 07-H | Gemini API 환경변수 준비 | ✅ 완료 | .env.example / .gitignore 준비, Notebook에서 GEMINI_API_KEY 설정 여부 확인 (값 미출력) |
| 07-I | Gemini API 최소 연결 테스트 | ⏳ 진행 중 | 짧은 프롬프트 1회 호출, response.text 수신, 키 미노출 |

> STEP 04~07은 샘플 데이터 실습, STEP 07-A~는 실데이터 검증 흐름이다. (위 "두 가지 작업 흐름" 참고)
| 08 | 기본 분석 / 관련 공고 필터링 | ⬜ 대기 | 기본 통계와 필터 검증 |
| 09 | Gemini API 연동 | ⬜ 대기 | 일부 공고 요약 성공 |
| 10 | Gemini 결과 검증 | ⬜ 대기 | 원문과 AI 결과 비교 |
| 11 | Markdown 보고서 생성 | ⬜ 대기 | reports에 보고서 생성 |
| 12 | Slack 발송 | ⬜ 대기 | 실제 채널 도착 확인 |
| 13 | Gmail 발송 | ⬜ 대기 | 실제 메일 도착 확인 |
| 14 | 함수화 | ⬜ 대기 | Notebook 코드를 src로 분리 |
| 15 | main.py 통합 | ⬜ 대기 | 전체 순서 연결 |
| 16 | 로컬 전체 실행 검증 | ⬜ 대기 | `python main.py` 성공 |
| 17 | GitHub Actions 수동 실행 | ⬜ 대기 | Run workflow 성공 |
| 18 | GitHub Actions 주간 실행 | ⬜ 대기 | schedule 등록 |

---

## 완료된 작업 상세

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
  `posted_date`(등록일), `closing_date`(마감일), `job_url`(공고 URL),
  `search_keyword`(공고를 발견한 검색어), `collected_at`(수집 시각)
- 처음에는 검색 결과에서 안정적으로 얻을 수 있는 정보만 사용하기로 결정 (초기 이전에 논의했던 13개 컬럼안은 폐기)

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
  - 사이트 차단을 우회하지 않고(b), 샘플 데이터로 다음 단계를 진행하기로 결정

### Notebook / STEP 04 (Claude Code가 노트북을 직접 열어 확인)

- `notebooks/ax_job_pipeline.ipynb`에 "STEP 04. 소량 샘플 데이터 준비" 셀 추가
- 방향: 잡코리아 접속 제한을 우회하지 않고, 파이프라인 학습을 위해 실습용 샘플 데이터 사용
- STEP 02에서 정의한 9개 컬럼을 그대로 사용해 실습용 채용공고 **5건**을 직접 작성
- `pd.DataFrame(sample_jobs)`로 `df_jobs` 생성, 실행 결과: `데이터 크기: (5, 9)` — 정상 생성 확인
- 해석 셀에 명시: "현재 데이터는 실제 크롤링 결과가 아니라 이후 전처리와 분석을 연습하기 위한 샘플 데이터"

### Notebook / STEP 05

- `df_jobs` 기본 구조 검증 완료
- 데이터 크기: **5행 × 9열**
- 컬럼 목록:
  `company_name`, `job_title`, `career`, `location`, `posted_date`,
  `closing_date`, `job_url`, `search_keyword`, `collected_at`
- 상위 5개 행을 직접 확인했고, 한 행이 채용공고 1건 구조로 정상 구성됨
- 모든 컬럼의 결측값: **0개**
- `job_url` 기준 중복 공고: **0건**
- 결론: 현재 샘플 DataFrame의 기본 구조에는 이상이 없으며 STEP 06 전처리로 진행 가능

### Notebook / STEP 06

- `notebooks/ax_job_pipeline.ipynb` 맨 끝에 3셀 세트 추가 완료
  - 작업 계획 Markdown
  - 실제 코드
  - 실행 결과 해석 / 분석 / 요약 Markdown
- 기존 STEP 01~05 셀은 수정하지 않음
- 전처리 전 shape: **(5, 9)**
- 전처리 후 shape: **(5, 9)**
- 제거된 행: **0개**
- 전처리 전 9개 컬럼은 문자열 타입으로 확인됨
- 날짜 컬럼 3개 변환 완료:
  - `posted_date` → `datetime64[us]`
  - `closing_date` → `datetime64[us]`
  - `collected_at` → `datetime64[us]`
- 날짜 변환 실패로 생성된 `NaT`: **0개**
- 문자열 컬럼 6개의 앞뒤 공백 제거 완료
- 샘플 데이터에는 기존 앞뒤 공백이 없어 값 변화 없음
- `job_url` 기준 중복 제거 결과: **0개 제거**
- 전처리 후 모든 컬럼의 결측값: **0개**
- `job_url` 중복 개수: **0개**
- pandas 3.x에서 문자열 dtype이 `object`가 아니라 `str`로 표시될 수 있음을 해석 셀에 기록
- 전체 Notebook 재실행은 STEP 03의 외부 요청을 다시 발생시키므로, STEP 04 샘플 데이터 셀 → STEP 06 셀 순서로 선택 실행
- 결론: STEP 06 완료 조건 충족, STEP 07 신규 공고 판별로 진행 가능

### Notebook / STEP 07 (진행 중)

- 샘플 `df_jobs`(5건)와 샘플 이전 이력 `previous_urls`(`job/1`, `job/2`)를 `isin()`으로 비교
- 결과: 전체 5건 / 기존 2건 / 신규 3건 (`new_jobs`: 회사C, 회사D, 회사E)
- 사용자 최종 확인 전

### Notebook / STEP 07-A 실제 JobKorea 소량 크롤링 검증 (완료)

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

### Notebook / STEP 07-B 날짜 데이터 전달 검증 (완료)

- `jobs` → `df_real_jobs` DataFrame 변환 (샘플 `df_jobs`는 덮어쓰지 않음)
- shape: **(5, 9)**, 9개 컬럼 모두 결측 **0건**
- `pd.to_datetime(errors="coerce")` 변환 실패: `posted_date` **0건**, `closing_date` **0건**
  (변환은 별도 변수로만 확인, 원본 날짜 문자열은 보존)

### Notebook / STEP 07-C 실데이터 중복 확인 및 제거 (완료)

- Notebook 마지막에 3셀 세트 추가 (기존 셀 수정 없음)
- 대상: `df_real_jobs` (실데이터 5건), 기준: `job_url`
- 범위: 현재 5건 **내부** 중복만 확인 (이전 실행 결과와 비교하지 않음)
- 실행 결과 (STEP 07-A → 07-B → 07-C 순서로 실행):
  - 중복 확인 전: **5건**, 중복 행: **0건**, 중복 제거 후: **5건**, 제거: **0건**
  - ㈜NAVER 공고 2건은 제목이 비슷하지만 `job_url`이 달라 서로 다른 공고로 판단됨
  - 원본 `df_real_jobs` 보존 확인, 중복 제거 결과는 `df_unique_jobs`(5건)에 저장
- 사용자 확인 완료

### Notebook / STEP 07-D 신규 공고 판별 및 이력 초기화 (완료)

- Notebook 마지막에 3셀 세트 추가 (기존 셀 수정 없음)
- 이력 파일: `data/processed/jobs_history.csv` (프로젝트 루트 기준, `notebooks/`에서 실행 시 상위 폴더를 루트로 계산)
  - 실행 전에는 `data/` 폴더와 history 파일이 없었음 → 이번 실행에서 생성
- 기준: `job_url`이 history의 `job_url` 집합에 없으면 신규
- 1차 실행 (첫 실행): 현재 5건 / 기존 이력 0건 / 신규 **5건** / 업데이트 후 이력 **5건**
- 2차 실행 (같은 5건으로 재실행): 기존 이력 5건 / 신규 **0건** / 업데이트 후 이력 **5건** (중복 누적 없음)
- 원본 `df_real_jobs`, `df_unique_jobs` 보존 확인, `new_jobs_df` / `updated_history_df` 역할 분리
- 참고:
  - 2차 실행은 재크롤링 없이 같은 5건으로 로직만 검증함
  - history는 `keep="last"`로 저장 → 같은 공고 재수집 시 `collected_at`이 최신 시각으로 갱신됨 ("처음 발견 시각" 보존은 후속 검토)
  - `data/`는 현재 git에서 추적되지 않은 새 폴더 (`.gitignore` 대상 여부 미결정)
- 사용자 확인 완료

### Notebook / STEP 07-E 실데이터 기본 분석 (완료)

- Notebook 마지막에 3셀 세트 추가 (기존 셀 수정 없음), 분석 대상: `df_unique_jobs` (원본 수정 없음)
- 실행 결과 (07-A → 07-B → 07-C → 07-E 순서로 실행, **현재 5건 기준**):
  - 전체 공고: **5건**, 검색어: `ax` 5건
  - 회사별: ㈜NAVER 2 / GS리테일 1 / 에스코어 1 / ㈜슈프리마 1
  - 지역별: 경기 성남시 3 / 서울 강남구 외 1 1 / 서울 송파구 1
  - 경력별: 경력 3 / 경력3년↑ 1 / 경력7년↑ 1
  - 지원 시작일 범위: 2026-07-01 ~ 2026-09-21, 지원 마감일 범위: 2026-09-29 10:00 ~ 2026-10-25 23:00
- 신규 공고 수: 검증 실행에서는 07-D를 실행하지 않아 `new_jobs_df` 없음 → "확인하지 못했습니다" 출력
  (07-D는 실행할 때마다 `jobs_history.csv`를 다시 저장하므로, 이번 작업 범위에서 제외.
  history를 읽기만 해서 비교한 결과 현재 5건 모두 history에 있음 → 07-D 실행 시 신규 0건 예상)
- 특이사항: 경력 값이 화면 문구 그대로라 `경력` / `경력3년↑` / `경력7년↑`가 별도로 집계됨,
  `서울 강남구 외 1`처럼 다중 근무지 요약 문구가 있음 → 값 정리 규칙은 후속 검토
- 사용자 확인 완료 (new_jobs_df 미존재로 신규 공고 수를 출력하지 못한 것은 완료를 막지 않음 — 신규 판별은 07-D에서 검증 완료)

### Notebook / STEP 07-F AX/AI 관련 공고 1차 필터링 (완료)

- Notebook 마지막에 3셀 세트 추가 (기존 셀 수정 없음), Gemini 미사용 — Python 문자열 검색만 사용
- 대상: `df_unique_jobs`의 `job_title`만 (회사명·상세 본문은 후속 검토)
- 키워드 13개: AX, AI, 인공지능, 생성형 AI, 생성형AI, LLM, Machine Learning, 머신러닝,
  Data Scientist, 데이터 사이언티스트, AI Engineer, AI 엔지니어, 데이터 분석 (소문자로 바꿔 비교)
- 실행 결과 (07-A → 07-B → 07-C → 07-F 순서로 실행, 07-D는 history 재저장 방지를 위해 제외):
  - 전체 **5건** / 통과 **5건** / 제외 **0건**
  - 5건 모두 `AX` 하나로만 매칭 (나머지 12개 키워드는 매칭 없음)
- 결과: `df_filtered_jobs` (5행 × 10열, `matched_keywords` 컬럼은 이 복사본에만 추가), `df_unique_jobs` 보존 확인
- 해석: "1차 후보"로만 봄 — 최종 의미 판단은 Gemini 단계에서 수행
- 한계:
  - 검색어가 `ax`라 전부 통과 → 제외되는 경우는 이번 데이터로 확인하지 못함
  - 단순 포함 검색이라 `ai`(maintenance, training), `ax`(tax, max) 같은 부분 문자열 오매칭 가능성 있음 (이번 5건에는 없음)
- 사용자 확인 완료 → 오탐 가능성은 STEP 07-G에서 검증

### Notebook / STEP 07-G 키워드 필터 오탐 검증 및 개선 (완료)

- Notebook 마지막에 3셀 세트 추가 (기존 셀 수정 없음, STEP 07-F 함수 수정 없음)
- 웹 재요청 없이 테스트 제목 12개(요청된 10개 + 한글이 바로 붙은 경우 2개)로 검증
- 새 함수 `find_matched_keywords_safe()`:
  - 영문 키워드(AX, AI, LLM, Machine Learning, Data Scientist, AI Engineer)
    → 앞뒤에 영문자·숫자가 없을 때만 매칭 (`(?<![A-Za-z0-9])키워드(?![A-Za-z0-9])`, 대소문자 무시)
  - 한글이 들어 있는 키워드 → 기존처럼 포함 검색
- 결과: 테스트 **12개 중 12개 통과, 실패 0**
  - 기존 포함 검색: Tax / Max(`AX`), Maintenance / Training(`AI`) **4건 오탐**
  - `\b` 방식: 한글이 붙은 `AX담당자`, `AI기반` **2건 누락** (Python에서는 한글도 단어 글자로 취급)
  - 개선 방식: 오탐 0, 누락 0
- 실데이터 적용: 이번 실행에서는 웹 재요청 금지로 07-A를 실행하지 않아 `df_unique_jobs`가 메모리에 없음 → 적용 건너뜀
  (history CSV 제목 5개를 읽기만 해서 확인한 결과 5건 모두 `['AX']` 매칭 — Notebook에는 저장하지 않음)
- `df_filtered_jobs_safe`는 사용자가 07-A → 07-B → 07-C → 07-G 순서로 실행하면 생성됨
- 한계: 정규식은 직무 의미를 판단하지 않음, `OpenAI`처럼 영문자가 붙은 표현은 `AI`로 매칭되지 않음
- 사용자 확인 완료

### Notebook / STEP 07-H Gemini API 환경변수 준비 (완료)

- Gemini API 호출 없음 — 키 보관·로딩 준비만 진행
- 새로 만든 파일 (프로젝트 루트 `chapter11/ax-job-agent/`):
  - `.gitignore`: `.env`, `.venv/`, `__pycache__/`, `.ipynb_checkpoints/` 제외
    (이전에는 저장소 전체에 `.gitignore`가 없었고, `.venv/`만 venv 내부 `.gitignore`로 제외되고 있었음)
  - `.env.example`: `GEMINI_API_KEY=`, `SLACK_WEBHOOK_URL=`, `GMAIL_USER=`, `GMAIL_APP_PASSWORD=` (모두 빈 값, Git 포함)
  - `git check-ignore`로 `.env` 제외 / `.env.example` 포함 확인
- Notebook 마지막에 3셀 세트 추가 (기존 셀 수정 없음)
  - `notebooks/`에서 실행 시 상위 폴더를 프로젝트 루트로 보고 `.env` 탐색 → 있으면 `load_dotenv()`
  - `GEMINI_API_KEY`는 "설정됨 / 미설정"만 출력 (값·길이 미출력)
- 실행 결과: `.env` **없음**, `GEMINI_API_KEY` **미설정**, 키 값 노출 없음
- `.env`는 Claude Code가 만들지 않음 — 사용자가 직접 작성 예정
- 참고: `data/`(history CSV)는 아직 `.gitignore` 대상이 아님 (Git 포함 여부 미결정)
- 사용자 확인 완료: 사용자가 `.env`를 직접 작성, `GEMINI_API_KEY` 설정됨

### Notebook / STEP 07-I Gemini API 최소 연결 테스트 (진행 중)

- 패키지: 프로젝트 `.venv`에 공식 SDK `google-genai` 2.25.0 설치 (구버전 `google-generativeai` 미사용)
  - 함께 설치된 의존성: pydantic, google-auth, cryptography, websockets, tenacity 등
- Notebook 마지막에 3셀 세트 추가 (기존 셀 수정 없음)
  - `.env` 로드 → `genai.Client(api_key=...)` → `client.models.generate_content()` **1회**
  - 키가 없으면 호출하지 않고 안내만 출력, 오류 시 오류 메시지 안의 키는 `***`로 가림
- 실행 결과:
  - `.env` 있음, `GEMINI_API_KEY` 설정됨
  - 모델: `gemini-3.6-flash`
  - 호출 성공, 응답: **"Gemini API 연결 성공"**
  - 저장된 셀 출력에 키 문자열 없음 확인
  - SDK 안내 메시지(`Direct use of automatic function calling (AFC) ...`)가 stderr에 출력됨 — 오류 아님, 이번 호출은 AFC 미사용
- 주의: 셀을 실행할 때마다 API 1회 호출
- 사용자 최종 확인 전

### STEP 07-A/07-B 남은 특이사항

- 일부 공고의 `applicationPeriod.end`가 `2070-01-01` — 의미 미검증 (상시채용 여부로 임의 해석하지 않음)
- 실제 페이지를 받으려면 브라우저 User-Agent 헤더가 필요함
- 사이트 내부 HTML/JSON 구조가 바뀌면 파싱 로직이 영향을 받을 수 있음
- `posted_date` 컬럼명이 실제 의미(지원 제출 시작일)와 다름 — 향후 리팩터링 시 `application_start_date` / `application_end_date`로 변경 검토

---

## 지난 STEP — STEP 01 개발환경 확인 (완료)

### 목표

실제 데이터 수집 전에 Notebook 실행 환경이 정상인지 확인합니다.

### 생성할 파일

```text
notebooks/ax_job_pipeline.ipynb
```

### 작성할 내용

#### Markdown Cell
- STEP 01 제목
- 작업 목표
- 확인 항목
- 완료 조건

#### Code Cell 1

확인:
- Python 버전
- OS / Platform

예시 개념:

```python
import sys
import platform

print("Python:", sys.version)
print("Platform:", platform.platform())
```

#### Code Cell 2

확인:
- pandas
- requests
- BeautifulSoup

예시 개념:

```python
import pandas as pd
import requests
from bs4 import BeautifulSoup

print("pandas:", pd.__version__)
print("requests:", requests.__version__)
print("BeautifulSoup import: OK")
```

### 사람이 직접 확인할 것

- Notebook이 정상적으로 열림
- Kernel이 `Python (ax-job-agent)`인지
- 모든 셀이 에러 없이 실행되는지
- Python이 `.venv`를 사용하는지
- import 오류가 없는지

### STEP 01 완료 조건

아래를 모두 만족해야 완료:

- [x] `notebooks/ax_job_pipeline.ipynb` 생성
- [x] Kernel = `Python (ax-job-agent)`
- [x] Python 버전 출력 성공
- [x] Platform 출력 성공
- [x] pandas import 성공
- [x] requests import 성공
- [x] BeautifulSoup import 성공
- [x] 사용자가 실제 출력 확인
- [x] 결과 해석 Markdown 작성

---

## 지난 STEP — STEP 02 수집 데이터 명세 (완료)

### 목표

실제 크롤링 전에 DataFrame의 한 행이 의미하는 것과 컬럼 구성을 확정합니다.

### 작성 위치

```text
notebooks/ax_job_pipeline.ipynb (STEP 02 Markdown 셀)
```

### 확정된 내용

- 한 행 = 잡코리아 채용공고 1건
- 컬럼(9개): company_name, job_title, career, location, posted_date,
  closing_date, job_url, search_keyword, collected_at
- 처음에는 검색 결과에서 안정적으로 얻을 수 있는 정보만 사용하기로 결정

### STEP 02 완료 조건

- [x] 컬럼 정의를 사람이 직접 검토
- [x] 컬럼 추가/삭제 여부 결정
- [x] 컬럼명과 의미 최종 확정
- [x] 확정 결과를 이 문서(PROGRESS.md)에 반영

---

## Local Agent용 현재 프롬프트

Claude Code 또는 Codex에 아래 범위만 전달합니다.

```text
현재 프로젝트는 AX 채용정보 Agent Pipeline입니다.
나는 Python 데이터 분석 초보자입니다.

현재 단계는 STEP 07 신규 공고 판별입니다.
STEP 01~06은 완료되었습니다 (docs/PROGRESS.md 참고).

이번 작업만 수행해 주세요.

Notebook 작성 규칙:
- 모든 작업은 작업 계획(Markdown Cell) → 실제 코드(Code Cell) → 실행 결과 해석/분석/요약(Markdown Cell) 순서의 3셀 세트로 작성합니다.

목표:
- 이전 실행 이력과 현재 df_jobs를 비교해 신규 공고를 구분합니다.
- 1차 기준은 job_url입니다.

하지 말 것:
- STEP 08 기본 분석 진행
- 실제 크롤링 재시도
- Gemini API 사용
- Slack / Gmail 구현
- main.py 작성
- 다음 STEP 구현

완료 조건:
- 이전 이력 데이터와 현재 df_jobs를 비교할 기준을 명확히 정의
- job_url 기준으로 신규/기존 공고가 구분됨
- 결과를 사람이 직접 확인
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
해결 방법: 사이트 차단을 우회하지 않기로 결정 — STEP 04부터는 실습용 샘플
  데이터로 파이프라인 개발을 계속 진행 (실제 크롤링 우회는 보류)
재실행 결과: Claude Code가 동일 코드로 직접 재현 — 동일하게 보안정책 페이지 반환 확인
```

```text
날짜: 2026-09-23
STEP: 07-A 실제 JobKorea 소량 크롤링 검증
명령/셀: requests.get("https://www.jobkorea.co.kr/Search/?stext=ax&tabType=recruit", timeout=10)
오류 메시지: (예외 없음, 상태 코드 200이지만 보안정책 페이지 반환)
원인: User-Agent가 없는 기본 요청을 자동화 요청으로 판단한 것으로 추정
해결 방법: 일반 브라우저 User-Agent 헤더를 붙여 1회만 재요청 (다른 우회 기법·반복 재시도는 사용하지 않음)
재실행 결과: 실제 검색 결과 HTML 수신, 공고 5건 추출 성공
```

```text
날짜: 2026-09-23
STEP: 07-A 실제 JobKorea 소량 크롤링 검증
명령/셀: STEP 07-A 코드 셀 (posted_date / closing_date 추출)
오류 메시지: (예외 없음, posted_date / closing_date가 None)
원인: 화면 카드 HTML에는 날짜 텍스트가 없고, 날짜는 같은 응답의 Next.js script JSON에만 존재
해결 방법: script JSON의 applicationPeriod.start / end를 공고 ID로 매칭해 추출
재실행 결과: 5건 모두 날짜 수집, STEP 07-B에서 결측 0 / 변환 실패 0 확인
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
