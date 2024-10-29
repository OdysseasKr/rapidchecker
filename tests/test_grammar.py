import pytest
from pyparsing import ParseException, ParseSyntaxException

from rapidchecker.parser.grammar import (
    argument_list,
    array,
    assignment,
    comment,
    eval_stmt,
    expression,
    function_call,
    named_arg,
    record_def,
    stmt,
    stmt_block,
    term,
    var_def,
    var_def_section,
    if_stmt,
    inline_if_stmt,
    test_stmt,
    while_stmt,
    for_stmt,
    proc_call_stmt,
    func_call_stmt,
    connect_stmt,
    return_stmt,
    func_def,
    proc_def,
    trap_def,
    def_section,
    module,
)
from rapidchecker.parser.indent import reset_level


def test_comment():
    result = comment.parseString("!This is a comment", parseAll=True).as_list()
    assert result == ["!", "This is a comment"]


def test_eval():
    result = eval_stmt.parseString("%procCall%", parseAll=True).as_list()
    assert result == ["%", "procCall%"]


@pytest.mark.parametrize("valid_expression", ["a + 1", "a{100}", "b.c.d{*} AND TRUE"])
def test_expression(valid_expression: str):
    assert expression.parseString(valid_expression, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    ["a := 1;", "RETURN TRUE;", "procCall;", 'a := funcCall(1, "string");'],
)
def test_statement(input_str: str):
    assert stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    ["a == 1;", "RETURN TRUE"],
)
def test_invalid_statement(input_str: str):
    with pytest.raises(ParseSyntaxException):
        stmt.parseString(input_str, parseAll=True)


@pytest.mark.parametrize(
    "valid_block", ["  a := 1;\n  b:=c;", "  RETURN TRUE;\n  a:=c;"]
)
def test_stmt_block(valid_block: str):
    reset_level()
    assert stmt_block.parseString(valid_block, parseAll=True).as_list()


@pytest.mark.parametrize("input_str", ["\\a", "\\a:=c"])
def test_named_arg(input_str: str):
    assert named_arg.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize("input_str", ["\\a", "\\a, \\b:=c", "\\a, c+1", "a, \\b:=c"])
def test_arg_list(input_str: str):
    assert argument_list.parseString(input_str, parseAll=True).as_list()


def test_empty_arg_list():
    assert argument_list.parseString("", parseAll=True).as_list() == []


@pytest.mark.parametrize("input_str", ["a(\\a)", "funcName()", "funcName(c+1, \\a)"])
def test_function_call(input_str: str):
    assert function_call.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str", ["[TRUE AND FALSE]", "[1,2]", '[b + c, "dsads", "dsadsa"]']
)
def test_array(input_str: str):
    assert array.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "funcCall(a,\\a:=1)",
        "varName",
        "TRUE",
        '"string"',
        "(1+1)",
        "NOT a AND B",
        "[1,2,3,4]",
    ],
)
def test_term(input_str: str):
    assert term.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    ["a:=b;", "a:=(1+2+3);", "object.attr := [1,2,34];", "objects{1}.attr := NOT b;"],
)
def test_assignment(input_str: str):
    assert assignment.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    ["RECORD test\n  string a;\n  robtarget target;\n  num a;\nENDRECORD"],
)
def test_record_def(input_str: str):
    reset_level()
    assert record_def.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "PERS string varName;",
        "VAR robtarget targets{1000};",
        "CONST num number := 1 + 1;",
    ],
)
def test_var_def(input_str: str):
    assert var_def.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "PERS string varName;\nVAR robtarget targets{1000};\nCONST num number := 1 + 1;",
    ],
)
def test_var_def_section(input_str: str):
    assert var_def_section.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "IF a THEN\n  callProc;\nELSE\n  callAnotherProc;\nENDIF",
        "IF a THEN\n  callProc;\nELSEIF new_condition AND B THEN\n  callNewProc;\nELSE\n  callAnotherProc;\nENDIF",
        "IF a THEN\n  callProc;\n  callProc2;\nELSEIF new_condition AND B THEN\n  callNewProc;\n  callProc2;\nELSE\n  callAnotherProc;\nENDIF",
    ],
)
def test_valid_if_stmt(input_str: str):
    reset_level()
    assert if_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "IF a THEN\n  callProc;\nELSE\n  callAnotherProc;",
        "IF a callProc;",
        "IF a THEN\n  callProc;\nELSEIF new_condition AND B\n  callNewProc;\nELSE\n  callAnotherProc;\nENDIF",
    ],
)
def test_invalid_if_stmt(input_str: str):
    reset_level()
    with pytest.raises((ParseException, ParseSyntaxException)):
        if_stmt.parseString(input_str, parseAll=True)


# TODO: Why does this fail?
@pytest.mark.parametrize(
    "input_str",
    [
        "IF a callProc;",
    ],
)
def test_inline_if(input_str: str):
    assert inline_if_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "TEST a\nCASE 1:\n  callProc1;\n  callProc2;\nCASE 2:\n  callProc3;\nDEFAULT:\n  callDefaultProc;\n  STOP;\nENDTEST",
    ],
)
def test_test_stmt(input_str: str):
    reset_level()
    assert test_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "WHILE NOT A OR B DO\n  callProc1;\n  callProc2;\nENDWHILE",
    ],
)
def test_while_stmt(input_str: str):
    reset_level()
    assert while_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "FOR i FROM 0 TO 10 STEP 2 DO\n  callProc1;\n  callProc2;\nENDFOR",
    ],
)
def test_for_stmt(input_str: str):
    reset_level()
    assert for_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "callProc;",
        "callProc arg1, arg2, A AND B;",
        "callProc arg1, arg2, \\switch;",
        "callProc arg1, arg2, \\opt:=(1+1), \\switch;",
    ],
)
def test_proc_call_stmt(input_str: str):
    assert proc_call_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "callFunc();",
        "callFunc(arg1, arg2, A AND B);",
        "callFunc(arg1, arg2, \\switch);",
        "callFunc(arg1, arg2, \\opt:=(1+1), \\switch);",
    ],
)
def test_func_call_stmt(input_str: str):
    assert func_call_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "CONNECT varName WITH something;",
    ],
)
def test_connect_stmt(input_str: str):
    assert connect_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    ["RETURN TRUE;", "RETURN 1+1;", "RETURN NOT (A OR B OR C);"],
)
def test_return_stmt(input_str: str):
    assert return_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "FUNC bool funcName()\nENDFUNC",
        "FUNC bool funcName(num arg1, \\num arg2, \\switch aa)\n  statement;\n  RETURN 1+1;\nENDFUNC",
    ],
)
def test_func_def(input_str: str):
    reset_level()
    assert func_def.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "PROC procName()\nENDPROC",
        "PROC procName(num arg1, \\num arg2, \\switch aa)\n  statement;\n  statement2;\nENDPROC",
        "PROC procName(num arg1, \\num arg2, \\switch aa)\n  statement;\n  ERROR\n  statement2;\nENDPROC",
    ],
)
def test_proc_def(input_str: str):
    reset_level()
    assert proc_def.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "TRAP trapName\nENDTRAP",
        "TRAP trapName\n  statement1;\n  statement2;\nENDTRAP",
    ],
)
def test_trap_def(input_str: str):
    reset_level()
    assert trap_def.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "TRAP trapName\nENDTRAP\nFUNC bool funcName()\nENDFUNC\nPROC procName()\nENDPROC\n",
    ],
)
def test_def_section(input_str: str):
    reset_level()
    assert def_section.parseString(input_str, parseAll=True).as_list()


def test_empty_def_section():
    reset_level()
    assert def_section.parseString("", parseAll=True).as_list() == []


@pytest.mark.parametrize(
    "input_str",
    [
        "MODULE ModuleName\nENDMODULE\n",
        "MODULE ModuleName(SYSMODULE)\n  VAR num aa;\n  FUNC bool funcName()\n    statement;\n  ENDFUNC\n  PROC procName()\n  ENDPROC\nENDMODULE",
    ],
)
def test_module(input_str: str):
    reset_level()
    assert module.parseString(input_str, parseAll=True).as_list()
