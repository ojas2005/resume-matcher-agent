from app.skills.extractor import extract_jd_skills, extract_skills


def test_aliases_map_to_canonical_names():
    skills = extract_skills("Worked with csharp, dotnet, EF Core and k8s")
    assert {"c#", ".net", "entity framework", "kubernetes"} <= set(skills)


def test_special_characters_do_not_bleed():
    # "asp.net" should not count as plain ".net" via the alias, and "c++" is not "c#"
    assert "c#" not in extract_skills("C++ developer")
    assert "java" not in extract_skills("JavaScript only")


def test_implied_skills():
    assert "python" in extract_skills("Built APIs in FastAPI", include_implied=True)
    assert "python" not in extract_skills("Built APIs in FastAPI")


def test_jd_required_vs_preferred(jd_text):
    required, preferred = extract_jd_skills(jd_text)
    assert "c#" in required and "docker" in required
    assert "kubernetes" in preferred and "redis" in preferred
    assert not set(required) & set(preferred)
