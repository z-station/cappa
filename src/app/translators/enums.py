import typing


class TranslatorType:

    GCC74 = 'GCC7.4'
    PROLOG_D = 'Prolog-D'
    POSTGRESQL = 'PostgreSQL'
    PASCAL = 'Pascal'
    PHP = 'Php'
    CSHARP = 'CSharp'
    JAVA = 'Java'
    RUST186 = 'Rust186'
    GO123 = 'Go123'
    NODE20 = 'Node20'
    JAVA17 = 'Java17'
    KOTLIN23 = 'Kotlin23'
    RUBY4 = 'Ruby4'
    PYTHON314 = 'Python314'

    CHOICES = (
        (GCC74, 'С++ (GCC 7.4)'),
        (CSHARP, 'C# 7.3'),
        (PROLOG_D, 'Пролог-Д'),
        (POSTGRESQL, 'PostgreSQL 13'),
        (PASCAL, 'PascalABC.NET'),
        (RUST186, 'Rust 1.86.0'),
        (GO123, 'Go 1.23'),
        (NODE20, 'Node.js 20'),
        (JAVA17, 'Java 17'),
        (KOTLIN23, 'Kotlin 2.3'),
        (RUBY4, 'Ruby 4'),
        (PYTHON314, 'Python 3.14'),
    )

    MAP = {
        GCC74: 'С++ (GCC 7.4)',
        CSHARP: 'C# 7.3',
        PROLOG_D: 'Пролог-Д',
        POSTGRESQL: 'PostgreSQL 13',
        PASCAL: 'PascalABC.NET',
        RUST186: 'Rust 1.86.0',
        GO123: 'Go 1.23',
        NODE20: 'Node.js 20',
        JAVA17: 'Java 17',
        KOTLIN23: 'Kotlin 2.3',
        RUBY4: 'Ruby 4',
        PYTHON314: 'Python 3.14',
    }

    ANTIPLAG_ALLOWED = {
        PYTHON314,
        GCC74,
        JAVA,
        POSTGRESQL
    }

    LITERALS = typing.Literal[
        GCC74,
        PROLOG_D,
        POSTGRESQL,
        PASCAL,
        PHP,
        CSHARP,
        JAVA,
        RUST186,
        GO123,
        NODE20,
        JAVA17,
        KOTLIN23,
        RUBY4,
        PYTHON314,
    ]
