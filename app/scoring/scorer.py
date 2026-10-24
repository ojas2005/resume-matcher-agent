"""Skill matching and weighted fit scoring."""

from app.config import Settings, get_settings
from app.models.schemas import JobProfile, ResumeProfile, ScoreBreakdown, SkillMatch


def match_skills(resume: ResumeProfile, job: JobProfile) -> SkillMatch:
    have = set(resume.skills)
    required, preferred = set(job.required_skills), set(job.preferred_skills)
    return SkillMatch(
        matched_required=sorted(required & have),
        missing_required=sorted(required - have),
        matched_preferred=sorted(preferred & have),
        missing_preferred=sorted(preferred - have),
        extra_skills=sorted(have - required - preferred),
    )


def _ratio(matched: int, total: int) -> float:
    return 1.0 if total == 0 else matched / total


def compute_score(
    match: SkillMatch, resume: ResumeProfile, job: JobProfile, settings: Settings | None = None
) -> ScoreBreakdown:
    s = settings or get_settings()
    required = _ratio(len(match.matched_required), len(match.matched_required) + len(match.missing_required))
    preferred = _ratio(len(match.matched_preferred), len(match.matched_preferred) + len(match.missing_preferred))

    if job.min_years_experience <= 0:
        experience = 1.0
    else:
        experience = min(1.0, resume.years_experience / job.min_years_experience)

    if job.education_level <= 0 or resume.education_level >= job.education_level:
        education = 1.0
    else:
        education = 0.5 if resume.education_level > 0 else 0.0

    overall = 100 * (
        s.weight_required * required
        + s.weight_preferred * preferred
        + s.weight_experience * experience
        + s.weight_education * education
    )
    return ScoreBreakdown(
        required=round(required * 100, 1),
        preferred=round(preferred * 100, 1),
        experience=round(experience * 100, 1),
        education=round(education * 100, 1),
        overall=round(overall, 1),
    )


def fit_label(overall: float) -> str:
    if overall >= 80:
        return "Strong fit"
    if overall >= 60:
        return "Good fit"
    if overall >= 40:
        return "Partial fit"
    return "Weak fit"
