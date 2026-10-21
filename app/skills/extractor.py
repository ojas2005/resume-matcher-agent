"""Rule-based skill extraction. Works offline and acts as the fallback for the LLM."""

import re
from functools import lru_cache

from app.skills.taxonomy import IMPLIED_SKILLS, SKILL_ALIASES

_PREFERRED_HEADINGS = ("nice to have", "good to have", "preferred", "bonus", "plus", "added advantage")
_REQUIRED_HEADINGS = ("requirements", "required", "must have", "qualifications", "what you bring", "skills")


@lru_cache
def _patterns() -> list[tuple[str, re.Pattern[str]]]:
    compiled = []
    for canonical, aliases in SKILL_ALIASES.items():
        for alias in sorted(aliases, key=len, reverse=True):
            # \w lookarounds so "c#" or ".net" work where \b would not
            pattern = re.compile(rf"(?<![\w.]){re.escape(alias)}(?![\w#+])", re.IGNORECASE)
            compiled.append((canonical, pattern))
    return compiled


def extract_skills(text: str, include_implied: bool = False) -> list[str]:
    found: set[str] = set()
    for canonical, pattern in _patterns():
        if canonical not in found and pattern.search(text):
            found.add(canonical)
    if include_implied:
        for skill in list(found):
            found.update(IMPLIED_SKILLS.get(skill, []))
    return sorted(found)


def _is_heading(line: str, keywords: tuple[str, ...]) -> bool:
    lowered = line.lower().strip(" :-#*")
    return len(lowered) < 60 and any(k in lowered for k in keywords)


def split_jd_sections(jd_text: str) -> tuple[str, str]:
    """Return (required_text, preferred_text) based on common JD headings."""
    required, preferred = [], []
    bucket = required
    for line in jd_text.splitlines():
        if _is_heading(line, _PREFERRED_HEADINGS):
            bucket = preferred
        elif _is_heading(line, _REQUIRED_HEADINGS):
            bucket = required
        elif re.search(r"\b(nice to have|good to have|is a plus|preferred)\b", line, re.IGNORECASE):
            preferred.append(line)
            continue
        bucket.append(line)
    return "\n".join(required), "\n".join(preferred)


def extract_jd_skills(jd_text: str) -> tuple[list[str], list[str]]:
    required_text, preferred_text = split_jd_sections(jd_text)
    preferred = set(extract_skills(preferred_text))
    required = set(extract_skills(required_text)) - preferred
    return sorted(required), sorted(preferred)
