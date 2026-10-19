"""Turn an uploaded file into clean plain text."""

from pathlib import Path

from app.parsers.docx_parser import extract_docx_text
from app.parsers.pdf_parser import extract_pdf_text
from app.parsers.text_cleaner import clean_text

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt", ".md"}


class UnsupportedFileError(ValueError):
    pass


def load_document(filename: str, data: bytes) -> str:
    ext = Path(filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileError(
            f"Unsupported file type '{ext}'. Use one of: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
        )
    if ext == ".pdf":
        raw = extract_pdf_text(data)
    elif ext == ".docx":
        raw = extract_docx_text(data)
    else:
        raw = data.decode("utf-8", errors="ignore")
    return clean_text(raw)


def load_path(path: str | Path) -> str:
    path = Path(path)
    return load_document(path.name, path.read_bytes())
