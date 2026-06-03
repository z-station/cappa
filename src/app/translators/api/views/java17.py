from app.translators.api.views import BaseViewSet
from app.translators.enums import TranslatorType


class Java17ViewSet(BaseViewSet):

    translator_type = TranslatorType.JAVA17
