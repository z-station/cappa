
_str_checker = """
# Сравнение двух строковых значений построчно

result = True
new_line = '\\n'
if new_line not in test_console_output:
    result = test_console_output == translator_console_output
else:
    e_list = test_console_output.split(new_line)
    v_list = translator_console_output.split(new_line)
    if len(e_list) != len(v_list):
        result = False
    else:
        for e, v in zip(e_list, v_list):
            if e != v:
                result = False
                break"""

_int_checker = """    
# Сравнение двух целочисленных значений
#    :param test_console_output: str - эталонное значение для сравнения
#    :param translator_console_output: str - сравниваемое с эталоном значение
#
#    Перед сравнением:
#    - проверить, если эталон это несколько значений, каждое с новой строки, то сравнивать построчно

def compare(test_console_output: str, translator_console_output: str) -> bool:

    # Сравнивает две строки как целые числа
    # если строка не является целым числом (а возможно float) то это ошибка

    if translator_console_output.isdigit() and test_console_output.isdigit():
        return int(test_console_output) == int(translator_console_output)
    else:
        return False

result = True
new_line = '\\n'
if new_line not in test_console_output:
    result = compare(test_console_output, translator_console_output)
else:
    e_list = test_console_output.split(new_line)
    v_list = translator_console_output.split(new_line)
    if len(e_list) != len(v_list):
        result = False
    else:
        for e, v in zip(e_list, v_list):
            if not compare(e, v):
                result = False
                break"""

_float_checker = """   
# Сравнение двух значений с плавающей точкой
#
#    :param test_console_output: str - эталонное значение для сравнения
#    :param translator_console_output: str - сравниваемое с эталоном значение
#
#    Перед сравнением:
#    - проверить, если эталон это несколько значений, каждое с новой строки, то сравнивать построчно
#    - перевести число из экспоненциальной в десятичную форму
#    - привести кол-во разрядов в дробной часи чисел к общему значению
#
#    Если test_console_output - некорректное значение то будет возбуждено исключение ValueError

def compare(test_console_output: str, translator_console_output: str) -> bool:
    try:
        if 'e' in test_console_output:
            test_console_output = format(float(test_console_output), 'f')
        if 'e' in translator_console_output:
            translator_console_output = format(float(translator_console_output), 'f')

        parts = test_console_output.split('.')
        if len(parts) == 1:
            sign_part_len = 0
        elif len(parts) == 2:
            sign_part_len = len(parts[1])
        else:
            raise ValueError()
        result = round(float(translator_console_output), sign_part_len) == float(test_console_output)
    except ValueError:
        result = False
    return result

result = True
new_line = '\\n'
if new_line not in test_console_output:
    result = compare(test_console_output, translator_console_output)
else:
    e_list = test_console_output.split(new_line)
    v_list = translator_console_output.split(new_line)
    if len(e_list) != len(v_list):
        result = False
    else:
        for e, v in zip(e_list, v_list):
            if not compare(e, v):
                result = False
                break"""

checkers = {
    'str': _str_checker,
    'int': _int_checker,
    'float': _float_checker
}
