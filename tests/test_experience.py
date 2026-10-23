from datetime import date

from app.scoring.experience import education_level, required_years, resume_years, years_from_ranges


def test_date_ranges_until_present():
    text = "Engineer (Jan 2023 - Present)"
    assert years_from_ranges(text, today=date(2025, 1, 1)) == 2.0


def test_resume_years_takes_explicit_mentions():
    assert resume_years("5+ years building APIs") == 5.0


def test_required_years_uses_minimum():
    assert required_years("3+ years C#, 5 years preferred") == 3.0
    assert required_years("No experience needed") == 0.0


def test_education_level():
    level, labels = education_level("B.Tech in Computer Science")
    assert level == 2 and labels == ["Bachelor's"]
