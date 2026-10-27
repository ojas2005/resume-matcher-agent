import re

from app.agent.state import MatcherState
from app.models.schemas import JobProfile
from app.scoring.experience import education_level, required_years
from app.skills.extractor import extract_jd_skills, extract_skills

_TITLE_HINT = re.compile(r"(developer|engineer|architect|analyst|lead|consultant|programmer)", re.IGNORECASE)


def guess_title(text: str) -> str | None:
    for line in text.splitlines()[:8]:
        line = line.strip(" :-#*")
        if line.lower().startswith(("job title", "role", "position")) and ":" in line:
            return line.split(":", 1)[1].strip()
        if _TITLE_HINT.search(line) and len(line) < 70:
            return line
    return None


def parse_jd(state: MatcherState) -> dict:
    text = state["jd_text"]
    required, preferred = extract_jd_skills(text)
    level, _ = education_level(text)
    job = JobProfile(
        title=guess_title(text),
        required_skills=required,
        preferred_skills=preferred,
        min_years_experience=required_years(text),
        education_level=level,
    )

    return {"job": job}
