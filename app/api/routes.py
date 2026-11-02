from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse

from app.agent.graph import run_matcher
from app.models.schemas import GapReport, MatchTextRequest
from app.parsers import clean_text
from app.report.formatter import to_markdown

router = APIRouter(tags=["matcher"])


def _respond(report: GapReport, fmt: str):
    if fmt == "markdown":
        return PlainTextResponse(to_markdown(report), media_type="text/markdown")
    return report


@router.post("/match/text", response_model=GapReport)
async def match_text(body: MatchTextRequest, format: str = Query("json", pattern="^(json|markdown)$")):
    report = run_matcher(clean_text(body.resume_text), clean_text(body.jd_text))
    return _respond(report, format)
