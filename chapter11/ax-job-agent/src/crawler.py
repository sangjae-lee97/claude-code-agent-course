"""JobKorea 검색 결과 수집 (Notebook STEP 07-A에서 검증한 로직)."""

import json
import re
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

SEARCH_URL = "https://www.jobkorea.co.kr/Search/?stext={keyword}&tabType=recruit"

# 기본 요청이 보안정책 페이지를 받았을 때만 1회 사용하는 일반 브라우저 User-Agent
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36"
}

JOB_COLUMNS = [
    "company_name",
    "job_title",
    "career",
    "location",
    "posted_date",    # 지원 제출 시작일 (applicationPeriod.start)
    "closing_date",   # 지원 제출 마감일 (applicationPeriod.end)
    "job_url",
    "search_keyword",
    "collected_at",
]


def _parse_search_page(response):
    """응답을 파싱하고, 실제 검색 결과인지 판단한다. (상태 코드 200만으로 판단하지 않음)"""
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.get_text(strip=True) if soup.title else ""
    is_search_result = ("채용공고" in title) and ("AX" in response.text.upper())
    return soup, is_search_result


class JobKoreaConnectionError(RuntimeError):
    """JobKorea 서버에 연결하지 못했을 때 (시간 초과·연결 오류) 사람이 읽을 수 있는 메시지로 알리는 오류."""


def _get(url, timeout, headers=None):
    """requests.get 1회. 연결 오류는 긴 traceback 대신 JobKoreaConnectionError로 바꾼다. (재시도하지 않음)"""
    try:
        return requests.get(url, headers=headers, timeout=timeout)
    except requests.exceptions.Timeout as e:
        raise JobKoreaConnectionError(
            f"JobKorea 연결 실패: 요청 시간이 초과되었습니다. (timeout={timeout}초, {type(e).__name__})"
        ) from None
    except requests.exceptions.ConnectionError as e:
        raise JobKoreaConnectionError(
            f"JobKorea 연결 실패: 서버에 연결할 수 없습니다. (네트워크 또는 사이트 접속 문제, {type(e).__name__})"
        ) from None


def fetch_search_page(url, timeout=10):
    """검색 페이지를 요청한다.

    기본 요청이 보안정책 페이지면 일반 브라우저 User-Agent로 1회만 다시 요청한다.
    반복 재시도나 그 외 우회 기법은 사용하지 않는다.
    연결 시간 초과·연결 오류는 JobKoreaConnectionError로 알린다. (다른 요청으로 이어서 시도하지 않음)
    """
    response = _get(url, timeout)
    response.raise_for_status()
    soup, is_search_result = _parse_search_page(response)

    if not is_search_result:
        response = _get(url, timeout, headers=BROWSER_HEADERS)
        response.raise_for_status()
        soup, is_search_result = _parse_search_page(response)

    if not is_search_result:
        raise RuntimeError("실제 검색 결과 HTML을 받지 못했습니다. (보안정책/접속 제한 페이지로 추정)")
    return soup


def extract_application_periods(soup):
    """Next.js script JSON에서 공고 ID별 applicationPeriod를 찾는다.

    반환: {"50032017": {"start": "...", "end": "..."}, ...}
    """
    period_by_id = {}
    for script in soup.find_all("script"):
        text = script.string or ""
        if "applicationPeriod" not in text:
            continue
        match = re.match(r'self\.__next_f\.push\(\[1,(".*")\]\)', text, re.S)
        if not match:
            continue
        payload = json.loads(match.group(1))  # JavaScript 문자열 → 일반 문자열
        for found in re.finditer(r'"content":\[\{"id":', payload):
            start_index = found.start() + len('"content":')
            content, _ = json.JSONDecoder().raw_decode(payload, start_index)
            for item in content:
                period_by_id[item["id"]] = item.get("applicationPeriod")
    return period_by_id


def parse_job_cards(soup, period_by_id, search_keyword, collected_at, max_jobs=5):
    """공고 카드(CardJob)에서 최대 max_jobs건을 추출해 list[dict]로 반환한다."""
    jobs = []
    cards = soup.select('div[data-sentry-component="CardJob"]')

    for card in cards[:max_jobs]:
        title_link = card.select_one('a[data-sentry-component="Title"]')
        company_link = title_link.find_next("a") if title_link else None
        company_tag = company_link.select_one("span") if company_link else None
        location_tag = card.select_one('[data-sentry-component="GrayChip"] span.truncate')
        career_tag = card.select_one("span.flex-shrink-0.text-typo-c1-13")

        # 추적용 파라미터(?Oem_Code=...&listno=...)를 제거한 기본 공고 URL
        job_url = title_link["href"].split("?")[0] if title_link else None

        # 카드 순서가 아니라 공고 ID로 JSON 날짜를 매칭한다 (createdAt은 사용하지 않음)
        job_id = job_url.rsplit("/", 1)[-1] if job_url else None
        period = period_by_id.get(job_id) or {}
        start_raw = period.get("start")
        end_raw = period.get("end")

        jobs.append({
            "company_name": company_tag.get_text(strip=True) if company_tag else None,
            "job_title": title_link.get_text(strip=True) if title_link else None,
            "career": career_tag.get_text(strip=True) if career_tag else None,
            "location": location_tag.get_text(strip=True) if location_tag else None,
            "posted_date": start_raw[:10] if start_raw else None,
            "closing_date": end_raw[:16].replace("T", " ") if end_raw else None,
            "job_url": job_url,
            "search_keyword": search_keyword,
            "collected_at": collected_at,
        })
    return jobs


def collect_jobs(search_keyword="ax", max_jobs=5):
    """JobKorea 검색 결과 1페이지에서 최대 max_jobs건을 수집해 DataFrame으로 반환한다."""
    url = SEARCH_URL.format(keyword=search_keyword)
    soup = fetch_search_page(url)
    collected_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    period_by_id = extract_application_periods(soup)
    jobs = parse_job_cards(soup, period_by_id, search_keyword, collected_at, max_jobs=max_jobs)
    return pd.DataFrame(jobs, columns=JOB_COLUMNS)
