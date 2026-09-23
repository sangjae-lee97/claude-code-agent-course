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
└── ai-job-agent/
    ├── docs/
    │   ├── START_HERE.md
    │   ├── PROJECT_SPEC.md
    │   └── PROGRESS.md
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

## 5. 데이터 정의

DataFrame의 한 행:

> 채용공고 1건

초기 컬럼:

| 컬럼 | 의미 |
|---|---|
| company_name | 회사명 |
| job_title | 공고 제목 |
| career | 경력 조건 |
| location | 근무 지역 |
| posted_date | 등록일 |
| closing_date | 마감일 |
| job_url | 공고 URL |
| search_keyword | 공고를 발견한 검색어 |
| collected_at | 수집 시각 |

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

## 9. Notebook 작성 규칙

모든 STEP에서 같은 패턴을 사용합니다.

### Markdown Cell — 작업 계획

- 이번 단계의 목적
- 확인할 항목
- 이번 단계에서 하지 않을 것
- 완료 조건

### Code Cell — 실행

- 현재 STEP에 필요한 최소 코드

### Code Cell — 확인

예:
- shape
- head
- status code
- 결측
- 중복
- 값 분포

### Markdown Cell — 결과 해석

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
```

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
