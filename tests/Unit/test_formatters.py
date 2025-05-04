from pathlib import Path

import pytest

from gendiff import generate_diff, parse_file

TEST_CASES = [
    ('file1.json', 'file2.json', 'result.txt'),
    ('file1_nested.json', 'file2_nested.json', 'result_nested.txt'),
    ('file1.yaml', 'file2.yaml', 'result.txt'),
    ('file1_nested.yml', 'file2_nested.yml', 'result_nested.txt'),
]


@pytest.fixture
def fixtures_path():
    return Path(__file__).parent.parent / "test_data"


@pytest.mark.parametrize("file1, file2, expected", TEST_CASES)
def test_generated_diff(file1, file2, expected, fixtures_path):
    file1_data = parse_file(fixtures_path / file1)
    file2_data = parse_file(fixtures_path / file2)
    expected = (fixtures_path / "plain" / expected).read_text()

    result = generate_diff(file1_data, file2_data, "plain")
    assert result == expected

@pytest.mark.parametrize("file1, file2, expected", TEST_CASES)
def test_generated_diff(file1, file2, expected, fixtures_path):
    file1_data = parse_file(fixtures_path / file1)
    file2_data = parse_file(fixtures_path / file2)
    expected = (fixtures_path / "stylish" / expected).read_text()

    result = generate_diff(file1_data, file2_data, 'stylish')
    assert result == expected