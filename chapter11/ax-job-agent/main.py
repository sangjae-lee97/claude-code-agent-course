"""AX 채용정보 Agent — 전체 실행 순서 연결 (STEP 15).

실제 로직은 src/ 모듈에 있고, 이 파일은 설정 읽기와 실행 순서 연결만 담당한다.

실행:
    python main.py            # 실제 실행 (JobKorea 요청, Gemini 호출, 파일 저장, Slack/Gmail 발송)

dry_run=True (예: Notebook에서 main(dry_run=True)):
    - JobKorea 요청 / Gemini 호출 / Slack·Gmail 발송 / history·report 파일 저장을 하지 않는다.
    - 기존 history CSV를 이번 수집 데이터 대신 입력으로 사용해 흐름과 데이터 전달만 확인한다.
"""

import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from src.crawler import collect_jobs, JobKoreaConnectionError
from src.preprocess import clean_jobs, find_new_jobs, update_history
from src.analyzer import analyze_jobs, filter_relevant_jobs
from src.gemini_client import summarize_with_gemini
from src.reporter import build_run_summary, create_report, save_report
from src.notifier import build_slack_message, build_email_text, send_slack, send_email

PROJECT_ROOT = Path(__file__).resolve().parent
ENV_PATH = PROJECT_ROOT / ".env"
HISTORY_PATH = PROJECT_ROOT / "data" / "processed" / "jobs_history.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "ax_job_report.md"

SEARCH_KEYWORD = "ax"
MAX_JOBS = 5
GEMINI_MODEL = "gemini-3.6-flash"
GEMINI_MAX_JOBS = 2

ENV_NAMES = ["GEMINI_API_KEY", "SLACK_WEBHOOK_URL", "GMAIL_USER", "GMAIL_APP_PASSWORD"]

# STEP 10 개발 과정의 과거 검증 기록 (에스코어 당시 응답 1건 기준)
# 이번 실행의 Gemini 응답을 검증한 값이 아니므로, Markdown 보고서의 "과거 기록" 부록에만 사용한다
HISTORICAL_VALIDATION_SUMMARY = {
    "target": "에스코어 / AX 컨설턴트 채용",
    "scope": "에스코어 1건",
    "total_items": 15,
    "counts": {"일치": 7, "의미상 일치": 3, "불일치": 0, "검증 불가": 5},
    "notes": [
        "원본과 다른 사실(불일치)은 발견되지 않았습니다.",
        "AX 약어 풀이(`AI Transformation`) → 원본으로 확인할 수 없어 **검증 불가**",
        "상세 업무 / 기술 스택 / 자격요건 / 우대사항 → 상세 페이지 데이터가 없으므로 **검증 불가**",
    ],
}


def read_history(path, columns):
    """history CSV가 있으면 읽고, 없으면 같은 컬럼의 빈 DataFrame을 반환한다."""
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame(columns=columns)


def main(dry_run=False):
    mode = "DRY RUN" if dry_run else "실제 실행"
    print(f"=== AX Job Agent ({mode}) ===")

    # [1] 환경변수 로드 — 값은 출력하지 않고 설정 여부만 표시
    load_dotenv(ENV_PATH)
    env = {name: os.getenv(name) for name in ENV_NAMES}
    print("[1] 환경변수:", ", ".join(f"{name} {'설정됨' if env[name] else '미설정'}" for name in ENV_NAMES))

    # [2] 데이터 준비 — dry_run에서는 JobKorea 요청 대신 기존 history CSV를 입력으로 사용
    if dry_run:
        raw_df = pd.read_csv(HISTORY_PATH)
        print(f"[2] 데이터 준비: history CSV를 입력으로 사용 ({len(raw_df)}건) — JobKorea 요청 생략")
    else:
        raw_df = collect_jobs(search_keyword=SEARCH_KEYWORD, max_jobs=MAX_JOBS)
        print(f"[2] 데이터 준비: JobKorea 수집 {len(raw_df)}건")

    # [3] 전처리 — current_df: 이번 수집 전체 (중복 제거)
    current_df = clean_jobs(raw_df)
    print(f"[3] 전처리 완료: {len(current_df)}건")

    # [4] 기존 history와 비교 — new_jobs_df: history에 없던 신규 공고
    history_df = read_history(HISTORY_PATH, current_df.columns)
    new_jobs_df = find_new_jobs(current_df, history_df)
    updated_history_df = update_history(current_df, history_df)
    print(f"[4] 신규 공고: {len(new_jobs_df)}건 (기존 이력 {len(history_df)}건 → 업데이트 후 {len(updated_history_df)}건)")

    # [5] 관련 공고 필터 — filtered_df: 분석·요약 대상 (현재는 이번 수집 전체 기준, Notebook 흐름 유지)
    filtered_df = filter_relevant_jobs(current_df)
    print(f"[5] 관련 공고: {len(filtered_df)}건")

    # [6] 기본 분석 (pandas 사실) — 보고서 대상도 이번 수집 전체
    report_jobs_df = current_df
    analysis = analyze_jobs(report_jobs_df)
    print(f"[6] 분석 완료: 전체 {analysis['total_jobs']}건")

    # [7] Gemini 요약 — 관련 공고 앞 GEMINI_MAX_JOBS건 (dry_run에서는 호출하지 않음)
    gemini_results = []
    if dry_run:
        print("[7] Gemini 요약: 생략 (DRY RUN)")
    else:
        if not env["GEMINI_API_KEY"]:
            raise RuntimeError("GEMINI_API_KEY가 설정되지 않아 Gemini 단계에서 중단합니다.")
        from google import genai
        client = genai.Client(api_key=env["GEMINI_API_KEY"])
        gemini_results = summarize_with_gemini(filtered_df, client, model=GEMINI_MODEL, max_jobs=GEMINI_MAX_JOBS)
        success = [r for r in gemini_results if r["gemini_summary"]]
        print(f"[7] Gemini 요약: 호출 {len(gemini_results)}회, 성공 {len(success)}건")
        # 실패 원인 전문은 실행 로그에만 남긴다 (Slack·Gmail에는 짧게 줄인 문구만 표시)
        for r in gemini_results:
            if r["error"]:
                print(f"    - {r['company_name']} 실패: {r['error']}")

    # 이번 실행 요약 — 보고서·Slack·Gmail이 모두 이 값만 사용한다 (알림 대상도 이번 수집 전체)
    run_summary = build_run_summary(report_jobs_df, analysis, gemini_results, HISTORICAL_VALIDATION_SUMMARY)

    # [8] 보고서 문자열 생성 (과거 STEP 10 기록은 부록으로만 표시)
    report_text = create_report(run_summary, historical_validation=HISTORICAL_VALIDATION_SUMMARY)
    print(f"[8] 보고서 문자열 생성 완료: {len(report_text)}자")

    # [9] Slack 메시지 · Gmail 본문 생성
    slack_message = build_slack_message(run_summary)
    email_text = build_email_text(run_summary)
    print(f"[9] Slack 메시지 생성 완료: {len(slack_message)}자 / Gmail 본문 생성 완료: {len(email_text)}자")

    result = {
        "dry_run": dry_run,
        "current_count": len(current_df),
        "history_count": len(history_df),
        "new_count": len(new_jobs_df),
        "updated_history_count": len(updated_history_df),
        "filtered_count": len(filtered_df),
        "analysis": analysis,
        "report_length": len(report_text),
        "slack_length": len(slack_message),
        "email_length": len(email_text),
        "gemini_calls": len(gemini_results),
        "slack_sent": False,
        "email_sent": False,
    }

    if dry_run:
        print("[DRY RUN] 외부 호출(Gemini·Slack·Gmail)과 파일 저장(history·report) 생략")
        return result

    # [10] 파일 저장 — history, 보고서
    HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    updated_history_df.to_csv(HISTORY_PATH, index=False, encoding="utf-8-sig")
    save_report(report_text, REPORT_PATH)
    print(f"[10] 저장 완료: {HISTORY_PATH.relative_to(PROJECT_ROOT)}, {REPORT_PATH.relative_to(PROJECT_ROOT)}")

    # [11] Slack 발송 (Webhook URL이 없으면 생략)
    if env["SLACK_WEBHOOK_URL"]:
        slack_response = send_slack(slack_message, env["SLACK_WEBHOOK_URL"])
        result["slack_sent"] = True
        print(f"[11] Slack 발송: HTTP {slack_response['status_code']} / {slack_response['text']}")
    else:
        print("[11] Slack 발송: 생략 (SLACK_WEBHOOK_URL 미설정)")

    # [12] Gmail 발송 (인증정보가 없으면 생략)
    if env["GMAIL_USER"] and env["GMAIL_APP_PASSWORD"]:
        send_email(email_text, env["GMAIL_USER"], env["GMAIL_APP_PASSWORD"])
        result["email_sent"] = True
        print("[12] Gmail 발송: 성공")
    else:
        print("[12] Gmail 발송: 생략 (GMAIL_USER / GMAIL_APP_PASSWORD 미설정)")

    return result


def cli():
    """명령줄 실행용. JobKorea 연결 실패는 짧은 안내를 출력하고 종료 코드 1을 돌려준다.

    수집에 실패하면 기존 history를 대신 쓰지 않고 그대로 중단한다. (GitHub Actions가 실패로 표시하도록)
    """
    try:
        main()
    except JobKoreaConnectionError as e:
        print(f"[중단] {e}", file=sys.stderr)
        print("[중단] 수집 단계에서 실패하여 이후 단계(Gemini·보고서·Slack·Gmail·history 저장)를 실행하지 않았습니다.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(cli())
