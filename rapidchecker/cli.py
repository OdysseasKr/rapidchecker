import sys
from rich import print
import click

from .check import check_format
from .io import get_sys_files, read_sys_file


def in_ignore_list(path: str, ignore_list: list[str]):
    return any(item in path for item in ignore_list)


@click.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--ignore", multiple=True)
def cli(path: str, ignore: list[str]):
    found_errors = False

    for filepath in get_sys_files(path):
        if in_ignore_list(filepath, ignore):
            print("Skipping", filepath)
            continue
        errors = check_format(read_sys_file(filepath))
        if len(errors) > 0:
            found_errors = True
            print(f"[bold]{filepath}[/bold]")
            for error in errors:
                print("\t", error)

    if not found_errors:
        print(":heavy_check_mark: ", "No RAPID format errors found!")  # noqa
    sys.exit(found_errors)
