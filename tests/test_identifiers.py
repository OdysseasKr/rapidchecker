import pytest
from pyparsing import ParseException

from rapidchecker.parser.identifiers import elem_index, identifier, parameter, variable


@pytest.mark.parametrize("valid_identifier", ["VARIABLE", "test_snake", "testCamel"])
def test_valid_identifier(valid_identifier: str) -> None:
    result = identifier.parseString(valid_identifier, parseAll=True).as_list()
    assert result == [valid_identifier]


@pytest.mark.parametrize("invalid_identifier", ["MODULE", "1dsads", "-dsadsa"])
def test_invalid_identifier(invalid_identifier: str) -> None:
    with pytest.raises(ParseException):
        identifier.parseString(invalid_identifier, parseAll=True)


@pytest.mark.parametrize(
    ("index", "expected"),
    [("*", "*"), ("111", 111), ("variable_name", "variable_name")],
)
def test_elem_index(index: str, expected: str | int) -> None:
    result = elem_index.parseString(f"{{{index}}}", parseAll=True).as_list()
    assert result == ["{", expected, "}"]


@pytest.mark.parametrize(
    "valid_variable",
    [
        "VARIABLE",
        "test_snake",
        "testCamel",
        "with_index{1}",
        "object.attribute{index}",
        "objects{1}.attribute",
    ],
)
def test_valid_variable(valid_variable: str) -> None:
    assert variable.parseString(valid_variable, parseAll=True).as_list()


@pytest.mark.parametrize("invalid_variable", ["MODULE,dsa", "1dsads", "{1}dsadsa"])
def test_invalid_variable(invalid_variable: str) -> None:
    with pytest.raises(ParseException):
        variable.parseString(invalid_variable, parseAll=True)


@pytest.mark.parametrize(
    "valid_parameter",
    [
        "INOUT string name{100}",
        "\\INOUT string name{100}",
        "string name",
        "\\robtarget target",
        "VAR signaldo signal",
    ],
)
def test_parameter(valid_parameter: str) -> None:
    assert parameter.parseString(valid_parameter, parseAll=True)
