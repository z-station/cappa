from app.translators.enums import TranslatorType
from app.training.api.views import BaseTaskItemViewSet


class PrologDViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.PROLOG_D
