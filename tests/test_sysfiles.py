from pathlib import Path

from rapidchecker.parser.grammar import module
from rapidchecker.parser.indent import reset_level


def test_simple_module_file() -> None:
    reset_level()
    file_contents = Path("./tests/rapid_samples/SimpleModule.sys").read_text()
    assert module.parseString(file_contents, parseAll=True).as_list()
