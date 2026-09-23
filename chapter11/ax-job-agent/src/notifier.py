"""Slack / Gmail 발송 (Notebook STEP 12, 13에서 검증한 로직).

Webhook URL, Gmail 주소, 앱 비밀번호는 이 파일에 쓰지 않는다. 모두 인자로 받는다.
발송 함수는 요청을 1회만 보내며 자동 재시도하지 않는다.
"""

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


def build_slack_message(jobs_df, validation_summary=None):
    """사용자가 최종 확인한 Slack 형식(공고별 상세 정보 + 공고 URL 1회 표시)으로 메시지를 만든다.

    - 공고 순서는 jobs_df 순서 그대로 (번호는 수집 순서이며 추천 순위가 아님)
    - Slack mrkdwn 최소 문법만 사용: *굵게*, • 목록
    - validation_summary 형식: {"target": "에스코어 / AX 컨설턴트 채용", "scope": "에스코어 1건",
                                "counts": {"일치": 7, ...}}  ("scope"가 없으면 "target"을 사용)
    """
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

    keywords = list(jobs_df["search_keyword"].unique())
    keyword_text = slack_escape(", ".join(keywords))

    gemini_text = ""
    if validation_summary:
        counts_text = "\n".join(f"• {k}: {v}" for k, v in validation_summary.get("counts", {}).items())
        gemini_text = (
            "*Gemini 검증*\n"
            f"• 검증 공고: {slack_escape(validation_summary.get('target', ''))}\n"
            f"{counts_text}\n\n"
        )
        scope = validation_summary.get("scope", validation_summary.get("target", "일부 공고"))
        limitation_gemini = f"• Gemini 검증은 {slack_escape(scope)} 기준\n"
    else:
        limitation_gemini = ""

    return f"""
*AX 채용 분석 보고서*

현재 수집된 {total_jobs}건 기준입니다. (공고 번호는 수집 순서이며 추천 순위가 아닙니다)

*공고별 상세 정보*

{jobs_text}

{gemini_text}*제한 사항*
• 현재 {total_jobs}건 기준
• 검색어 {keyword_text} {len(keywords)}개
• 상세페이지 미수집
{limitation_gemini}• 전체 채용시장으로 일반화하지 않음
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


def build_email_body(report_text):
    return f"""안녕하세요.

AX 채용정보 Agent에서 생성한 분석 보고서입니다.

아래 내용은 현재 수집된 데이터 기준입니다.

---

{report_text}
"""


def send_email(report_text, gmail_user, gmail_app_password, subject=DEFAULT_EMAIL_SUBJECT, timeout=15):
    """Gmail SMTP_SSL(smtp.gmail.com:465)로 자기 자신에게 Plain Text 메일을 1회 보낸다.

    gmail_app_password는 Google 계정에서 발급한 앱 비밀번호이다. (일반 로그인 비밀번호 아님)
    오류가 나면 주소·비밀번호를 *** 로 가린 메시지로 RuntimeError를 낸다.
    """
    if not (gmail_user and gmail_app_password):
        raise ValueError("gmail_user 또는 gmail_app_password가 비어 있습니다.")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = gmail_user
    msg["To"] = gmail_user
    msg.set_content(build_email_body(report_text))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=timeout) as smtp:
            smtp.login(gmail_user, gmail_app_password)
            smtp.send_message(msg)
    except Exception as e:
        safe = _mask(str(e), [gmail_user, gmail_app_password])[:300]
        raise RuntimeError(f"Gmail 발송 실패 ({type(e).__name__}): {safe}") from None
    return True
