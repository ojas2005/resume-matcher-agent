from fastapi import APIRouter, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import PlainTextResponse

from app.agent.graph import run_matcher
from app.config import get_settings
from app.models.schemas import GapReport, MatchTextRequest
from app.parsers import UnsupportedFileError, clean_text, load_document
from app.report.formatter import to_markdown

router = APIRouter(tags=["matcher"])


async def _read_upload(upload: UploadFile) -> str:
    data = await upload.read()
    limit = get_settings().max_file_size_mb * 1024 * 1024
    if len(data) > limit:
        raise HTTPException(413, f"{upload.filename} is larger than {get_settings().max_file_size_mb} MB")
    try:
        text = load_document(upload.filename or "upload.txt", data)
    except UnsupportedFileError as exc:
        raise HTTPException(415, str(exc)) from exc
    if len(text) < 20:
        raise HTTPException(422, f"Could not read enough text from {upload.filename}")
    return text


def _respond(report: GapReport, fmt: str):
    if fmt == "markdown":
        return PlainTextResponse(to_markdown(report), media_type="text/markdown")
    return report


@router.post("/match", response_model=GapReport)
async def match_files(
    resume: UploadFile = File(..., description="Resume as PDF, DOCX or TXT"),
    jd_file: UploadFile | None = File(None, description="Job description file"),
    jd_text: str | None = Form(None, description="Job description as plain text"),
    format: str = Query("json", pattern="^(json|markdown)$"),
):
    if not jd_file and not jd_text:
        raise HTTPException(422, "Provide the job description as jd_file or jd_text")
    resume_text = await _read_upload(resume)
    job_text = await _read_upload(jd_file) if jd_file else clean_text(jd_text or "")
    return _respond(run_matcher(resume_text, job_text), format)


@router.post("/match/text", response_model=GapReport)
async def match_text(body: MatchTextRequest, format: str = Query("json", pattern="^(json|markdown)$")):
    report = run_matcher(clean_text(body.resume_text), clean_text(body.jd_text))
    return _respond(report, format)
