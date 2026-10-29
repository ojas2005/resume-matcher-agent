"""LangGraph workflow:

    START -> parse_resume ─┐
    START -> parse_jd ─────┴-> match -> score -> (has_gaps) recommend ─┐
                                              -> (no_gaps)  strong_fit ┴-> report -> END
"""

from functools import lru_cache

from langgraph.graph import END, START, StateGraph

from app.agent.nodes import (
    match_node, parse_jd, parse_resume, recommend_node,
    report_node, route_after_score, score_node, strong_fit_node,
)
from app.agent.state import MatcherState
from app.models.schemas import GapReport


def build_graph():
    g = StateGraph(MatcherState)
    g.add_node("parse_resume", parse_resume)
    g.add_node("parse_jd", parse_jd)
    g.add_node("match", match_node)
    g.add_node("score", score_node)
    g.add_node("recommend", recommend_node)
    g.add_node("strong_fit", strong_fit_node)
    g.add_node("report", report_node)

    # resume and JD are parsed in parallel, match waits for both
    g.add_edge(START, "parse_resume")
    g.add_edge(START, "parse_jd")
    g.add_edge(["parse_resume", "parse_jd"], "match")
    g.add_edge("match", "score")
    g.add_conditional_edges("score", route_after_score, {"has_gaps": "recommend", "no_gaps": "strong_fit"})
    g.add_edge("recommend", "report")
    g.add_edge("strong_fit", "report")
    g.add_edge("report", END)
    return g.compile()


@lru_cache
def get_graph():
    return build_graph()


def run_matcher(resume_text: str, jd_text: str) -> GapReport:
    state = get_graph().invoke({"resume_text": resume_text, "jd_text": jd_text, "errors": []})
    return state["report"]
