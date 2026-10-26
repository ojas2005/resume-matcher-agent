import re

from app.agent.state import MatcherState
from app.models.schemas import ResumeProfile
from app.scoring.experience import education_level, resume_years
from app.skills.extractor import extract_skills


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

    return {"resume": profile}
