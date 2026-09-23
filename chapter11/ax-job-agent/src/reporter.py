"""Markdown 보고서 생성 (Notebook STEP 11에서 검증한 구조).

create_report()는 문자열만 만들고, 파일 저장은 save_report()로 분리한다.

gemini_summary 형식 (summarize_with_gemini() 결과 1건):
    {"company_name": ..., "job_title": ..., "gemini_summary": "응답 텍스트", "model": "..."(선택)}

validation_summary 형식 (STEP 10 과거 검증 기록 — 이번 실행의 새 Gemini 응답을 검증한 결과가 아님):
    {"target": "에스코어 / AX 컨설턴트 채용", "scope": "에스코어 1건", "total_items": 15,
     "counts": {"일치": 7, "의미상 일치": 3, "불일치": 0, "검증 불가": 5},
     "notes": ["...", ...]}
"""

from pathlib import Path

from src.analyzer import RELEVANCE_KEYWORDS, find_matched_keywords_safe


def _counts_to_lines(counts):
    return "\n".join(f"- {name}: {count}건" for name, count in counts.items())


def _md_cell(value):
    # 표 안에서 '|' 문자가 칸을 깨뜨리지 않도록 바꾼다
    return str(value).replace("|", "/")


def _job_table(jobs_df):
    lines = ["| 회사명 | 공고 제목 | 경력 | 지역 | 지원 시작일 | 지원 마감일 | 공고 URL |",
             "|---|---|---|---|---|---|---|"]
    for _, job in jobs_df.iterrows():
        lines.append(
            f"| {_md_cell(job['company_name'])} | {_md_cell(job['job_title'])} | {_md_cell(job['career'])} "
            f"| {_md_cell(job['location'])} | {job['posted_date']} | {job['closing_date']} | [링크]({job['job_url']}) |"
        )
    return "\n".join(lines)


def _filter_section(jobs_df):
    matched = jobs_df["job_title"].apply(find_matched_keywords_safe)
    pass_count = int((matched.apply(len) > 0).sum())
    keyword_counts = matched.explode().dropna().value_counts()
    keyword_text = ", ".join(f"{k} {v}건" for k, v in keyword_counts.items()) or "없음"
    return pass_count, keyword_text


def _gemini_section(gemini_summary):
    if not gemini_summary or not gemini_summary.get("gemini_summary"):
        return "Gemini 분석 결과가 없습니다."
    model = gemini_summary.get("model")
    quoted = "\n".join(f"> {line}" if line else ">" for line in gemini_summary["gemini_summary"].strip().splitlines())
    return (
        "**[Gemini 생성 설명]**\n\n"
        "아래 내용은 이번 실행에서 Gemini가 생성한 설명입니다.\n"
        "이 응답은 아직 원본 데이터와 비교 검증하지 않았습니다. (6장의 검증 기록은 과거 응답에 대한 것입니다)\n\n"
        f"대상: {gemini_summary['company_name']} / {gemini_summary['job_title']}"
        f"{f' (모델: {model})' if model else ''}\n\n"
        f"{quoted}"
    )


def _validation_section(validation_summary):
    if not validation_summary:
        return "Gemini 검증 결과가 없습니다."
    rows = []
    if validation_summary.get("total_items") is not None:
        rows.append(f"| 검증 항목 | {validation_summary['total_items']} |")
    rows += [f"| {k} | {v} |" for k, v in validation_summary.get("counts", {}).items()]
    notes = "\n".join(f"- {note}" for note in validation_summary.get("notes", []))
    return (
        "**[과거 검증 기록]**\n\n"
        f"아래 검증 결과는 STEP 10에서 {validation_summary.get('target', '')} 공고의 **당시 Gemini 응답**을\n"
        "원본 데이터와 비교한 기록입니다.\n"
        "이번 실행에서 새로 생성된 Gemini 응답 전체를 검증했다는 뜻은 아닙니다.\n"
        "(\"일치\"는 글자 비교, \"의미상 일치\"·\"검증 불가\"는 사람이 판단)\n\n"
        "| 구분 | 개수 |\n|---|---:|\n"
        + "\n".join(rows)
        + (f"\n\n{notes}" if notes else "")
    )


def create_report(jobs_df, analysis, gemini_summary=None, validation_summary=None,
                  data_source="data/processed/jobs_history.csv", extra_limitations=None,
                  next_step_text="GitHub Actions에서 자동 실행 검증"):
    """보고서 Markdown 문자열을 만들어 반환한다. (파일 저장은 하지 않음)"""
    total = analysis["total_jobs"]
    keywords = ", ".join(analysis["keyword_counts"].keys())
    pass_count, matched_keyword_text = _filter_section(jobs_df)

    limitations = [
        f"현재 데이터는 {total}건뿐입니다.",
        f"검색어는 `{keywords}` {len(analysis['keyword_counts'])}개뿐입니다.",
        "검색 결과 한 페이지의 일부 공고만 사용했습니다.",
        "공고 상세 페이지 본문은 아직 수집하지 않았습니다.",
    ]
    if validation_summary:
        scope = validation_summary.get("scope", validation_summary.get("target", "일부 공고"))
        limitations.append(f"Gemini 검증 기록(STEP 10)은 과거 응답 {scope} 기준이며, 이번 실행의 Gemini 응답은 검증하지 않았습니다.")
    limitations += list(extra_limitations or [])
    limitations.append("현재 결과를 전체 채용시장 경향으로 일반화하면 안 됩니다.")
    limitation_text = "\n".join(f"- {item}" for item in limitations)

    return f"""# AX 채용 분석 보고서

> 이 보고서는 **현재 수집된 {total}건 기준**입니다. 채용 시장 전체의 경향을 나타내지 않습니다.
>
> - **[데이터 기반 사실]** 표시: 수집 데이터를 pandas로 계산한 값
> - **[Gemini 생성 설명]** 표시: 이번 실행에서 Gemini가 만든 문장 (아직 원본과 비교 검증하지 않음)
> - **[과거 검증 기록]** 표시: STEP 10에서 과거 Gemini 응답 1건을 원본과 비교한 기록 (일부 판정은 사람이 판단)

## 1. 분석 기준

**[데이터 기반 사실]**

- 검색어: {keywords}
- 분석 대상 공고 수: {total}건
- 수집 기준: JobKorea 검색 결과 1페이지의 상위 {total}건 (검색 결과 페이지에 보이는 정보만 사용, 상세 페이지 미수집)
- 데이터 파일: `{data_source}`
- 지원 시작일 범위: {analysis['posted_date_min']} ~ {analysis['posted_date_max']}
- 지원 마감일 범위: {analysis['closing_date_min']} ~ {analysis['closing_date_max']}

## 2. 현재 수집 데이터 요약

**[데이터 기반 사실]** — 현재 수집된 {total}건 기준

전체 공고 수: {total}건

회사별 공고 수:

{_counts_to_lines(analysis['company_counts'])}

지역별 공고 수:

{_counts_to_lines(analysis['location_counts'])}

경력별 공고 수:

{_counts_to_lines(analysis['career_counts'])}

- 경력 값은 화면 문구 그대로 집계했습니다.
- 근무지가 여러 곳인 공고는 요약 문구(예: `서울 강남구 외 1`) 그대로 집계했습니다.

## 3. AX/AI 관련 공고 필터 결과

**[데이터 기반 사실]**

- 필터 통과 공고 수: {pass_count}건 / 전체 {total}건
- 사용한 기준: 공고 제목(`job_title`)에 AX/AI 관련 키워드 {len(RELEVANCE_KEYWORDS)}개 중 하나 이상 포함
  - 영문 키워드는 앞뒤에 영문자·숫자가 없을 때만 매칭, 한글 키워드는 포함 검색
- 매칭된 키워드: {matched_keyword_text}

이 필터는 **1차 후보 선별용**입니다. 제목에 키워드가 있다고 원하는 AX 직무라는 뜻은 아닙니다.

## 4. 주요 공고

**[데이터 기반 사실]** — 현재 수집된 {total}건 전체

{_job_table(jobs_df)}

- 지원 시작일 = `applicationPeriod.start`, 지원 마감일 = `applicationPeriod.end` (원본 값 그대로)

## 5. Gemini 분석 예시

{_gemini_section(gemini_summary)}

## 6. Gemini 검증 결과

{_validation_section(validation_summary)}

## 7. 제한 사항

{limitation_text}

## 8. 다음 단계

- {next_step_text}
"""


def save_report(report_text, report_path):
    """보고서 문자열을 UTF-8로 저장하고 저장 경로를 반환한다. (폴더가 없으면 만든다)"""
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")
    return report_path
