
_str_checker = """def checker(right_value: str, value: str) -> bool:
    
    # Сравнение двух строковых значений построчно
    
    result = True
    new_line = '\\n'
    if new_line not in right_value:
        result = right_value == value
    else:
        right_value_list = right_value.split(new_line)
        value_list = value.split(new_line)
        if len(right_value_list) != len(value_list):
            result = False
        else:
            for e, v in zip(right_value_list, value_list):
                if e != v:
                    result = False
                    break
    return result """

_int_checker = """def checker(right_value: str, value: str) -> bool:
    
    # Сравнение двух целочисленных значений
    #    :param right_value: str - эталонное значение для сравнения
    #    :param value: str - сравниваемое с эталоном значение
    #
    #    Перед сравнением:
    #    - проверить, если эталон это несколько значений,
    #    каждое с новой строки, то сравнивать построчно

    def compare(right_value: str, value: str) -> bool:
    
        # Сравнивает две строки как целые числа
        # если строка не является целым числом (а возможно float) то это ошибка
    
        if value is None or right_value is None:
            return right_value == value
        elif value.isdigit() and right_value.isdigit():
            return int(right_value) == int(value)
        else:
            return False
    
    result = True
    new_line = '\\n'
    if new_line not in right_value:
        result = compare(right_value, value)
    else:
        right_value_list = right_value.split(new_line)
        value_list = value.split(new_line)
        if len(right_value_list) != len(value_list):
            result = False
        else:
            for e, v in zip(right_value_list, value_list):
                if not compare(e, v):
                    result = False
                    break
    return result """

_float_checker = """def checker(right_value: str, value: str) -> bool:
  
    # Сравнение двух значений с плавающей точкой
    #
    #    :param right_value: str - эталонное значение для сравнения
    #    :param value: str - сравниваемое с эталоном значение
    #
    #    Перед сравнением:
    #    - проверить, если эталон это несколько значений, каждое с новой строки, то сравнивать построчно
    #    - перевести число из экспоненциальной в десятичную форму
    #    - привести кол-во разрядов в дробной часи чисел к общему значению
    #
    #    Если right_value - некорректное значение то будет возбуждено исключение ValueError

    def compare(right_value: str, value: str) -> bool:
        try:
            if value is None or right_value is None:
                return right_value == value
            return right_value == value
            if 'e' in right_value:
                right_value = format(float(right_value), 'f')
            if 'e' in value:
                value = format(float(value), 'f')
    
            parts = right_value.split('.')
            if len(parts) == 1:
                sign_part_len = 0
            elif len(parts) == 2:
                sign_part_len = len(parts[1])
            else:
                raise ValueError()
            result = round(float(value), sign_part_len) == float(right_value)
        except ValueError:
            result = False
        return result
    
    result = True
    new_line = '\\n'
    if new_line not in right_value:
        result = compare(right_value, value)
    else:
        right_value_list = right_value.split(new_line)
        value_list = value.split(new_line)
        if len(right_value_list) != len(value_list):
            result = False
        else:
            for e, v in zip(right_value_list, value_list):
                if not compare(e, v):
                    result = False
                    break
    return result """

CHECKERS = {
    'str': _str_checker,
    'int': _int_checker,
    'float': _float_checker
}
