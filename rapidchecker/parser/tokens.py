from pyparsing import CaselessKeyword, ParseResults, oneOf

from rapidchecker.config import CONFIG


def case_check(s: str, loc: int, tokens: ParseResults) -> bool:
    return s[loc : loc + len(tokens[0])].isupper()


class RapidKeyword(CaselessKeyword):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if CONFIG.require_uppercase_keywords:
            self.addCondition(case_check, message="Keyword needs to be in uppercase")


# TODO: Can we turn these into enums?
MODULE = RapidKeyword("MODULE")
ENDMODULE = RapidKeyword("ENDMODULE")
VAR = RapidKeyword("VAR")
PERS = RapidKeyword("PERS")
FUNC = RapidKeyword("FUNC")
ENDFUNC = RapidKeyword("ENDFUNC")
PROC = RapidKeyword("PROC")
ENDPROC = RapidKeyword("ENDPROC")
TRAP = RapidKeyword("TRAP")
ENDTRAP = RapidKeyword("ENDTRAP")
IF = RapidKeyword("IF")
ENDIF = RapidKeyword("ENDIF")
ELSE = RapidKeyword("ELSE")
ELSEIF = RapidKeyword("ELSEIF")
THEN = RapidKeyword("THEN")
WHILE = RapidKeyword("WHILE")
ENDWHILE = RapidKeyword("ENDWHILE")
FOR = RapidKeyword("FOR")
ENDFOR = RapidKeyword("ENDFOR")
DO = RapidKeyword("DO")
FROM = RapidKeyword("FROM")
TO = RapidKeyword("TO")
STEP = RapidKeyword("STEP")
RETURN = RapidKeyword("RETURN")
CONNECT = RapidKeyword("CONNECT")
WITH = RapidKeyword("WITH")
CONST = RapidKeyword("CONST")
AND = RapidKeyword("AND")
OR = RapidKeyword("OR")
NOT = RapidKeyword("NOT")
DIV = RapidKeyword("DIV")
MOD = RapidKeyword("MOD")
XOR = RapidKeyword("XOR")
RECORD = RapidKeyword("RECORD")
ENDRECORD = RapidKeyword("ENDRECORD")
TEST = RapidKeyword("TEST")
ENDTEST = RapidKeyword("ENDTEST")
CASE = RapidKeyword("CASE")
DEFAULT = RapidKeyword("DEFAULT")
ERROR = RapidKeyword("ERROR")
INOUT = RapidKeyword("INOUT")

RESERVED_WORD = (
    MODULE
    | ENDMODULE
    | VAR
    | PERS
    | FUNC
    | ENDFUNC
    | PROC
    | ENDPROC
    | TRAP
    | ENDTRAP
    | IF
    | ENDIF
    | ELSE
    | ELSEIF
    | THEN
    | WHILE
    | ENDWHILE
    | FOR
    | ENDFOR
    | DO
    | FROM
    | TO
    | STEP
    | RETURN
    | CONNECT
    | WITH
    | CONST
    | AND
    | OR
    | NOT
    | DIV
    | MOD
    | XOR
    | RECORD
    | ENDRECORD
    | TEST
    | ENDTEST
    | CASE
    | DEFAULT
    | ERROR
)

MODULE_OPTIONS = oneOf("SYSMODULE NOSTEPIN VIEWONLY READONLY")
