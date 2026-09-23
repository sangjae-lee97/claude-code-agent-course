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

## 현재 진행 상태

### 완료
- GitHub 원본 저장소 Fork
- Fork 저장소 Local Clone
- `origin` 확인
- `upstream` 연결
- 별도 브랜치 생성은 생략하고 `main`에서 진행하기로 결정
- 프로젝트 폴더 생성
- Python 가상환경 `.venv` 생성
- 가상환경 활성화 확인
- Python 3.14.6 확인
- 필수 패키지 설치
  - pandas
  - requests
  - beautifulsoup4
  - jupyter
  - python-dotenv
- `ipykernel` 설치
- Jupyter 커널 `Python (ax-job-agent)` 등록

### 아직 하지 않음
- `notebooks/ax_job_pipeline.ipynb` 생성
- STEP 01 환경 확인 셀 작성 및 실행
- 실제 크롤링
- DataFrame 생성
- 전처리
- 신규 공고 판별
- 기본 분석
- Gemini API 연동
- 보고서 생성
- Slack / Gmail 연동
- `main.py` 통합
- GitHub Actions

## 지금 바로 해야 할 다음 작업

**STEP 01 — 개발환경 확인용 Notebook 생성**

생성할 파일:

```text
notebooks/ax_job_pipeline.ipynb
```

이번 STEP에서는 아래만 수행합니다.

1. 현재 프로젝트 구조 확인
2. `notebooks/` 폴더 생성
3. Notebook 생성
4. Python 버전 / OS 확인
5. pandas / requests / BeautifulSoup import 확인
6. VS Code에서 커널을 `Python (ax-job-agent)`로 선택
7. 모든 셀을 직접 실행
8. 에러가 없는지 사람이 확인

### 이번 STEP에서 하면 안 되는 것

- 실제 크롤링
- Gemini API 호출
- Slack / Gmail 연동
- `main.py` 작성
- GitHub Actions 작성
- 여러 STEP을 한 번에 구현

## 작업 재개 체크리스트

프로젝트를 다시 열 때 아래 순서로 확인합니다.

```text
1. VS Code에서 프로젝트 루트 열기
2. Terminal 현재 경로 확인
3. .venv 활성화 확인
4. git status 확인
5. docs/PROGRESS.md 확인
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
