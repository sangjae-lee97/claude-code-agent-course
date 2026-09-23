"""전처리 / 중복 제거 / 신규 공고 판별 (Notebook STEP 06, 07-C, 07-D에서 검증한 로직)."""

import pandas as pd

TEXT_COLUMNS = ["company_name", "job_title", "career", "location", "job_url", "search_keyword"]


def clean_jobs(df):
    """문자열 앞뒤 공백을 정리하고 job_url 기준 중복을 제거한 복사본을 반환한다.

    - 원본 df는 수정하지 않는다.
    - 날짜 컬럼은 원본 문자열 그대로 둔다.
    - 컬럼 구조와 이름은 바꾸지 않는다.
    """
    cleaned = df.copy()
    for col in TEXT_COLUMNS:
        if col in cleaned.columns:
            cleaned[col] = cleaned[col].str.strip()
    return cleaned.drop_duplicates(subset=["job_url"], keep="first").reset_index(drop=True)


def find_new_jobs(current_df, history_df):
    """history_df에 없는 job_url만 신규 공고로 판단해 반환한다.

    history_df가 None이거나 비어 있으면 current_df 전체가 신규이다.
    """
    if history_df is None or history_df.empty:
        return current_df.copy()
    known_urls = set(history_df["job_url"].dropna().astype(str))
    return current_df[~current_df["job_url"].isin(known_urls)].copy()


def update_history(current_df, history_df):
    """기존 이력 + 현재 공고를 합치고 job_url 기준으로 중복을 제거한 DataFrame을 반환한다.

    같은 공고는 나중 행(현재 수집 정보)을 남긴다 (keep="last").
    CSV 저장은 호출하는 쪽에서 결정한다.
    """
    if history_df is None or history_df.empty:
        combined = current_df.copy()
    else:
        combined = pd.concat([history_df, current_df], ignore_index=True)
    return combined.drop_duplicates(subset=["job_url"], keep="last").reset_index(drop=True)
