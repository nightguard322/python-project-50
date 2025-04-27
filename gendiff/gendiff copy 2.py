INDENTS = {
    'removed': '-',
    'added': '+',
    'empty': ' ',
    'unchanged': ' ',
    'changed': 'hui'
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
                    diff[key] = {'status': 'changed','value': (file1[key], file2[key])}
        return diff

    generated = make_diff(file1, file2)

    return stylish(generated)

def stylish(data: dict) -> str:

    def render(current, depth):
        res = []
        for key, inner_data in current.items():
            value = prepare_value(inner_data.get('value', inner_data))
            status = inner_data.get('status', None)

            if status == 'changed':
                old_value, new_value = value
                res.append(to_string(key, old_value, depth + 4, 'removed'))
                res.append(to_string(key, new_value, depth + 4, 'added'))

            if status == 'nested':
                strings_list = render(value, depth + 4) #вернется список столк
                
                # возможно тут надо через join вернуть строки со скобками {}
            res.append(to_string(key, value, depth + 4, status))

        return res #список строк

    inner_strings = render(data, 2)
    return inner_strings

def to_string(key, value, depth = 0, indent = 'empty'):

    inner_space = ' ' * depth
    if not isinstance(value, dict):
        return f"{INDENTS[indent]}{inner_space}{key}: {value}"

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