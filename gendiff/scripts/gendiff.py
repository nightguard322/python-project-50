import argparse
import sys

from gendiff import generate_diff
from gendiff import parse_file


def main():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()
    try:
        file1 = parse_file(args.first_file)
        file2 = parse_file(args.second_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    return generate_diff(file1, file2, args.format)


if __name__ == 'main':
    main()