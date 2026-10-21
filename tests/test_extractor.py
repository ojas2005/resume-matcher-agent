from app.skills.extractor import extract_jd_skills, extract_skills


def test_aliases_map_to_canonical_names():
    skills = extract_skills("Worked with csharp, dotnet, EF Core and k8s")
    assert {"c#", ".net", "entity framework", "kubernetes"} <= set(skills)


def test_jd_required_vs_preferred(jd_text):
    required, preferred = extract_jd_skills(jd_text)
    assert "c#" in required and "docker" in required
    assert "kubernetes" in preferred and "redis" in preferred
    assert not set(required) & set(preferred)
