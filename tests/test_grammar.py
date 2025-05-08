import pytest
from pyparsing import ParseException, ParseSyntaxException

from rapidchecker.parser.grammar import (
    argument_list,
    array,
    assignment,
    comment,
    compact_if_stmt,
    connect_stmt,
    def_section,
    eval_stmt,
    expression,
    for_stmt,
    func_call_stmt,
    func_def,
    function_call,
    if_stmt,
    module,
    optional_arg,
    proc_call_stmt,
    proc_def,
    record_def,
    return_stmt,
    stmt,
    stmt_block,
    term,
    test_stmt,
    trap_def,
    var_def,
    var_def_section,
    while_stmt,
)
from rapidchecker.parser.indent import reset_level


def test_comment() -> None:
    result = comment.parseString("!This is a comment", parseAll=True).as_list()
    assert result == ["!", "This is a comment"]


def test_eval() -> None:
    result = eval_stmt.parseString("%procCall%", parseAll=True).as_list()
    assert result == ["%", "procCall%"]


@pytest.mark.parametrize(
    "valid_expression",
    [
        "a + 1",
        "a{100}",
        "b.c.d{*} AND TRUE",
        "-a",
        "-10",
        "-funCall(a,b)",
        "a = b AND b <> z",
    ],
)
def test_expression(valid_expression: str) -> None:
    assert expression.parseString(valid_expression, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    ["a := 1;", "RETURN TRUE;", "procCall;", 'a := funcCall(1, "string");'],
)
def test_statement(input_str: str) -> None:
    assert stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    ["a == 1;", "RETURN TRUE"],
)
def test_invalid_statement(input_str: str) -> None:
    with pytest.raises(ParseSyntaxException):
        stmt.parseString(input_str, parseAll=True)


@pytest.mark.parametrize(
    "valid_block",
    ["  a := 1;\n  b:=c;", "  RETURN TRUE;\n  a:=c;"],
)
def test_stmt_block(valid_block: str) -> None:
    reset_level()
    assert stmt_block.parseString(valid_block, parseAll=True).as_list()


@pytest.mark.parametrize("input_str", ["\\a", "\\a:=c"])
def test_optional_arg(input_str: str) -> None:
    assert optional_arg.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize("input_str", ["\\a", "\\a, \\b:=c", "\\a, c+1", "a, \\b:=c"])
def test_arg_list(input_str: str) -> None:
    assert argument_list.parseString(input_str, parseAll=True).as_list()


def test_empty_arg_list() -> None:
    assert argument_list.parseString("", parseAll=True).as_list() == []


@pytest.mark.parametrize("input_str", ["a(\\a)", "funcName()", "funcName(c+1, \\a)"])
def test_function_call(input_str: str) -> None:
    assert function_call.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    ["[TRUE AND FALSE]", "[1,2]", '[b + c, "dsads", "dsadsa"]'],
)
def test_array(input_str: str) -> None:
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
        "-(a AND B)",
        "[1,2,3,4]",
    ],
)
def test_term(input_str: str) -> None:
    assert term.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    ["a:=b;", "a:=(1+2+3);", "object.attr := [1,2,34];", "objects{1}.attr := NOT b;"],
)
def test_assignment(input_str: str) -> None:
    assert assignment.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    ["RECORD test\n  string a;\n  robtarget target;\n  num a;\nENDRECORD"],
)
def test_record_def(input_str: str) -> None:
    reset_level()
    assert record_def.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "PERS string varName;",
        "VAR robtarget targets{1000};",
        "VAR robtarget targets{var1 + var2};",
        "CONST num number := 1 + 1;",
        "LOCAL CONST num number := 1 + 1;",
    ],
)
def test_var_def(input_str: str) -> None:
    assert var_def.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "PERS string varName;\nVAR robtarget targets{1000};\nCONST num number := 1 + 1;",
    ],
)
def test_var_def_section(input_str: str) -> None:
    assert var_def_section.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "IF a THEN\n  callProc;\nELSE\n  callAnotherProc;\nENDIF",
        "IF a THEN\n  callProc;\nELSEIF new_condition AND B THEN\n  callNewProc;\nELSE\n  callAnotherProc;\nENDIF",
        "IF a THEN\n  callProc;\n  callProc2;\nELSEIF new_condition AND B THEN\n  callNewProc;\n  callProc2;\nELSE\n  callAnotherProc;\nENDIF",
        "IF a = b AND b <> 1 THEN\n  var1 := 0;\nENDIF",
    ],
)
def test_valid_if_stmt(input_str: str) -> None:
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
def test_invalid_if_stmt(input_str: str) -> None:
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
def test_compact_if(input_str: str) -> None:
    assert compact_if_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "TEST a\nCASE 1:\n  callProc1;\n  callProc2;\nCASE 2:\n  callProc3;\nDEFAULT:\n  callDefaultProc;\n  STOP;\nENDTEST",
    ],
)
def test_test_stmt(input_str: str) -> None:
    reset_level()
    assert test_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "WHILE NOT A OR B DO\n  callProc1;\n  callProc2;\nENDWHILE",
    ],
)
def test_while_stmt(input_str: str) -> None:
    reset_level()
    assert while_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "FOR i FROM 0 TO 10 STEP 2 DO\n  callProc1;\n  callProc2;\nENDFOR",
    ],
)
def test_for_stmt(input_str: str) -> None:
    reset_level()
    assert for_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "callProc;",
        "callProc arg1, arg2, A AND B;",
        "callProc arg1, arg2, \\switch;",
        "callProc arg1, arg2, \\opt:=(1+1), \\switch;",
        "callProc arg1, name:=arg2 \\opt:=(1+1) \\switch;",
        "MoveL RelTool(target, 0, 0, -Abs(z)), v1000, fine, tool, \\WObj:=wobj0;",
    ],
)
def test_proc_call_stmt(input_str: str) -> None:
    assert proc_call_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "callFunc();",
        "callFunc(arg1, arg2, A AND B);",
        "callFunc(arg1, arg2, \\switch);",
        "callFunc(arg1, arg2, \\opt:=(1+1), \\switch);",
        "callFunc(arg1, name:=arg2 \\opt:=(1+1) \\switch);",
    ],
)
def test_func_call_stmt(input_str: str) -> None:
    assert func_call_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "CONNECT varName WITH something;",
    ],
)
def test_connect_stmt(input_str: str) -> None:
    assert connect_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    ["RETURN TRUE;", "RETURN 1+1;", "RETURN NOT (A OR B OR C);"],
)
def test_return_stmt(input_str: str) -> None:
    assert return_stmt.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "FUNC bool funcName()\nENDFUNC",
        "FUNC bool funcName(num arg1, \\num arg2, \\switch aa)\n  statement;\n  RETURN 1+1;\nENDFUNC",
    ],
)
def test_func_def(input_str: str) -> None:
    reset_level()
    assert func_def.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "PROC procName()\nENDPROC",
        "PROC procName(num arg1, \\num arg2, \\switch aa)\n  statement;\n  statement2;\nENDPROC",
        "PROC procName(num arg1, \\num arg2, \\switch aa)\n  statement;\nERROR\n  statement2;\nENDPROC",
        "PROC procName(num arg1, \\num arg2, \\switch aa)\n  statement;\nBACKWARD\n  statement2;\nERROR\n  statement3;\nUNDO\n  statement2;\nENDPROC",
    ],
)
def test_proc_def(input_str: str) -> None:
    reset_level()
    assert proc_def.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "TRAP trapName\nENDTRAP",
        "TRAP trapName\n  statement1;\n  statement2;\nENDTRAP",
    ],
)
def test_trap_def(input_str: str) -> None:
    reset_level()
    assert trap_def.parseString(input_str, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input_str",
    [
        "TRAP trapName\nENDTRAP\nFUNC bool funcName()\nENDFUNC\nPROC procName()\nENDPROC\n",
    ],
)
def test_def_section(input_str: str) -> None:
    reset_level()
    assert def_section.parseString(input_str, parseAll=True).as_list()


def test_empty_def_section() -> None:
    reset_level()
    assert def_section.parseString("", parseAll=True).as_list() == []


@pytest.mark.parametrize(
    "input_str",
    [
        "MODULE ModuleName\nENDMODULE\n",
        "MODULE ModuleName(SYSMODULE)\n  VAR num aa;\n  FUNC bool funcName()\n    statement;\n  ENDFUNC\n  PROC procName()\n  ENDPROC\nENDMODULE",
    ],
)
def test_module(input_str: str) -> None:
    reset_level()
    assert module.parseString(input_str, parseAll=True).as_list()
