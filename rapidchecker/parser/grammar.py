import pyparsing as pp

from . import tokens as T
from .identifiers import datatype, identifier, parameter_list, variable
from .indent import (
    INDENT,
    INDENT_CHECKPOINT,
    UNDENT,
    register_indent_checks,
)
from .literals import RAPIDLITERAL
from .operators import infix_op

pp.ParserElement.enable_packrat()

# Simple rules for entire lines
comment = "!" + pp.rest_of_line
eval_stmt = "%" - pp.rest_of_line  # TODO: Fix this to account for the last %

# These elements are needed to define the next rules
expression = pp.Forward()
stmt_block = pp.Forward()
stmt = pp.Forward()

# Arguments for proc and functon calls
optional_arg = pp.Combine("\\" + identifier) + pp.Optional(":=" + expression)
required_arg = pp.Optional(identifier + ":=") + expression
first_argument = optional_arg | required_arg
argument = ("," + (optional_arg | required_arg)) | optional_arg
argument_list = pp.Optional(first_argument + pp.ZeroOrMore(argument))

function_call = identifier + "(" - argument_list - ")"

array = "[" + pp.delimitedList(expression) + "]"

# Terms and expressions can be defined now
term = (
    function_call
    | variable
    | RAPIDLITERAL
    | "(" + expression + ")"
    | T.NOT + expression
    | array
)
expression <<= (term + infix_op + expression) | term
assignment = variable + ":=" - expression - ";"

# Record definition
record_item = datatype + identifier + ";"
record_def = (
    T.RECORD
    - identifier
    - INDENT
    - pp.OneOrMore(record_item)
    - UNDENT
    - INDENT_CHECKPOINT
    - T.ENDRECORD
)
record_def_section = pp.ZeroOrMore(record_def)

# Variable definition
var_def = (
    (T.PERS | T.VAR | T.CONST)
    + datatype
    + identifier
    + pp.Optional("{" + expression + "}")
    + pp.Optional(":=" + expression)
    + ";"
)
var_def_section = pp.ZeroOrMore(var_def)

# If statement
if_stmt = (
    T.IF
    + expression
    + T.THEN
    - stmt_block
    - pp.ZeroOrMore(INDENT_CHECKPOINT + T.ELSEIF - expression - T.THEN - stmt_block)
    - pp.Optional(INDENT_CHECKPOINT + T.ELSE - stmt_block)
    - INDENT_CHECKPOINT
    - T.ENDIF
)

# Test statement
test_stmt = (
    T.TEST
    - expression
    - pp.OneOrMore(INDENT_CHECKPOINT + T.CASE - term - ":" - stmt_block)
    - pp.Optional(INDENT_CHECKPOINT + T.DEFAULT - ":" - stmt_block)
    - INDENT_CHECKPOINT
    - T.ENDTEST
)

# Loops
while_stmt = T.WHILE - expression - T.DO - stmt_block - T.ENDWHILE
for_stmt = (
    T.FOR
    - identifier
    - T.FROM
    - expression
    - T.TO
    - expression
    - pp.Optional(T.STEP + expression)
    - T.DO
    - stmt_block
    - INDENT_CHECKPOINT
    - T.ENDFOR
)

# Simple statements
proc_call_stmt = identifier - argument_list - ";"
func_call_stmt = function_call - ";"
connect_stmt = T.CONNECT - identifier - T.WITH - identifier - ";"
return_stmt = T.RETURN - pp.Optional(expression) - ";"

compact_if_stmt = (
    T.IF
    + expression
    + (assignment | func_call_stmt | proc_call_stmt | return_stmt | connect_stmt)
)

stmt <<= (
    assignment
    | if_stmt
    | compact_if_stmt
    | test_stmt
    | while_stmt
    | for_stmt
    | eval_stmt
    | func_call_stmt
    | proc_call_stmt
    | return_stmt
    | connect_stmt
)
stmt_block <<= INDENT - var_def_section - pp.ZeroOrMore(stmt) - UNDENT

# Function definition
func_def = (
    T.FUNC
    - datatype
    - identifier
    - "("
    - parameter_list
    - ")"
    - stmt_block
    - INDENT_CHECKPOINT
    - T.ENDFUNC
)

# Proc definition
error_section = T.ERROR - stmt_block
proc_def = (
    T.PROC
    - identifier
    - "("
    - parameter_list
    - ")"
    - stmt_block
    - pp.Optional(error_section)
    - INDENT_CHECKPOINT
    - T.ENDPROC
)

# Trap definition
trap_def = T.TRAP - identifier - stmt_block - INDENT_CHECKPOINT - T.ENDTRAP

def_section = pp.ZeroOrMore(func_def | proc_def | trap_def)

module_args = "(" - pp.delimitedList(T.MODULE_OPTIONS) - ")"
module = (
    T.MODULE
    - identifier
    - pp.Optional(module_args)
    - INDENT
    - record_def_section
    - var_def_section
    - def_section
    - UNDENT
    - INDENT_CHECKPOINT
    - T.ENDMODULE
)
module.ignore(comment)

register_indent_checks(
    [
        stmt,
        var_def,
        record_item,
        T.PROC,
        T.MODULE,
        T.FUNC,
        T.TRAP,
        T.RECORD,
        T.IF,
        T.FOR,
        T.WHILE,
        T.TEST,
    ],
)
