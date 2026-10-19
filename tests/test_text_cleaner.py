from app.parsers import clean_text


def test_bullets_and_spaces_are_normalised():
    assert clean_text("\u2022  C#  and   .NET\n\n\n\nSQL") == "- C# and .NET\n\nSQL"


def test_empty_input():
    assert clean_text("") == ""
