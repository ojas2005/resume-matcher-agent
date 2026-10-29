from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from app.models.schemas import Recommendation


class LLMResumeExtraction(BaseModel):
    name: str | None = Field(None, description="Candidate full name if present")
    skills: list[str] = Field(default_factory=list, description="Technical skills, lowercase, short canonical names")


class LLMJobExtraction(BaseModel):
    title: str | None = Field(None, description="Job title")
    required_skills: list[str] = Field(default_factory=list, description="Must-have technical skills, lowercase")
    preferred_skills: list[str] = Field(default_factory=list, description="Nice-to-have technical skills, lowercase")


class LLMAdvice(BaseModel):
    summary: str = Field(description="3-4 sentence honest summary of the candidate's fit for this role")
    recommendations: list[Recommendation] = Field(default_factory=list)


RESUME_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You extract structured data from resumes. Only list skills the resume actually shows. "
               "Use short lowercase names like 'c#', 'asp.net core', 'docker'."),
    ("human", "Resume:\n\n{text}"),
])

JD_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You extract structured hiring requirements from job descriptions. Separate must-have skills "
               "from nice-to-have ones. Use short lowercase names like 'c#', 'asp.net core', 'docker'."),
    ("human", "Job description:\n\n{text}"),
])

ADVICE_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "You are a practical technical career coach. Given a gap analysis between a resume and a job, "
               "write a short honest summary and concrete recommendations. Each recommendation names the area, "
               "a priority (high, medium, low) and one specific action the candidate can take in under a month. "
               "Do not invent experience the candidate does not have. Do not use em dashes."),
    ("human", "Job title: {job_title}\nOverall score: {overall}/100 ({fit})\n"
              "Matched required: {matched_required}\nMissing required: {missing_required}\n"
              "Missing preferred: {missing_preferred}\nExperience: {have_years} yrs (needs {need_years})\n"
              "Extra skills the candidate has: {extra}"),
])
