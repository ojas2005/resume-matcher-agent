from app.agent.state import MatcherState
from app.scoring.scorer import compute_score, match_skills


def match_node(state: MatcherState) -> dict:
    return {"skills": match_skills(state["resume"], state["job"])}


def score_node(state: MatcherState) -> dict:
    return {"score": compute_score(state["skills"], state["resume"], state["job"])}


def route_after_score(state: MatcherState) -> str:
    """Skip the advice step when there is nothing meaningful to fix."""
    skills, resume, job = state["skills"], state["resume"], state["job"]
    no_gaps = not skills.missing_required and not skills.missing_preferred
    if no_gaps and resume.years_experience >= job.min_years_experience:
        return "no_gaps"
    return "has_gaps"
