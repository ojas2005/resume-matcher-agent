import io

import pytest
from docx import Document

from app.parsers import UnsupportedFileError, load_document


def test_txt_file():
    assert load_document("cv.txt", b"Python   developer") == "Python developer"


def test_docx_file_includes_tables():
    doc = Document()
    doc.add_paragraph("Ojas")
    table = doc.add_table(rows=1, cols=2)
    table.rows[0].cells[0].text = "Docker"
    table.rows[0].cells[1].text = "Azure"
    buf = io.BytesIO()
    doc.save(buf)
    text = load_document("cv.docx", buf.getvalue())
    assert "Ojas" in text and "Docker | Azure" in text


def test_unsupported_extension():
    with pytest.raises(UnsupportedFileError):
        load_document("cv.png", b"...")
