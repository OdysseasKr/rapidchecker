from collections.abc import Iterable
from pathlib import Path


def get_sys_files(paths: list[str]) -> Iterable[Path]:
    for path_str in paths:
        path = Path(path_str)
        if path.is_dir():
            yield from path.glob("**/*.sys")
        else:
            yield path


def read_sys_file(path: str | Path) -> str:
    with Path(path).open() as f:
        return f.read()
