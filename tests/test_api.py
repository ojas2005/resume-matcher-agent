from fastapi.testclient import TestClient

from app.api.main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "mode": "rule-based"}


def test_match_text(resume_text, jd_text):
    res = client.post("/match/text", json={"resume_text": resume_text, "jd_text": jd_text})
    assert res.status_code == 200
    body = res.json()
    assert body["fit_label"] in {"Strong fit", "Good fit", "Partial fit", "Weak fit"}
    assert "c#" in body["skills"]["matched_required"]


def test_match_upload_markdown(resume_text, jd_text):
    res = client.post(
        "/match?format=markdown",
        files={"resume": ("cv.txt", resume_text.encode(), "text/plain")},
        data={"jd_text": jd_text},
    )
    assert res.status_code == 200
    assert res.text.startswith("# Resume Gap Analysis")


def test_match_requires_jd(resume_text):
    res = client.post("/match", files={"resume": ("cv.txt", resume_text.encode(), "text/plain")})
    assert res.status_code == 422


def test_unsupported_file(jd_text):
    res = client.post(
        "/match",
        files={"resume": ("cv.png", b"not really an image but long enough", "image/png")},
        data={"jd_text": jd_text},
    )
    assert res.status_code == 415
