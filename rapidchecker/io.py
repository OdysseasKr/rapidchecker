from collections.abc import Iterable
from pathlib import Path


def expand_filepaths(paths: list[Path | str]) -> Iterable[Path]:
    for path in paths:
        path = Path(path)
        if path.is_dir():
            yield from get_sys_files(path)
        else:
            yield path


def get_sys_files(path: str | Path) -> Iterable[Path]:
    path = Path(path)
    if path.suffix == ".sys":
        return [path]
    return path.glob("**/*.sys")


def read_sys_file(path: str | Path) -> str:
    with Path(path).open() as f:
        return f.read()
