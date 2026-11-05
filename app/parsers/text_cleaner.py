import re
import unicodedata

_BULLETS = re.compile(r"[•●▪‣⁃◦]")
_SPACES = re.compile(r"[ \t ]+")
_BLANK_LINES = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    """Normalise text pulled out of PDFs/DOCX so regex matching behaves."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = _BULLETS.sub("-", text)
    text = _SPACES.sub(" ", text)
    text = "".join(ch for ch in text if ch == "\n" or ch.isprintable())
    text = "\n".join(line.strip() for line in text.split("\n"))
    text = _BLANK_LINES.sub("\n\n", text)
    return text.strip()
