import sys
from pathlib import Path

import click
from pyparsing import ParseBaseException
from rich import print

from rapidchecker.whitespace_checks import WhiteSpaceError

from .check import check_format
from .whitespace_checks import check_whitespace


def read_sys_file(path: str | Path) -> str:
    with Path(path).open() as f:
        return f.read()


def check_file(file_contents: str) -> list[ParseBaseException | WhiteSpaceError]:
    errors: list[ParseBaseException | WhiteSpaceError] = []
    errors.extend(check_format(file_contents))
    errors.extend(check_whitespace(file_contents))
    errors.sort(key=lambda e: e.lineno)
    return errors


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, dir_okay=False))
def cli(paths: list[str]) -> None:
    found_errors = False

    for filepath in paths:
        errors = check_file(read_sys_file(filepath))
        if not errors:
            continue

        found_errors = True
        print(f"[bold]{filepath}[/bold]")
        for error in errors:
            print("\t", str(error))

    if not found_errors:
        print(":heavy_check_mark: ", "No RAPID format errors found!")
    sys.exit(found_errors)
