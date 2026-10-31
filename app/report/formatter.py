"""Render a GapReport as Markdown for the CLI and the /match?format=markdown endpoint."""

from app.models.schemas import GapReport


def _bullets(items: list[str]) -> str:
    return "\n".join(f"- {i}" for i in items) if items else "- none"


def to_markdown(report: GapReport) -> str:
    s, k = report.score, report.skills
    lines = [
        "# Resume Gap Analysis",
        "",
        f"**Candidate:** {report.candidate_name or 'Unknown'}  ",
        f"**Role:** {report.job_title or 'Unknown'}  ",
        f"**Result:** {report.fit_label} ({s.overall:g}/100)",
        "",
        "## Score breakdown",
        "",
        "| Area | Score |",
        "|---|---|",
        f"| Required skills | {s.required:g}% |",
        f"| Preferred skills | {s.preferred:g}% |",
        f"| Experience | {s.experience:g}% |",
        f"| Education | {s.education:g}% |",
        "",
        "## Summary",
        "",
        report.summary,
        "",
        "## Skills",
        "",
        "**Matched (required)**",
        _bullets(k.matched_required),
        "",
        "**Missing (required)**",
        _bullets(k.missing_required),
        "",
        "**Missing (nice to have)**",
        _bullets(k.missing_preferred),
        "",
        "**Extra strengths**",
        _bullets(k.extra_skills),
    ]
    if report.experience_gap_years > 0:
        lines += ["", f"**Experience gap:** {report.experience_gap_years:g} years"]
    if report.recommendations:
        lines += ["", "## Recommendations", ""]
        for r in report.recommendations:
            lines.append(f"- **[{r.priority.upper()}] {r.area}:** {r.suggestion}")
    return "\n".join(lines) + "\n"
