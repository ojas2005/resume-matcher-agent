import os
from pathlib import Path

import pytest

# Tests always run offline, without calling an LLM.
os.environ["USE_LLM"] = "false"

SAMPLES = Path(__file__).resolve().parent.parent / "samples"


@pytest.fixture
def resume_text() -> str:
    return (SAMPLES / "resume_dotnet.txt").read_text(encoding="utf-8")


@pytest.fixture
def jd_text() -> str:
    return (SAMPLES / "jd_dotnet_backend.txt").read_text(encoding="utf-8")


@pytest.fixture
def genai_jd_text() -> str:
    return (SAMPLES / "jd_genai_engineer.txt").read_text(encoding="utf-8")
