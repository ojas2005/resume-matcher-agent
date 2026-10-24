"""Skill matching and weighted fit scoring."""

from app.models.schemas import JobProfile, ResumeProfile, SkillMatch


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
