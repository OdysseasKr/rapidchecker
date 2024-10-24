import pytest
from pyparsing import ParseSyntaxException
from rapidchecker.parser.grammar import (
    comment,
    eval_stmt,
    stmt,
    stmt_block,
    expression,
    named_arg,
    argument_list,
    function_call,
    array,
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
    "valid_stmt",
    ["a := 1;", "RETURN TRUE;", "procCall;", 'a := funcCall(1, "string");'],
)
def test_stmt(valid_stmt: str):
    assert stmt.parseString(valid_stmt, parseAll=True).as_list()


@pytest.mark.parametrize(
    "invalid_stmt",
    ["a == 1;", "RETURN TRUE"],
)
def test_invalid_stmt(invalid_stmt: str):
    with pytest.raises(ParseSyntaxException):
        stmt.parseString(invalid_stmt, parseAll=True)


# TODO: This can fail if there is an "inline if" in the block
@pytest.mark.parametrize(
    "valid_block", ["  a := 1;\n  b:=c;", "  RETURN TRUE;\n  a:=c;"]
)
def test_stmt_block(valid_block: str):
    reset_level()
    assert stmt_block.parseString(valid_block, parseAll=True).as_list()


@pytest.mark.parametrize("input", ["\\a", "\\a:=c"])
def test_named_arg(input: str):
    assert named_arg.parseString(input, parseAll=True).as_list()


@pytest.mark.parametrize("input", ["\\a", "\\a, \\b:=c", "\\a, c+1", "a, \\b:=c"])
def test_arg_list(input: str):
    assert argument_list.parseString(input, parseAll=True).as_list()


def test_empty_arg_list():
    assert argument_list.parseString("", parseAll=True).as_list() == []


@pytest.mark.parametrize("input", ["a(\\a)", "funcName()", "funcName(c+1, \\a)"])
def test_function_call(input: str):
    assert function_call.parseString(input, parseAll=True).as_list()


@pytest.mark.parametrize(
    "input", ["[TRUE AND FALSE]", "[1,2]", '[b + c, "dsads", "dsadsa"]']
)
def test_array(input: str):
    assert array.parseString(input, parseAll=True).as_list()
