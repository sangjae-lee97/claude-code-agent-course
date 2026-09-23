# START HERE — AX 채용정보 Agent 프로젝트

이 문서는 프로젝트를 다시 시작할 때 **가장 먼저 읽는 문서**입니다.

## 현재 프로젝트 목적

잡코리아의 AX / AI / 데이터 분석 관련 채용공고를 수집하고,
pandas로 정제·분석한 뒤 Gemini API로 주요 내용을 요약하고,
Markdown 보고서를 생성하여 Slack / Gmail로 전달하고,
최종적으로 GitHub Actions에서 주 1회 자동 실행되는 파이프라인을 만드는 것이 목표입니다.

## 현재 개발 방식

- 개발 환경: Windows + VS Code
- 주 작업 공간: Jupyter Notebook
- Orchestrator: GPT Web
- Local Coding Agent: Claude Code / Codex를 사용량에 따라 교대
- Human Validator: 사용자가 Notebook 셀과 Terminal 결과를 직접 확인
- 원칙: 한 번에 전체 프로그램을 만들지 않고 STEP 단위로 검증

## 프로젝트 위치

```text
저장소: sangjae-lee97/claude-code-agent-course (브랜치 main)
프로젝트 루트: chapter11/ax-job-agent
Notebook: notebooks/ax_job_pipeline.ipynb
```

## 현재 진행 상태

### 완료: STEP 01 ~ 11 (DONE)

- STEP 00 환경 준비 (Fork/Clone, `.venv`, Python 3.14.6, 패키지, 커널 `Python (ax-job-agent)`)
- STEP 01 개발환경 확인
- STEP 02 수집 데이터 명세 (컬럼 9개)
- STEP 03 채용공고 페이지 접근 테스트
- STEP 04 소량 데이터 수집 — 실제 JobKorea `ax` 검색 결과 5건
- STEP 05 DataFrame 기본 구조 확인
- STEP 06 전처리 / 중복 제거
- STEP 07 신규 공고 판별 (`data/processed/jobs_history.csv`)
- STEP 08 기본 분석 / 관련 공고 필터링
- STEP 09 Gemini API 연동 — `.env`/`GEMINI_API_KEY`/`google-genai` 준비, 연결 테스트, 실제 공고 2건 전달
  (에스코어 응답 수신, GS리테일은 503 서버 과부하로 실패)
- STEP 10 Gemini 결과 검증 — 에스코어 응답 1건을 원본 CSV와 비교 (15개 항목, 불일치 0)
- STEP 11 Markdown 보고서 생성 — `reports/ax_job_report.md`

Notebook의 `STEP 07-A` ~ `07-I` 셀은 위 STEP 04~09의 **세부 검증 기록**입니다.
공식 STEP과의 매핑은 `docs/PROGRESS.md`의 "개발 과정 세부 검증 기록"을 참고하세요.
Notebook의 STEP 04~07 샘플 데이터 셀은 과거 프로토타입 기록입니다.

### 현재: STEP 12 Slack 발송 (NOT_STARTED)

### 아직 하지 않음

- STEP 12 Slack 발송 — **다음 단계, 아직 시작하지 않음**
- STEP 13 Gmail 발송
- STEP 14~16 함수화 / `main.py` 통합 / 로컬 전체 실행
- STEP 17~18 GitHub Actions

## 지금 바로 해야 할 다음 작업

**STEP 12 — Slack 발송**

완료 기준 (STEP 진행표 기준):

```text
실제 Slack 채널에 도착한 것을 확인한다.
(발송 대상 보고서: reports/ax_job_report.md)
```

### 이번 STEP에서 하면 안 되는 것

- STEP 13 이후 작업 (Gmail 발송 등)
- API Key 출력 (값, 일부, 길이 모두)
- 불필요한 반복 API 호출
- Slack / Gmail 연동
- `main.py` 작성
- GitHub Actions 작성
- 여러 STEP을 한 번에 구현

### 실행 시 주의

- 실데이터 변수(`df_unique_jobs` 등)는 STEP 07-A → 07-B → 07-C 셀을 실행해야 메모리에 생깁니다.
  (07-A는 실행할 때마다 검색 페이지 요청 2회가 발생)
- STEP 07-D 셀은 실행할 때마다 `jobs_history.csv`를 다시 저장합니다.
- Gemini 호출 셀은 실행할 때마다 API가 호출됩니다.

## 작업 재개 체크리스트

프로젝트를 다시 열 때 아래 순서로 확인합니다.

```text
1. VS Code에서 프로젝트 루트 열기
2. Terminal 현재 경로 확인
3. .venv 활성화 확인
4. git status 확인
5. docs/PROGRESS.md 확인 (docs/DEVELOPMENT_RULES.md 규칙도 함께 확인)
6. 현재 STEP 확인
7. 현재 STEP의 완료 조건 확인
8. Claude Code 또는 Codex에 현재 STEP만 전달
9. 생성된 코드를 Notebook에서 직접 실행
10. 결과 확인 후 PROGRESS.md 갱신
```

## 가장 중요한 원칙

**AI가 코드를 만들었다고 STEP이 완료되는 것이 아닙니다.**

STEP 완료 조건은 항상 다음과 같습니다.

```text
코드 생성
→ 직접 실행
→ 실제 출력 확인
→ 데이터/결과 검증
→ Markdown으로 해석
→ 완료 여부 판단
→ 다음 STEP 진행
```
