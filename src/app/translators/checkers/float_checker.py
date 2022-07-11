
def checker(right_value: str, value: str) -> bool:

    """ Сравнение двух значений с плавающей точкой

    :param right_value: str - эталонное значение для сравнения
    :param value: str - сравниваемое с right_valueом значение

    Сценарии сравнения:
    - если right_value или value содержит пустое значение то
      окончить сравнение на этом шаге.
    - проверить, если right_value это несколько значений, каждое с новой строки,
      то сравнивать построчно.
    - перевести число из экспоненциальной в десятичную форму.
    - привести кол-во разрядов в дробной части value
      к числу разрядов в дробной часи right_value
    - если right_value или value - некорректное значение то результат False """

    empty_values = ('', None)

    def compare(right_value: str, value: str) -> bool:
        try:
            if value in empty_values or right_value in empty_values:
                return right_value == value
            if 'e' in right_value:
                right_value = format(float(right_value), 'f').rstrip('0')
            if 'e' in value:
                value = format(float(value), 'f').rstrip('0')

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

    if value in empty_values or right_value in empty_values:
        result = right_value == value
    else:
        result = True
        new_line = '\n'
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
    return result


checker_str = """def checker(right_value: str, value: str) -> bool:

    empty_values = ('', None)

    def compare(right_value: str, value: str) -> bool:
        try:
            if value in empty_values or right_value in empty_values:
                return right_value == value
            if 'e' in right_value:
                right_value = format(float(right_value), 'f').rstrip('0')
            if 'e' in value:
                value = format(float(value), 'f').rstrip('0')

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

    if value in empty_values or right_value in empty_values:
        result = right_value == value
    else:
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
