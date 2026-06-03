from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class Kotlin23ViewSet(BaseViewSet):

    translator_type = TranslatorType.KOTLIN23
