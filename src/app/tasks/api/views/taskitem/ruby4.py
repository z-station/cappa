from app.translators.enums import TranslatorType
from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet


class Ruby4ViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.RUBY4
