# Resume Matcher Agent

A LangGraph agent that compares a resume with a job description and returns a **skill gap analysis**: what matches, what is missing, a weighted fit score, and concrete recommendations to close the gaps.

It runs in two modes:

- **Rule-based (offline):** a skill taxonomy with 50+ skills and their aliases, regex based JD section detection, experience and education parsing. No API key needed.
- **LLM-enhanced:** when an LLM is configured (OpenAI, Azure OpenAI, Anthropic or Ollama), extraction is enriched with structured output and the advice is written by the model. Rule-based results are always the fallback.

## How it works

```
START ──> parse_resume ──┐
START ──> parse_jd ──────┴──> match ──> score ──(has gaps)──> recommend ───┐
                                               └─(no gaps)──> strong_fit ──┴──> report ──> END
```

| Node | What it does |
|---|---|
| `parse_resume` | Extracts name, skills (plus implied skills, e.g. FastAPI implies Python), years of experience from date ranges, education level |
| `parse_jd` | Extracts title, splits **required** vs **nice to have** skills, minimum years, education requirement |
| `match` | Buckets skills into matched/missing required, matched/missing preferred, and extra strengths |
| `score` | Weighted score: required 55%, preferred 15%, experience 20%, education 10% (configurable) |
| `recommend` | Prioritised, actionable suggestions for every gap |
| `report` | Builds the final `GapReport` |

The two parse nodes run in parallel; `match` waits for both.

## Project structure

```
app/
  agent/        LangGraph state, nodes and graph
  api/          FastAPI app and routes
  llm/          optional LLM client and prompts
  models/       Pydantic schemas
  parsers/      PDF, DOCX and TXT loading and cleaning
  report/       Markdown report formatter
  scoring/      experience/education parsing, matching and scoring
  skills/       skill taxonomy and extractor
samples/        sample resume and job descriptions
tests/          pytest suite (runs offline)
cli.py          command line entry point
```

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env             # add a key, or set USE_LLM=false
```

### CLI

```bash
python cli.py --resume samples/resume_dotnet.txt --jd samples/jd_dotnet_backend.txt
python cli.py --resume my_cv.pdf --jd jd.docx --json --out report.json
```

### API

```bash
uvicorn app.api.main:app --reload
```

Open http://localhost:8000/docs for Swagger.

| Method | Route | Body |
|---|---|---|
| GET | `/health` | none |
| POST | `/match` | multipart: `resume` file + `jd_file` or `jd_text` |
| POST | `/match/text` | JSON: `resume_text`, `jd_text` |

Add `?format=markdown` to either match route to get a Markdown report instead of JSON.

```bash
curl -X POST "http://localhost:8000/match?format=markdown" \
  -F "resume=@samples/resume_dotnet.txt" \
  -F "jd_text=$(cat samples/jd_dotnet_backend.txt)"
```

### Docker

```bash
docker build -t resume-matcher-agent .
docker run -p 8000:8000 --env-file .env resume-matcher-agent
```

## Sample output

```
# Resume Gap Analysis
**Candidate:** Rahul Verma
**Role:** Senior .NET Backend Developer
**Result:** Strong fit (80/100)

| Area | Score |
|---|---|
| Required skills | 80% |
| Preferred skills | 40% |
| Experience | 100% |
| Education | 100% |

## Recommendations
- [HIGH] docker: Containerise one of your existing APIs and push the image to a registry.
- [HIGH] microservices: Split a monolith project into two services that talk over REST or gRPC.
- [MEDIUM] kubernetes: Deploy a containerised service to a local kind/minikube cluster ...
```

## Configuration

All settings live in `.env` (see `.env.example`): LLM provider and model, upload size limit, log level and the four scoring weights.

## Tests

```bash
pytest -q
```

The suite forces `USE_LLM=false`, so it never calls a paid API. CI runs ruff and pytest on every push.

## Roadmap

- Semantic skill matching with embeddings for skills outside the taxonomy
- Batch mode: rank many resumes against one JD
- Simple web UI for uploads
