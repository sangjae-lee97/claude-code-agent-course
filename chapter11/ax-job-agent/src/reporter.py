"""실행 요약(run_summary) 만들기 + Markdown 보고서 생성.

build_run_summary()로 이번 실행의 사실(수집·분석·Gemini 결과·검증 상태·제한 사항)을 한 번만 정리하고,
Markdown 보고서(create_report), Slack 메시지, Gmail 본문(notifier)은 모두 이 run_summary만 사용한다.
→ 같은 실행에서 채널마다 다른 사실을 전달하지 않도록 하기 위함

create_report()는 문자열만 만들고, 파일 저장은 save_report()로 분리한다.

historical_validation 형식 (STEP 10 과거 개발 검증 기록 — 이번 실행 결과에 대한 검증이 아님):
    {"target": "에스코어 / AX 컨설턴트 채용", "scope": "에스코어 1건", "total_items": 15,
     "counts": {"일치": 7, "의미상 일치": 3, "불일치": 0, "검증 불가": 5},
     "notes": ["...", ...]}
"""

from pathlib import Path

from src.analyzer import RELEVANCE_KEYWORDS, find_matched_keywords_safe

DEFAULT_NEXT_STEP = "GitHub Actions 주간 자동 실행 운영 (매주 월요일 09:00 KST), 실행 결과는 Slack / Gmail에서 확인"


def short_gemini_error(error):
    """사람이 읽는 알림용으로 Gemini 오류를 짧게 줄인다. (원본 오류 전문은 실행 로그에만 남긴다)"""
    if not error:
        return None
    if "503" in error or "UNAVAILABLE" in error:
        return "503 UNAVAILABLE — Gemini 서버 일시 과부하"
    return f"{error.split(':')[0].strip()} — Gemini 호출 실패"


def build_run_summary(jobs_df, analysis, gemini_results, historical_validation=None):
    """이번 실행 결과를 Slack·Gmail·보고서가 함께 쓰는 dict로 정리한다."""
    total = analysis["total_jobs"]
    keywords = ", ".join(analysis["keyword_counts"].keys())

    # AX/AI 1차 필터 결과 (이번 수집 데이터 기준)
    matched = jobs_df["job_title"].apply(find_matched_keywords_safe)
    keyword_counts = matched.explode().dropna().value_counts()

    # 이번 실행의 Gemini 결과 (성공/실패를 공고별로 구분)
    gemini_items = [{
        "company_name": r["company_name"],
        "job_title": r["job_title"],
        "job_url": r["job_url"],
        "success": bool(r["gemini_summary"]),
        "summary_text": r["gemini_summary"],
        "error_display": short_gemini_error(r["error"]),
    } for r in gemini_results]
    success_count = sum(item["success"] for item in gemini_items)

    if gemini_items:
        validation_status = "검증 전"
        validation_lines = ["이번 실행의 Gemini 응답은 아직 원본 데이터와 대조 검증하지 않았습니다. (검증 전)"]
    else:
        validation_status = "호출 없음"
        validation_lines = ["이번 실행에서는 Gemini를 호출하지 않았습니다."]
    validation_lines.append("상세 페이지를 수집하지 않아 상세 업무·기술 스택·자격요건·우대사항은 확인 불가입니다.")
    validation_lines.append("STEP 10의 Gemini 검증 결과는 개발 과정의 과거 검증 기록이며, 이번 실행 결과에 대한 검증이 아닙니다.")

    history_scope = (historical_validation or {}).get("scope", "과거 응답 1건")
    limitations = [
        f"현재 수집 데이터는 {total}건입니다.",
        f"검색어는 {keywords} {len(analysis['keyword_counts'])}개입니다.",
        "검색 결과 한 페이지의 일부 공고만 사용했습니다.",
        "상세 공고 페이지 본문은 수집하지 않았습니다. (Gemini가 보는 정보는 검색 결과 메타데이터 수준)",
        "상세 업무·기술 스택·자격요건·우대사항은 확인하지 못했습니다.",
        "Gemini API는 개별 호출에서 503 UNAVAILABLE이 발생할 수 있으며, 일부 호출이 실패해도 파이프라인은 계속 진행됩니다.",
        "이번 실행의 Gemini 응답은 원본 데이터와 자동 대조 검증을 하지 않았습니다. (검증 전)",
        f"STEP 10 검증은 과거 {history_scope} 응답에 대한 개발 기록입니다.",
        f"현재 {total}건 결과를 전체 채용시장 경향으로 일반화하면 안 됩니다.",
    ]

    return {
        "jobs_df": jobs_df,
        "analysis": analysis,
        "filter_pass_count": int((matched.apply(len) > 0).sum()),
        "matched_keyword_text": ", ".join(f"{k} {v}건" for k, v in keyword_counts.items()) or "없음",
        "gemini_items": gemini_items,
        "gemini_call_count": len(gemini_items),
        "gemini_success_count": success_count,
        "gemini_failure_count": len(gemini_items) - success_count,
        "gemini_validation_status": validation_status,
        "gemini_validation_lines": validation_lines,
        "limitations": limitations,
    }


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


def _gemini_run_section(summary):
    lines = [
        f"- 호출: {summary['gemini_call_count']}건",
        f"- 성공: {summary['gemini_success_count']}건",
        f"- 실패: {summary['gemini_failure_count']}건",
    ]
    for item in summary["gemini_items"]:
        status = "응답 생성 성공" if item["success"] else item["error_display"]
        lines.append(f"  - {item['company_name']}: {status}")

    responses = []
    for item in summary["gemini_items"]:
        if not item["success"]:
            continue
        quoted = "\n".join(f"> {line}" if line else ">" for line in item["summary_text"].strip().splitlines())
        responses.append(f"대상: {item['company_name']} / {item['job_title']}\n\n{quoted}")

    text = "**[Gemini 생성 설명]** — 이번 실행에서 Gemini가 생성한 응답입니다. (원본 대조 검증 전)\n\n" + "\n".join(lines)
    if responses:
        text += "\n\n" + "\n\n".join(responses)
    return text


def _historical_section(historical_validation):
    rows = []
    if historical_validation.get("total_items") is not None:
        rows.append(f"| 검증 항목 | {historical_validation['total_items']} |")
    rows += [f"| {k} | {v} |" for k, v in historical_validation.get("counts", {}).items()]
    notes = "\n".join(f"- {note}" for note in historical_validation.get("notes", []))
    return (
        "## 9. 과거 Gemini 검증 기록 — STEP 10 (참고)\n\n"
        "**[과거 검증 기록]** — **이번 실행 결과의 검증값이 아닙니다.**\n\n"
        f"아래는 개발 과정의 STEP 10에서 {historical_validation.get('target', '')} 공고의 당시 Gemini 응답을\n"
        "원본 데이터와 비교한 기록입니다. (\"일치\"는 글자 비교, \"의미상 일치\"·\"검증 불가\"는 사람이 판단)\n\n"
        "| 구분 | 개수 |\n|---|---:|\n"
        + "\n".join(rows)
        + (f"\n\n{notes}" if notes else "")
        + "\n"
    )


def create_report(run_summary, historical_validation=None,
                  data_source="data/processed/jobs_history.csv", next_step_text=DEFAULT_NEXT_STEP):
    """run_summary로 보고서 Markdown 문자열을 만들어 반환한다. (파일 저장은 하지 않음)"""
    jobs_df = run_summary["jobs_df"]
    analysis = run_summary["analysis"]
    total = analysis["total_jobs"]
    keywords = ", ".join(analysis["keyword_counts"].keys())
    validation_text = "\n".join(f"- {line}" for line in run_summary["gemini_validation_lines"])
    limitation_text = "\n".join(f"- {item}" for item in run_summary["limitations"])

    report = f"""# AX 채용 분석 보고서

> 이 보고서는 **현재 수집된 {total}건 기준**입니다. 채용 시장 전체의 경향을 나타내지 않습니다.
>
> - **[데이터 기반 사실]** 표시: 수집 데이터를 pandas로 계산한 값
> - **[Gemini 생성 설명]** 표시: 이번 실행에서 Gemini가 만든 문장 (원본 대조 검증 전)
> - **[과거 검증 기록]** 표시: STEP 10 개발 과정의 과거 기록 (이번 실행 결과의 검증값이 아님)

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

- 필터 통과 공고 수: {run_summary['filter_pass_count']}건 / 전체 {total}건
- 사용한 기준: 공고 제목(`job_title`)에 AX/AI 관련 키워드 {len(RELEVANCE_KEYWORDS)}개 중 하나 이상 포함
  - 영문 키워드는 앞뒤에 영문자·숫자가 없을 때만 매칭, 한글 키워드는 포함 검색
- 매칭된 키워드: {run_summary['matched_keyword_text']}

이 필터는 **1차 후보 선별용**입니다. 제목에 키워드가 있다고 원하는 AX 직무라는 뜻은 아닙니다.

## 4. 주요 공고

**[데이터 기반 사실]** — 현재 수집된 {total}건 전체

{_job_table(jobs_df)}

- 지원 시작일 = `applicationPeriod.start`, 지원 마감일 = `applicationPeriod.end` (원본 값 그대로)

## 5. Gemini 실행 결과

{_gemini_run_section(run_summary)}

## 6. Gemini 검증 상태

{validation_text}

## 7. 제한 사항

{limitation_text}

## 8. 다음 단계

- {next_step_text}
"""
    if historical_validation:
        report += "\n" + _historical_section(historical_validation)
    return report


def save_report(report_text, report_path):
    """보고서 문자열을 UTF-8로 저장하고 저장 경로를 반환한다. (폴더가 없으면 만든다)"""
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text, encoding="utf-8")
    return report_path
