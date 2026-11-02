from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.llm.client import get_llm
from app.logging_config import setup_logging

setup_logging()

app = FastAPI(
    title=get_settings().app_name,
    description="Upload a resume and a job description, get a skill gap analysis back.",
    version="0.1.0",
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@app.get("/health", tags=["meta"])
def health():
    return {"status": "ok", "mode": "llm" if get_llm() is not None else "rule-based"}
