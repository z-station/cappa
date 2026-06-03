from app.translators.enums import TranslatorType
from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet


class Kotlin23ViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.KOTLIN23
