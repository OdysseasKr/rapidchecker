import pyparsing as pp

from . import tokens as T

boolean_op = T.AND | T.OR | T.NOT | T.XOR
boolean_op.set_name("bool_op")

infix_op = pp.oneOf("+ - * / = <= < >= > <>") | boolean_op | T.DIV | T.MOD
