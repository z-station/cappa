from app.translators.enums import TranslatorType
from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet


class Node20ViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.NODE20
