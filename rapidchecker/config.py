import tomllib
from dataclasses import dataclass, replace
from pathlib import Path


@dataclass
class Config:
    indentation_check: bool = True
    indentation_size: int = 2
    require_uppercase_keywords: bool = True
    max_empty_lines: int = 2
    require_new_line_eof: bool = True
    allow_trailing_space: bool = False
    indent_error_section: bool = False

    @classmethod
    def read_config(cls, config_file: Path) -> "Config":
        default_dict = cls()
        if not config_file.exists():
            return default_dict
        with config_file.open("rb") as f:
            user_data = tomllib.load(f)
        return replace(default_dict, **user_data)


CONFIG = Config.read_config(Path("rapidchecker.toml"))
