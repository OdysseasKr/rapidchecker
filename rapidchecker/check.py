import pyparsing as pp

from .parser.grammar import module
from .parser.indent import reset_level


def get_exception_message(e: pp.ParseSyntaxException) -> str:
    return f"{e.lineno}:{e.column} {e.msg}, found {e.found}"


pp.ParseSyntaxException.__str__ = get_exception_message  # type: ignore


def check_format(content: str) -> list[pp.ParseBaseException]:
    reset_level()
    errors: list[pp.ParseBaseException] = []
    try:
        module.parseString(content, parseAll=True)
    except pp.ParseSyntaxException as e:
        errors.append(e)
    return errors
