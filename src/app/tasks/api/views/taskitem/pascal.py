from app.translators.enums import TranslatorType
from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet


class PascalViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.PASCAL
