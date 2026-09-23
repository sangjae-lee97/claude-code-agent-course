# PROJECT SPEC — AX 채용정보 Agent Pipeline

## 1. 프로젝트 목표

AX / AI / 데이터 분석 관련 채용공고를 주기적으로 수집하고,
데이터를 정제·분석한 뒤 AI 요약과 사람 검증을 거쳐
주간 보고서로 전달하는 자동화 파이프라인을 구현합니다.

최종 흐름:

```text
GitHub Actions
→ main.py
→ Crawler
→ pandas 정제/분석
→ 신규 공고 판별
→ 관련 공고 필터링
→ Gemini API 요약
→ Markdown Report
→ Slack / Gmail
```

## 2. 역할 분담

### GPT Web — Orchestrator

담당:
- 전체 목표 관리
- 현재 STEP 결정
- 작업을 작은 단위로 분리
- 완료 조건 정의
- Claude Code / Codex에 전달할 프롬프트 작성
- 실행 결과를 기반으로 다음 STEP 판단

하지 않는 것:
- 로컬 파일을 직접 수정했다고 가정하지 않음
- 여러 STEP을 한 번에 구현하도록 지시하지 않음

### Claude Code / Codex — Local Coding Agent

담당:
- 실제 로컬 프로젝트 파일 확인
- 현재 STEP에 필요한 파일 작성/수정
- 필요 시 명령 실행
- 오류 원인 확인 및 수정

운영 규칙:
- 토큰/사용량에 따라 두 Agent를 교대 사용
- Agent를 바꿀 때 이전 Agent가 대화 내용을 알고 있다고 가정하지 않음
- 프롬프트에 현재 STEP, 완료된 내용, 수정 대상 파일, 금지 사항, 완료 조건을 포함

### Human Validator — 사용자

담당:
- Notebook 셀 직접 실행
- Terminal 출력 직접 확인
- DataFrame의 shape / head / 결측 / 중복 확인
- Gemini 요약을 원문과 비교
- 다음 단계 진행 여부 승인

## 3. 개발 환경

- OS: Windows
- IDE: VS Code
- 주요 작업 방식: Jupyter Notebook
- Python: 3.14.6
- Virtual Env: `.venv`
- Jupyter Kernel: `Python (ax-job-agent)`
- Git: GitHub Fork 기반
- 작업 브랜치: `main` 사용

## 4. 기본 프로젝트 구조

목표 구조:

```text
chapter11/
└── ax-job-agent/
    ├── docs/
    │   ├── START_HERE.md
    │   ├── PROJECT_SPEC.md
    │   ├── PROGRESS.md
    │   └── DEVELOPMENT_RULES.md
    ├── notebooks/
    │   └── ax_job_pipeline.ipynb
    ├── src/
    │   ├── crawler.py
    │   ├── preprocess.py
    │   ├── analyzer.py
    │   ├── gemini_client.py
    │   ├── reporter.py
    │   └── notifier.py
    ├── data/
    │   ├── raw/
    │   └── processed/
    ├── reports/
    ├── .env
    ├── .env.example
    ├── .gitignore
    ├── main.py
    ├── requirements.txt
    └── README.md
```

주의:
- 이 구조를 처음부터 전부 만들지 않습니다.
- 필요해질 때 하나씩 추가합니다.
- 현재 존재: `docs/`, `notebooks/`, `data/processed/jobs_history.csv`, `.env`(Git 제외), `.env.example`, `.gitignore`
- 아직 없음: `src/`, `data/raw/`, `reports/`, `main.py`, `requirements.txt`, `README.md`

## 5. 데이터 정의

DataFrame의 한 행:

> 채용공고 1건

컬럼 (9개):

| 컬럼 | 의미 | 현재 실제 수집 출처 (JobKorea 검색 결과 페이지) |
|---|---|---|
| company_name | 회사명 | 공고 카드 HTML |
| job_title | 공고 제목 | 공고 카드 HTML |
| career | 경력 조건 | 공고 카드 HTML (화면 문구 그대로, 예: `경력3년↑`) |
| location | 근무 지역 | 공고 카드 HTML (화면 문구 그대로, 예: `서울 강남구 외 1`) |
| posted_date | **지원 제출 시작일** | Next.js script JSON의 `applicationPeriod.start` (날짜 부분, 예: `2026-09-21`) |
| closing_date | **지원 제출 마감일** | Next.js script JSON의 `applicationPeriod.end` (날짜 + 시:분, 예: `2026-10-01 23:00`) |
| job_url | 공고 URL | 제목 링크 `href`에서 추적용 `?` 파라미터를 제거한 기본 주소 |
| search_keyword | 공고를 발견한 검색어 | 수집 시 사용한 검색어 (예: `ax`) |
| collected_at | 수집 시각 | 페이지를 받아 온 시각 |

날짜 컬럼 관련 확정 사항:
- 이 프로젝트에서 `posted_date`는 **공고 등록일이 아니라 지원 제출 시작일**을 의미한다.
- 공고 JSON의 `createdAt`(사이트에 공고가 등록된 시각)은 사용하지 않는다. (지원 시작일과 다를 수 있음)
- 공고 카드와 JSON은 순서가 아니라 공고 ID(`job_url` 끝 숫자)로 매칭한다.
- 원본 날짜 문자열은 보존하고, 날짜 변환은 필요할 때 별도 변수로 수행한다.
- 일부 공고의 마감일이 `2070-01-01`처럼 매우 먼 날짜일 수 있다. 의미(상시채용 여부)는 아직 검증하지 않았으므로 원본 값을 그대로 둔다.
- 컬럼명 `posted_date` / `closing_date`는 현재 유지한다.
  향후 리팩터링 시 `application_start_date` / `application_end_date`로 이름을 바꿀 수 있다.

초기에는 검색 결과 페이지에서 안정적으로 얻을 수 있는 필드부터 사용합니다.

## 6. 데이터 분석 원칙

Python/pandas가 담당하는 사실:
- 행/열 개수
- 결측값
- 중복
- 날짜 변환
- 신규 공고 수
- 회사별 공고 수
- 지역별 공고 수
- 경력 조건 분포
- 검색어별 공고 수
- 기본 키워드 집계

Gemini가 담당하는 내용:
- 공고 핵심 내용 요약
- 요구 기술 추출
- 직무 유형 분류
- AX 관련성 설명
- 추천 이유 작성

핵심 원칙:

> Python이 계산할 수 있는 사실은 Python으로 계산하고,
> Gemini는 요약과 설명에 사용합니다.

## 7. 신규 공고 판별

1차 기준:
- `job_url`

개념:

```text
이전 실행에서 저장한 URL
+
이번 실행에서 수집한 URL
→ 이번에 처음 나타난 URL만 신규 공고
```

필요 시 보조 기준:
- 회사명 + 공고 제목 + 마감일

초기에는 DB 대신 CSV / JSON으로 충분히 구현합니다.

현재 구현: 이력 파일 `data/processed/jobs_history.csv` (`job_url` 기준으로 누적, 중복 제거)

## 8. 크롤링 원칙

처음부터 대량 수집하지 않습니다.

확장 순서:

```text
검색어 1개
→ 페이지 1개
→ 공고 1개
→ 공고 5~10개
→ DataFrame
→ 여러 공고
→ 필요하면 여러 검색어
```

확인할 것:
- 사이트 이용약관
- robots.txt
- 과도한 요청 여부
- HTTP 상태 코드
- 응답 Content-Type
- 페이지 구조

자동 요청이 어렵거나 제한되면 샘플 HTML / CSV로 파이프라인 학습을 계속합니다.

현재 실제 수집 방식 (STEP 04 / 07-A):
- URL: `https://www.jobkorea.co.kr/Search/?stext=ax&tabType=recruit` (검색어 1개, 페이지 1개, 최대 5건)
- 기본 요청이 보안정책 페이지를 받으면, 일반 브라우저 User-Agent 헤더로 **1회만** 다시 요청한다.
- 보안 우회 기법, CAPTCHA 우회, 프록시/IP 변경, 반복 재시도는 사용하지 않는다.
- HTTP 200만 보고 성공으로 판단하지 않고, title과 본문 문자열로 실제 검색 결과인지 확인한다.

## 9. Notebook 작성 규칙

모든 STEP에서 아래 **3셀 세트**를 하나의 작업 단위로 사용합니다. (상세 규칙: `docs/DEVELOPMENT_RULES.md`)

### 1. 작업 계획 — Markdown Cell

- 이번 단계의 목적
- 확인할 항목
- 이번 단계에서 하지 않을 것
- 완료 조건

### 2. 실제 코드 — Code Cell

- 현재 STEP에 필요한 최소 코드
- **확인 출력도 이 Cell 안에서 함께 수행** (별도의 "확인용 Code Cell"을 두지 않음)
  - 예: shape, head, status code, 결측, 중복, 값 분포

### 3. 실행 결과 해석 / 분석 / 요약 — Markdown Cell

- 실행 성공 여부
- 확인한 사실
- 예상과 다른 점
- 다음 단계 진행 가능 여부
- 추가 확인 사항

Notebook은 단순 코드 파일이 아니라 **실행·검증 기록**입니다.

## 10. API Key / 인증정보 관리

코드에 직접 쓰지 않습니다.

로컬:
- `.env`

GitHub:
- Repository Secrets

예정 환경변수:

```text
GEMINI_API_KEY
SLACK_WEBHOOK_URL
GMAIL_USER
GMAIL_APP_PASSWORD
```

`.gitignore` 필수:

```text
.env
.venv/
__pycache__/
.ipynb_checkpoints/
```

- `.env.example`(값이 비어 있는 샘플)은 Git에 포함한다.
- Notebook 출력에는 키 값, 키 일부, 키 길이를 표시하지 않고 "설정됨 / 미설정"만 표시한다.
- Gemini SDK: 공식 패키지 `google-genai` (`from google import genai`) 사용. 구버전 `google-generativeai`는 사용하지 않는다.

## 11. 운영 코드 전환

Notebook에서 단계별 검증이 모두 끝난 뒤 함수로 분리합니다.

예정 함수:

```python
collect_jobs()
clean_jobs(df)
find_new_jobs(df, history_df)
analyze_jobs(df)
summarize_with_gemini(df)
create_report(analysis, summaries)
send_slack(report)
send_email(report)
```

Notebook:
- 실험
- 검증
- 실행 기록

`src/`:
- 재사용 가능한 운영 코드

`main.py`:
- 전체 실행 순서만 조정

## 12. GitHub Actions 원칙

GitHub Actions는 마지막 단계입니다.

조건:
1. `python main.py`가 로컬에서 끝까지 성공
2. 민감정보가 코드에 없음
3. requirements.txt 정리
4. 경로 문제 없음
5. Secrets 등록 완료

먼저:
- `workflow_dispatch` 수동 실행

그 다음:
- 주 1회 schedule

## 13. 최종 완료 기준

- 수집 결과가 존재
- 필수 컬럼 존재
- 중복 검증 완료
- 날짜 변환 검증 완료
- 신규 공고 판별 정상
- pandas 통계 검증
- Gemini 결과 원문 대조 완료
- Markdown 보고서 생성
- Slack 발송 성공
- Gmail 발송 성공
- `python main.py` 로컬 성공
- GitHub Actions 수동 실행 성공
- GitHub Actions 주간 실행 설정 완료
