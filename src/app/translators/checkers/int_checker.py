
def checker(right_value: str, value: str) -> bool:

    """ Сравнение двух целочисленных значений

    :param right_value: str - эталонное значение для сравнения
    :param value: str - сравниваемое с эталоном значение

    Сценарии сравнения:
    - если right_value или value содержит пустое значение то
      окончить сравнение на этом шаге.
    - проверить, если right_value это несколько значений,
      каждое с новой строки, то сравнивать построчно.
    - если right_value или value - некорректное значение
    то результат False """

    empty_values = ('', None)

    def compare(right_value: str, value: str) -> bool:

        # Сравнивает две строки как целые числа
        # если строка не является целым числом (а возможно float) то это ошибка

        if value in empty_values or right_value in empty_values:
            return right_value == value
        elif value.isdigit() and right_value.isdigit():
            return int(right_value) == int(value)
        else:
            return False

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

        # Сравнивает две строки как целые числа
        # если строка не является целым числом (а возможно float) то это ошибка

        if value in empty_values or right_value in empty_values:
            return right_value == value
        elif value.isdigit() and right_value.isdigit():
            return int(right_value) == int(value)
        else:
            return False

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

