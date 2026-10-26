import operator
from typing import Annotated, TypedDict

from app.models.schemas import GapReport, JobProfile, Recommendation, ResumeProfile, ScoreBreakdown, SkillMatch


class MatcherState(TypedDict, total=False):
    resume_text: str
    jd_text: str
    resume: ResumeProfile
    job: JobProfile
    skills: SkillMatch
    score: ScoreBreakdown
    summary: str
    recommendations: list[Recommendation]
    report: GapReport
    errors: Annotated[list[str], operator.add]
