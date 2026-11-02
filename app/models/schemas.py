"""Pydantic models shared across the agent, API and CLI."""

from pydantic import BaseModel, Field


class ResumeProfile(BaseModel):
    name: str | None = None
    skills: list[str] = Field(default_factory=list)
    years_experience: float = 0.0
    education_level: int = 0
    education: list[str] = Field(default_factory=list)


class JobProfile(BaseModel):
    title: str | None = None
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    min_years_experience: float = 0.0
    education_level: int = 0


class SkillMatch(BaseModel):
    matched_required: list[str] = Field(default_factory=list)
    missing_required: list[str] = Field(default_factory=list)
    matched_preferred: list[str] = Field(default_factory=list)
    missing_preferred: list[str] = Field(default_factory=list)
    extra_skills: list[str] = Field(default_factory=list)


class ScoreBreakdown(BaseModel):
    required: float = 0.0
    preferred: float = 0.0
    experience: float = 0.0
    education: float = 0.0
    overall: float = 0.0


class Recommendation(BaseModel):
    area: str
    priority: str  # high | medium | low
    suggestion: str


class GapReport(BaseModel):
    candidate_name: str | None = None
    job_title: str | None = None
    fit_label: str
    score: ScoreBreakdown
    skills: SkillMatch
    experience_gap_years: float = 0.0
    summary: str
    recommendations: list[Recommendation] = Field(default_factory=list)


class MatchTextRequest(BaseModel):
    resume_text: str = Field(min_length=20)
    jd_text: str = Field(min_length=20)
