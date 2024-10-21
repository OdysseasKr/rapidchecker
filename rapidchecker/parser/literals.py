from pyparsing import QuotedString, pyparsing_common

from .tokens import RapidKeyword

NUMBER = pyparsing_common.number
STRING = (QuotedString('"') | QuotedString("'")).set_name("string")
BOOL = (RapidKeyword("TRUE") | RapidKeyword("FALSE")).set_name("string")

RAPIDLITERAL = NUMBER | STRING | BOOL
