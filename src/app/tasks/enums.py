import typing


class TaskItemType:

    COURSE = 'course'
    EXTERNAL = 'external'
    TASKBOOK = 'taskbook'

    CHOICES = (
        (COURSE, 'Курс'),
        (TASKBOOK, 'Задачник'),
        (EXTERNAL, 'Внешний источник'),
    )
    MAP = {
        COURSE: 'Курс',
        TASKBOOK: 'Задачник',
        EXTERNAL: 'Внешний источник',
    }

    LITERALS = typing.Literal[
        COURSE,
        EXTERNAL,
        TASKBOOK,
    ]


class ReviewStatus:
    
    READY_TO_REVIEW = 'ready'
    REVIEW_IN_PROGRESS = 'review'
    CHECKED = 'checked'

    AWAITING_CHECK = (
        READY_TO_REVIEW,
        REVIEW_IN_PROGRESS
    )
    BLOCKED_STATUS = (
        REVIEW_IN_PROGRESS,
        CHECKED
    )
    CHOICES = (
        (READY_TO_REVIEW, 'ожидает проверки'),
        (REVIEW_IN_PROGRESS, 'в процессе проверки'),
        (CHECKED, 'проверено'),
    )
    MAP = {
        READY_TO_REVIEW: 'ожидает проверки',
        REVIEW_IN_PROGRESS: 'в процессе проверки',
        CHECKED: 'проверено'
    }


class ScoreMethod:

    TESTS = 'tests'
    REVIEW = 'review'
    TESTS_AND_REVIEW = 'tests_and_review'

    CHOICES = (
        (TESTS, 'Тестирование кода'),
        (REVIEW, 'Проверка преподавателем'),
        (TESTS_AND_REVIEW, 'Тестирование и проверка'),
    )
    MAP = {
        TESTS: 'Тестирование кода',
        REVIEW: 'Проверка преподавателем',
        TESTS_AND_REVIEW: 'Тестирование и проверка',
    }
    REVIEW_METHODS = {REVIEW, TESTS_AND_REVIEW}
    TESTS_METHODS = {TESTS, TESTS_AND_REVIEW}


class DifficultyLevel:

    SIMPLEST = '0'
    SIMPLE = '1'
    MEDIUM = '2'
    HARD = '3'
    HARDEST = '4'

    CHOICES = (
        (SIMPLEST, 'Очень простая'),
        (SIMPLE, 'Простая'),
        (MEDIUM, 'Средняя'),
        (HARD, 'Сложная'),
        (HARDEST, 'Легендарная'),
    )

    MAP = {
        SIMPLEST: 'Очень простая',
        SIMPLE: 'Простая',
        MEDIUM: 'Средняя',
        HARD: 'Сложная',
        HARDEST: 'Легендарная',
    }
