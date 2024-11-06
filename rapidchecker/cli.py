import sys

import click
from rich import print

from .check import check_format
from .io import get_sys_files, read_sys_file
from .whitespace_checks import check_whitespace


def in_ignore_list(path: str, ignore_list: list[str]) -> bool:
    return any(item in path for item in ignore_list)


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--ignore", multiple=True)
def cli(path: str, ignore: list[str]) -> None:
    found_errors = False

    for filepath in get_sys_files(path):
        if in_ignore_list(filepath, ignore):
            print("Skipping", filepath)
            continue
        file_contents = read_sys_file(filepath)
        errors = check_format(file_contents)
        errors.extend(check_whitespace(file_contents))
        if len(errors) > 0:
            found_errors = True
            print(f"[bold]{filepath}[/bold]")
            for error in errors:
                print("\t", str(error))

    if not found_errors:
        print(":heavy_check_mark: ", "No RAPID format errors found!")
    sys.exit(found_errors)
