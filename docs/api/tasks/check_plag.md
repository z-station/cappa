## Функции проверки кода
## Функции сверки решения с тестами
### Сравнение двух целочисленных значений

```python
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
```
Тесты:

1. Целые числа в виде строки - тест пройден
```python
right_value = '92'
value = '92'
```

2. Целые числа в многострочном тексте - тест пройден
```python
right_value = '92\n50'
value = '92\n50'
```

3. Вещественное число - тест не пройден
```python
right_value = ('92.0', '92.001')
value = ('92.0', '92.001')
```

4. Не числовое значение - тест не пройден
```python
right_value = ('[]', 'null', 'one')
value = ('[]', 'null', 'one')
```

5. Пустое значение - тест пройден
```python
right_value = ('', None, '0')
value = ('', None, '0')
```

6. Пустое значение в многострочном тексте - тест пройден
```python
right_value = ('92\n\n1', '0\n0')
value = ('92\n\n1', '0\n0')
```


### Сравнение двух вещественных чисел

```python
def checker(right_value: str, value: str) -> bool:

    """ Сравнение двух вещественных чисел

    :param right_value: str - эталонное значение для сравнения
    :param value: str - сравниваемое с right_valueом значение

    Сценарии сравнения:
    - если right_value или value содержит пустое значение то
      окончить сравнение на этом шаге.
    - проверить, если right_value это несколько значений, каждое с новой строки,
      то сравнивать построчно.
    - перевести число из экспоненциальной в десятичную форму.
    - привести кол-во разрядов в дробной части value
      к числу разрядов в дробной части right_value
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
```

Тесты:

1. Вещественные числа в виде строки - тест пройден
```python
right_value = '92.1'
value = '92.1'
```

2. Различная дробная часть вещественного числа - тест не пройден
```python
right_value = '92.100001'
value = '92.1'
```

2. Целые числа - тест пройден
```python
right_value = '92'
value = '92'
```

3. Округление - тест пройден
```python
right_value = '92.72'
value = '92.72000862812729'
```

4. Многострочный текст - тест пройден
```python
right_value = '92.72\n50'
value = '92.720014\n50'
```

5. Решение в экспоненциальной форме - тест пройден
```python
right_value = '12.3456'
value = '1.234560e+01'
```

6. Тестовое значение в экспоненциальной форме - тест пройден
```python
right_value = '1.234560e+01'
value = '12.3456'
```

7. Не числовое значение - тест не пройден
```python
right_value = ('[]', 'null', 'one')
value = ('[]', 'null', 'one')
```

8. Пустое значение - тест пройден
```python
right_value = ('', None, '0')
value = ('', None, '0')
```
9. Пустое значение в многострочном тексте - тест пройден
```python
right_value =  ('92.01\n\n1.0', '0\n0.0', None)
value =  ('92.01\n\n1.0', '0\n0.0', None)
```
### Сравнение двух строковых значений построчно

```python
def checker(right_value: str, value: str) -> bool:

    """ Сравнение двух строковых значений построчно

       :param right_value: str - эталонное значение для сравнения
       :param value: str - сравниваемое с эталоном значение

    Сценарии сравнения:
    - проверить, если right_value это несколько значений,
      каждое с новой строки, то сравнивать построчно.
    - если right_value или value - некорректное значение
      то результат False """

    empty_values = ('', None)

    if value in empty_values or right_value in empty_values:
        return right_value == value
    else:
        result = True
        new_line = '\n'
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
    return result
```
Тесты:

1. Простой однострочный текст - тест пройден
```python
right_value = 'test'
value = 'test'
```

2. Многострочный текст - тест пройден
```python
right_value = 'test\n50'
value = 'test\n50'
```

3. Пустые значения - тест пройден
```python
right_value = ('', None, '0')
value = ('', None, '0')
```

4. Пустые значения в многострочном тексте - тест пройден
```python
right_value = ('test\n\n1', '0\n0')
value = ('test\n\n1', '0\n0')
```

5. Перевод на новую строку в конце  - тест не пройден
```python
right_value = 'test'
value = 'test\n'
```
