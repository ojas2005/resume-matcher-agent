from app.parsers import clean_text


def test_bullets_and_spaces_are_normalised():
    raw = "•  C#\t\tand   .NET\r\n\r\n\r\n\r\nSQL"
    assert clean_text(raw) == "- C# and .NET\n\nSQL"


def test_empty_input():
    assert clean_text("") == ""
