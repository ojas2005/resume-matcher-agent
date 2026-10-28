from app.agent.state import MatcherState
from app.models.schemas import GapReport
from app.scoring.scorer import fit_label


def report_node(state: MatcherState) -> dict:
    resume, job, score = state["resume"], state["job"], state["score"]
    report = GapReport(
        candidate_name=resume.name,
        job_title=job.title,
        fit_label=fit_label(score.overall),
        score=score,
        skills=state["skills"],
        experience_gap_years=round(max(0.0, job.min_years_experience - resume.years_experience), 1),
        summary=state.get("summary", ""),
        recommendations=state.get("recommendations", []),
    )
    return {"report": report}
