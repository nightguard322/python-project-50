import argparse
from pathlib import Path
import json
from gendiff.gendiff import generate_diff

def parse_file(filename: str):
    fixtures_path = Path(__file__).parent.parent / "tests" / "fixtures"
    file_path = fixtures_path / filename
    with file_path.open() as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
                        prog='gendiff',
                        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    file1 = parse_file(args.first_file)
    file2 = parse_file(args.second_file)
    return generate_diff(file1, file2)
    
    
if __name__ == 'main':
    main()