import json

from .utils.parser import parse_file

INDENTS = {
    'removed': '- ',
    'added': '+ ',
    'empty': '  ',
    'unchanged': '  '
}


def generate_diff(file1: dict, file2: dict, format='stylish'):

    def make_diff(file1: dict, file2: dict):
        if not isinstance(file1, dict) or not isinstance(file2, dict):
            raise ValueError(f"file1 - {file1}, file2 - {file2}")
        
        all_keys = set(file1) | set(file2)
        diff = {}
        for key in sorted(all_keys):
            if key not in file2:
                diff[key] = {'status': 'removed', 'value': file1[key]}
            elif key not in file1:
                diff[key] = {'status': 'added', 'value': file2[key]}
            else:
                if (
                    isinstance(file1[key], dict) 
                    and isinstance(file2[key], dict)
                    ):
                    diff[key] = {
                        'status': 'nested', 
                        'value': make_diff(file1[key], file2[key])
                    }
                elif file1[key] == file2[key]:
                    diff[key] = {'status': 'unchanged', 'value': file1[key]}
                else:
                    diff[key] = {
                        'status': 'changed',
                        'value': (file1[key], file2[key])
                    }
        return diff

    file1_data = parse_file(file1)
    file2_data = parse_file(file2)
    try:
        generated = make_diff(file1_data, file2_data)
        return get_format(format, generated)
    except ValueError as e:
        print(f"Error with gendiff: {e}")


def stylish(data: dict) -> str:

    def render(current, depth=0):
        res = []
        for key, inner_data in current.items():
            value = inner_data.get('value', inner_data)
            status = inner_data.get('status', None)

            if status == 'changed':
                old_value, new_value = value
                res.append(stylish_to_string(key, old_value, depth, 'removed'))
                res.append(stylish_to_string(key, new_value, depth, 'added'))
            elif status == 'nested':
                value = render(value, depth + 4)
                res.append(stylish_to_string(key, value, depth))
            else:
                res.append(stylish_to_string(key, value, depth, status))
        closing_bracket_indent = (depth - 2) * ' '
        return "\n".join(["{", *res, f"{closing_bracket_indent}{"}"}"])

    inner_strings = render(data, 2)
    return inner_strings


def stylish_to_string(key, value, depth=0, indent='empty'):
    prepare = make_preparer()
    inner_space = ' ' * depth
    if not isinstance(value, dict):
        prepared = prepare(value)
        return f"{inner_space}{INDENTS[indent]}{key}: {prepared}"

    inner_lines = []
    for inner_key, inner_value in value.items():
        inner_lines.append(stylish_to_string(inner_key, inner_value, depth + 4))

    closing_bracket_indent = (depth + 2) * ' '
    return (
        f"{inner_space}{INDENTS[indent]}{key}: " 
        + 
        "\n".join(["{", *inner_lines, f"{closing_bracket_indent}{'}'}"])
        )


def make_preparer(quotes: bool = False):
    def prepare(value):
        if isinstance(value, dict):
            return '[complex value]'
        
        if value is None:
            return 'null'
        
        if isinstance(value, bool):
            return 'true' if value else 'false'
        
        if isinstance(value, int):
            return value
    
        return f"'{value}'" if quotes else value
    return prepare


def plain(diff: dict) -> str:

    res = []

    def walk(current, path):

        for key, inner_data in current.items():
            status = inner_data.get('status', 'unchanged')

            if status == 'unchanged':
                continue
            
            new_path = path + [key]

            if status == 'nested':
                walk(inner_data['value'], new_path)
            else:
                res.append(
                    plain_to_string(
                        status,
                        inner_data['value'],
                        new_path)
                    )

    walk(diff, [])
    return "\n".join(res)


def plain_to_string(status, value, path):

    property_path = '.'.join(path)
    prepare = make_preparer(quotes=True)
    match (status):
        case 'removed':
            return f"Property {prepare(property_path)} was removed"
        case 'added':
            return (
                f"Property {prepare(property_path)} "
                f"was added with value: {prepare(value)}"
            )
        case 'changed':
            old_value, new_value = value
            return (
                f"Property {prepare(property_path)} was updated. "
                f"From {prepare(old_value)} "
                f"to {prepare(new_value)}"
            )
        case _:
            raise ValueError('Wrong value')
        

def get_format(format: str, data) -> None:
    match (format):
        case 'stylish':
            return stylish(data)
        case 'plain':
            return plain(data)
        case 'json':
            return json.dumps(data, indent=2)
        case _:
            raise ValueError(f"Wrong format - {format}")