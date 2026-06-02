from app.translators.enums import TranslatorType
from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet


class Go123ViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.GO123
