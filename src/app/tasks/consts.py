from dataclasses import dataclass


@dataclass
class SolutionSource:

    TASK_SET = '1'
    TASK_BOOK = '2'
    TOPIC = '3'

    choices = (
        (TASK_SET, 'Набор задач'),
        (TASK_BOOK, 'Задачник'),
        (TOPIC, 'Тема курса')
    )


@dataclass
class Status:

    NONE = '0'
    UN_LUCK = '1'
    IN_PROGRESS = '2'
    SUCCESS = '3'

    choices = (
        (NONE, 'нет попыток'),
        (UN_LUCK, 'нет решения'),
        (IN_PROGRESS, 'частично решено'),
        (SUCCESS, 'решено'),
    )

    names = {
        NONE: 'нет попыток',
        UN_LUCK: 'нет решения',
        IN_PROGRESS: 'частично решено',
        SUCCESS: 'решено'
    }


@dataclass
class Complexity:

    choices = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10')
    )


@dataclass
class Checker:

    INT = 'int'
    FLOAT = 'float'
    STR = 'str'

    choices = (
        (STR, 'строка'),
        (INT, 'целое число'),
        (FLOAT, 'вещественное число')
    )
