"""Rule-based skill extraction. Works offline and acts as the fallback for the LLM."""

import re
from functools import lru_cache

from app.skills.taxonomy import IMPLIED_SKILLS, SKILL_ALIASES


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
