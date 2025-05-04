import json
from pathlib import Path

import yaml


def parse_file(filename: str) -> None:
    """
    Return text file data

    Args:
        filename: Path to file, str
    Return:
        text file data
    """

    filepath = filename if isinstance(filename, Path) else Path(filename)
    if not filepath.exists():
        raise FileNotFoundError(f"file {filepath} not found")

    if not filepath.is_file():
        raise ValueError(f"{filepath} is not a file")

    return open_file(filepath)


def open_file(file_path) -> None:
    """
    Load and parse JSON and YAML/YML file

    Args:
        file_path: Path to the file (str or Path obj)

    Return:
        Parsed data as dict

    Raises:
        ValueError: file extension not supported
        FileNotFoundError: file doesn't exists
        yaml.YAMLError: YAML reading error
        json.JSONDecodeError: JSON parsing error
    """
    with file_path.open() as file:
        match (file_path.suffix.lower()):
            case '.json':
                return json.load(file)
            case '.yaml' | '.yml':
                return yaml.safe_load(file)
            case _:
                raise ValueError(f"Unknown file extension - {file_path.suffix}")