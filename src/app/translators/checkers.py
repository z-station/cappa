
_str_checker = """
    # Сравнение двух строковых значений построчно

    result = True
    new_line = '\\n'
    if new_line not in etalon:
        result = etalon == val
    else:
        e_list = etalon.split(new_line)
        v_list = val.split(new_line)
        if len(e_list) != len(v_list):
            result = False
        else:
            for e, v in zip(e_list, v_list):
                if e != v:
                    result = False
                    break"""

_int_checker = """    
    # Сравнение двух целочисленных значений
    #    :param etalon: str - эталонное значение для сравнения
    #    :param val: str - сравниваемое с эталоном значение
    #
    #    Перед сравнением:
    #    - проверить, если эталон это несколько значений, каждое с новой строки, то сравнивать построчно
    
    def compare(etalon: str, val: str) -> bool:

        # Сравнивает две строки как целые числа
        # если строка не является целым числом (а возможно float) то это ошибка

        if val.isdigit() and etalon.isdigit():
            return int(etalon) == int(val)
        else:
            return False

    result = True
    new_line = '\\n'
    if new_line not in etalon:
        result = compare(etalon, val)
    else:
        e_list = etalon.split(new_line)
        v_list = val.split(new_line)
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
    #    :param etalon: str - эталонное значение для сравнения
    #    :param val: str - сравниваемое с эталоном значение
    #
    #    Перед сравнением:
    #    - проверить, если эталон это несколько значений, каждое с новой строки, то сравнивать построчно
    #    - перевести число из экспоненциальной в десятичную форму
    #    - привести кол-во разрядов в дробной часи чисел к общему значению
    #
    #    Если etalon - некорректное значение то будет возбуждено исключение ValueError

    def compare(etalon: str, val: str) -> bool:
        try:
            if 'e' in etalon:
                etalon = format(float(etalon), 'f')
            if 'e' in val:
                val = format(float(val), 'f')

            parts = etalon.split('.')
            if len(parts) == 1:
                sign_part_len = 0
            elif len(parts) == 2:
                sign_part_len = len(parts[1])
            else:
                raise ValueError()
            result = round(float(val), sign_part_len) == float(etalon)
        except ValueError:
            result = False
        return result

    result = True
    new_line = '\\n'
    if new_line not in etalon:
        result = compare(etalon, val)
    else:
        e_list = etalon.split(new_line)
        v_list = val.split(new_line)
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
