# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations


def _create_checkers(apps, schema_editor):
    Checker = apps.get_model("tasks", "Checker")

    Checker.objects.bulk_create(objs=[
        Checker(
            name='Сравнение строк',
            description=""" Сравнение двух строковых значений построчно

       :param right_value: str - эталонное значение для сравнения
       :param value: str - сравниваемое с эталоном значение

    Сценарии сравнения:
    - проверить, если right_value это несколько значений,
      каждое с новой строки, то сравнивать построчно.
    - если right_value или value - некорректное значение
      то результат False """,
            content="""def checker(right_value: str, value: str) -> bool:

    empty_values = ('', None)

    if value in empty_values or right_value in empty_values:
        return right_value == value
    else:
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
        ),
        Checker(
            name="Сравнение целых чисел",
            description=""" Сравнение двух целочисленных значений

    :param right_value: str - эталонное значение для сравнения
    :param value: str - сравниваемое с эталоном значение

    Сценарии сравнения:
    - если right_value или value содержит пустое значение то
      окончить сравнение на этом шаге.
    - проверить, если right_value это несколько значений,
      каждое с новой строки, то сравнивать построчно.
    - если right_value или value - некорректное значение
    то результат False """,
            content="""def checker(right_value: str, value: str) -> bool:

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
        ),
        Checker(
            name="Сравнение дробных чисел",
            description=    """ Сравнение двух значений с плавающей точкой

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
    - если right_value или value - некорректное значение то результат False """,
            content="""def checker(right_value: str, value: str) -> bool:

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

        ),
        Checker(
            name="SQL SELECT",
            description="""Нельзя изменять функцию сверки решения!
Чекер считается пройденым если результат запроса SELECT из решения совпадает с результатом запроса SELECT из теста""",
            content="select"
        ),
        Checker(
            name="SQL DELETE",
            description="""Нельзя изменять функцию сверки решения!
Чекер считается пройденым если SELECT запрос из теста не обнаружит записи, которые должна удалить DELETE команда из решения""",
            content="delete"
        ),
        Checker(
            name="SQL INSERT",
            description="""Нельзя изменять функцию сверки решения!
"Чекер считается пройденым если SELECT запрос из теста обнаружит записи, которые должна добавить команда INSERT из решения. Тест состоит из двух строк: первая - это кол-во новых записей, вторая - SELECT-запрос возвращающий новые записи""",
            content="insert"
        ),
        Checker(
            name="SQL UPDATE",
            description="""Нельзя изменять функцию сверки решения!
Чекер считается пройденым если SELECT запрос из теста обнаружит записи, которые должна изменить команда UPDATE из решения. Тест состоит из двух строк: первая - это кол-во измененных записей, вторая - SELECT-запрос возвращающий измененные записи""",
            content="update"
        ),
    ])


def _set_checkers(apps, schema_editor):
    Task = apps.get_model("tasks", "Task")
    Checker = apps.get_model("tasks", "Checker")

    class CheckerType:
        STR = 'str'
        INT = 'int'
        FLOAT = 'float'
        SQL_SELECT = 'select'
        SQL_DELETE = 'delete'
        SQL_INSERT = 'insert'
        SQL_UPDATE = 'update'

        CHOICES = (

            (STR, 'строка'),
            (INT, 'целое число'),
            (FLOAT, 'вещественное число'),
            (SQL_SELECT, 'SQL SELECT'),
            (SQL_DELETE, 'SQL DELETE'),
            (SQL_INSERT, 'SQL INSERT'),
            (SQL_UPDATE, 'SQL UPDATE'),
        )

    str_checker = Checker.objects.get(name="Сравнение строк")
    Task.objects.filter(output_type=CheckerType.STR).update(
        testing_checker=str_checker
    )

    int_checker = Checker.objects.get(name="Сравнение целых чисел")
    Task.objects.filter(output_type=CheckerType.INT).update(
        testing_checker=int_checker
    )

    float_checker = Checker.objects.get(name="Сравнение дробных чисел")
    Task.objects.filter(output_type=CheckerType.FLOAT).update(
        testing_checker=float_checker
    )

    sql_select_checker = Checker.objects.get(name="SQL SELECT")
    Task.objects.filter(output_type=CheckerType.SQL_SELECT).update(
        testing_checker=sql_select_checker
    )

    sql_delete_checker = Checker.objects.get(name="SQL DELETE")
    Task.objects.filter(output_type=CheckerType.SQL_DELETE).update(
        testing_checker=sql_delete_checker
    )

    sql_insert_checker = Checker.objects.get(name="SQL INSERT")
    Task.objects.filter(output_type=CheckerType.SQL_INSERT).update(
        testing_checker=sql_insert_checker
    )

    sql_update_checker = Checker.objects.get(name="SQL UPDATE")
    Task.objects.filter(output_type=CheckerType.SQL_UPDATE).update(
        testing_checker=sql_update_checker
    )



class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0019_auto_20240703_0452'),
    ]

    operations = [
        migrations.RunPython(_create_checkers),
        migrations.RunPython(_set_checkers)
    ]
