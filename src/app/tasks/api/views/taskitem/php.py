from app.translators.enums import TranslatorType
from app.tasks.api.views.taskitem.base import BaseTaskItemViewSet


class PhpViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.PHP
