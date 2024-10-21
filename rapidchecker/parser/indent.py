import pyparsing as pp

indent_level = 0
INDENT_SIZE = 2
CHECK_INDENT = True


def check_indent(s, loc, tokens):
    global indent_level
    if not CHECK_INDENT:
        return

    # Why is this necessary?
    while s[loc].strip() == "":
        loc += 1

    cur_col = pp.col(loc, s)
    expected_col = indent_level * INDENT_SIZE + 1

    if cur_col != expected_col:
        raise pp.ParseFatalException(
            s,
            loc,
            f"Bad indentation, (expected col {expected_col}, starts at col {cur_col})",
        )


def add_indent(s, loc, tokens):
    global indent_level
    indent_level += 1


def remove_indent():
    global indent_level
    indent_level -= 1


def reset_level():
    global indent_level
    indent_level = 0


def register_indent_checks(parse_elements: list[pp.ParserElement]):
    for p in parse_elements:
        p.add_parse_action(check_indent)


INDENT = pp.Empty().set_parse_action(add_indent)
UNDENT = pp.Empty().set_parse_action(remove_indent)
INDENT_CHECKPOINT = pp.Empty().set_parse_action(check_indent)
