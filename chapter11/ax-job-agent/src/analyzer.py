"""기본 분석 / AX·AI 관련 공고 필터 (Notebook STEP 07-E, 07-F, 07-G에서 검증한 로직)."""

import re

import pandas as pd

RELEVANCE_KEYWORDS = [
    "AX",
    "AI",
    "인공지능",
    "생성형 AI",
    "생성형AI",
    "LLM",
    "Machine Learning",
    "머신러닝",
    "Data Scientist",
    "데이터 사이언티스트",
    "AI Engineer",
    "AI 엔지니어",
    "데이터 분석",
]


def _date_range(df, column):
    """날짜로 비교해 가장 이른/늦은 값을 찾고, 원본 문자열을 그대로 반환한다."""
    parsed = pd.to_datetime(df[column], errors="coerce")
    if parsed.isna().all():
        return None, None
    return df.loc[parsed.idxmin(), column], df.loc[parsed.idxmax(), column]


def analyze_jobs(df):
    """pandas로 계산 가능한 사실만 모아 dict로 반환한다."""
    posted_min, posted_max = _date_range(df, "posted_date")
    closing_min, closing_max = _date_range(df, "closing_date")
    return {
        "total_jobs": len(df),
        "company_counts": df["company_name"].value_counts().to_dict(),
        "location_counts": df["location"].value_counts().to_dict(),
        "career_counts": df["career"].value_counts().to_dict(),
        "keyword_counts": df["search_keyword"].value_counts().to_dict(),
        "posted_date_min": posted_min,
        "posted_date_max": posted_max,
        "closing_date_min": closing_min,
        "closing_date_max": closing_max,
    }


def _is_english_keyword(keyword):
    return re.fullmatch(r"[A-Za-z0-9 ]+", keyword) is not None


def find_matched_keywords_safe(title, keywords=RELEVANCE_KEYWORDS):
    """제목에서 매칭된 키워드 목록을 반환한다.

    - 영문 키워드: 앞뒤에 영문자·숫자가 붙어 있지 않을 때만 매칭 (Tax/Max/Maintenance/Training 오탐 방지,
      AX담당자/AI기반처럼 한글이 붙은 경우는 매칭)
    - 한글이 들어 있는 키워드: 포함 검색
    """
    if not isinstance(title, str):
        return []
    matched = []
    for keyword in keywords:
        if _is_english_keyword(keyword):
            pattern = r"(?<![A-Za-z0-9])" + re.escape(keyword) + r"(?![A-Za-z0-9])"
            if re.search(pattern, title, re.IGNORECASE):
                matched.append(keyword)
        elif keyword.lower() in title.lower():
            matched.append(keyword)
    return matched


def filter_relevant_jobs(df, keywords=RELEVANCE_KEYWORDS):
    """job_title에 관련 키워드가 있는 행만 matched_keywords 컬럼과 함께 반환한다. (원본 df는 수정하지 않음)"""
    matches = df["job_title"].apply(lambda title: find_matched_keywords_safe(title, keywords))
    has_match = matches.apply(len) > 0
    filtered = df[has_match].copy()
    filtered["matched_keywords"] = matches[has_match]
    return filtered
