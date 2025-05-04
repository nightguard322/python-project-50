import argparse
import sys
import traceback

from gendiff import generate_diff


def main():
    try:
        parser = argparse.ArgumentParser(
            prog='gendiff',
            description=(
                'Compares two configuration files and shows a difference.')
            )
        parser.add_argument('first_file')
        parser.add_argument('second_file')
        parser.add_argument('-f', '--format', help='set format of output')
        args = parser.parse_args()
        try:
            file1 = args.first_file
            file2 = args.second_file
        except (FileNotFoundError, ValueError) as e:
            print(f"Error: {e}", file=sys.stderr)
        format = args.format if args.format else 'stylish'
        print(generate_diff(file1, file2, format))
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)


if __name__ == 'main':
    main()