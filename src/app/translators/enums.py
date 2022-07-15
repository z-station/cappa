from app.translators.checkers import (
    str_checker,
    int_checker,
    float_checker
)


class TranslatorType:

    PYTHON38 = 'Python3.8'
    GCC74 = 'GCC7.4'
    PROLOG_D = 'Prolog-D'
    POSTGRESQL = 'PostgreSQL'
    PASCAL = 'Pascal'
    PHP = 'Php'
    CSHARP = 'CSharp'
    JAVA = 'Java'

    CHOICES = (
        (PYTHON38, 'Python 3.8'),
        (GCC74, 'С++ (GCC 7.4)'),
        (PROLOG_D, 'Пролог-Д'),
        (POSTGRESQL, 'PostgreSQL 13'),
        (PASCAL, 'PascalABC.NET'),
    )

    MAP = {
        PYTHON38: 'Python 3.8',
        GCC74: 'С++ (GCC 7.4)',
        PROLOG_D: 'Пролог-Д',
        POSTGRESQL: 'PostgreSQL 13',
        PASCAL: 'PascalABC.NET',
    }

    ANTIPLAG_ALLOWED = {
        PYTHON38,
        GCC74,
        JAVA
    }


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

    MAP = {
        STR: str_checker,
        INT: int_checker,
        FLOAT: float_checker,
        SQL_SELECT: SQL_SELECT,
        SQL_DELETE: SQL_DELETE,
        SQL_INSERT: SQL_INSERT,
        SQL_UPDATE: SQL_UPDATE,
    }
