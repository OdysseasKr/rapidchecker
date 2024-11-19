import pyparsing as pp

from . import tokens as T
from .literals import NUMBER

identifier = ~T.RESERVED_WORD + pp.pyparsing_common.identifier
identifier.set_name("identifier")

datatype = identifier.set_name("datatype")

elem_index = pp.Optional("{" + (identifier | NUMBER | "*") + "}").set_name("index")

variable = identifier + elem_index + pp.ZeroOrMore("." - identifier + elem_index)
variable.set_name("variable")


parameter = (
    pp.Optional("\\")
    + pp.Optional(T.INOUT | T.PERS | T.VAR)
    + datatype
    + identifier
    + elem_index
)
parameter.set_name("param")
parameter_list = pp.Optional(pp.delimitedList(parameter))
