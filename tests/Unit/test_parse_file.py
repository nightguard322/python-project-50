import json

import pytest

from cli.gendiff import parse_file


def test_parse_file_valid_json(tmp_path):
    test_file_data = {'test': 'test'}
    test_file = tmp_path / "test_file.json"
    test_file.write_text(json.dumps(test_file_data))

    result = parse_file(test_file)
    assert result == test_file_data


def test_parse_file_not_found(tmp_path):
    test_file = tmp_path / "test_file.json"
    with pytest.raises(FileNotFoundError):
        parse_file(test_file)


def test_parse_not_a_file(tmp_path):
    with pytest.raises(ValueError):
        parse_file(tmp_path)