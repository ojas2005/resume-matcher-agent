"""Pull years of experience and education level out of free text."""

import re
from datetime import date

_MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}

_YEARS_MENTION = re.compile(r"(\d{1,2}(?:\.\d)?)\s*\+?\s*(?:years?|yrs?)", re.IGNORECASE)
_RANGE = re.compile(
    r"(?:(?P<m1>[a-z]{3})[a-z]*\.?\s+)?(?P<y1>(?:19|20)\d{2})\s*(?:-|to|–)\s*"
    r"(?:(?:(?P<m2>[a-z]{3})[a-z]*\.?\s+)?(?P<y2>(?:19|20)\d{2})|(?P<now>present|current|now|till date))",
    re.IGNORECASE,
)

EDUCATION_LEVELS: list[tuple[int, str, tuple[str, ...]]] = [
    (4, "PhD", ("phd", "ph.d", "doctorate")),
    (3, "Master's", ("master", "m.tech", "mtech", "m.sc", "msc", "mca", "mba", "m.e.")),
    (2, "Bachelor's", ("bachelor", "b.tech", "btech", "b.e.", "b.sc", "bsc", "bca", "b.s.", "graduate")),
    (1, "Diploma", ("diploma",)),
]


def _month(token: str | None, default: int) -> int:
    return _MONTHS.get((token or "").lower()[:3], default)


def years_from_ranges(text: str, today: date | None = None) -> float:
    today = today or date.today()
    months = 0
    for m in _RANGE.finditer(text):
        start = int(m["y1"]) * 12 + _month(m["m1"], 1)
        if m["now"]:
            end = today.year * 12 + today.month
        else:
            end = int(m["y2"]) * 12 + _month(m["m2"], 12) + 1  # end month counts in full
        if end > start:
            months += end - start
    return round(months / 12, 1)


def resume_years(text: str, today: date | None = None) -> float:
    mentioned = [float(x) for x in _YEARS_MENTION.findall(text)]
    return max([years_from_ranges(text, today), *mentioned], default=0.0)


def required_years(jd_text: str) -> float:
    found = [float(x) for x in _YEARS_MENTION.findall(jd_text)]
    return min(found) if found else 0.0


def education_level(text: str) -> tuple[int, list[str]]:
    lowered = text.lower()
    labels = [label for _, label, keys in EDUCATION_LEVELS if any(k in lowered for k in keys)]
    level = max((lvl for lvl, _, keys in EDUCATION_LEVELS if any(k in lowered for k in keys)), default=0)
    return level, labels
