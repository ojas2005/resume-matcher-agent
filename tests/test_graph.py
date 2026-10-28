from app.agent.graph import run_matcher


def test_dotnet_resume_against_dotnet_jd(resume_text, jd_text):
    report = run_matcher(resume_text, jd_text)
    assert report.candidate_name == "Rahul Verma"
    assert report.job_title == "Senior .NET Backend Developer"
    assert "c#" in report.skills.matched_required
    assert "docker" in report.skills.missing_required
    assert report.score.overall > 50
    assert any(r.area == "docker" and r.priority == "high" for r in report.recommendations)


def test_dotnet_resume_against_genai_jd_is_weaker(resume_text, jd_text, genai_jd_text):
    dotnet = run_matcher(resume_text, jd_text)
    genai = run_matcher(resume_text, genai_jd_text)
    assert genai.score.overall < dotnet.score.overall
    assert "langgraph" in genai.skills.missing_required
