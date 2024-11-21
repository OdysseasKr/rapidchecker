import sys

import click
from pyparsing import ParseBaseException
from rich import print

from rapidchecker.whitespace_checks import WhiteSpaceError

from .check import check_format
from .io import get_sys_files, read_sys_file
from .whitespace_checks import check_whitespace


def check_file(file_contents: str) -> list[ParseBaseException | WhiteSpaceError]:
    errors: list[ParseBaseException | WhiteSpaceError] = []
    errors.extend(check_format(file_contents))
    errors.extend(check_whitespace(file_contents))
    errors.sort(key=lambda e: e.lineno)
    return errors


@click.command()
@click.argument("paths", nargs=-1, type=click.Path(exists=True, dir_okay=True))
def cli(paths: list[str]) -> None:
    found_errors = False

    for filepath in get_sys_files(paths):
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
