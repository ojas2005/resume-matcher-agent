"""Run the matcher from the terminal.

    python cli.py --resume samples/resume_dotnet.txt --jd samples/jd_dotnet_backend.txt
"""

import argparse
import sys

from app.agent.graph import run_matcher
from app.logging_config import setup_logging
from app.parsers import load_path
from app.report.formatter import to_markdown


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Resume vs job description gap analysis")
    parser.add_argument("--resume", required=True, help="Path to resume (.pdf, .docx, .txt)")
    parser.add_argument("--jd", required=True, help="Path to job description (.pdf, .docx, .txt)")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    parser.add_argument("--out", help="Write the report to this file")
    args = parser.parse_args(argv)

    setup_logging()
    report = run_matcher(load_path(args.resume), load_path(args.jd))
    output = report.model_dump_json(indent=2) if args.json else to_markdown(report)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(output)
        print(f"Report written to {args.out}")
    else:
        sys.stdout.write(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
