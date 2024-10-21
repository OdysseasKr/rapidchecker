import glob
from typing import Iterable


def get_sys_files(path: str) -> Iterable[str]:
    if path.endswith(".sys"):
        return [path]
    if path.endswith("/"):
        path = path[:-1]
    return glob.iglob(path + "/**/*.sys", recursive=True)


def read_sys_file(path: str) -> list[str]:
    with open(path) as f:
        return f.read()
