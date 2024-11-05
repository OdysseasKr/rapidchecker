import pytest
from pyparsing import ParseException

from rapidchecker.parser.tokens import MODULE, RESERVED_WORD


def test_rapid_keyword():
    assert MODULE.parseString("MODULE", parseAll=True).as_list() == ["MODULE"]


def test_lowercase_rapid_keyword():
    with pytest.raises(ParseException):
        assert MODULE.parseString("module", parseAll=True)


def test_reserved_word():
    assert RESERVED_WORD.parseString("MODULE", parseAll=True).as_list() == ["MODULE"]
