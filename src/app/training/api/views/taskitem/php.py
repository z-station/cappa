from app.translators.enums import TranslatorType
from app.training.api.views import BaseTaskItemViewSet


class PhpViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.PHP
