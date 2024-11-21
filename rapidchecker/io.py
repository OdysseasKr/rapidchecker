from collections.abc import Iterable
from pathlib import Path


def expand_filepaths(paths: list[str]) -> Iterable[Path]:
    for path_str in paths:
        path = Path(path_str)
        if path.is_dir():
            yield from get_sys_files(path)
        else:
            yield path


def get_sys_files(path: Path) -> Iterable[Path]:
    if path.suffix == ".sys":
        return [path]
    return path.glob("**/*.sys")


def read_sys_file(path: str | Path) -> str:
    with Path(path).open() as f:
        return f.read()
