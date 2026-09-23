"""Slack / Gmail 메시지 만들기와 발송 (Notebook STEP 12, 13에서 검증한 로직).

Slack 메시지와 Gmail 본문은 모두 reporter.build_run_summary()가 만든 run_summary만 사용한다.
(같은 실행에서 Slack과 Gmail이 서로 다른 사실을 전달하지 않도록)

Webhook URL, Gmail 주소, 앱 비밀번호는 이 파일에 쓰지 않는다. 모두 인자로 받는다.
발송 함수는 요청을 1회만 보내며 자동 재시도하지 않는다.
"""

import re
import smtplib
from email.message import EmailMessage

import requests

DEFAULT_EMAIL_SUBJECT = "[AX Job Agent] AX 채용 분석 보고서"


def slack_escape(text):
    # Slack mrkdwn에서 특수 문자인 &, <, > 를 Slack 방식으로 바꾼다 (화면에는 원래 글자로 보임)
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _mask(message, secrets):
    for secret in secrets:
        if secret:
            message = message.replace(secret, "***")
    return message


def _gemini_status_line(item):
    return "응답 생성 성공" if item["success"] else item["error_display"]


def build_slack_message(run_summary):
    """사용자가 최종 확인한 Slack 형식(공고별 상세 정보 + 공고 URL 1회 표시)으로 메시지를 만든다.

    - 공고 순서는 수집 순서 그대로 (번호는 수집 순서이며 추천 순위가 아님)
    - Slack mrkdwn 최소 문법만 사용: *굵게*, • 목록
    - Gemini 부분은 이번 실행 결과(성공/실패)와 검증 상태만 표시한다. (과거 STEP 10 숫자는 표시하지 않음)
    """
    jobs_df = run_summary["jobs_df"]
    total_jobs = len(jobs_df)

    job_blocks = []
    for i, (_, row) in enumerate(jobs_df.iterrows(), start=1):
        job_blocks.append(
            f"*{i}. {slack_escape(row['company_name'])}*\n"
            f"• 공고 제목: {slack_escape(row['job_title'])}\n"
            f"• 경력: {slack_escape(row['career'])}\n"
            f"• 지역: {slack_escape(row['location'])}\n"
            f"• 지원 시작일: {row['posted_date']}\n"
            f"• 지원 마감일: {row['closing_date']}\n"
            f"• 검색어: {slack_escape(row['search_keyword'])}\n"
            f"• 수집 시각: {row['collected_at']}\n"
            f"• 공고 URL: {row['job_url']}\n"
        )
    jobs_text = "\n\n".join(job_blocks)

    gemini_lines = [
        f"• 호출: {run_summary['gemini_call_count']}건",
        f"• 성공: {run_summary['gemini_success_count']}건",
        f"• 실패: {run_summary['gemini_failure_count']}건",
    ] + [f"• {slack_escape(item['company_name'])}: {_gemini_status_line(item)}" for item in run_summary["gemini_items"]]
    gemini_text = "\n".join(gemini_lines)
    validation_text = "\n".join(f"• {slack_escape(line)}" for line in run_summary["gemini_validation_lines"])
    limitation_text = "\n".join(f"• {slack_escape(line)}" for line in run_summary["limitations"])

    return f"""
*AX 채용 분석 보고서*

현재 수집된 {total_jobs}건 기준입니다. (공고 번호는 수집 순서이며 추천 순위가 아닙니다)

*공고별 상세 정보*

{jobs_text}

*Gemini 실행 결과*
{gemini_text}

*Gemini 검증 상태*
{validation_text}

*제한 사항*
{limitation_text}
""".strip()


def send_slack(message, webhook_url, timeout=10):
    """Slack Incoming Webhook으로 메시지를 1회 보낸다. 반환: {"status_code", "text"}

    오류가 나면 Webhook URL을 *** 로 가린 메시지로 RuntimeError를 낸다.
    """
    if not webhook_url:
        raise ValueError("webhook_url이 비어 있습니다.")
    try:
        response = requests.post(webhook_url, json={"text": message}, timeout=timeout)
    except Exception as e:
        raise RuntimeError(f"Slack 요청 실패 ({type(e).__name__}): {_mask(str(e), [webhook_url])[:300]}") from None
    return {"status_code": response.status_code, "text": response.text}


def _heading(title, underline="-"):
    return f"{title}\n{underline * 20}"


def _plain(text):
    # Gemini 응답 안에 Markdown 굵게(**)나 제목(#)이 섞여 있어도 메일에는 기호 없이 보이도록 정리
    text = str(text).replace("**", "")
    return re.sub(r"(?m)^#+\s*", "", text)


def build_email_text(run_summary):
    """run_summary로 사람이 읽기 좋은 Plain Text 메일 본문을 만든다. (Markdown 기호를 쓰지 않음)"""
    jobs_df = run_summary["jobs_df"]
    analysis = run_summary["analysis"]
    total = analysis["total_jobs"]
    keywords = ", ".join(analysis["keyword_counts"].keys())

    def counts(values):
        return "\n".join(f"  - {name}: {count}건" for name, count in values.items())

    job_blocks = []
    for i, (_, row) in enumerate(jobs_df.iterrows(), start=1):
        job_blocks.append(
            f"[{i}] {row['company_name']}\n"
            f"회사명: {row['company_name']}\n"
            f"공고 제목: {row['job_title']}\n"
            f"경력: {row['career']}\n"
            f"지역: {row['location']}\n"
            f"지원 시작일: {row['posted_date']}\n"
            f"지원 마감일: {row['closing_date']}\n"
            f"검색어: {row['search_keyword']}\n"
            f"수집 시각: {row['collected_at']}\n"
            f"공고 URL: {row['job_url']}"
        )

    gemini_parts = [
        f"호출: {run_summary['gemini_call_count']}건",
        f"성공: {run_summary['gemini_success_count']}건",
        f"실패: {run_summary['gemini_failure_count']}건",
    ]
    for item in run_summary["gemini_items"]:
        if item["success"]:
            gemini_parts.append(
                "\n[성공 응답] (이번 실행에서 Gemini가 생성한 설명 — 원본 대조 검증 전)\n"
                f"회사: {item['company_name']}\n"
                f"공고: {item['job_title']}\n"
                f"{_plain(item['summary_text']).strip()}"
            )
        else:
            gemini_parts.append(f"\n[실패]\n회사: {item['company_name']}\n오류: {item['error_display']}")

    jobs_text = "\n\n".join(job_blocks)
    gemini_text = "\n".join(gemini_parts)
    validation_text = "\n".join(run_summary["gemini_validation_lines"])
    limitation_text = "\n".join(f"- {line}" for line in run_summary["limitations"])

    return f"""안녕하세요.

AX 채용정보 Agent에서 생성한 분석 보고서입니다.

{_heading("AX 채용 분석 보고서", "=")}

현재 수집된 {total}건 기준입니다. (공고 번호는 수집 순서이며 추천 순위가 아닙니다)


{_heading("1. 분석 기준")}

검색어: {keywords}
분석 대상: {total}건
지원 시작일 범위: {analysis['posted_date_min']} ~ {analysis['posted_date_max']}
지원 마감일 범위: {analysis['closing_date_min']} ~ {analysis['closing_date_max']}
AX/AI 1차 필터 통과: {run_summary['filter_pass_count']}건 (매칭 키워드: {run_summary['matched_keyword_text']})

회사별 공고 수:
{counts(analysis['company_counts'])}
지역별 공고 수:
{counts(analysis['location_counts'])}
경력별 공고 수:
{counts(analysis['career_counts'])}


{_heading("2. 공고별 상세 정보")}

{jobs_text}


{_heading("3. Gemini 실행 결과")}

{gemini_text}


{_heading("4. Gemini 검증 상태")}

{validation_text}


{_heading("5. 제한 사항")}

{limitation_text}
"""


def send_email(email_text, gmail_user, gmail_app_password, subject=DEFAULT_EMAIL_SUBJECT, timeout=15):
    """Gmail SMTP_SSL(smtp.gmail.com:465)로 자기 자신에게 Plain Text 메일을 1회 보낸다.

    email_text는 build_email_text(run_summary)로 만든 본문이다.
    gmail_app_password는 Google 계정에서 발급한 앱 비밀번호이다. (일반 로그인 비밀번호 아님)
    오류가 나면 주소·비밀번호를 *** 로 가린 메시지로 RuntimeError를 낸다.
    """
    if not (gmail_user and gmail_app_password):
        raise ValueError("gmail_user 또는 gmail_app_password가 비어 있습니다.")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = gmail_user
    msg.set_content(email_text)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=timeout) as smtp:
            smtp.login(gmail_user, gmail_app_password)
            smtp.send_message(msg)
    except Exception as e:
        safe = _mask(str(e), [gmail_user, gmail_app_password])[:300]
        raise RuntimeError(f"Gmail 발송 실패 ({type(e).__name__}): {safe}") from None
    return True
