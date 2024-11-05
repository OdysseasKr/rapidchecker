from collections.abc import Iterable
from pathlib import Path


def get_sys_files(path: str | Path) -> Iterable[str]:
    path = Path(path)
    if path.endswith(".sys"):
        return [path]
    if path.endswith("/"):
        path = path[:-1]
    return path.glob("**/*.sys")


def read_sys_file(path: str | Path) -> list[str]:
    with Path(path).open() as f:
        return f.read()
