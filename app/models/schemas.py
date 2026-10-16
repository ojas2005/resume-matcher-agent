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
