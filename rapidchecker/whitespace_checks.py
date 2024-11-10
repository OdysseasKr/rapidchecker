from dataclasses import dataclass

from .config import CONFIG


@dataclass
class WhiteSpaceError:
    lineno: int
    col: int = 0
    error: str = ""
    suggestion: str = ""

    def __str__(self) -> str:
        return f"{self.lineno}:{self.col} {self.error}. => {self.suggestion}"


@dataclass
class TooManyEmptyLinesError(WhiteSpaceError):
    def __post_init__(self) -> None:
        self.error = "Too many empty lines"
        self.suggestion = f"Use up to {CONFIG.max_empty_lines} empty lines"


@dataclass
class TrailingSpaceError(WhiteSpaceError):
    def __post_init__(self) -> None:
        self.error = "Line ends with space"
        self.suggestion = "Remove trailing spaces"


@dataclass
class NoTrailingLineError(WhiteSpaceError):
    def __post_init__(self) -> None:
        self.error = "Line does not end with a new line character"
        self.suggestion = "Add a new line character at the end of the line"


def trailing_space(line: str) -> bool:
    if CONFIG.allow_trailing_space:
        return False
    return line.endswith(" ")


def empty_line(line: str) -> bool:
    return line.strip() == ""


def check_whitespace(content: str) -> list[WhiteSpaceError]:
    errors: list[WhiteSpaceError] = []
    empty_line_count = 0
    lines = content.split("\n")
    for i, line in enumerate(lines, start=1):
        if empty_line(line):
            empty_line_count += 1
            if empty_line_count > CONFIG.max_empty_lines:
                errors.append(TooManyEmptyLinesError(i))
            continue

        empty_line_count = 0
        if trailing_space(line):
            errors.append(TrailingSpaceError(i, col=len(line)))

    if CONFIG.require_new_line_eof and not empty_line(lines[-1]):
        errors.append(NoTrailingLineError(len(lines)))

    return errors
