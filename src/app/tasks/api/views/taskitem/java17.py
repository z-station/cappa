from app.translators.enums import TranslatorType
from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet


class Java17ViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.JAVA17
