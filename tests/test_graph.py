from app.agent.graph import run_matcher
from app.report.formatter import to_markdown


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


def test_perfect_match_skips_recommendations():
    resume = "Asha Rao\nC# and Docker developer, 4 years of experience. B.Tech."
    jd = "Backend Developer\nRequirements\n- C#\n- Docker\n- 2+ years"
    report = run_matcher(resume, jd)
    assert report.fit_label == "Strong fit"
    assert report.recommendations == []


def test_markdown_report(resume_text, jd_text):
    md = to_markdown(run_matcher(resume_text, jd_text))
    assert md.startswith("# Resume Gap Analysis")
    assert "## Recommendations" in md
