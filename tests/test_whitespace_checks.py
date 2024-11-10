from pathlib import Path

from rapidchecker.whitespace_checks import (
    NoTrailingLineError,
    TooManyEmptyLinesError,
    TrailingSpaceError,
    check_whitespace,
)


def test_check_whitespace_no_errors() -> None:
    file_contents = Path("./tests/rapid_samples/SimpleModule.sys").read_text()
    result = check_whitespace(file_contents)
    assert not result


def test_check_whitespace_with_errors() -> None:
    file_contents = Path("./tests/rapid_samples/BadWhitespaceModule.sys").read_text()
    result = check_whitespace(file_contents)
    expected = [
        TrailingSpaceError(
            lineno=4,
            col=26,
            error="Line ends with space",
            suggestion="Remove trailing spaces",
        ),
        TooManyEmptyLinesError(
            lineno=7,
            col=0,
            error="Too many empty lines",
            suggestion="Use up to 2 empty lines",
        ),
        TooManyEmptyLinesError(
            lineno=8,
            col=0,
            error="Too many empty lines",
            suggestion="Use up to 2 empty lines",
        ),
        NoTrailingLineError(
            lineno=27,
            col=0,
            error="Line does not end with a new line character",
            suggestion="Add a new line character at the end of the line",
        ),
    ]

    assert result == expected
