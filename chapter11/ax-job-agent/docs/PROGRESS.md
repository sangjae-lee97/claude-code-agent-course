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
STEP 12 Slack 발송                          → DONE  (공고 5건 상세 정보 Slack 전송, 사용자 확인 완료)
STEP 13 Gmail 발송                          → DONE  (자기 자신에게 1회 발송, 받은편지함 도착 사용자 확인)
STEP 14 함수화                              → DONE  (src/ 7개 파일, 로컬 함수 검증, 외부 요청 0회)
STEP 15 main.py 통합                        → DONE  (main.py 생성, main(dry_run=True) 흐름 검증, 외부 요청 0회)
STEP 16 로컬 전체 실행 검증                  → DONE  (python main.py 1회 성공, Slack·Gmail 실제 도착 사용자 확인)
STEP 17 GitHub Actions 수동 실행             → DONE  (Run workflow 성공, Slack·Gmail 실제 도착 사용자 확인)
STEP 18 GitHub Actions 주간 실행             → IN_PROGRESS  (최종 검증 1회 JobKorea ConnectTimeout으로 실패, 연결 오류 메시지 보완 — 재검증 대기)
```

**현재 공식 진행 위치: STEP 18 GitHub Actions 주간 실행 (IN_PROGRESS)**

STEP 18 진행 상황:

```text
완료 (schedule 및 history persistence 준비 완료):
- .github/workflows/ax-job-agent.yml: 이름 "AX Job Agent", workflow_dispatch 유지 + schedule cron "0 0 * * 1"
  (매주 월요일 00:00 UTC = 09:00 KST), permissions contents: write
- main.py 성공 뒤 "Persist updated history" step: history CSV 하나만 변경 시 commit/push
  (git add "$HISTORY_FILE", 메시지 "chore: update AX job history", GITHUB_TOKEN 사용, 새 Secret·PAT 없음, 보고서 commit 없음)
- src/reporter.py 8장 기본 문구 → "GitHub Actions 주간 자동 실행 운영 (매주 월요일 09:00 KST), 실행 결과는 Slack / Gmail에서 확인"
- Notebook STEP 18 정적 검증 통과, 임시 Git 저장소로 history 저장 step 사전 시험 통과 (외부 요청 0회)

진행 중 확인된 사항:
- 사용자가 push(6af850e) 후 수동 실행 → 봇 commit adbe833 "chore: update AX job history" 생성,
  변경 파일은 chapter11/ax-job-agent/data/processed/jobs_history.csv 하나뿐 (git show로 확인)
- STEP 18 최종화 전에 Slack/Gmail 출력 정합성 문제 발견 → 보완 완료 (아래 상세 기록 참고, 새 STEP 번호 없음)
- 출력 정합성 보완 push 후 GitHub Actions 최종 검증 실행 → **JobKorea ConnectTimeout으로 실패** (수집 단계 이전 종료,
  Slack·Gmail·history commit 미실행) → 연결 오류 메시지 보완 완료 (아래 상세 기록 참고)

남은 작업 (사용자):
- 로컬이 origin/main보다 1 commit 뒤처짐(봇 commit) → git pull 후 보완 내용 push
- GitHub Actions에서 "AX Job Agent" workflow에 schedule 표시 확인
- 수정된 workflow를 수동으로 1회 실행 → 전체 성공, Persist history step 성공, Slack·Gmail 도착,
  main에 "chore: update AX job history" commit 생성(history CSV 한 파일만), 비밀값 노출 없음, 반복 실행 없음 확인
- 확인 후 STEP 18 DONE → 공식 STEP 01 ~ 18 전체 완료
```

STEP 17 결과 요약 (DONE):

```text
- 사용자 GitHub Actions 수동 실행 결과: "AX Job Agent - Manual Run" 전체 성공, python main.py 끝까지 성공
  JobKorea 수집 5건 / 전처리 5건 / 신규 0건 / 관련 5건 / Gemini 2회 호출·2건 성공 / 보고서 3456자
  / Slack HTTP 200 ok, 실제 채널 도착 확인 / Gmail SMTP 성공, 실제 받은편지함 도착 확인 / 비밀값 노출 없음
- GitHub runner(IP)에서도 JobKorea 수집 성공 (User-Agent 1회 재요청 방식 그대로)

준비 내용 (workflow/requirements):
- 저장소 루트 .github/workflows/ax-job-agent.yml ("AX Job Agent - Manual Run")
  workflow_dispatch만, contents: read, ubuntu-latest, Python 3.14, working-directory chapter11/ax-job-agent,
  Secrets 4개를 환경변수로 주입, pip install -r requirements.txt → python main.py, commit/push 없음
- chapter11/ax-job-agent/requirements.txt (pandas, requests, beautifulsoup4, python-dotenv, google-genai)
- src/reporter.py 8장 기본 문구: "Slack / Gmail 발송" → "GitHub Actions에서 자동 실행 검증"
- Notebook STEP 17 정적 검증 통과 (외부 요청 0회)

```

STEP 16 결과 요약 (DONE):

```text
- src/reporter.py 검증 문구 수정: 5장 "이번 실행에서 Gemini가 생성한 설명(검증 전)" / 6장 "[과거 검증 기록]"(STEP 10 에스코어 당시 응답)
- python main.py 1회 실행 → 종료 코드 0, 12단계 모두 완료
  수집 5건(결측 0, 중복 0) / 신규 0건 / history 5 → 5 / 관련 5건 / Gemini 2회 호출(GS리테일 성공, 에스코어 503 실패, 파이프라인 계속 진행)
  / 보고서 3674자 저장 / Slack HTTP 200 ok / Gmail SMTP 성공 / 비밀값 노출 없음
- 사용자 확인: Slack 실제 채널 도착, Gmail 실제 받은편지함 도착
```

STEP 15 결과 요약 (DONE):

```text
- main.py 생성 (프로젝트 루트): main(dry_run=False), if __name__ == "__main__": main()
- src 함수를 순서대로 연결: 수집 → 전처리 → 신규 판별/이력 업데이트 → 필터 → 분석 → Gemini → 보고서 → Slack 메시지
  → (실제 실행 시) history·보고서 저장 → Slack 발송 → Gmail 발송
- main(dry_run=True) 검증: history CSV 5건 입력, clean 5, 신규 0, 필터 5, 분석 동일, 보고서 2662자, Slack 1398자
- JobKorea·Gemini·Slack·Gmail 호출 0회, history·report 체크섬 동일, 비밀값 노출 없음, src 수정 없음
```

STEP 14 결과 요약 (DONE):

```text
- src/ 생성: __init__.py, crawler.py, preprocess.py, analyzer.py, gemini_client.py, reporter.py, notifier.py
- Notebook 검증 로직을 동작 변경 없이 함수로 분리 (리팩터링)
- 로컬 데이터(jobs_history.csv 읽기 전용) 검증: clean 5→5, 신규 0, 분석 값 이전과 동일,
  안전 키워드 8/8, 필터 5/5, 보고서 문자열 생성, Slack 메시지 = 사용자 최종본과 동일
- 외부 요청 함수(collect_jobs, summarize_with_gemini, send_slack, send_email)는 callable 확인만
- 실제 외부 요청 0회 (네트워크 차단 상태로 검증), history CSV·보고서 변경 없음
```

STEP 13 결과 요약 (DONE):

```text
- Notebook "STEP 13. Gmail 발송" 3셀 (보고서 읽기, Plain Text 메일, SMTP_SSL 1회 발송)
- 사용자가 .env에 GMAIL_USER / GMAIL_APP_PASSWORD(앱 비밀번호) 입력 후 실행 (사용자 확인 결과):
  GMAIL_USER·GMAIL_APP_PASSWORD 설정 성공, 보고서 3331자 읽기, 이메일 본문 3403자,
  Gmail SMTP 발송 성공, 발송 횟수 1, 실제 Gmail 받은편지함 도착 확인
```

STEP 12 결과 요약 (DONE):

```text
완료:
- 1차 전송 (STEP 12. Slack 발송 셀, 사용자가 VS Code에서 실행):
  SLACK_WEBHOOK_URL 설정, 실제 채널 도착, 한글 정상, 보고서 전체 전달 — 사용자 확인
  문제: 일반 Markdown(#, ##, **굵게**, 표, 일부 링크, 역슬래시)이 Slack에서 기호 그대로 보임
- 보완 전송 1 (STEP 12. Slack 메시지 포맷 보완 셀): Slack 전용 요약 메시지(1047자, 공고 5건) 1회 재전송
  → HTTP 200 / 응답 "ok", Webhook URL 미노출
- 보완 전송 2 (STEP 12. Slack 메시지 포맷 보완 (공고별 상세 정보) 셀):
  공고 5건 × CSV 컬럼 9개 전부 표시(1393자) 1회 전송 → HTTP 200 / 응답 "ok", Webhook URL 미노출
- 보완 전송 3 (STEP 12. Slack 메시지 포맷 보완 (공고 URL 표시) 셀):
  공고마다 "공고 URL: https://..." 문자열 추가(1703자) 1회 전송 → HTTP 200 / 응답 "ok", Webhook URL 미노출

- 사용자 최종 확인 (Slack 화면): 메시지 도착, 공고 5건 모두 표시, 회사명·제목·경력·지역·지원 시작일·마감일·
  검색어·수집 시각·실제 공고 URL 표시, 한글 정상, 마지막 제한 사항까지 표시
- URL이 2번 보이던 부분은 사용자가 직접 수정 (공고 URL 표시 셀에서 "공고 보기" 링크 줄 삭제)
```

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
STEP 18 GitHub Actions 주간 실행 (IN_PROGRESS)
push → updated workflow("AX Job Agent") 수동 검증 1회 → history 자동 commit 확인
실패해도 바로 다시 실행하지 않고 로그를 먼저 확인한다.
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
| 12 | Slack 발송 | ✅ DONE | 실제 채널 도착 확인 | STEP 12 발송 / 포맷 보완 / 공고별 상세 / 공고 URL 표시 (사용자 확인 완료) |
| 13 | Gmail 발송 | ✅ DONE | 실제 메일 도착 확인 | STEP 13 (1회 발송, 사용자 수신 확인) |
| 14 | 함수화 | ✅ DONE | Notebook 코드를 src로 분리 | STEP 14 (`src/` 7개 파일, 로컬 검증) |
| 15 | main.py 통합 | ✅ DONE | 전체 순서 연결 | STEP 15 (`main.py`, dry_run 검증) |
| 16 | 로컬 전체 실행 검증 | ✅ DONE | `python main.py` 성공 | STEP 16 (실행 성공, Slack·Gmail 도착 사용자 확인) |
| 17 | GitHub Actions 수동 실행 | ✅ DONE | Run workflow 성공 | STEP 17 (수동 실행 성공, Slack·Gmail 도착 사용자 확인) |
| 18 | GitHub Actions 주간 실행 | ⏳ IN_PROGRESS | schedule 등록 | STEP 18 (schedule·history persistence 준비, push·GitHub 검증 대기) |

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

### STEP 12 Slack 발송 (완료)

- Notebook 셀 제목: `# STEP 12. Slack 발송`, Notebook 마지막에 3셀 세트 추가 (기존 셀 수정 없음)
- 코드 흐름:
  - `.env` 로드 → `SLACK_WEBHOOK_URL`은 "설정됨 / 미설정"만 출력 (값 미출력)
  - `reports/ax_job_report.md` 읽기 (수정 없음, 체크섬 동일) — 3331자
  - Markdown 링크만 Slack 형식으로 변환: `[링크](URL)` → `<URL|링크>` (5개), 다른 문법은 변환하지 않음
  - 단순 `{"text": ...}` payload, Webhook URL이 있을 때만 `requests.post` **1회** (재시도 없음)
  - 오류 시 오류 메시지 안의 Webhook URL은 `***`로 가림
- 실제 실행 결과: `.env`에 `SLACK_WEBHOOK_URL=` 줄은 있으나 **값이 비어 있음** → **Slack 요청 0회**
- 가짜 Webhook 주소 + 가짜 `requests.post`로 흐름만 점검 (실제 네트워크 요청 없음):
  요청 1회에서 멈춤, 남은 Markdown 링크 0개, 메시지 3375자
- 예상 표시 문제 (사용자 확인 필요): Slack `text` 메시지는 Markdown 표·`#` 제목·`**` 굵게를 그대로 기호로 보여 줄 수 있음

1차 전송 (사용자 실행):
- 사용자가 `.env`에 `SLACK_WEBHOOK_URL`을 입력하고 VS Code에서 STEP 12 셀 실행
- 결과 (사용자 확인): 실제 채널 도착, 한글 정상, 보고서 전체 내용 전달 성공
- 문제: 일반 Markdown 원문을 그대로 보내서 Slack에서 `#`/`##`, `**굵게**`, Markdown 표, 일부 링크, 역슬래시가 기호 그대로 보임
- 참고: Notebook 파일에 저장된 STEP 12 셀 출력은 Claude Code 실행 시점("미설정")의 것 (사용자 실행 출력은 파일에 저장되지 않음)

보완 전송 — `# STEP 12. Slack 메시지 포맷 보완` 셀 (Notebook 마지막 3셀 추가, 기존 STEP 12 셀 수정 없음):
- 보고서 전체 대신 **Slack 전용 요약 메시지**를 새로 구성 (보고서 재생성 없음)
  - `jobs_history.csv`(읽기 전용)로 분석 기준·회사별·지역별 공고 수·날짜 범위 다시 계산
  - Gemini 검증 결과는 STEP 10 값(일치 7 / 의미상 일치 3 / 불일치 0 / 검증 불가 5)
  - 주요 공고 5건 (수집 순서 그대로, 추천 순위 없음), 회사명·제목·`<URL|공고 보기>` 링크
  - 제한 사항 5개
- Slack mrkdwn 최소 문법만 사용: `*굵게*`, `•`, `<URL|표시문구>` — `#`, `**`, 표, `[링크](URL)` 미사용 (전송 전 검사로 확인)
- 회사명·제목의 `&`, `<`, `>`는 Slack 규칙대로 `&amp;` 등으로 변환 (`HRD & AX`)
- 메시지 **1047자**, Slack 요청 **1회** (자동 재시도 없음)
- 결과: **HTTP 200 / 응답 본문 "ok"**, 저장된 셀 출력에 Webhook URL 없음 확인
- 보고서 파일·history CSV 체크섬 동일
- 사용자 확인 후 추가 요청: 공고별로 CSV의 정보를 가능한 한 모두 표시

보완 전송 2 — `# STEP 12. Slack 메시지 포맷 보완 (공고별 상세 정보)` 셀 (Notebook 마지막 3셀 추가, 기존 셀 수정 없음):
- 공고 5건을 CSV 순서 그대로 `*번호. 회사명*` + `•` 항목 8개 + `<URL|공고 보기>` 형식으로 표시
  (공고 제목, 경력, 지역, 지원 시작일, 지원 마감일, 검색어, 수집 시각, 링크 — CSV 컬럼 9개 전부)
- 메시지 첫 부분에 "공고 번호는 수집 순서이며 추천 순위가 아닙니다" 안내
- Gemini 검증 결과, 제한 사항 포함, Slack mrkdwn 최소 문법만 사용 (전송 전 검사: `#`, `**`, 표, `[..](..)` 없음, 링크 5개)
- 메시지 **1393자**, Slack 요청 **1회** → **HTTP 200 / "ok"**, Webhook URL 미노출, 보고서·CSV 체크섬 동일
- 참고: 5건 모두 수집 시각이 `2026-09-23 14:00:39`로 같음 (STEP 07-D에서 한 번에 저장)
- 사용자 추가 요청: "공고 보기" 링크와 함께 실제 URL 문자열도 표시

보완 전송 3 — `# STEP 12. Slack 메시지 포맷 보완 (공고 URL 표시)` 셀 (Notebook 마지막 3셀 추가, 기존 셀 수정 없음):
- 보완 전송 2 형식에 공고마다 `• 공고 URL: https://...` 줄 추가 (history CSV `job_url` 값 그대로), `<URL|공고 보기>` 링크 유지
- 전송 전 검사: 표시된 URL 5개가 CSV 값·순서와 완전히 같음, 링크 5개, `#`·`**`·표 없음
- 메시지 **1703자**, Slack 요청 **1회** → **HTTP 200 / "ok"**, Webhook URL 미노출, 보고서·CSV 체크섬 동일
- 사용자 최종 확인 완료 (Slack 화면): 도착, 공고 5건, 회사명·제목·경력·지역·지원 시작일·마감일·검색어·수집 시각·
  실제 공고 URL 표시, 한글 정상, 마지막 제한 사항까지 표시 → **STEP 12 DONE**
- 사용자 직접 수정: URL이 2번 보이던 부분 → "공고 URL 표시" 셀에서 `• <URL|공고 보기>` 줄 삭제 (공고 URL 문자열만 남김)

### STEP 13 Gmail 발송 (완료)

- Notebook 셀 제목: `# STEP 13. Gmail 발송`, Notebook 마지막에 3셀 세트 추가 (기존 셀 수정 없음)
- 코드 흐름:
  - `.env` 로드 → `GMAIL_USER`, `GMAIL_APP_PASSWORD`는 "설정됨 / 미설정"만 출력 (주소·비밀번호·일부·길이 미출력)
  - 둘 중 하나라도 없으면 SMTP 연결·발송 없이 멈춤
  - `reports/ax_job_report.md` 읽기 (수정 없음) — 3331자
  - 제목 `[AX Job Agent] AX 채용 분석 보고서`, 본문은 안내 문장 + 보고서 Markdown (Plain Text, 3403자)
  - 발신 = 수신 = `GMAIL_USER` (다른 주소 하드코딩 없음)
  - `smtplib.SMTP_SSL("smtp.gmail.com", 465)` → `login` → `send_message` **1회** (자동 재시도 없음)
  - 오류 시 오류 메시지 안의 주소·비밀번호는 `***`로 가림
  - 표준 라이브러리만 사용 (`smtplib`, `email.message.EmailMessage`) — 추가 설치 없음
- 실제 실행 결과: `.env`에 두 줄은 있으나 **값이 비어 있음** → **발송 0회**, 오류 없음, 인증정보 노출 없음
- 가짜 계정·가짜 SMTP 서버로 흐름만 점검 (네트워크 없음): 1회 발송, 한글 제목 복원, UTF-8 본문,
  보고서 전체·공고 URL 5개 포함, From == To
- 사용자 실행 (인증정보 입력 후 STEP 13 셀 1회 실행, 사용자 확인 결과):
  GMAIL_USER·GMAIL_APP_PASSWORD 설정 성공, 보고서 3331자, 이메일 본문 3403자,
  **Gmail SMTP 발송 성공, 발송 횟수 1, 실제 Gmail 받은편지함 도착 확인** → STEP 13 DONE
- 참고: Notebook 파일에 저장된 STEP 13 셀 출력은 Claude Code 실행 시점("미설정")의 것

### STEP 14 함수화 (완료)

- `src/` 생성 (7개 파일) — Notebook 검증 로직을 동작 변경 없이 함수로 분리 (리팩터링):

| 파일 | 함수 | 옮겨 온 로직 |
|---|---|---|
| `__init__.py` | (빈 파일) | 패키지 인식용 |
| `crawler.py` | `collect_jobs(search_keyword="ax", max_jobs=5)` + `fetch_search_page`, `extract_application_periods`, `parse_job_cards` | STEP 07-A |
| `preprocess.py` | `clean_jobs(df)`, `find_new_jobs(current_df, history_df)`, `update_history(current_df, history_df)` | STEP 06, 07-C, 07-D |
| `analyzer.py` | `analyze_jobs(df)`, `find_matched_keywords_safe(title)`, `filter_relevant_jobs(df)`, `RELEVANCE_KEYWORDS` | STEP 07-E, 07-F, 07-G |
| `gemini_client.py` | `summarize_with_gemini(df, client, model="gemini-3.6-flash", max_jobs=2)`, `build_prompt(job)` | STEP 09 |
| `reporter.py` | `create_report(jobs_df, analysis, gemini_summary=None, validation_summary=None, ...)`, `save_report(report_text, report_path)` | STEP 11 |
| `notifier.py` | `build_slack_message(jobs_df, validation_summary=None)`, `send_slack(message, webhook_url)`, `send_email(report_text, gmail_user, gmail_app_password, subject=...)` | STEP 12, 13 |

- 유지한 규칙: posted_date/closing_date = applicationPeriod.start/end (createdAt 미사용), job_url 기준 식별·history(keep="last"),
  User-Agent 1회만 재요청(우회 없음), 영문 키워드 안전 매칭, Gemini "제공된 정보만/확인 불가", Slack 공고 URL 1회 표시(사용자 최종본),
  인증정보는 인자로만 받음(하드코딩 없음), 발송 함수는 1회·자동 재시도 없음, 오류 메시지 속 비밀값은 `***`로 가림
- 함수는 결과를 반환하고 파일 저장은 분리 (`save_report`, history CSV 저장은 main.py 단계에서 결정)
- 함수화하면서 달라진 점:
  - `create_report()`의 5장은 `summarize_with_gemini()` 결과 1건의 응답 원문을 인용 블록으로 싣는다 (STEP 11은 응답을 소제목별로 나눠 적었음)
  - `create_report()` / `build_slack_message()`의 검증 결과와 추가 제한 사항은 인자(`validation_summary`, `extra_limitations`)로 받는다
  - `summarize_with_gemini()`는 실패한 공고에 `error`(오류 종류: 메시지)를 함께 담아 반환한다 (Notebook은 print로 출력)
- Notebook `# STEP 14. 함수화` 3셀 추가 (기존 셀 수정 없음) — 로컬 데이터(`jobs_history.csv` 읽기 전용) 검증 결과:
  - `clean_jobs`: 5 → 5, 중복 URL 0, 컬럼 유지
  - `analyze_jobs`: 이전 STEP 값과 동일 (NAVER 2 등, 시작일 2026-07-01 ~ 2026-09-21, 마감일 2026-09-29 10:00 ~ 2026-10-25 23:00)
  - `find_matched_keywords_safe`: 대표 테스트 **8/8 통과**
  - `filter_relevant_jobs`: 5 → 5 (모두 AX)
  - `find_new_jobs`: 현재 vs 같은 history → 신규 **0건**
  - `create_report`: str, 2514자 (Gemini 결과 미포함 상태), 주요 제목 9개 포함 — 파일 저장 안 함
  - `build_slack_message`: 1398자, 공고 5건·날짜·URL 포함, "공고 보기" 없음 — 사용자 최종 Slack 메시지와 글자까지 동일(별도 비교)
  - 외부 함수 `collect_jobs`, `summarize_with_gemini`, `send_slack`, `send_email`, `save_report`: callable True (실행 안 함)
- 네트워크 없이 추가 확인 (Notebook 미저장): 저장해 둔 실제 검색 결과 HTML 파싱 결과 = history CSV(수집 시각 제외),
  `build_prompt` = STEP 09 프롬프트, 가짜 client/서버로 호출 횟수(Gemini 최대 2회, Slack·Gmail 1회)와 비밀값 마스킹 확인
- 실제 외부 요청 **0회** (검증 시 네트워크 연결 차단·계수: 0), history CSV·`reports/ax_job_report.md` 체크섬 동일
- `src/__pycache__/`는 `.gitignore`의 `__pycache__/` 규칙으로 Git에서 제외됨

### STEP 15 main.py 통합 (완료)

- `main.py` 생성 (프로젝트 루트) — 설정 읽기와 실행 순서 연결만 담당, 로직은 src 함수 호출
  - 경로: `PROJECT_ROOT = Path(__file__).resolve().parent`, `HISTORY_PATH`, `REPORT_PATH`, `ENV_PATH`
  - 설정: `SEARCH_KEYWORD="ax"`, `MAX_JOBS=5`, `GEMINI_MODEL="gemini-3.6-flash"`, `GEMINI_MAX_JOBS=2`
  - `VALIDATION_SUMMARY`: STEP 10 검증 결과(에스코어 1건, 15개 항목, 일치 7 / 의미상 일치 3 / 불일치 0 / 검증 불가 5)와 STEP 11 보고서의 검증 설명
  - `main(dry_run=False)` 실행 순서:
    [1] `.env` 로드(설정 여부만 출력) → [2] `collect_jobs()` → [3] `clean_jobs()` → [4] history 읽기 → `find_new_jobs()` / `update_history()`
    → [5] `filter_relevant_jobs()` → [6] `analyze_jobs()` → [7] Gemini client 생성 + `summarize_with_gemini()`
    → [8] `create_report()` → [9] `build_slack_message()` → [10] history CSV 저장 + `save_report()` → [11] `send_slack()` → [12] `send_email()`
  - 인증정보 부족 처리: GEMINI_API_KEY 없으면 [7]에서 RuntimeError로 중단, Slack·Gmail 인증정보 없으면 해당 발송만 생략
  - Gemini 실패 공고는 보고서 제한 사항에 "○○ 공고의 Gemini 호출은 실패했습니다" 로 추가 (`extra_limitations`)
  - 결과 요약 dict 반환 (건수, 문자 수, 호출·발송 여부)
- `dry_run=True`: JobKorea 대신 history CSV를 입력으로 사용, Gemini·Slack·Gmail 호출과 history·report 저장을 하지 않음
- 설계 판단 (데이터 역할):
  - `current_df`(이번 수집 전체) / `new_jobs_df`(신규) / `filtered_df`(관련 공고, 분석·Gemini 대상)를 변수로 분리
  - 보고서·Slack 대상(`report_jobs_df`, `notify_jobs_df`)은 **이번 수집 전체**로 유지 — Notebook(STEP 07-E ~ 12)이 현재 공고 전체를 대상으로 했고,
    "신규 공고만 알림" 동작은 아직 확정된 적이 없기 때문 (신규 공고 기준으로 바꿀지는 이후 Orchestrator가 결정)
  - Gemini 대상은 `filtered_df` 앞 2건 (STEP 09 흐름), 보고서 5장에는 성공한 첫 응답
- Notebook `# STEP 15. main.py 통합` 3셀 추가 (기존 셀 수정 없음) — `main(dry_run=True)` 결과:
  - 환경변수 4개 "설정됨", 입력 5건, clean 5, 신규 0 (이력 5 → 5), 필터 5, 분석 동일(NAVER 2 등)
  - 보고서 문자열 2662자 (Gemini 미호출로 5장 "결과 없음"), Slack 메시지 1398자
  - 실행 전후 history CSV·report 체크섬 동일
  - 검증 시 네트워크 차단 + 외부/저장 함수 호출 감지: 네트워크 연결 0회, `collect_jobs`·`summarize_with_gemini`·`send_slack`·`send_email`·`save_report`·`to_csv` 호출 0회
- `main.py`에 비밀값 형식 문자열 없음, src 파일 수정 없음
- STEP 16에서 확인할 점:
  - 실제 실행은 history CSV와 `reports/ax_job_report.md`를 **덮어쓴다**
  - `reporter`의 5장 문구 "STEP 10에서 원본 데이터와 비교 검증했습니다"가 고정되어 있어, 실제 실행에서 새로 받은 (검증 전) Gemini 응답에도 붙는다 → 표현 확인 필요 (STEP 16에서 수정)

### STEP 16 로컬 전체 실행 검증 (완료)

실행 전 수정 — `src/reporter.py` (검증 문구, 최소 수정. main.py·다른 src 수정 없음):
- 5장 `[Gemini 생성 설명]`: "이번 실행에서 Gemini가 생성한 설명입니다. 이 응답은 아직 원본 데이터와 비교 검증하지 않았습니다."
- 6장 `[과거 검증 기록]`(기존 `[STEP 10 검증 결과]`): "STEP 10에서 ○○ 공고의 당시 Gemini 응답을 원본과 비교한 기록 — 이번 실행의 새 응답 전체를 검증했다는 뜻은 아님"
- 보고서 첫 부분 이름표 설명과 7장 제한 사항 문장도 같은 의미로 수정
- 수정 후 네트워크 차단 상태에서 `create_report()`만 로컬 데이터로 호출해 문구 확인

실행 전 상태 (체크섬만 기록, 백업은 Git 밖 임시 폴더):
- 환경변수 4개(GEMINI_API_KEY, SLACK_WEBHOOK_URL, GMAIL_USER, GMAIL_APP_PASSWORD) 모두 설정됨
- `jobs_history.csv`: 5행, SHA256 `14ddb83c…02fe`
- `reports/ax_job_report.md`: 3331자, SHA256 `f0573bef…f5a6`

실제 실행 — Terminal, 프로젝트 루트, `python main.py` **1회** (콘솔 한글 출력 오류 방지를 위해 `PYTHONIOENCODING=utf-8`만 설정), 종료 코드 **0**:
- [2] JobKorea 수집 **5건** — 컬럼 9개, 결측 0, `job_url` 중복 0, 이전과 같은 5개 공고·같은 지원 시작일/마감일
- [4] 신규 공고 **0건**, history 5건 → 5건 (같은 URL 중복 누적 없음, `collected_at`만 `14:00:39` → `16:31:15`로 갱신 — keep="last")
- [5] 관련 공고 5건, [6] 분석 전체 5건
- [7] Gemini **2회** 호출: GS리테일 **성공**, 에스코어 **실패** (`ServerError 503 UNAVAILABLE`, 서버 과부하) — 자동 재시도 없음, 파이프라인은 계속 진행
- [8]·[10] 보고서 **3674자** 저장, 제목 + 8개 장, 5장에 GS리테일 새 응답("확인 불가" 4개 유지), 6장 과거 검증 기록, 7장에 에스코어 실패 기록
- [11] Slack **1회**, HTTP 200 / ok
- [12] Gmail **1회**, SMTP 발송 성공
- 실행 후 SHA256: history `98e2e8ba…ca5a`, report `868fb846…28c4`
- 비밀값 노출 없음 (출력·보고서·history·코드 확인)
- Notebook `# STEP 16. 로컬 전체 실행 검증` 3셀 추가 — 코드 셀은 결과 파일을 읽기만 함 (main.py 재실행 없음, 네트워크 연결 0회)
- 참고: 보고서 8장 "다음 단계"가 `create_report()` 기본값 "Slack / Gmail 발송"으로 남아 있어 실제 상태와 맞지 않음 (후속 수정 후보)
- 사용자 최종 확인 완료: Slack 실제 채널 도착, Gmail 실제 받은편지함 도착 → **STEP 16 DONE**

### STEP 17 GitHub Actions 수동 실행 (완료)

준비한 파일 (Claude Code는 commit/push 하지 않음 — 사용자가 직접 올림):
- `.github/workflows/ax-job-agent.yml` (저장소 루트 — GitHub 규칙상 workflow는 저장소 루트 `.github/workflows/`에 있어야 함)
  - 이름 `AX Job Agent - Manual Run`, 트리거 `workflow_dispatch`만 (`schedule` 없음 — STEP 18)
  - `permissions: contents: read`, `runs-on: ubuntu-latest`, `defaults.run.working-directory: chapter11/ax-job-agent`
  - `env`: `GEMINI_API_KEY`, `SLACK_WEBHOOK_URL`, `GMAIL_USER`, `GMAIL_APP_PASSWORD` ← `${{ secrets.이름 }}`, `PYTHONIOENCODING: utf-8`
  - steps: `actions/checkout@v4` → `actions/setup-python@v5` (Python `3.14`) → `pip install -r requirements.txt` → `python main.py`
  - actions 버전은 이 저장소의 기존 workflow(fast-track-smoke, resource-smoke 등)와 같게 맞춤
  - git commit/push 없음, Artifact 업로드 없음
- `chapter11/ax-job-agent/requirements.txt`: `pandas`, `requests`, `beautifulsoup4`, `python-dotenv`, `google-genai`
  - main.py·src의 외부 import(bs4, dotenv, google, pandas, requests)와 1:1 대응, jupyter·ipykernel 제외
  - 버전 고정 없음 (로컬 검증 버전은 파일 주석에 기록: pandas 3.0.6, requests 2.34.2, beautifulsoup4 4.15.0, python-dotenv 1.2.3, google-genai 2.25.0)
- `src/reporter.py`: `create_report()`의 `next_step_text` 기본값 "Slack / Gmail 발송" → "GitHub Actions에서 자동 실행 검증" (최소 수정, main.py 수정 없음)

확인한 점:
- `.env`가 없는 환경에서 `load_dotenv()`는 오류 없이 넘어가고 이미 주입된 환경변수를 유지 → GitHub Secrets를 `os.getenv()`로 읽음 (로컬 확인)
- Notebook `# STEP 17. GitHub Actions 수동 실행` 3셀 — 정적 검증 모두 통과 (YAML 파싱, workflow_dispatch, schedule 없음, 권한 read, 경로,
  Secret 이름 4개, `python main.py`, commit/push 없음, 비밀값 형식 문자열 없음, requirements와 import 일치), 외부 요청 0회
  - "schedule 없음" 검사가 처음에는 주석 속 단어 때문에 False → 트리거 설정만 보도록 검사를 고쳐 True 확인
- 기존 `resource-policy-guard.yml`은 chapter01~10만 검사하므로 chapter11 파일과 충돌하지 않음

STEP 18에서 판단할 사항 (history / report 유지):
- GitHub-hosted runner에서 갱신된 `data/processed/jobs_history.csv`와 `reports/ax_job_report.md`는 **실행이 끝나면 사라진다.**
- STEP 17에서는 자동 commit/push를 하지 않으므로, 매번 checkout된(Git에 있는) history 기준으로 신규 판별이 된다.
- 주간 자동 실행에서 신규 공고 판별이 의미 있으려면 history를 실행 사이에 유지하는 방법이 필요하다. (방식은 STEP 18에서 결정)

예상 위험 (실제 결과를 그대로 기록할 것):
- runner는 GitHub 서버 IP에서 실행되므로 JobKorea가 보안정책 페이지를 줄 수 있음 → `collect_jobs()` RuntimeError로 workflow 실패 가능. 우회하지 않음
- Gemini 503은 개별 공고 실패로 기록되고 파이프라인 계속 진행 (자동 재시도 없음)

사용자 실행 결과 (Secrets 4개 등록 → push(`d80dbfe`) → Run workflow 1회):
- "AX Job Agent - Manual Run" 전체 성공, `python main.py` 끝까지 성공
- JobKorea 수집 5건 (GitHub runner IP에서도 성공), 전처리 5건, 신규 0건, 관련 5건
- Gemini 2회 호출, 2건 성공 (로컬 STEP 16과 달리 503 없음)
- 보고서 3456자 생성 (runner 안에서만, commit 없음)
- Slack HTTP 200 / ok, 실제 채널 도착 사용자 확인
- Gmail SMTP 발송 성공, 실제 받은편지함 도착 사용자 확인
- 로그에 비밀값 노출 없음 → **STEP 17 DONE**

### STEP 18 GitHub Actions 주간 실행 (진행 중)

`.github/workflows/ax-job-agent.yml` 변경 (main.py, requirements.txt, 다른 src 수정 없음):
- 이름: `AX Job Agent - Manual Run` → `AX Job Agent`
- 트리거: `workflow_dispatch` 유지 + `schedule: - cron: "0 0 * * 1"`
  - cron은 UTC 기준: 매주 월요일 00:00 UTC = **매주 월요일 09:00 KST**
  - GitHub Actions schedule은 정확한 시각을 보장하지 않음 → "월요일 오전 9시 전후 자동 실행"
- 권한: `contents: read` → `contents: write` (history push용, 그 외 권한 없음)
- Secret: 기존 4개 그대로 (새 Secret·PAT 없음, 기본 `GITHUB_TOKEN`으로 push)
- 마지막 step `Persist updated history` 추가 (`python main.py` 뒤 — 앞 step이 실패하면 실행되지 않음):
  - `working-directory: .` (저장소 루트), `HISTORY_FILE="chapter11/ax-job-agent/data/processed/jobs_history.csv"`
  - `git diff --quiet -- "$HISTORY_FILE"`로 변경이 없으면 "history 변경 없음 — commit 생략"
  - 변경이 있으면 `github-actions[bot]` 사용자로 `git add "$HISTORY_FILE"` (그 파일 하나만) → `git commit -m "chore: update AX job history"` → `git push`
  - `git add .` 없음, 보고서(`reports/ax_job_report.md`)는 commit하지 않음 (Slack/Gmail로 전달되므로)
- `src/reporter.py`: `next_step_text` 기본값 → "GitHub Actions 주간 자동 실행 운영 (매주 월요일 09:00 KST), 실행 결과는 Slack / Gmail에서 확인"

검증 (외부 요청 0회):
- Notebook `# STEP 18. GitHub Actions 주간 실행` 3셀 — 정적 검증 모두 통과
  (workflow_dispatch·schedule 존재, cron `0 0 * * 1` 1개, 그 외 트리거 없음, `contents: write`만, Secret 4개만,
  `python main.py`, history step이 main 실행 뒤, `git add` 대상 history 하나, `git add .`·보고서 add 없음, commit 메시지, `git push`, PAT 없음)
- 임시 Git 저장소(로컬 bare 원격)로 history 저장 step 스크립트 사전 시험:
  변경 없음 → commit 생략 / history + 보고서 동시 변경 → 원격 commit에 history CSV 한 파일만 포함

설계 특이사항:
- 현재 history는 같은 공고 재수집 시 `collected_at`을 최신 시각으로 갱신하므로(keep="last"),
  **신규 공고가 0건이어도 history commit이 발생할 수 있다.** 처음 발견 시각 보존 방식은 향후 개선 후보다.
- 반복 실행: 이 workflow에는 `push` 트리거가 없고, GitHub는 `GITHUB_TOKEN`으로 만든 push로 새 workflow 실행을 만들지 않는다
  → 자동 commit이 이 workflow나 기존 push 트리거 workflow(Resource Smoke Test, Resource Policy Guard, Fast Track Smoke Test)를 다시 실행시키지 않을 것으로 예상 (실제 실행에서 확인)
- 자동 push 직전에 다른 commit이 main에 먼저 올라가면 push가 거절될 수 있음 (자동 재시도 없음, 발생 시 로그로 판단)
- 향후 개선 후보 (이번 STEP에서 구현하지 않음): 신규 공고 0건이면 알림 생략, 신규 공고만 Gemini 요약, 신규 공고만 Slack/Gmail

상태: schedule 및 history persistence 준비 완료, push 및 GitHub 검증 대기

#### STEP 18 최종화 전 보완 — 운영 출력 정합성 (새 STEP 아님)

발견한 문제:
- Slack이 main.py의 고정값 `VALIDATION_SUMMARY`(STEP 10 과거 에스코어 검증: 일치 7 / 의미상 일치 3 / 불일치 0 / 검증 불가 5)를
  "Gemini 검증"이라는 이름으로 표시 → 이번 실행 Gemini 응답의 검증 결과처럼 보였음
- Gmail은 이번 실행 Gemini 응답을 "검증 전"으로 정확히 표시했지만, 보고서 Markdown 원문을 그대로 보내 `#`, `**`, 표, `[링크](...)` 기호가 보였음
- Gmail·보고서에 503 오류의 Python 예외 dict 전문이 그대로 들어갔음
- → 같은 실행에서 Slack과 Gmail이 서로 다른 의미를 전달

보완 내용 (수정 파일: `src/reporter.py`, `src/notifier.py`, `main.py` — gemini_client·analyzer·crawler·preprocess 수정 없음):
- `reporter.build_run_summary(jobs_df, analysis, gemini_results, historical_validation)` 추가 — 이번 실행 사실을 한 번만 정리:
  공고·분석, AX 필터 결과, 공고별 Gemini 성공/실패(`gemini_items`), 호출·성공·실패 수, 검증 상태("검증 전"/"호출 없음"),
  검증 상태 문장, 제한 사항 9개 → **보고서·Slack·Gmail이 모두 이 run_summary만 사용**
- `reporter.short_gemini_error()`: 알림에는 "503 UNAVAILABLE — Gemini 서버 일시 과부하"처럼 짧게 표시 (원본 오류 전문은 실행 로그에만 출력)
- `main.py`: `VALIDATION_SUMMARY` → `HISTORICAL_VALIDATION_SUMMARY`로 이름 변경, 운영 Slack/Gmail에는 전달하지 않고 보고서 부록에서만 사용
- Slack (`build_slack_message(run_summary)`): 공고별 상세 정보(사용자 확정 형식) 유지 → `*Gemini 실행 결과*`(호출/성공/실패, 공고별 성공·실패)
  → `*Gemini 검증 상태*`(이번 응답 검증 전, 상세 정보 확인 불가, STEP 10은 과거 기록) → `*제한 사항*` — 과거 7/3/0/5 숫자 제거
- Gmail (`build_email_text(run_summary)`, 새 함수): Markdown 대신 Plain Text 형식
  (제목 밑줄 `====`/`----`, 1. 분석 기준 / 2. 공고별 상세 정보 / 3. Gemini 실행 결과(성공 응답·실패) / 4. Gemini 검증 상태 / 5. 제한 사항),
  Gemini 응답 속 `**`·`#`도 제거. `send_email(email_text, ...)`은 받은 본문을 그대로 발송
- Markdown 보고서 (`create_report(run_summary, historical_validation=...)`): 5장 "Gemini 실행 결과"(성공 응답 전부), 6장 "Gemini 검증 상태",
  7장 제한 사항(공통 목록), 8장 다음 단계, 부록 "## 9. 과거 Gemini 검증 기록 — STEP 10 (참고)" + "이번 실행 결과의 검증값이 아닙니다"
- STEP 10 기록 자체는 이 문서와 Notebook에 그대로 보존

검증 (외부 요청 0회 — 네트워크 차단, 가짜 Gemini 결과 사용, history CSV 읽기만, 보고서 파일 덮어쓰기 없음):
- CASE A (2건 성공) / CASE B (1건 성공 + 실제 형식의 503 오류 1건) 모두 15~16개 항목 통과:
  Slack·Gmail에 과거 7/3/0/5 없음, 보고서 본문(1~8장)에도 없음(부록에만), Slack·Gmail·보고서의 호출/성공/실패 수 동일,
  세 곳 모두 "검증 전", Gmail에 Markdown 기호 없음, 503 raw dict 없음(짧은 문구만), 공고 URL 5개, 지원 시작/마감일, 제한 사항·검증 상태 문장 동일
- 문자 수: CASE A 보고서 3549 / Slack 1881 / Gmail 2595, CASE B 보고서 3482 / Slack 1907 / Gmail 2527
- `main(dry_run=True)` 성공 (보고서 3245 / Slack 1824 / Gmail 2272자), 네트워크·외부/저장 함수 호출 0회
- history CSV·`reports/ax_job_report.md` 체크섬 변경 없음

참고:
- `create_report()`, `build_slack_message()`, `send_email()`의 인자가 바뀌었다. Notebook STEP 14 검증 셀은 이전 시그니처로 작성된 과거 기록이라 그대로 다시 실행하면 오류가 난다. (STEP 15 셀의 `main(dry_run=True)`는 그대로 동작)

#### STEP 18 GitHub 최종 검증 실패 사례 — JobKorea ConnectTimeout

실제 발생 (GitHub Actions, "AX Job Agent" 수동 실행, 출력 정합성 보완 push 후):
- 오류: `requests.exceptions.ConnectTimeout` — `www.jobkorea.co.kr:443`, `connect timeout=10`
- 수집 단계(`collect_jobs`)에서 예외로 `main.py` 종료 → 긴 traceback만 로그에 남음
- 이후 단계 미실행: Gemini·보고서·Slack·Gmail 모두 실행 안 됨, `Persist updated history` step도 실행 안 됨 (history commit 없음)
- 판단: STEP 17에서 같은 GitHub Actions 환경에서 수집에 성공했으므로 **파싱 오류가 아니라 외부 사이트 연결 불안정 사례**로 기록
- **운영 리스크**: 주간 자동 실행은 JobKorea 연결 안정성에 의존한다. GitHub runner(IP)에서 연결이 실패하면 그 주에는 알림이 오지 않고 workflow가 실패로 표시된다.
- STEP 18은 **IN_PROGRESS 유지**

보완 (수정 파일: `src/crawler.py`, `main.py` — Secret·Gemini·Slack·Gmail 로직, workflow, history persistence 수정 없음):
- `crawler.py`: `JobKoreaConnectionError` 추가, `requests.get`을 `_get()`으로 감싸 연결 오류를 사람이 읽는 메시지로 변환
  - `requests.exceptions.Timeout`(ConnectTimeout 포함) → "JobKorea 연결 실패: 요청 시간이 초과되었습니다. (timeout=10초, ConnectTimeout)"
  - `requests.exceptions.ConnectionError` → "JobKorea 연결 실패: 서버에 연결할 수 없습니다. (네트워크 또는 사이트 접속 문제, ConnectionError)"
  - timeout 10초, 요청 횟수(기본 1 + 보안정책일 때만 User-Agent 1), User-Agent 재요청 정책 **변경 없음**
  - 연결 오류가 나면 다음 요청으로 이어가지 않음 (재시도·프록시·IP 우회·CAPTCHA 우회 없음)
- `main.py`: `cli()` 추가 — `python main.py` 실행 시 `JobKoreaConnectionError`는 짧은 안내 2줄을 stderr에 출력하고 **종료 코드 1**
  - 수집 실패 시 기존 history CSV를 최신 데이터처럼 대신 쓰지 않음 (fallback 없음) → GitHub Actions가 실패로 표시하고 history step은 건너뜀
  - 그 밖의 오류는 이전처럼 그대로 예외로 종료 (non-zero)

검증 (실제 외부 요청 0회 — 네트워크 차단, 가짜 `requests.get`, 이후 단계 함수 호출 감시):
- CASE 1 첫 요청 ConnectTimeout / CASE 2 첫 요청 ConnectionError / CASE 3 보안정책 후 User-Agent 재요청이 ConnectTimeout:
  모두 `python main.py`와 같은 방식(`__main__`)으로 실행 → 종료 코드 1, 사람이 읽는 메시지, traceback 없음,
  요청 횟수 그대로(1 / 1 / 2회, timeout=10), 수집 이후 단계(Gemini·Slack·Gmail·보고서 저장·history 저장) 호출 0회
- CASE 4 정상 응답(보안정책 → User-Agent 성공): 요청 2회, 5건·9컬럼, 결과가 history CSV와 같음(수집 시각 제외)
- CASE 5 정상 응답(첫 요청 성공): 요청 1회, 5건
- history CSV·보고서 체크섬 변경 없음

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

현재 단계는 STEP 18 GitHub Actions 주간 실행입니다. (공식 마지막 STEP)
(schedule 및 history persistence 준비 완료, push 및 GitHub 검증 대기)
STEP 01~17은 완료되었습니다 (docs/PROGRESS.md 참고).
- STEP 17: GitHub Actions 수동 실행 성공, Slack·Gmail 도착 확인
- STEP 18: workflow "AX Job Agent" — workflow_dispatch + schedule(cron "0 0 * * 1" = 월 09:00 KST),
  contents: write, main.py 성공 후 history CSV 하나만 자동 commit/push

이번 작업만 수행해 주세요.

목표:
- 사용자가 수정된 workflow를 수동으로 1회 실행한 결과(로그, 자동 commit)를 확인하고 기록합니다.

하지 말 것:
- git add . / 보고서 자동 commit / 새 Secret·PAT
- Secret 값 출력·기록
- main.py 로직, 신규 알림 정책, Gemini 호출 수 변경
- GitHub Actions 반복 실행

완료 조건:
- workflow 전체 성공, Persist history step 성공
- 자동 commit "chore: update AX job history"가 history CSV 한 파일만 포함
- Slack·Gmail 실제 도착 사용자 확인, 로그에 비밀값 노출 없음, 반복 실행 없음
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
