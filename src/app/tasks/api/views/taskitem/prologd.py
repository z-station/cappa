from app.translators.enums import TranslatorType
from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet


class PrologDViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.PROLOG_D
