INDENTS = {
    'removed': '- ',
    'added': '+ ',
    'empty': '  ',
    'unchanged': '  '
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

    def render(current, depth=0):
        res = []
        for key, inner_data in current.items():
            value = prepare_value(inner_data.get('value', inner_data))
            status = inner_data.get('status', None)

            if status == 'changed':
                old_value, new_value = value
                res.append(to_string(key, old_value, depth, 'removed'))
                res.append(to_string(key, new_value, depth, 'added'))
            elif status == 'nested':
                value = render(value, depth + 4)
                res.append(to_string(key, value, depth))
            else:
                res.append(to_string(key, value, depth, status))
        closing_bracket_indent = (depth - 2) * ' '
        return "\n".join(["{", *res, f"{closing_bracket_indent}{"}"}"])

    inner_strings = render(data)
    return inner_strings

def to_string(key, value, depth = 0, indent = 'empty'):

    inner_space = ' ' * depth
    if not isinstance(value, dict):
        return f"{inner_space}{INDENTS[indent]}{key}: {value}"

    inner_lines = []
    for inner_key, inner_value in value.items():
        inner_lines.append(to_string(inner_key, inner_value, depth + 4))

    closing_bracket_indent = (depth + 2) * ' '
    return f"{inner_space}{INDENTS[indent]}{key}: " + "\n".join(["{", *inner_lines, f"{closing_bracket_indent}{'}'}"])


def prepare_value(value: str):
    if value == True:
        value = 'true'
    
    if value == False:
        value = 'false'
    
    if value == '':
        value = ' '

    return value
"""
Анализ вашего рабочего решения
Базовая структура:

render() рекурсивно обрабатывает данные

to_string() форматирует отдельные строки

Ключевые моменты в render():

python
closing_bracket_indent = (depth - 2) * ' '
return "\n".join(["{", *res, f"{closing_bracket_indent}{"}"}"])
Открывающая { идёт без отступа

Закрывающая } получает отступ depth - 2

Логика to_string():

Для простых значений: {inner_space}{INDENTS[indent]}{key}: {value}

Для словарей:

python
closing_bracket_indent = (depth + 2) * ' '
return f"{inner_space}{INDENTS[indent]}{key}: " + "\n".join(["{", *inner_lines, f"{closing_bracket_indent}{'}'}"])
Почему это работает?
Система отступов:

Базовый отступ = depth пробелов

Для вложенных элементов:

+4 к глубине для содержимого

+2 для закрывающей скобки (чтобы выровнять под ключом)

Магия чисел (-2 и +2):

depth - 2 в render() компенсирует:

4 пробела стандартного отступа

2 пробела для выравнивания относительно родительского ключа

depth + 2 в to_string() создаёт:

Выравнивание закрывающей скобки посередине между уровнями

Пример для depth = 4:

{
    key: {
        nested: value
      }  # depth + 2 = 6 пробелов
  }  # depth - 2 = 2 пробела
Как сделать более понятным?
Константы для отступов:

python
BASE_INDENT = 4
BRACKET_OFFSET = 2
Улучшенный render():

python
closing_indent = max(0, depth - BRACKET_OFFSET) * ' '
Улучшенный to_string():

python
closing_indent = (depth + BRACKET_OFFSET) * ' '
Итоговый совет
Ваше решение работает, потому что:

Вы эмпирически подобрали правильные коэффициенты (-2 и +2)

Эти значения компенсируют друг друга в рекурсии

Система сохраняет целостность при любой глубине вложенности

Для большей ясности можно:

Добавить комментарии к "магическим числам"

Вынести их в константы с понятными названиями

Протестировать на глубоко вложенных структурах

"""