from app.agent.state import MatcherState
from app.scoring.scorer import compute_score, match_skills


def match_node(state: MatcherState) -> dict:
    return {"skills": match_skills(state["resume"], state["job"])}


def score_node(state: MatcherState) -> dict:
    return {"score": compute_score(state["skills"], state["resume"], state["job"])}
