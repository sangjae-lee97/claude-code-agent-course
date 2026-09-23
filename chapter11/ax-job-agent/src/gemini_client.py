"""Gemini 요약 (Notebook STEP 09에서 검증한 로직).

API 키는 이 파일에 쓰지 않는다. 호출하는 쪽에서 genai.Client(api_key=...)를 만들어 client로 넘긴다.
"""

import pandas as pd

DEFAULT_MODEL = "gemini-3.6-flash"


def _show_value(value):
    # 값이 비어 있으면 '정보 없음'으로 표시해서, 빈 값을 Gemini가 추측하지 않게 한다
    return "정보 없음" if pd.isna(value) else str(value)


def build_prompt(job):
    """공고 1건(행)으로 프롬프트를 만든다. 제공된 필드만 사용하고 추측을 금지한다."""
    return f"""당신은 채용공고 정보를 정리하는 도우미입니다.

아래에 제공된 채용공고 정보만 사용하세요.
제공되지 않은 세부 업무, 기술 스택, 자격요건은 추측하지 마세요.
확인할 수 없는 항목은 '확인 불가'라고 적으세요.

[제공된 채용공고 정보]
- 회사명: {_show_value(job["company_name"])}
- 공고 제목: {_show_value(job["job_title"])}
- 경력: {_show_value(job["career"])}
- 근무 지역: {_show_value(job["location"])}
- 지원 시작일: {_show_value(job["posted_date"])}
- 지원 마감일: {_show_value(job["closing_date"])}
- 검색어: {_show_value(job["search_keyword"])}
- 공고 URL: {_show_value(job["job_url"])}

아래 형식 그대로 한국어로 답하세요.

[회사명]
...

[공고 제목]
...

[한줄 요약]
...

[확인 가능한 정보]
- 경력:
- 지역:
- 지원 시작일:
- 지원 마감일:
- 검색어:

[AX/AI 관련성]
- 제목에서 확인되는 범위만 설명

[확인 불가]
- 상세 업무
- 상세 기술 스택
- 자격요건
- 우대사항
"""


def summarize_with_gemini(df, client, model=DEFAULT_MODEL, max_jobs=2):
    """앞 max_jobs건을 공고당 1회씩 Gemini에 보내고 결과 목록을 반환한다. (자동 재시도 없음)

    반환: [{"company_name", "job_title", "job_url", "gemini_summary", "error"}, ...]
    - 성공: gemini_summary = 응답 텍스트, error = None
    - 실패: gemini_summary = None, error = "오류 종류: 메시지"
    """
    results = []
    for _, job in df.head(max_jobs).iterrows():
        summary, error = None, None
        try:
            response = client.models.generate_content(model=model, contents=build_prompt(job))
            summary = response.text
        except Exception as e:
            error = f"{type(e).__name__}: {str(e)[:300]}"
        results.append({
            "company_name": job["company_name"],
            "job_title": job["job_title"],
            "job_url": job["job_url"],
            "gemini_summary": summary,
            "error": error,
        })
    return results
