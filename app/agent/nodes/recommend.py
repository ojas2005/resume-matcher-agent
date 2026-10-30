from app.agent.state import MatcherState
from app.llm.client import get_llm
from app.llm.prompts import ADVICE_PROMPT, LLMAdvice
from app.logging_config import get_logger
from app.models.schemas import Recommendation
from app.scoring.scorer import fit_label
from app.skills.taxonomy import LEARNING_HINTS

log = get_logger(__name__)


def rule_based_recommendations(state: MatcherState) -> list[Recommendation]:
    skills, resume, job = state["skills"], state["resume"], state["job"]
    recs = []
    for skill in skills.missing_required:
        hint = LEARNING_HINTS.get(skill, f"Build a small project that uses {skill} and list it on your resume.")
        recs.append(Recommendation(area=skill, priority="high", suggestion=hint))
    for skill in skills.missing_preferred:
        hint = LEARNING_HINTS.get(skill, f"Get hands-on basics in {skill}; even a weekend project helps.")
        recs.append(Recommendation(area=skill, priority="medium", suggestion=hint))
    gap = job.min_years_experience - resume.years_experience
    if gap > 0:
        recs.append(Recommendation(
            area="experience",
            priority="high" if gap >= 2 else "medium",
            suggestion=f"The role asks for {job.min_years_experience:g}+ years. Highlight internships, "
                       "freelance and production-grade projects to cover the gap.",
        ))
    return recs


def rule_based_summary(state: MatcherState) -> str:
    skills, score = state["skills"], state["score"]
    total_req = len(skills.matched_required) + len(skills.missing_required)
    parts = [
        f"Overall match is {score.overall:g}/100 ({fit_label(score.overall).lower()}).",
        f"The resume covers {len(skills.matched_required)} of {total_req} required skills.",
    ]
    if skills.missing_required:
        parts.append(f"Biggest gaps: {', '.join(skills.missing_required[:4])}.")
    if skills.extra_skills:
        parts.append(f"Additional strengths: {', '.join(skills.extra_skills[:4])}.")
    return " ".join(parts)


def recommend_node(state: MatcherState) -> dict:
    fallback = {"summary": rule_based_summary(state), "recommendations": rule_based_recommendations(state)}
    llm = get_llm()
    if llm is None:
        return fallback

    skills, resume, job, score = state["skills"], state["resume"], state["job"], state["score"]
    try:
        advice: LLMAdvice = (ADVICE_PROMPT | llm.with_structured_output(LLMAdvice)).invoke({
            "job_title": job.title or "unknown",
            "overall": score.overall,
            "fit": fit_label(score.overall),
            "matched_required": ", ".join(skills.matched_required) or "none",
            "missing_required": ", ".join(skills.missing_required) or "none",
            "missing_preferred": ", ".join(skills.missing_preferred) or "none",
            "have_years": resume.years_experience,
            "need_years": job.min_years_experience,
            "extra": ", ".join(skills.extra_skills) or "none",
        })
        return {"summary": advice.summary, "recommendations": advice.recommendations or fallback["recommendations"]}
    except Exception as exc:
        log.warning("LLM advice failed: %s", exc)
        return {**fallback, "errors": [f"llm_advice: {exc}"]}


def strong_fit_node(state: MatcherState) -> dict:
    return {
        "summary": rule_based_summary(state) + " No skill gaps found against this job description.",
        "recommendations": [],
    }
