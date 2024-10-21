import pyparsing as pp

from .parser.grammar import module
from .parser.indent import reset_level


def format_exception_message(e: pp.ParseSyntaxException):
    return f"{e.msg}{foundstr(e)}"


def foundstr(e: pp.ParseSyntaxException):
    if not e.pstr:
        return ""

    if e.loc >= len(e.pstr):
        return ", found end of text"
    # pull out next word at error location
    found_match = pp.exceptions._exception_word_extractor.match(e.pstr, e.loc)
    if found_match is not None:
        found = found_match.group(0)
    else:
        found = e.pstr[e.loc : e.loc + 1]
    return (", found %r" % found).replace(r"\\", "\\")


def check_format(content: str) -> list[pp.ParseSyntaxException]:
    reset_level()
    errors = []
    try:
        module.parseString(content, parseAll=True)
    except pp.ParseSyntaxException as e:
        # TODO: Fix message formatting here
        errors.append(f"{e.lineno}:{e.column} {format_exception_message(e)}")
    return errors
