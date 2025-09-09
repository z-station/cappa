import typing


class TranslatorType:

    PYTHON38 = 'Python3.8'
    GCC74 = 'GCC7.4'
    PROLOG_D = 'Prolog-D'
    POSTGRESQL = 'PostgreSQL'
    PASCAL = 'Pascal'
    PHP = 'Php'
    CSHARP = 'CSharp'
    JAVA = 'Java'
    RUST186 = 'Rust186'

    CHOICES = (
        (PYTHON38, 'Python 3.8'),
        (GCC74, 'С++ (GCC 7.4)'),
        (PROLOG_D, 'Пролог-Д'),
        (POSTGRESQL, 'PostgreSQL 13'),
        (PASCAL, 'PascalABC.NET'),
        (RUST186, 'Rust 1.86.0'),
    )

    MAP = {
        PYTHON38: 'Python 3.8',
        GCC74: 'С++ (GCC 7.4)',
        PROLOG_D: 'Пролог-Д',
        POSTGRESQL: 'PostgreSQL 13',
        PASCAL: 'PascalABC.NET',
        RUST186: 'Rust 1.86.0',
    }

    ANTIPLAG_ALLOWED = {
        PYTHON38,
        GCC74,
        JAVA
    }

    LITERALS = typing.Literal[
        PYTHON38,
        GCC74,
        PROLOG_D,
        POSTGRESQL,
        PASCAL,
        PHP,
        CSHARP,
        JAVA,
        RUST186,
    ]
