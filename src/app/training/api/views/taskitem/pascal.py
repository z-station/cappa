from app.translators.enums import TranslatorType
from app.training.api.views import BaseTaskItemViewSet


class PascalViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.PASCAL
