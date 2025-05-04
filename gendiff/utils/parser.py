import json
from pathlib import Path

import yaml


def parse_file(filename: str) -> None:
    filepath = Path(filename)
    if not filepath.exists():
        raise FileNotFoundError(f"file {filepath} not found")

    if not filepath.is_file():
        raise ValueError(f"{filepath} is not a file")

    return open_file(filepath)


