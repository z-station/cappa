from app.translators.enums import TranslatorType
from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet


class Python314ViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.PYTHON314
