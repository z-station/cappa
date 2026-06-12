from django.test import SimpleTestCase

from app.tasks.models import TaskItem
from app.training.models import Course, Topic
from app.translators.enums import TranslatorType


class TaskItemTranslatorTests(SimpleTestCase):

    def _taskitem(self, translators, course_translator=None):
        taskitem = TaskItem(translator=translators)
        if course_translator is not None:
            course = Course(translator=course_translator)
            topic = Topic(course=course)
            topic.pk = 1
            taskitem.topic = topic
        return taskitem

    def test_get_valid_translator_without_request_uses_first(self):
        # Arrange
        taskitem = self._taskitem([
            TranslatorType.PYTHON314,
            TranslatorType.GCC74,
        ])

        # Act
        result = taskitem.get_valid_translator(None)

        # Assert
        self.assertEqual(result, TranslatorType.PYTHON314)

    def test_get_valid_translator_valid_request(self):
        # Arrange
        taskitem = self._taskitem([
            TranslatorType.PYTHON314,
            TranslatorType.GCC74,
        ])

        # Act
        result = taskitem.get_valid_translator(TranslatorType.GCC74)

        # Assert
        self.assertEqual(result, TranslatorType.GCC74)

    def test_get_valid_translator_invalid_request_uses_first(self):
        # Arrange
        taskitem = self._taskitem([
            TranslatorType.PYTHON314,
            TranslatorType.GCC74,
        ])

        # Act
        result = taskitem.get_valid_translator(TranslatorType.POSTGRESQL)

        # Assert
        self.assertEqual(result, TranslatorType.PYTHON314)

    def test_get_valid_translator_request_overrides_default(self):
        # Arrange
        taskitem = self._taskitem(
            [
                TranslatorType.PYTHON314,
                TranslatorType.GCC74,
            ],
            course_translator=TranslatorType.PYTHON314,
        )

        # Act
        result = taskitem.get_valid_translator(TranslatorType.GCC74)

        # Assert
        self.assertEqual(result, TranslatorType.GCC74)

    def test_get_valid_translator_uses_default_when_in_list(self):
        # Arrange
        taskitem = self._taskitem(
            [
                TranslatorType.PYTHON314,
                TranslatorType.GCC74,
            ],
            course_translator=TranslatorType.GCC74,
        )

        # Act
        result = taskitem.get_valid_translator(None)

        # Assert
        self.assertEqual(result, TranslatorType.GCC74)

    def test_get_valid_translator_ignores_default_not_in_list(self):
        # Arrange
        taskitem = self._taskitem(
            [
                TranslatorType.PYTHON314,
                TranslatorType.GCC74,
            ],
            course_translator=TranslatorType.POSTGRESQL,
        )

        # Act
        result = taskitem.get_valid_translator(None)

        # Assert
        self.assertEqual(result, TranslatorType.PYTHON314)

    def test_get_translator_choices(self):
        # Arrange
        taskitem = self._taskitem([
            TranslatorType.GCC74,
            TranslatorType.PYTHON314,
        ])

        # Act
        result = taskitem.get_translator_choices()

        # Assert
        self.assertEqual(
            result,
            [
                (TranslatorType.GCC74, TranslatorType.MAP[TranslatorType.GCC74]),
                (TranslatorType.PYTHON314, TranslatorType.MAP[TranslatorType.PYTHON314]),
            ],
        )
