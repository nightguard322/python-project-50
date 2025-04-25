INDENTS = {
    'removed': '-',
    'added': '+',
    'unchanged': ' ',
    'nested': ' '
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

    def render(current, inner_space, res = []):
        print(current)
        for key, inner_data in current.items():
            value = prepare_value(inner_data.get('value', None))

            if (isinstance(value, dict)): #обработка вложенных словарей
                value = to_string(value, inner_space * 2)
                #Обработка вложенного словаря (обычного, без разметки)
            status = inner_data.get('status', None)
            match status:
                case 'removed':
                    res.append(f"{INDENTS['removed']} {key}: {value}")
                case 'added':
                    res.append(f"{INDENTS['added']} {key}: {value}")
                case 'changed':
                    res.append(f"{INDENTS['removed']} {key}: {inner_data['old_value']}")
                    res.append(f"{INDENTS['added']} {key}: {inner_data['new_value']}")
                case 'nested':
                    res.append(f"{INDENTS['unchanged']} {key}: {render(inner_data['value'], inner_space)}") #обработка вложенных дифов
                case 'unchanged':
                    res.append(f"{INDENTS['unchanged']} {key}: {value}")
                case _:
                    res.append(f"{INDENTS['unchanged']} {key}: {value}")
            return res

    inner_strings = render(data, INDENTS['nested'])
    return "{\n" + "\n".join(inner_strings) + "\n}"

def to_string(data: str, inner_space: str):
    string = [f"{inner_space}{k}: {v}" for k, v in data.items()]
    return "\n".join(['{', *string, '}'])

def prepare_value(value: str):

    if value == True:
        value = 'true'
    
    if value == False:
        value = 'false'

    return value