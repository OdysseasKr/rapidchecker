import sys

import click
from pyparsing import ParseBaseException
from rich import print

from rapidchecker.whitespace_checks import WhiteSpaceError

from .check import check_format
from .io import get_sys_files, read_sys_file
from .whitespace_checks import check_whitespace


def in_ignore_list(path: str, ignore_list: list[str]) -> bool:
    return any(item in path for item in ignore_list)


def check_file(file_contents: str) -> list[ParseBaseException | WhiteSpaceError]:
    errors: list[ParseBaseException | WhiteSpaceError] = []
    errors.extend(check_format(file_contents))
    errors.extend(check_whitespace(file_contents))
    errors.sort(key=lambda e: e.lineno)
    return errors


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--ignore", multiple=True)
def cli(path: str, ignore: list[str]) -> None:
    found_errors = False

    for filepath in get_sys_files(path):
        if in_ignore_list(str(filepath), ignore):
            print("Skipping", filepath)
            continue
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
