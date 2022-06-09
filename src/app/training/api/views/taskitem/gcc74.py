from app.translators.enums import TranslatorType
from app.training.api.views import BaseTaskItemViewSet


class GCC74ViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.GCC74
