import pyparsing as pp

from rapidchecker.config import CONFIG

indent_level = 0
INDENT_SIZE = 2
CHECK_INDENT = True


def check_indent(s: str, loc: int, _: pp.ParseResults) -> None:
    global indent_level
    if not CONFIG.indentation_check:
        return

    # Why is this necessary?
    while s[loc].strip() == "":
        loc += 1

    cur_col = pp.col(loc, s)
    expected_col = indent_level * CONFIG.indentation_size + 1

    if cur_col != expected_col:
        raise pp.ParseFatalException(
            s,
            loc,
            f"Bad indentation, (expected col {expected_col}, starts at col {cur_col})",
        )


def add_indent() -> None:
    global indent_level
    indent_level += 1


def remove_indent() -> None:
    global indent_level
    indent_level -= 1


def reset_level() -> None:
    global indent_level
    indent_level = 0


def register_indent_checks(parse_elements: list[pp.ParserElement]) -> None:
    for p in parse_elements:
        p.add_parse_action(check_indent)


INDENT = pp.Empty().set_parse_action(add_indent)
UNDENT = pp.Empty().set_parse_action(remove_indent)
INDENT_CHECKPOINT = pp.Empty().set_parse_action(check_indent)
