from app.translators.enums import TranslatorType
from app.training.api.views import BaseTaskItemViewSet


class Python38ViewSet(BaseTaskItemViewSet):

    translator_type = TranslatorType.PYTHON38
