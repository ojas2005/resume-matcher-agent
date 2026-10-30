import re

from app.agent.state import MatcherState
from app.llm.client import get_llm
from app.llm.prompts import RESUME_PROMPT, LLMResumeExtraction
from app.logging_config import get_logger
from app.models.schemas import ResumeProfile
from app.scoring.experience import education_level, resume_years
from app.skills.extractor import extract_skills

log = get_logger(__name__)


def guess_name(text: str) -> str | None:
    for line in text.splitlines()[:5]:
        line = line.strip()
        if re.fullmatch(r"[A-Za-z][A-Za-z.' ]{1,40}", line) and 1 <= len(line.split()) <= 4:
            return line.title()
    return None


def parse_resume(state: MatcherState) -> dict:
    text = state["resume_text"]
    level, labels = education_level(text)
    profile = ResumeProfile(
        name=guess_name(text),
        skills=extract_skills(text, include_implied=True),
        years_experience=resume_years(text),
        education_level=level,
        education=labels,
    )

    llm = get_llm()
    if llm is None:
        return {"resume": profile}
    try:
        result: LLMResumeExtraction = (RESUME_PROMPT | llm.with_structured_output(LLMResumeExtraction)).invoke(
            {"text": text[:12000]}
        )
        llm_skills = extract_skills(" , ".join(result.skills))  # map LLM names onto our taxonomy
        profile.skills = sorted(set(profile.skills) | set(llm_skills))
        profile.name = result.name or profile.name
        return {"resume": profile}
    except Exception as exc:
        log.warning("LLM resume parsing failed: %s", exc)
        return {"resume": profile, "errors": [f"llm_resume: {exc}"]}
