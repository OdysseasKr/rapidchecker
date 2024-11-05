import pyparsing as pp

from .parser.grammar import module
from .parser.indent import reset_level


def get_exception_message(e: pp.ParseSyntaxException) -> str:
    return f"{e.lineno}:{e.column} {e.msg}, found {e.found}"


def check_format(content: str) -> list[pp.ParseSyntaxException]:
    reset_level()
    errors = []
    try:
        module.parseString(content, parseAll=True)
    except pp.ParseSyntaxException as e:
        message = get_exception_message(e)
        errors.append(message)
    return errors
