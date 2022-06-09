from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class GCC74ViewSet(BaseViewSet):

    translator_type = TranslatorType.GCC74
