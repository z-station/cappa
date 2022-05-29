
class TranslatorType:

    PYTHON38 = 'Python3.8'
    GCC74 = 'GCC7.4'
    PROLOG_D = 'Prolog-D'

    CHOICES = (
        (PYTHON38, 'Python 3.8'),
        (GCC74, 'С++ (GCC 7.4)'),
        (PROLOG_D, 'Пролог-Д'),
    )

    MAP = {
        PYTHON38: 'Python 3.8',
        GCC74: 'С++ (GCC 7.4)',
        PROLOG_D: 'Пролог-Д'
    }
