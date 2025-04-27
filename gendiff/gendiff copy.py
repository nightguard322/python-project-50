INDENTS = {
    'removed': '-',
    'added': '+',
    'empty': ' '
}
def generate_diff(file1: dict, file2: dict):

    def make_diff(file1: dict, file2: dict):
        all_keys = set(file1) | set(file2)
        diff = {}
        for key in sorted(all_keys):
            if key not in file2:
                diff[key] = {'status': 'removed', 'value': file1[key]}
            elif key not in file1:
                diff[key] = {'status': 'added', 'value': file2[key]}
            else:
                if file1[key] == file2[key]:
                    diff[key] = {'status': 'unchanged', 'value': file1[key]}
                elif isinstance(file1[key], dict) and isinstance(file2[key], dict):
                    diff[key] = {'status': 'nested', 'value': make_diff(file1[key], file2[key])}
                else:
                    diff[key] = {
                        'status': 'changed',
                        'old_value': file1[key],
                        'new_value': file2[key]
                    }
        return diff

    generated = make_diff(file1, file2)

    return stylish(generated)

def stylish(data: dict) -> str:

    def render(current, depth):
        res = []
        for key, inner_data in current.items():
            value = prepare_value(inner_data.get('value', None))
            status = inner_data.get('status', None)
            match status:
                case 'removed':
                    res.append(to_string(f"{INDENTS['removed']} {key}", value, depth))
                case 'added':
                    res.append(to_string(f"{INDENTS['added']} {key}", value, depth))
                case 'changed':
                    res.append(to_string(f"{INDENTS['removed']} {key}", prepare_value(inner_data['old_value']), depth))
                    res.append(to_string(f"{INDENTS['added']} {key}", prepare_value(inner_data['new_value']), depth))
                case 'nested':
                    value = render(value, depth + 4)
                    res.append(to_string(f"{INDENTS['empty']} {key}", value, depth)) #обработка вложенных дифов
                case 'unchanged':
                    res.append(to_string(f"{INDENTS['empty']} {key}", value, depth))
        closing_bracket_indent = (depth - 2) * INDENTS['empty']
        return "\n".join(["{", *res, f"{closing_bracket_indent}{"}"}"])

    inner_strings = render(data, 2)
    return inner_strings

def to_string(key, value, depth = 0):

    inner_space = ' ' * depth
    if not isinstance(value, dict):
        return f"{inner_space}{key}: {value}"

    inner_lines = []
    for inner_key, inner_value in value.items():
        inner_lines.append(to_string(inner_key, inner_value, depth + 4))

    return f"{inner_space}{key}: " + "\n".join(["{", *inner_lines, f"{inner_space}{'2}'}"])

def prepare_value(value: str):
    if value == True:
        value = 'true'
    
    if value == False:
        value = 'false'
    
    if value == '':
        value = ' '

    return value