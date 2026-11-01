# Resume Matcher Agent

A LangGraph agent that compares a resume with a job description and returns a skill gap analysis:
what matches, what is missing, a fit score and recommendations.

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## CLI

```bash
python cli.py --resume samples/resume_dotnet.txt --jd samples/jd_dotnet_backend.txt
python cli.py --resume my_cv.pdf --jd jd.docx --json
```

Set `USE_LLM=false` to run fully offline.
