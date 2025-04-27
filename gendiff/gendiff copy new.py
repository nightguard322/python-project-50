INDENTS = {
    'removed': '-',
    'added': '+',
    'empty': ' ',
    'unchanged': ' '
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
        inner_space = depth * INDENTS['empty']
        res = []
        for key, inner_data in current.items():
            print(inner_data)
            status = inner_data['status'] if isinstance(inner_data, dict) else 'empty'
            value = inner_data['value'] if isinstance(inner_data, dict) else 'inner_data'
            if not isinstance(value, dict): #отсечка для nested и списков
                if status == 'changed':
                    old_value, new_value = value
                    res.append(f"{inner_space}{INDENTS['removed']}{key}: {old_value}")
                    res.append(f"{inner_space}{INDENTS['added']}{key}: {new_value}")
                else:
                    res.append(f"{inner_space}{INDENTS[status]}{key}: {value}")
                continue
            
            children = render(value, depth + 4)
            preapred_children = "\n".join(children)
            res.append(f"{inner_space}{INDENTS[status]}{key}: {'{'}{preapred_children}{'}'}")  
        return res

    inner_strings = render(data, 2)
    return inner_strings


def prepare_value(value: str):
    if value == True:
        value = 'true'
    
    if value == False:
        value = 'false'
    
    if value == '':
        value = ' '

    return value