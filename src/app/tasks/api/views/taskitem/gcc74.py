from app.translators.enums import TranslatorType
from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet


class GCC74ViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.GCC74
