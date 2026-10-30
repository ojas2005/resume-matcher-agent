import re

from app.agent.state import MatcherState
from app.llm.client import get_llm
from app.llm.prompts import JD_PROMPT, LLMJobExtraction
from app.logging_config import get_logger
from app.models.schemas import JobProfile
from app.scoring.experience import education_level, required_years
from app.skills.extractor import extract_jd_skills, extract_skills

log = get_logger(__name__)

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

    llm = get_llm()
    if llm is None:
        return {"job": job}
    try:
        result: LLMJobExtraction = (JD_PROMPT | llm.with_structured_output(LLMJobExtraction)).invoke(
            {"text": text[:12000]}
        )
        llm_pref = set(extract_skills(" , ".join(result.preferred_skills)))
        llm_req = set(extract_skills(" , ".join(result.required_skills))) - llm_pref
        job.preferred_skills = sorted((set(job.preferred_skills) | llm_pref) - llm_req)
        job.required_skills = sorted((set(job.required_skills) | llm_req) - set(job.preferred_skills))
        job.title = result.title or job.title
        return {"job": job}
    except Exception as exc:
        log.warning("LLM JD parsing failed: %s", exc)
        return {"job": job, "errors": [f"llm_jd: {exc}"]}
