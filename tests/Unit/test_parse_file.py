import pytest
from pathlib import Path
from gendiff.scripts.gendiff import parse_file

def parse_file(filename: str):
    fixtures_path = Path(__file__).parent.parent.parent / "tests" / "fixtures"
    file_path = fixtures_path / filename
    if not file_path.exists():
        raise FileNotFoundError(f"File {file_path} does not exists")
    if not file_path.is_file():
        raise ValueError(f"{file_path} is not a file")
    with file_path.open() as f:
        return json.load(f)

def test_parse_file_valid_json(tmp_dir):
    test_file_data = {'test': 'test'}
    test_file = tmp_dir / "test_file.json"
    test_file.write_text(test_file_data)

    result = parse_file(test_file)
    assert result == test_file_data

def test_parse_file_not_found(tmp_dir):

    result = parse_file(test_file)
    assert result == test_file_data