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
```

다음 작업:

```text
샘플 DataFrame(df_jobs)의 컬럼 구조 / 결측값 / 중복 여부를 확인한다 (STEP 05)
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
| 05 | DataFrame 생성 | ⏳ 다음 (STEP 04에서 `df_jobs` 이미 생성됨, 검증 필요) | 컬럼/shape/head 확인 |
| 06 | 전처리 / 중복 제거 | ⬜ 대기 | 결측/중복/날짜 처리 검증 |
| 07 | 신규 공고 판별 | ⬜ 대기 | 기존 vs 신규 URL 구분 |
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

현재 단계는 STEP 03 채용공고 페이지 접근 테스트입니다.
STEP 01, STEP 02는 이미 완료되었습니다 (docs/PROGRESS.md 참고).

이번 작업만 수행해 주세요.

1. notebooks/ax_job_pipeline.ipynb에 STEP 03 Markdown Cell을 추가합니다.
2. requests로 잡코리아 채용공고 검색 결과 페이지에 GET 요청을 보내는
   Code Cell을 추가합니다.
3. 응답의 HTTP 상태 코드, Content-Type, 응답 길이를 출력합니다.
4. 초보자가 이해할 수 있도록 간단한 주석을 작성합니다.

하지 말 것:
- 실제 HTML 파싱 / 데이터 추출
- DataFrame 생성
- Gemini API 사용
- Slack / Gmail 구현
- main.py 작성
- 다음 STEP 구현

완료 조건:
- 요청이 정상적으로 응답을 받음 (상태 코드 확인)
- 사용자가 VS Code에서 직접 셀을 실행할 수 있음
- 응답 내용이 예상한 채용공고 검색 결과인지 사람이 직접 확인
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
