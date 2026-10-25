from app.config import Settings
from app.models.schemas import JobProfile, ResumeProfile
from app.scoring.scorer import compute_score, fit_label, match_skills


def _profiles():
    resume = ResumeProfile(skills=["c#", "docker", "python"], years_experience=2, education_level=2)
    job = JobProfile(
        required_skills=["c#", "docker", "azure", "sql"],
        preferred_skills=["python", "redis"],
        min_years_experience=4,
        education_level=2,
    )
    return resume, job


def test_match_skills_buckets():
    m = match_skills(*_profiles())
    assert m.matched_required == ["c#", "docker"]
    assert m.missing_required == ["azure", "sql"]
    assert m.matched_preferred == ["python"]
    assert m.missing_preferred == ["redis"]
    assert m.extra_skills == []


def test_weighted_score():
    resume, job = _profiles()
    score = compute_score(match_skills(resume, job), resume, job, Settings())
    # 0.55*0.5 + 0.15*0.5 + 0.20*0.5 + 0.10*1.0 = 0.55
    assert score.overall == 55.0
    assert score.experience == 50.0


def test_empty_requirements_are_full_marks():
    resume, job = ResumeProfile(), JobProfile()
    assert compute_score(match_skills(resume, job), resume, job, Settings()).overall == 100.0


def test_fit_labels():
    assert fit_label(85) == "Strong fit"
    assert fit_label(65) == "Good fit"
    assert fit_label(45) == "Partial fit"
    assert fit_label(10) == "Weak fit"
