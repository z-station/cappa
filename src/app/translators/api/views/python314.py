from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class Python314ViewSet(BaseViewSet):

    translator_type = TranslatorType.PYTHON314
